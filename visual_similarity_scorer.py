"""
Visual Similarity Scorer
Calculates visual similarity between test images and reference images
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import math

@dataclass
class SimilarityResult:
    """Result of visual similarity analysis"""
    overall_score: float
    histogram_similarity: float
    structural_similarity: float
    texture_similarity: float
    edge_similarity: float
    recommendations: List[str]

class VisualSimilarityScorer:
    """Calculates comprehensive visual similarity scores"""
    
    def __init__(self):
        """Initialize the visual similarity scorer"""
        self.target_size = (256, 256)  # Standard size for comparison
        
    def calculate_similarity(self, 
                           test_image: np.ndarray, 
                           reference_image: np.ndarray,
                           detailed: bool = True) -> SimilarityResult:
        """Calculate comprehensive visual similarity between two images"""
        
        # Preprocess images
        test_processed = self._preprocess_image(test_image)
        ref_processed = self._preprocess_image(reference_image)
        
        # Calculate different similarity metrics
        hist_sim = self._calculate_histogram_similarity(test_processed, ref_processed)
        struct_sim = self._calculate_structural_similarity(test_processed, ref_processed)
        texture_sim = self._calculate_texture_similarity(test_processed, ref_processed)
        edge_sim = self._calculate_edge_similarity(test_processed, ref_processed)
        
        # Weighted overall score
        weights = {
            'histogram': 0.25,
            'structural': 0.35,
            'texture': 0.25,
            'edge': 0.15
        }
        
        overall_score = (
            hist_sim * weights['histogram'] +
            struct_sim * weights['structural'] +
            texture_sim * weights['texture'] +
            edge_sim * weights['edge']
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            hist_sim, struct_sim, texture_sim, edge_sim
        )
        
        return SimilarityResult(
            overall_score=overall_score,
            histogram_similarity=hist_sim,
            structural_similarity=struct_sim,
            texture_similarity=texture_sim,
            edge_similarity=edge_sim,
            recommendations=recommendations
        )
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for similarity analysis"""
        
        # Resize to standard size
        resized = cv2.resize(image, self.target_size)
        
        # Normalize lighting
        if len(resized.shape) == 3:
            lab = cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            normalized = cv2.merge([l, a, b])
            result = cv2.cvtColor(normalized, cv2.COLOR_LAB2BGR)
        else:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            result = clahe.apply(resized)
        
        return result
    
    def _calculate_histogram_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate histogram-based similarity"""
        
        # Convert to grayscale if needed
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray1, gray2 = img1, img2
        
        # Calculate histograms
        hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
        
        # Normalize histograms
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
        
        # Calculate correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        return max(0, correlation)
    
    def _calculate_structural_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate structural similarity (simplified SSIM)"""
        
        # Convert to grayscale if needed
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray1, gray2 = img1, img2
        
        # Convert to float
        img1_float = gray1.astype(np.float64)
        img2_float = gray2.astype(np.float64)
        
        # Calculate means
        mu1 = np.mean(img1_float)
        mu2 = np.mean(img2_float)
        
        # Calculate variances and covariance
        var1 = np.var(img1_float)
        var2 = np.var(img2_float)
        cov = np.mean((img1_float - mu1) * (img2_float - mu2))
        
        # SSIM constants
        c1 = 0.01 ** 2
        c2 = 0.03 ** 2
        
        # Calculate SSIM
        numerator = (2 * mu1 * mu2 + c1) * (2 * cov + c2)
        denominator = (mu1**2 + mu2**2 + c1) * (var1 + var2 + c2)
        
        if denominator == 0:
            return 1.0 if numerator == 0 else 0.0
        
        ssim = numerator / denominator
        return max(0, min(1, ssim))
    
    def _calculate_texture_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate texture-based similarity using Local Binary Patterns"""
        
        # Convert to grayscale if needed
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray1, gray2 = img1, img2
        
        # Simple texture analysis using gradient magnitude
        # Calculate gradients
        grad_x1 = cv2.Sobel(gray1, cv2.CV_64F, 1, 0, ksize=3)
        grad_y1 = cv2.Sobel(gray1, cv2.CV_64F, 0, 1, ksize=3)
        grad_mag1 = np.sqrt(grad_x1**2 + grad_y1**2)
        
        grad_x2 = cv2.Sobel(gray2, cv2.CV_64F, 1, 0, ksize=3)
        grad_y2 = cv2.Sobel(gray2, cv2.CV_64F, 0, 1, ksize=3)
        grad_mag2 = np.sqrt(grad_x2**2 + grad_y2**2)
        
        # Calculate histograms of gradient magnitudes
        hist1 = cv2.calcHist([grad_mag1.astype(np.uint8)], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([grad_mag2.astype(np.uint8)], [0], None, [256], [0, 256])
        
        # Normalize histograms
        cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)
        
        # Calculate correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        return max(0, correlation)
    
    def _calculate_edge_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate edge-based similarity"""
        
        # Convert to grayscale if needed
        if len(img1.shape) == 3:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        else:
            gray1, gray2 = img1, img2
        
        # Apply Canny edge detection
        edges1 = cv2.Canny(gray1, 50, 150)
        edges2 = cv2.Canny(gray2, 50, 150)
        
        # Calculate edge density similarity
        edge_density1 = np.sum(edges1 > 0) / edges1.size
        edge_density2 = np.sum(edges2 > 0) / edges2.size
        
        density_similarity = 1 - abs(edge_density1 - edge_density2)
        
        # Calculate edge pattern similarity using template matching
        if np.sum(edges1) > 0 and np.sum(edges2) > 0:
            result = cv2.matchTemplate(edges1, edges2, cv2.TM_CCOEFF_NORMED)
            pattern_similarity = np.max(result)
        else:
            pattern_similarity = 1.0 if edge_density1 == edge_density2 == 0 else 0.0
        
        # Combine similarities
        edge_similarity = (density_similarity + pattern_similarity) / 2
        
        return max(0, min(1, edge_similarity))
    
    def _generate_recommendations(self, 
                                hist_sim: float, 
                                struct_sim: float, 
                                texture_sim: float, 
                                edge_sim: float) -> List[str]:
        """Generate recommendations based on similarity scores"""
        
        recommendations = []
        
        if hist_sim < 0.7:
            recommendations.append("Consider adjusting lighting or exposure for better color matching")
        
        if struct_sim < 0.6:
            recommendations.append("Structural patterns differ significantly from reference")
        
        if texture_sim < 0.5:
            recommendations.append("Surface texture shows notable differences from reference")
        
        if edge_sim < 0.6:
            recommendations.append("Edge patterns indicate potential defects or surface irregularities")
        
        if all(score > 0.8 for score in [hist_sim, struct_sim, texture_sim, edge_sim]):
            recommendations.append("Excellent visual similarity to reference image")
        elif all(score > 0.6 for score in [hist_sim, struct_sim, texture_sim, edge_sim]):
            recommendations.append("Good visual similarity with minor variations")
        else:
            recommendations.append("Significant visual differences detected - further analysis recommended")
        
        return recommendations
    
    def calculate_defect_similarity(self, 
                                  test_defects: List[Dict[str, Any]], 
                                  reference_defects: List[Dict[str, Any]]) -> float:
        """Calculate similarity between defect patterns"""
        
        if not test_defects and not reference_defects:
            return 1.0  # Both have no defects - perfect match
        
        if not test_defects or not reference_defects:
            return 0.0  # One has defects, other doesn't
        
        # Compare defect counts
        count_similarity = 1 - abs(len(test_defects) - len(reference_defects)) / max(len(test_defects), len(reference_defects))
        
        # Compare average defect sizes
        test_avg_size = np.mean([self._get_defect_size(d) for d in test_defects])
        ref_avg_size = np.mean([self._get_defect_size(d) for d in reference_defects])
        
        size_similarity = 1 - abs(test_avg_size - ref_avg_size) / max(test_avg_size, ref_avg_size)
        
        # Combine similarities
        defect_similarity = (count_similarity + size_similarity) / 2
        
        return max(0, min(1, defect_similarity))
    
    def _get_defect_size(self, defect: Dict[str, Any]) -> float:
        """Get approximate defect size from bounding box"""
        
        bbox = defect.get('bbox', [0, 0, 10, 10])
        if len(bbox) >= 4:
            width = abs(bbox[2] - bbox[0])
            height = abs(bbox[3] - bbox[1])
            return math.sqrt(width * height)  # Approximate area-based size
        
        return 10.0  # Default size
    
    def compare_multiple_references(self, 
                                  test_image: np.ndarray, 
                                  reference_images: List[np.ndarray]) -> List[SimilarityResult]:
        """Compare test image against multiple reference images"""
        
        results = []
        
        for ref_image in reference_images:
            similarity = self.calculate_similarity(test_image, ref_image)
            results.append(similarity)
        
        return results
    
    def find_best_match(self, 
                       test_image: np.ndarray, 
                       reference_images: List[Tuple[str, np.ndarray]]) -> Tuple[str, SimilarityResult]:
        """Find the best matching reference image"""
        
        best_match_id = None
        best_similarity = None
        best_score = 0
        
        for ref_id, ref_image in reference_images:
            similarity = self.calculate_similarity(test_image, ref_image)
            
            if similarity.overall_score > best_score:
                best_score = similarity.overall_score
                best_match_id = ref_id
                best_similarity = similarity
        
        return best_match_id, best_similarity
