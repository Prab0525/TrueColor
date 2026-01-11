"""
Skin Analysis Service
Analyzes skin tone using LAB color space and K-Means clustering
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from typing import Optional


class SkinAnalysisService:
    """Service for analyzing skin tone in LAB color space"""
    
    def __init__(self, n_clusters: int = 5):
        """
        Initialize skin analysis service
        
        Args:
            n_clusters: Number of clusters for K-Means (default: 5)
        """
        self.n_clusters = n_clusters
    
    def analyze_skin_tone(self, skin_pixels: np.ndarray) -> Optional[np.ndarray]:
        """
        Analyze skin tone using K-Means clustering in LAB color space
        
        Args:
            skin_pixels: Array of skin pixels in BGR format
            
        Returns:
            Dominant skin tone as [L, A, B] vector or None
        """
        if len(skin_pixels) == 0:
            return None
        
        # Convert BGR to LAB
        # Reshape for cv2.cvtColor if needed
        if len(skin_pixels.shape) == 2:
            skin_pixels = skin_pixels.reshape(-1, 1, 3)
        
        lab_pixels = cv2.cvtColor(skin_pixels.astype(np.uint8), cv2.COLOR_BGR2LAB)
        lab_pixels = lab_pixels.reshape(-1, 3)
        
        # Remove outliers (very dark or very bright pixels)
        L_channel = lab_pixels[:, 0]
        valid_mask = (L_channel > 20) & (L_channel < 240)
        lab_pixels = lab_pixels[valid_mask]
        
        if len(lab_pixels) < 10:
            return None
        
        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=min(self.n_clusters, len(lab_pixels)), 
                       random_state=42, 
                       n_init=10)
        kmeans.fit(lab_pixels)
        
        # Find the dominant cluster (largest)
        labels = kmeans.labels_
        cluster_sizes = np.bincount(labels)
        dominant_cluster = np.argmax(cluster_sizes)
        
        # Get the centroid of the dominant cluster
        dominant_lab = kmeans.cluster_centers_[dominant_cluster]
        
        return dominant_lab
    
    def determine_undertone(self, skin_lab: np.ndarray) -> str:
        """
        Determine skin undertone based on LAB values
        
        Args:
            skin_lab: LAB color vector [L, A, B]
            
        Returns:
            Undertone classification: "warm", "neutral", or "cool"
        """
        if skin_lab is None or len(skin_lab) < 3:
            return "neutral"
        
        L, A, B = skin_lab
        
        # Undertone classification based on A and B channels
        # A: green (-) to red (+)
        # B: blue (-) to yellow (+)
        
        # Warm undertones: Higher B (yellow), moderate to high A (red)
        # Cool undertones: Lower B (less yellow/more blue), lower A
        # Neutral: Balanced A and B
        
        # Threshold-based classification
        if B > 15 and A > 8:
            return "warm"
        elif B < 10 and A < 8:
            return "cool"
        else:
            return "neutral"
    
    def get_pantone_family(self, skin_lab: np.ndarray) -> str:
        """
        Approximate Pantone SkinTone family based on LAB values
        
        Pantone SkinTone Guide uses notation like: 1Y01, 2Y02, 3R05, etc.
        Format: [Depth][Undertone][Value]
        
        Args:
            skin_lab: LAB color vector [L, A, B]
            
        Returns:
            Pantone family approximation
        """
        if skin_lab is None or len(skin_lab) < 3:
            return "Unknown"
        
        L, A, B = skin_lab
        
        # Determine depth (1-7, where 1 is lightest)
        if L > 75:
            depth = 1
        elif L > 65:
            depth = 2
        elif L > 55:
            depth = 3
        elif L > 45:
            depth = 4
        elif L > 35:
            depth = 5
        elif L > 25:
            depth = 6
        else:
            depth = 7
        
        # Determine undertone letter
        if B > 15:
            undertone_letter = "Y"  # Yellow (warm)
        elif A > 10:
            undertone_letter = "R"  # Red (warm-neutral)
        elif B < 8:
            undertone_letter = "P"  # Pink (cool)
        else:
            undertone_letter = "N"  # Neutral
        
        # Value (simplified 01-10 based on combination)
        value = int((A + B) / 4) + 1
        value = min(max(value, 1), 10)
        
        return f"{depth}{undertone_letter}{value:02d}"
    
    def calculate_color_distance(self, lab1: np.ndarray, lab2: np.ndarray) -> float:
        """
        Calculate Delta E (ΔE) color distance in LAB space
        Using CIE76 formula (Euclidean distance)
        
        Args:
            lab1: First LAB color [L, A, B]
            lab2: Second LAB color [L, A, B]
            
        Returns:
            Delta E distance
        """
        return np.sqrt(np.sum((lab1 - lab2) ** 2))
    
    def lab_to_rgb(self, lab: np.ndarray) -> np.ndarray:
        """
        Convert LAB to RGB for visualization
        
        Args:
            lab: LAB color [L, A, B]
            
        Returns:
            RGB color [R, G, B] in range 0-255
        """
        # Create a 1x1 LAB image
        lab_img = np.uint8([[lab]])
        
        # Convert LAB to BGR
        bgr_img = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)
        
        # Convert BGR to RGB
        rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        
        return rgb[0, 0]
