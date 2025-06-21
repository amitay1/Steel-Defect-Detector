#!/usr/bin/env python3
"""
Test the highlighting functionality by creating a test image with visible defects
"""

import cv2
import numpy as np
import os
from unified_intelligent_defect_analyzer import UnifiedIntelligentDefectAnalyzer

def create_test_image_with_defects():
    """Create a test image with clear defects for testing"""
    
    # Create a metal-like base image
    height, width = 400, 600
    base_color = (120, 120, 130)  # Steel-like color
    
    # Create base image
    image = np.full((height, width, 3), base_color, dtype=np.uint8)
    
    # Add metal texture
    noise = np.random.normal(0, 10, (height, width, 3))
    image = np.clip(image + noise, 0, 255).astype(np.uint8)
    
    # Add clear defects that should be detected
    
    # Defect 1: Dark spot (rust/corrosion)
    cv2.circle(image, (150, 100), 15, (60, 60, 70), -1)
    cv2.circle(image, (150, 100), 20, (80, 80, 90), 3)
    
    # Defect 2: Scratch
    cv2.line(image, (300, 150), (350, 180), (50, 50, 60), 4)
    
    # Defect 3: Pit
    cv2.circle(image, (450, 250), 12, (40, 40, 50), -1)
    
    # Defect 4: Inclusion
    cv2.ellipse(image, (200, 300), (25, 15), 30, 0, 360, (30, 30, 40), -1)
    
    # Defect 5: Surface crack
    pts = np.array([[100, 200], [120, 210], [140, 205], [160, 220]], np.int32)
    cv2.polylines(image, [pts], False, (40, 40, 50), 3)
    
    return image

def test_highlighting():
    """Test the highlighting functionality"""
    
    print("🔬 Testing Defect Highlighting System")
    print("=" * 40)
    
    # Create test image
    print("📸 Creating test image with visible defects...")
    test_image = create_test_image_with_defects()
    test_image_path = "test_defects_image.jpg"
    cv2.imwrite(test_image_path, test_image)
    print(f"✅ Test image saved: {test_image_path}")
    
    # Initialize analyzer
    print("🚀 Initializing analyzer...")
    analyzer = UnifiedIntelligentDefectAnalyzer()
    
    # Run analysis
    print("🔍 Running analysis...")
    result = analyzer.analyze_image_unified(
        image_path=test_image_path,
        metal_type="steel",
        thickness=2.0,
        quality_grade="B",
        enable_grid_analysis=True
    )
    
    # Check results
    print("\\n📊 Analysis Results:")
    print(f"   Defects detected: {result.total_defects_detected}")
    print(f"   Pixels highlighted: {result.defect_pixels_highlighted}")
    
    # Save highlighted image
    if result.yellow_highlighted_image is not None:
        highlighted_path = "test_highlighted_result.jpg"
        cv2.imwrite(highlighted_path, result.yellow_highlighted_image)
        print(f"   ✅ Highlighted image saved: {highlighted_path}")
        
        # Check if highlighting actually occurred
        original_diff = np.sum(np.abs(test_image.astype(int) - result.yellow_highlighted_image.astype(int)))
        if original_diff > 0:
            print(f"   🟡 Image was modified (diff: {original_diff})")
        else:
            print("   ⚠️ No highlighting detected - image unchanged")
    else:
        print("   ❌ No highlighted image generated")
    
    return result

if __name__ == "__main__":
    test_highlighting()
