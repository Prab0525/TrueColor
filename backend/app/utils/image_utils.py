"""
Image processing utilities
"""

import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Optional


def preprocess_image(image_bytes: bytes) -> Optional[np.ndarray]:
    """
    Convert uploaded image bytes to OpenCV format
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        OpenCV image (BGR) or None if conversion fails
    """
    try:
        # Convert bytes to PIL Image
        pil_image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert PIL to numpy array
        image_array = np.array(pil_image)
        
        # Convert RGB to BGR for OpenCV
        bgr_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        return bgr_image
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None


def resize_image(image: np.ndarray, max_dimension: int = 1024) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: OpenCV image
        max_dimension: Maximum width or height
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    if max(height, width) <= max_dimension:
        return image
    
    if height > width:
        new_height = max_dimension
        new_width = int(width * (max_dimension / height))
    else:
        new_width = max_dimension
        new_height = int(height * (max_dimension / width))
    
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized


def enhance_image(image: np.ndarray) -> np.ndarray:
    """
    Apply basic enhancement to improve skin tone detection
    
    Args:
        image: OpenCV image
        
    Returns:
        Enhanced image
    """
    # Convert to LAB for luminance adjustment
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced_lab = cv2.merge([l, a, b])
    
    # Convert back to BGR
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    return enhanced


def hex_to_lab(hex_color: str) -> np.ndarray:
    """
    Convert hex color to LAB color space
    
    Args:
        hex_color: Hex color string (e.g., "#FFAA88")
        
    Returns:
        LAB color as numpy array [L, A, B]
    """
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Create BGR image (OpenCV format)
    bgr = np.uint8([[[b, g, r]]])
    
    # Convert to LAB
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    
    return lab[0, 0].astype(float)


def lab_to_hex(lab: np.ndarray) -> str:
    """
    Convert LAB color to hex string
    
    Args:
        lab: LAB color [L, A, B]
        
    Returns:
        Hex color string
    """
    # Create LAB image
    lab_img = np.uint8([[lab]])
    
    # Convert to BGR
    bgr = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)
    b, g, r = bgr[0, 0]
    
    # Convert to hex
    return f"#{r:02x}{g:02x}{b:02x}"
