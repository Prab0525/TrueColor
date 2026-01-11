"""
TrueShade Backend API
Main FastAPI application for skin tone analysis and makeup shade matching
Now with Supabase integration for persistent storage
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import os
from typing import Optional

from app.services.face_detection import FaceDetectionService
from app.services.skin_analysis import SkinAnalysisService
from app.services.shade_matcher import ShadeMatcherService
from app.models.response_models import AnalysisResponse
from app.utils.image_utils import preprocess_image
from app.database.supabase_client import supabase_client
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="TrueShade API",
    description="Skin tone analysis and makeup shade recommendation engine with Supabase backend",
    version="2.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
face_detector = FaceDetectionService()
skin_analyzer = SkinAnalysisService()
shade_matcher = ShadeMatcherService()


@app.get("/")
async def root():
    """Health check endpoint"""
    config_status = settings.get_status()
    return {
        "status": "online",
        "service": "TrueShade Backend",
        "version": "2.0.0",
        "supabase_connected": config_status["supabase_configured"],
        "database_mode": "Supabase" if config_status["supabase_configured"] else "Local (Python Dict)"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    config_status = settings.get_status()
    return {
        "status": "healthy",
        "services": {
            "face_detection": "ready (MediaPipe)",
            "skin_analysis": "ready (LAB + K-Means)",
            "shade_matching": "ready",
            "database": "Supabase" if supabase_client.is_connected() else "Local"
        },
        "configuration": config_status
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_face(
    file: UploadFile = File(...),
    user_id: Optional[str] = Query(None, description="Optional user ID to save analysis history")
):
    """
    Main endpoint for skin tone analysis and shade matching
    
    Args:
        file: Uploaded image file containing a face
        user_id: Optional user ID to save analysis to history
        
    Returns:
        AnalysisResponse with skin LAB values, undertone, and shade recommendations
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read and preprocess image
        contents = await file.read()
        image = preprocess_image(contents)
        
        if image is None:
            raise HTTPException(
                status_code=400,
                detail="Could not read image. Please ensure it's a valid image file."
            )
        
        # Step 1: Detect face and extract landmarks
        face_landmarks = face_detector.detect_face(image)
        
        if face_landmarks is None:
            raise HTTPException(
                status_code=422,
                detail="No face detected in the image. Please upload a clear photo with a visible face."
            )
        
        # Step 2: Extract skin regions
        skin_regions = face_detector.extract_skin_regions(image, face_landmarks)
        
        if skin_regions is None or len(skin_regions) == 0:
            raise HTTPException(
                status_code=422,
                detail="Could not extract skin regions from the detected face."
            )
        
        # Step 3: Analyze skin tone in LAB color space
        skin_lab = skin_analyzer.analyze_skin_tone(skin_regions)
        
        if skin_lab is None:
            raise HTTPException(
                status_code=500,
                detail="Could not analyze skin tone from the extracted regions."
            )
        
        # Step 4: Determine undertone
        undertone = skin_analyzer.determine_undertone(skin_lab)
        
        # Step 5: Get Pantone family approximation
        pantone_family = skin_analyzer.get_pantone_family(skin_lab)
        
        # Step 6: Match to makeup shades (now async with Supabase support)
        matches = await shade_matcher.find_matches(skin_lab, undertone)
        
        # Step 7: Save to history if user_id provided and Supabase is connected
        if user_id and supabase_client.is_connected():
            analysis_data = {
                "user_id": user_id,
                "skin_lab_l": float(skin_lab[0]),
                "skin_lab_a": float(skin_lab[1]),
                "skin_lab_b": float(skin_lab[2]),
                "undertone": undertone,
                "pantone_family": pantone_family,
                "recommended_fenty": matches.get("fenty", []),
                "recommended_nars": matches.get("nars", []),
                "recommended_toofaced": matches.get("tooFaced", [])
            }
            await supabase_client.save_analysis(analysis_data)
        
        # Prepare response
        response = AnalysisResponse(
            skinLAB=skin_lab.tolist(),
            undertone=undertone,
            pantone_family=pantone_family,
            fenty=matches.get("fenty", []),
            nars=matches.get("nars", []),
            tooFaced=matches.get("tooFaced", [])
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/analyze-debug")
async def analyze_face_debug(file: UploadFile = File(...)):
    """
    Debug endpoint that returns intermediate processing results
    Useful for testing and debugging the pipeline
    """
    try:
        contents = await file.read()
        image = preprocess_image(contents)
        
        if image is None:
            return {"error": "Could not read image"}
        
        # Detect face
        face_landmarks = face_detector.detect_face(image)
        
        if face_landmarks is None:
            return {
                "error": "No face detected",
                "image_shape": image.shape
            }
        
        # Extract skin regions
        skin_regions = face_detector.extract_skin_regions(image, face_landmarks)
        
        # Analyze skin tone
        skin_lab = skin_analyzer.analyze_skin_tone(skin_regions)
        undertone = skin_analyzer.determine_undertone(skin_lab)
        
        return {
            "status": "success",
            "image_shape": image.shape,
            "landmarks_detected": len(face_landmarks.landmark) if face_landmarks else 0,
            "skin_pixels_extracted": len(skin_regions),
            "skin_lab": skin_lab.tolist() if skin_lab is not None else None,
            "undertone": undertone,
            "debug_info": {
                "L_channel": float(skin_lab[0]) if skin_lab is not None else None,
                "A_channel": float(skin_lab[1]) if skin_lab is not None else None,
                "B_channel": float(skin_lab[2]) if skin_lab is not None else None,
            }
        }
        
    except Exception as e:
        return {"error": str(e)}


# ==================== NEW SUPABASE ENDPOINTS ====================

@app.get("/user/{user_id}/history")
async def get_user_history(user_id: str, limit: int = Query(10, ge=1, le=50)):
    """
    Get analysis history for a user
    
    Args:
        user_id: User ID
        limit: Number of recent analyses to return (1-50)
        
    Returns:
        List of past analyses
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Enable Supabase to use this feature."
        )
    
    try:
        analyses = await supabase_client.get_user_analyses(user_id, limit)
        return {
            "user_id": user_id,
            "total_analyses": len(analyses),
            "analyses": analyses
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")


@app.get("/user/{user_id}/latest")
async def get_latest_analysis(user_id: str):
    """
    Get the most recent analysis for a user
    
    Args:
        user_id: User ID
        
    Returns:
        Most recent analysis or 404 if none found
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Enable Supabase to use this feature."
        )
    
    try:
        latest = await supabase_client.get_latest_analysis(user_id)
        if not latest:
            raise HTTPException(status_code=404, detail="No analysis found for this user")
        return latest
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching latest analysis: {str(e)}")


@app.post("/user/{user_id}/favorites/{product_id}")
async def add_favorite(user_id: str, product_id: str):
    """
    Add a product to user's favorites
    
    Args:
        user_id: User ID
        product_id: Product ID to favorite
        
    Returns:
        Favorite record
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Enable Supabase to use this feature."
        )
    
    try:
        favorite = await supabase_client.add_favorite(user_id, product_id)
        if not favorite:
            raise HTTPException(status_code=400, detail="Could not add favorite (may already exist)")
        return {
            "status": "success",
            "message": "Product added to favorites",
            "favorite": favorite
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding favorite: {str(e)}")


@app.delete("/user/{user_id}/favorites/{product_id}")
async def remove_favorite(user_id: str, product_id: str):
    """
    Remove a product from user's favorites
    
    Args:
        user_id: User ID
        product_id: Product ID to unfavorite
        
    Returns:
        Success message
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Enable Supabase to use this feature."
        )
    
    try:
        success = await supabase_client.remove_favorite(user_id, product_id)
        if not success:
            raise HTTPException(status_code=404, detail="Favorite not found")
        return {
            "status": "success",
            "message": "Product removed from favorites"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing favorite: {str(e)}")


@app.get("/user/{user_id}/favorites")
async def get_favorites(user_id: str):
    """
    Get all favorited products for a user
    
    Args:
        user_id: User ID
        
    Returns:
        List of favorited products
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Enable Supabase to use this feature."
        )
    
    try:
        favorites = await supabase_client.get_user_favorites(user_id)
        return {
            "user_id": user_id,
            "total_favorites": len(favorites),
            "favorites": favorites
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching favorites: {str(e)}")


@app.get("/products")
async def get_all_products(brand: Optional[str] = Query(None, description="Filter by brand")):
    """
    Get all makeup products (or filter by brand)
    
    Args:
        brand: Optional brand filter (Fenty, Nars, Too Faced)
        
    Returns:
        List of products
    """
    if not supabase_client.is_connected():
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Products only available via Supabase."
        )
    
    try:
        if brand:
            products = await supabase_client.get_products_by_brand(brand)
        else:
            products = await supabase_client.get_all_products()
        
        return {
            "total": len(products),
            "brand_filter": brand,
            "products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
