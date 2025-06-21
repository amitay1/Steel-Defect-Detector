"""
ASTM Reference Generator
Generates reference images and cards for ASTM standards compliance
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import os
from pathlib import Path
from astm_standards import MetalType, QualityGrade

@dataclass
class ReferenceCard:
    """Reference card data structure"""
    id: str
    metal_type: str
    quality_grade: str
    thickness_range: Tuple[float, float]
    reference_image: np.ndarray
    defect_examples: List[Dict[str, Any]]
    standards_reference: str
    creation_date: str

class ASTMReferenceGenerator:
    """Generator for ASTM standard reference images and cards"""
    
    def __init__(self):
        """Initialize the ASTM reference generator"""
        self.reference_cards = {}
        self.standards_db = self._initialize_standards_db()
        
    def _initialize_standards_db(self) -> Dict[str, Any]:
        """Initialize the standards database"""
        return {
            'steel': {
                'grades': ['A', 'B', 'C'],
                'thickness_ranges': [(0.5, 2.0), (2.0, 5.0), (5.0, 10.0)],
                'allowable_defects': {
                    'A': {'max_size': 0.5, 'max_count': 2},
                    'B': {'max_size': 1.0, 'max_count': 5},
                    'C': {'max_size': 2.0, 'max_count': 10}
                }
            },
            'aluminum': {
                'grades': ['A', 'B', 'C'],
                'thickness_ranges': [(0.2, 1.0), (1.0, 3.0), (3.0, 8.0)],
                'allowable_defects': {
                    'A': {'max_size': 0.3, 'max_count': 1},
                    'B': {'max_size': 0.8, 'max_count': 3},
                    'C': {'max_size': 1.5, 'max_count': 8}
                }
            },
            'copper': {
                'grades': ['A', 'B', 'C'],
                'thickness_ranges': [(0.3, 1.5), (1.5, 4.0), (4.0, 9.0)],
                'allowable_defects': {
                    'A': {'max_size': 0.4, 'max_count': 1},
                    'B': {'max_size': 0.9, 'max_count': 4},
                    'C': {'max_size': 1.8, 'max_count': 9}
                }
            }
        }
    
    def generate_reference_card(self, 
                              metal_type: str, 
                              quality_grade: str, 
                              thickness: float) -> ReferenceCard:
        """Generate a reference card for specific parameters"""
        
        # Create synthetic reference image
        reference_image = self._create_reference_image(metal_type, quality_grade, thickness)
        
        # Generate defect examples
        defect_examples = self._generate_defect_examples(metal_type, quality_grade)
        
        # Create reference card
        card_id = f"{metal_type}_{quality_grade}_{thickness:.1f}mm"
        
        reference_card = ReferenceCard(
            id=card_id,
            metal_type=metal_type,
            quality_grade=quality_grade,
            thickness_range=(thickness * 0.9, thickness * 1.1),
            reference_image=reference_image,
            defect_examples=defect_examples,
            standards_reference=f"ASTM-E1932-{metal_type.upper()}-{quality_grade}",
            creation_date="2025-06-20"
        )
        
        self.reference_cards[card_id] = reference_card
        return reference_card
    
    def _create_reference_image(self, metal_type: str, quality_grade: str, thickness: float) -> np.ndarray:
        """Create a synthetic reference image"""
        
        # Base image dimensions
        height, width = 400, 600
        
        # Create base metal surface
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
        noise = np.random.normal(0, 10, (height, width, 3))
        image = np.clip(image + noise, 0, 255).astype(np.uint8)
        
        # Add acceptable defects based on quality grade
        if quality_grade in self.standards_db.get(metal_type, {}).get('allowable_defects', {}):
            defect_params = self.standards_db[metal_type]['allowable_defects'][quality_grade]
            self._add_acceptable_defects(image, defect_params)
        
        return image
    
    def _add_acceptable_defects(self, image: np.ndarray, defect_params: Dict[str, Any]):
        """Add acceptable defects to reference image"""
        
        max_size = defect_params['max_size']
        max_count = defect_params['max_count']
        
        height, width = image.shape[:2]
        
        # Add some acceptable defects
        num_defects = min(max_count, np.random.randint(0, max_count + 1))
        
        for _ in range(num_defects):
            # Random position
            x = np.random.randint(int(max_size * 20), width - int(max_size * 20))
            y = np.random.randint(int(max_size * 20), height - int(max_size * 20))
            
            # Random size within acceptable range
            size = np.random.uniform(max_size * 0.3, max_size)
            radius = int(size * 10)  # Convert to pixels
            
            # Add small defect
            cv2.circle(image, (x, y), radius, (50, 50, 50), -1)
    
    def _generate_defect_examples(self, metal_type: str, quality_grade: str) -> List[Dict[str, Any]]:
        """Generate examples of acceptable defects"""
        
        examples = []
        
        if metal_type in self.standards_db and quality_grade in self.standards_db[metal_type]['allowable_defects']:
            params = self.standards_db[metal_type]['allowable_defects'][quality_grade]
            
            examples.append({
                'type': 'surface_scratch',
                'max_size_mm': params['max_size'],
                'acceptable_count': params['max_count'],
                'severity': 'minor' if quality_grade == 'A' else 'moderate' if quality_grade == 'B' else 'major'
            })
            
            examples.append({
                'type': 'pit_corrosion',
                'max_depth_mm': params['max_size'] * 0.5,
                'acceptable_count': max(1, params['max_count'] // 2),
                'severity': 'minor' if quality_grade == 'A' else 'moderate' if quality_grade == 'B' else 'major'
            })
        
        return examples
    
    def get_reference_card(self, metal_type: str, quality_grade: str, thickness: float) -> Optional[ReferenceCard]:
        """Get or generate a reference card"""
        
        card_id = f"{metal_type}_{quality_grade}_{thickness:.1f}mm"
        
        if card_id not in self.reference_cards:
            return self.generate_reference_card(metal_type, quality_grade, thickness)
        
        return self.reference_cards[card_id]
    
    def compare_with_reference(self, 
                             test_image: np.ndarray, 
                             reference_card: ReferenceCard,
                             detected_defects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare test image with reference card"""
        
        result = {
            'compliance': 'UNKNOWN',
            'pass_fail': False,
            'defect_analysis': [],
            'recommendations': []
        }
        
        # Analyze detected defects against reference standards
        allowable_params = self.standards_db.get(
            reference_card.metal_type, {}
        ).get('allowable_defects', {}).get(
            reference_card.quality_grade, {'max_size': 1.0, 'max_count': 5}
        )
        
        defect_count = len(detected_defects)
        max_defect_size = 0
        
        for defect in detected_defects:
            # Estimate defect size from bounding box
            bbox = defect.get('bbox', [0, 0, 10, 10])
            if len(bbox) >= 4:
                width = abs(bbox[2] - bbox[0])
                height = abs(bbox[3] - bbox[1])
                # Convert pixels to approximate mm (rough estimation)
                size_mm = max(width, height) * 0.1  # Assuming 10 pixels = 1mm
                max_defect_size = max(max_defect_size, size_mm)
        
        # Check compliance
        count_ok = defect_count <= allowable_params['max_count']
        size_ok = max_defect_size <= allowable_params['max_size']
        
        if count_ok and size_ok:
            result['compliance'] = 'COMPLIANT'
            result['pass_fail'] = True
        else:
            result['compliance'] = 'NON_COMPLIANT'
            result['pass_fail'] = False
        
        # Add analysis details
        result['defect_analysis'] = [
            f"Detected defects: {defect_count} (limit: {allowable_params['max_count']})",
            f"Max defect size: {max_defect_size:.2f}mm (limit: {allowable_params['max_size']}mm)",
            f"Count compliance: {'PASS' if count_ok else 'FAIL'}",
            f"Size compliance: {'PASS' if size_ok else 'FAIL'}"
        ]
        
        # Add recommendations
        if not count_ok:
            result['recommendations'].append(f"Reduce defect count from {defect_count} to {allowable_params['max_count']}")
        
        if not size_ok:
            result['recommendations'].append(f"Reduce maximum defect size from {max_defect_size:.2f}mm to {allowable_params['max_size']}mm")
        
        if count_ok and size_ok:
            result['recommendations'].append("Material meets ASTM standards for specified grade")
        
        return result
