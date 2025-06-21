"""
Reference Image System
Manages reference images for metal defect analysis and ASTM compliance
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import os
from pathlib import Path
import json

@dataclass
class ReferenceImage:
    """Reference image data structure"""
    id: str
    name: str
    metal_type: str
    quality_grade: str
    thickness: float
    image_data: np.ndarray
    metadata: Dict[str, Any]
    file_path: Optional[str] = None

class ReferenceImageManager:
    """Manages reference images for defect analysis"""
    
    def __init__(self, reference_dir: str = "reference_images"):
        """Initialize the reference image manager"""
        self.reference_dir = Path(reference_dir)
        self.reference_dir.mkdir(exist_ok=True)
        
        self.reference_images = {}
        self.metadata_cache = {}
        
        # Load existing reference images
        self._load_existing_references()
    
    def _load_existing_references(self):
        """Load existing reference images from directory"""
        
        metadata_file = self.reference_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    self.metadata_cache = json.load(f)
            except Exception as e:
                print(f"Warning: Could not load reference metadata: {e}")
                self.metadata_cache = {}
        
        # Load image files
        for image_file in self.reference_dir.glob("*.jpg"):
            try:
                image_id = image_file.stem
                image_data = cv2.imread(str(image_file))
                
                if image_data is not None and image_id in self.metadata_cache:
                    metadata = self.metadata_cache[image_id]
                    
                    ref_image = ReferenceImage(
                        id=image_id,
                        name=metadata.get('name', image_id),
                        metal_type=metadata.get('metal_type', 'unknown'),
                        quality_grade=metadata.get('quality_grade', 'C'),
                        thickness=metadata.get('thickness', 1.0),
                        image_data=image_data,
                        metadata=metadata,
                        file_path=str(image_file)
                    )
                    
                    self.reference_images[image_id] = ref_image
                    
            except Exception as e:
                print(f"Warning: Could not load reference image {image_file}: {e}")
    
    def add_reference_image(self, 
                          image_data: np.ndarray,
                          metal_type: str,
                          quality_grade: str,
                          thickness: float,
                          name: Optional[str] = None) -> str:
        """Add a new reference image"""
        
        # Generate unique ID
        image_id = f"ref_{metal_type}_{quality_grade}_{thickness:.1f}mm_{len(self.reference_images)}"
        
        if name is None:
            name = f"{metal_type.title()} Grade {quality_grade} ({thickness}mm)"
        
        # Create metadata
        metadata = {
            'name': name,
            'metal_type': metal_type,
            'quality_grade': quality_grade,
            'thickness': thickness,
            'creation_date': "2025-06-20",
            'image_size': image_data.shape[:2],
            'source': 'generated'
        }
        
        # Save image file
        image_file = self.reference_dir / f"{image_id}.jpg"
        cv2.imwrite(str(image_file), image_data)
        
        # Create reference image object
        ref_image = ReferenceImage(
            id=image_id,
            name=name,
            metal_type=metal_type,
            quality_grade=quality_grade,
            thickness=thickness,
            image_data=image_data,
            metadata=metadata,
            file_path=str(image_file)
        )
        
        # Store in memory
        self.reference_images[image_id] = ref_image
        self.metadata_cache[image_id] = metadata
        
        # Save metadata
        self._save_metadata()
        
        return image_id
    
    def get_reference_image(self, 
                          metal_type: str,
                          quality_grade: str,
                          thickness: float,
                          tolerance: float = 0.5) -> Optional[ReferenceImage]:
        """Get best matching reference image"""
        
        best_match = None
        best_score = 0
        
        for ref_id, ref_image in self.reference_images.items():
            # Calculate matching score
            score = 0
            
            # Metal type match (most important)
            if ref_image.metal_type.lower() == metal_type.lower():
                score += 40
            
            # Quality grade match
            if ref_image.quality_grade.upper() == quality_grade.upper():
                score += 30
            
            # Thickness match (with tolerance)
            thickness_diff = abs(ref_image.thickness - thickness)
            if thickness_diff <= tolerance:
                thickness_score = 30 * (1 - thickness_diff / tolerance)
                score += thickness_score
            
            # Update best match
            if score > best_score:
                best_score = score
                best_match = ref_image
        
        return best_match
    
    def find_similar_references(self, 
                              test_image: np.ndarray,
                              metal_type: Optional[str] = None,
                              top_k: int = 3) -> List[Tuple[ReferenceImage, float]]:
        """Find similar reference images using visual similarity"""
        
        similarities = []
        
        for ref_id, ref_image in self.reference_images.items():
            # Filter by metal type if specified
            if metal_type and ref_image.metal_type.lower() != metal_type.lower():
                continue
            
            # Calculate visual similarity
            similarity = self._calculate_image_similarity(test_image, ref_image.image_data)
            similarities.append((ref_image, similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _calculate_image_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate visual similarity between two images"""
        
        try:
            # Resize images to same size for comparison
            target_size = (256, 256)
            img1_resized = cv2.resize(img1, target_size)
            img2_resized = cv2.resize(img2, target_size)
            
            # Convert to grayscale
            gray1 = cv2.cvtColor(img1_resized, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)
            
            # Calculate histogram correlation
            hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
            
            correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            
            # Calculate structural similarity (simplified)
            # Using normalized cross-correlation
            ncc = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0][0]
            
            # Combine metrics
            similarity = (correlation + ncc) / 2.0
            return max(0, similarity)
            
        except Exception as e:
            print(f"Warning: Could not calculate similarity: {e}")
            return 0.0
    
    def _save_metadata(self):
        """Save metadata to file"""
        
        metadata_file = self.reference_dir / "metadata.json"
        try:
            with open(metadata_file, 'w') as f:
                json.dump(self.metadata_cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save metadata: {e}")
    
    def create_default_references(self):
        """Create default reference images for common materials"""
        
        print("Creating default reference images...")
        
        # Define default materials
        materials = [
            ('steel', 'A', 2.0),
            ('steel', 'B', 3.0),
            ('steel', 'C', 5.0),
            ('aluminum', 'A', 1.0),
            ('aluminum', 'B', 2.0),
            ('aluminum', 'C', 3.0),
            ('copper', 'A', 1.5),
            ('copper', 'B', 2.5),
            ('copper', 'C', 4.0)
        ]
        
        for metal_type, quality_grade, thickness in materials:
            # Create synthetic reference image
            ref_image = self._create_synthetic_reference(metal_type, quality_grade, thickness)
            
            # Add to system
            self.add_reference_image(
                image_data=ref_image,
                metal_type=metal_type,
                quality_grade=quality_grade,
                thickness=thickness,
                name=f"{metal_type.title()} Grade {quality_grade} Reference"
            )
        
        print(f"Created {len(materials)} default reference images")
    
    def _create_synthetic_reference(self, metal_type: str, quality_grade: str, thickness: float) -> np.ndarray:
        """Create a synthetic reference image"""
        
        # Image dimensions
        height, width = 400, 600
        
        # Base color based on metal type
        if metal_type == 'steel':
            base_color = (100, 100, 120)  # Steel gray
        elif metal_type == 'aluminum':
            base_color = (200, 200, 200)  # Aluminum silver
        elif metal_type == 'copper':
            base_color = (80, 120, 180)   # Copper brownish
        else:
            base_color = (128, 128, 128)  # Default gray
        
        # Create base image
        image = np.full((height, width, 3), base_color, dtype=np.uint8)
        
        # Add metal texture
        noise = np.random.normal(0, 15, (height, width, 3))
        image = np.clip(image + noise, 0, 255).astype(np.uint8)
        
        # Add surface patterns
        self._add_metal_surface_patterns(image, metal_type)
        
        # Add acceptable defects based on quality grade
        self._add_reference_defects(image, quality_grade)
        
        return image
    
    def _add_metal_surface_patterns(self, image: np.ndarray, metal_type: str):
        """Add realistic metal surface patterns"""
        
        height, width = image.shape[:2]
        
        if metal_type == 'steel':
            # Add rolling patterns
            for i in range(0, height, 20):
                cv2.line(image, (0, i), (width, i), (90, 90, 110), 1)
        
        elif metal_type == 'aluminum':
            # Add brushed finish
            for i in range(0, width, 3):
                cv2.line(image, (i, 0), (i, height), (190, 190, 190), 1)
        
        elif metal_type == 'copper':
            # Add patina patterns
            for _ in range(10):
                x = np.random.randint(0, width)
                y = np.random.randint(0, height)
                cv2.circle(image, (x, y), np.random.randint(5, 15), (70, 110, 170), -1)
    
    def _add_reference_defects(self, image: np.ndarray, quality_grade: str):
        """Add reference defects based on quality grade"""
        
        height, width = image.shape[:2]
        
        # Define defect parameters by grade
        if quality_grade == 'A':
            num_defects = np.random.randint(0, 2)
            defect_size_range = (2, 5)
        elif quality_grade == 'B':
            num_defects = np.random.randint(1, 4)
            defect_size_range = (3, 8)
        else:  # Grade C
            num_defects = np.random.randint(2, 6)
            defect_size_range = (5, 12)
        
        # Add defects
        for _ in range(num_defects):
            x = np.random.randint(20, width - 20)
            y = np.random.randint(20, height - 20)
            size = np.random.randint(*defect_size_range)
            
            # Random defect type
            defect_type = np.random.choice(['scratch', 'pit', 'inclusion'])
            
            if defect_type == 'scratch':
                # Linear scratch
                x2 = x + np.random.randint(-30, 30)
                y2 = y + np.random.randint(-10, 10)
                cv2.line(image, (x, y), (x2, y2), (50, 50, 50), 2)
            
            elif defect_type == 'pit':
                # Circular pit
                cv2.circle(image, (x, y), size//2, (40, 40, 40), -1)
            
            else:  # inclusion
                # Irregular inclusion
                cv2.ellipse(image, (x, y), (size, size//2), 
                          np.random.randint(0, 180), 0, 360, (30, 30, 30), -1)
    
    def get_all_references(self) -> Dict[str, ReferenceImage]:
        """Get all available reference images"""
        return self.reference_images.copy()
    
    def get_reference_by_id(self, ref_id: str) -> Optional[ReferenceImage]:
        """Get reference image by ID"""
        return self.reference_images.get(ref_id)
    
    def remove_reference(self, ref_id: str) -> bool:
        """Remove a reference image"""
        
        if ref_id in self.reference_images:
            ref_image = self.reference_images[ref_id]
            
            # Remove file
            if ref_image.file_path and os.path.exists(ref_image.file_path):
                os.remove(ref_image.file_path)
            
            # Remove from memory
            del self.reference_images[ref_id]
            
            # Remove from metadata
            if ref_id in self.metadata_cache:
                del self.metadata_cache[ref_id]
            
            # Save updated metadata
            self._save_metadata()
            
            return True
        
        return False
