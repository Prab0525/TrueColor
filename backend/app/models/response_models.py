"""
Pydantic models for API responses
"""

from pydantic import BaseModel, Field
from typing import List


class AnalysisResponse(BaseModel):
    """Response model for the /analyze endpoint"""
    
    skinLAB: List[float] = Field(
        ...,
        description="Dominant skin tone in LAB color space [L, A, B]",
        min_items=3,
        max_items=3
    )
    
    undertone: str = Field(
        ...,
        description="Skin undertone classification: warm, neutral, or cool"
    )
    
    pantone_family: str = Field(
        ...,
        description="Approximate Pantone SkinTone family code"
    )
    
    fenty: List[str] = Field(
        default_factory=list,
        description="Recommended Fenty Beauty foundation shades"
    )
    
    nars: List[str] = Field(
        default_factory=list,
        description="Recommended NARS foundation shades"
    )
    
    tooFaced: List[str] = Field(
        default_factory=list,
        description="Recommended Too Faced foundation shades"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "skinLAB": [65.2, 12.4, 18.6],
                "undertone": "warm",
                "pantone_family": "4Y05",
                "fenty": ["310", "330"],
                "nars": ["Barcelona", "Stromboli"],
                "tooFaced": ["Warm Sand", "Golden Beige"]
            }
        }
