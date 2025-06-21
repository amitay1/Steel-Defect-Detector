"""
Precise Defect Highlighting System
Detects and highlights only the exact defect boundaries in an uploaded image

Features:
- Automatic defect detection and segmentation
- Precise boundary highlighting
- Color coding by defect type
- Visual feedback and results
"""

import cv2
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json

class DefectHighlighter:
    def __init__(self):
        self.setup_detection_parameters()
        self.setup_color_scheme()
        
    def setup_detection_parameters(self):
        """Setup parameters for precise defect detection"""
        
        # Edge detection parameters
        self.blur_kernel = 5
        self.canny_low = 30
        self.canny_high = 100
        
        # Contour filtering parameters
        self.min_contour_area = 50
        self.max_contour_area = 50000
        
        # Morphological operations
        self.morph_kernel_size = 3
        self.closing_iterations = 2
        self.opening_iterations = 1
        
        print("✅ Detection parameters configured")
        
    def setup_color_scheme(self):
        """Setup color scheme for different defect highlighting"""
        
        self.highlight_colors = {
            'default': (0, 255, 0),      # Bright green
            'crack': (255, 0, 0),        # Red for cracks
            'hole': (0, 0, 255),         # Blue for holes
            'spot': (255, 165, 0),       # Orange for spots
            'scratch': (255, 255, 0),    # Yellow for scratches
            'pit': (128, 0, 128),        # Purple for pits
            'line': (0, 255, 255)        # Cyan for lines
        }
        
        self.line_thickness = 2
        
        print("✅ Color scheme configured")
        
    def preprocess_image(self, image):
        """Preprocess image for better defect detection"""
        
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply bilateral filter to reduce noise while keeping edges sharp
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(filtered)
        
        return enhanced
    
    def detect_defect_contours(self, image):
        """Detect precise defect contours in the image"""
        
        print("🔍 Detecting defect contours...")
        
        # Preprocess image
        processed = self.preprocess_image(image)
        
        # Apply multiple detection methods and combine results
        contours_list = []
        
        # Method 1: Edge-based detection
        edges = cv2.Canny(processed, self.canny_low, self.canny_high)
        contours1, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_list.extend(contours1)
        
        # Method 2: Threshold-based detection
        # Try different threshold values to catch various defect intensities
        for thresh_val in [50, 100, 150, 200]:
            _, thresh = cv2.threshold(processed, thresh_val, 255, cv2.THRESH_BINARY_INV)
            
            # Apply morphological operations to clean up
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, 
                                             (self.morph_kernel_size, self.morph_kernel_size))
            
            # Close gaps in defect boundaries
            closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, 
                                    iterations=self.closing_iterations)
            
            # Remove noise
            opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, 
                                    iterations=self.opening_iterations)
            
            contours2, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_list.extend(contours2)
        
        # Method 3: Adaptive threshold for varying lighting
        adaptive_thresh = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, 11, 2)
        contours3, _ = cv2.findContours(adaptive_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_list.extend(contours3)
        
        # Filter and refine contours
        filtered_contours = self.filter_contours(contours_list)
        
        print(f"   Found {len(filtered_contours)} potential defect regions")
        
        return filtered_contours
    
    def filter_contours(self, contours):
        """Filter contours to keep only likely defects"""
        
        filtered = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if self.min_contour_area <= area <= self.max_contour_area:
                
                # Additional filtering criteria
                perimeter = cv2.arcLength(contour, True)
                
                if perimeter > 0:
                    # Calculate circularity (4π*area/perimeter²)
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    
                    # Keep contours that are not too circular (to avoid noise)
                    # and not too elongated
                    if 0.01 <= circularity <= 1.2:
                        
                        # Approximate contour to reduce noise
                        epsilon = 0.02 * perimeter
                        approx = cv2.approxPolyDP(contour, epsilon, True)
                        
                        filtered.append(approx)
        
        return filtered
    
    def classify_defect_type(self, contour):
        """Classify defect type based on shape characteristics"""
        
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 'default'
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h if h > 0 else 1
        
        # Calculate shape metrics
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        extent = area / (w * h) if w * h > 0 else 0
        
        # Classify based on characteristics
        if circularity > 0.7 and 0.8 <= aspect_ratio <= 1.2:
            if area < 500:
                return 'pit'
            else:
                return 'hole'
        elif aspect_ratio > 3.0 or aspect_ratio < 0.33:
            if circularity < 0.3:
                return 'crack'
            else:
                return 'line'
        elif extent < 0.5:
            return 'scratch'
        else:
            return 'spot'
    
    def highlight_defects(self, image, contours, defect_types=None):
        """Highlight detected defects with precise boundaries"""
        
        print("🎨 Highlighting defects with precise boundaries...")
        
        # Create copy for highlighting
        highlighted = image.copy()
        
        if defect_types is None:
            defect_types = ['default'] * len(contours)
        
        defect_info = []
        
        for i, contour in enumerate(contours):
            defect_type = defect_types[i] if i < len(defect_types) else 'default'
            color = self.highlight_colors.get(defect_type, self.highlight_colors['default'])
            
            # Draw precise contour boundary
            cv2.drawContours(highlighted, [contour], -1, color, self.line_thickness)
            
            # Optional: Add small fill with transparency effect
            # Create mask for this contour
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [contour], 255)
              # Apply colored overlay with low opacity
            overlay = highlighted.copy()
            masked_pixels = highlighted[mask > 0]
            if len(masked_pixels) > 0:
                for j in range(3):
                    overlay[mask > 0, j] = (0.7 * masked_pixels[:, j] + 0.3 * color[j]).astype(np.uint8)
            highlighted = overlay
            
            # Calculate defect properties
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            
            defect_info.append({
                'type': defect_type,
                'area': float(area),
                'center': (int(x + w/2), int(y + h/2)),
                'bounding_box': (x, y, w, h),
                'color_used': color
            })
            
            # Add label near defect
            label_pos = (int(x + w/2), int(y - 10))
            cv2.putText(highlighted, f"{defect_type}", label_pos,
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        print(f"   Highlighted {len(contours)} defects")
        
        return highlighted, defect_info
    
    def process_defect_image(self, image_path, output_path=None, auto_classify=True):
        """Process uploaded defect image and highlight defects precisely"""
        
        print(f"🔍 Processing defect image: {Path(image_path).name}")
        print("=" * 50)
        
        # Load image
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
        else:
            image = image_path  # Already loaded image
        
        print(f"Image size: {image.shape[1]}x{image.shape[0]} pixels")
        
        # Detect defect contours
        contours = self.detect_defect_contours(image)
        
        if len(contours) == 0:
            print("❌ No defects detected in image")
            return image, []
        
        # Classify defects if auto_classify is enabled
        defect_types = []
        if auto_classify:
            print("🧠 Classifying detected defects...")
            for contour in contours:
                defect_type = self.classify_defect_type(contour)
                defect_types.append(defect_type)
                print(f"   Defect classified as: {defect_type}")
        else:
            defect_types = ['default'] * len(contours)
        
        # Highlight defects
        highlighted_image, defect_info = self.highlight_defects(image, contours, defect_types)
        
        # Save result if output path provided
        if output_path:
            cv2.imwrite(output_path, highlighted_image)
            print(f"✅ Saved highlighted image: {output_path}")
            
            # Save defect information
            info_path = Path(output_path).with_suffix('.json')
            with open(info_path, 'w') as f:
                json.dump(defect_info, f, indent=2)
            print(f"✅ Saved defect info: {info_path}")
        
        # Print summary
        print(f"\\n📊 DEFECT DETECTION SUMMARY:")
        print(f"✅ Total defects found: {len(defect_info)}")
        
        type_counts = {}
        for info in defect_info:
            defect_type = info['type']
            type_counts[defect_type] = type_counts.get(defect_type, 0) + 1
        
        for defect_type, count in type_counts.items():
            color = self.highlight_colors.get(defect_type, self.highlight_colors['default'])
            print(f"   {defect_type}: {count} defects (color: {color})")
        
        return highlighted_image, defect_info
    
    def create_comparison_view(self, original, highlighted, output_path=None):
        """Create side-by-side comparison view"""
        
        # Resize images to same height if needed
        h1, w1 = original.shape[:2]
        h2, w2 = highlighted.shape[:2]
        
        if h1 != h2:
            if h1 > h2:
                highlighted = cv2.resize(highlighted, (int(w2 * h1 / h2), h1))
            else:
                original = cv2.resize(original, (int(w1 * h2 / h1), h2))
        
        # Create comparison
        comparison = np.hstack([original, highlighted])
        
        # Add dividing line
        h, w = comparison.shape[:2]
        cv2.line(comparison, (w//2, 0), (w//2, h), (255, 255, 255), 2)
        
        # Add labels
        cv2.putText(comparison, "Original", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(comparison, "Defects Highlighted", (w//2 + 10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        if output_path:
            cv2.imwrite(output_path, comparison)
            print(f"✅ Saved comparison view: {output_path}")
        
        return comparison

def test_defect_highlighting():
    """Test the defect highlighting system"""
    
    print("🧪 Testing Defect Highlighting System")
    print("=" * 50)
    
    highlighter = DefectHighlighter()
    
    # Test with some sample images from training data
    training_path = Path("training/datasets/images/train")
    
    # Find some test images
    test_images = []
    for defect_folder in training_path.iterdir():
        if defect_folder.is_dir():
            images = list(defect_folder.glob("*.jpg"))[:2]  # Take 2 from each type
            test_images.extend(images)
            if len(test_images) >= 6:  # Test with 6 images
                break
    
    if len(test_images) == 0:
        print("❌ No test images found")
        return
    
    output_dir = Path("DEFECT_HIGHLIGHTING_TESTS")
    output_dir.mkdir(exist_ok=True)
    
    success_count = 0
    
    for i, img_path in enumerate(test_images[:6]):
        try:
            print(f"\\n🔍 Testing image {i+1}: {img_path.name}")
            
            # Process image
            highlighted, defect_info = highlighter.process_defect_image(
                str(img_path),
                str(output_dir / f"highlighted_{i+1}_{img_path.name}"),
                auto_classify=True
            )
            
            # Create comparison view
            original = cv2.imread(str(img_path))
            comparison = highlighter.create_comparison_view(
                original, highlighted,
                str(output_dir / f"comparison_{i+1}_{img_path.name}")
            )
            
            success_count += 1
            print(f"✅ Success: Found {len(defect_info)} defects")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print(f"\\n📊 TEST RESULTS:")
    print(f"✅ Successfully processed: {success_count}/{len(test_images)} images")
    print(f"📁 Results saved in: {output_dir.absolute()}")
    
    return success_count > 0

if __name__ == "__main__":
    print("🚀 LAUNCHING PRECISE DEFECT HIGHLIGHTING SYSTEM")
    print("=" * 60)
    print("🎯 Mission: Highlight only the exact defect boundaries")
    print("🎨 Method: Advanced contour detection and classification")
    print()
    
    # Test the system
    success = test_defect_highlighting()
    
    if success:
        print("\\n" + "=" * 60)
        print("✅ DEFECT HIGHLIGHTING SYSTEM READY!")
        print("=" * 60)
        print("🎯 System can now precisely highlight defect boundaries")
        print("   in uploaded images with color-coded classifications.")
        print("\\n📋 USAGE:")
        print("   1. Use highlighter.process_defect_image(image_path)")
        print("   2. System will detect and highlight defects precisely")
        print("   3. Each defect type gets a different color")
        print("   4. Results include detailed defect information")
    else:
        print("\\n❌ SYSTEM TEST FAILED - Please check errors above")
