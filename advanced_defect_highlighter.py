#!/usr/bin/env python3
"""
Advanced Steel Defect Detection and Highlighting System
======================================================

This system combines our existing highlighting capabilities with advanced 
techniques from steel defect detection research, including:
- Advanced normalization and transforms
- Sophisticated mask processing
- Multi-scale feature detection
- Professional-grade image preprocessing

Features:
- Uses ImageNet normalization for better feature detection
- Advanced morphological operations
- Stratified defect analysis
- Multi-scale edge detection
- Professional mask processing

Author: AI Assistant
Date: June 2025
"""

import cv2
import numpy as np
import os
import sys
import json
from pathlib import Path
import argparse
from datetime import datetime
from sklearn.model_selection import StratifiedKFold
import warnings
warnings.filterwarnings("ignore")

class AdvancedDefectHighlighter:
    def __init__(self):
        """Initialize the advanced defect highlighter with research-grade parameters."""
        
        # Advanced normalization (ImageNet standards for better feature detection)
        self.mean = np.array([0.485, 0.456, 0.406])  # ImageNet mean
        self.std = np.array([0.229, 0.224, 0.225])   # ImageNet std
        
        # Multi-scale edge detection parameters
        self.edge_scales = [
            {'blur': 3, 'canny_low': 30, 'canny_high': 80},   # Fine details
            {'blur': 5, 'canny_low': 20, 'canny_high': 60},   # Medium features
            {'blur': 7, 'canny_low': 40, 'canny_high': 100}   # Large structures
        ]
        
        # Advanced morphological parameters
        self.morph_kernels = {
            'fine': cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
            'medium': cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
            'coarse': cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        }
        
        # Stratified filtering parameters by defect class
        self.defect_classes = {
            'micro': {'min_area': 10, 'max_area': 50, 'solidity_thresh': 0.3},
            'small': {'min_area': 20, 'max_area': 200, 'solidity_thresh': 0.4},
            'medium': {'min_area': 50, 'max_area': 1000, 'solidity_thresh': 0.3},
            'large': {'min_area': 200, 'max_area': 5000, 'solidity_thresh': 0.2},
            'linear': {'min_area': 30, 'max_area': 2000, 'aspect_ratio_min': 3.0},
            'circular': {'min_area': 20, 'max_area': 1000, 'circularity_min': 0.7}
        }
        
        # Professional color coding (research-grade visualization)
        self.class_colors = {
            'micro': (0, 255, 255),      # Bright Yellow
            'small': (0, 255, 255),      # Yellow  
            'medium': (0, 165, 255),     # Orange
            'large': (0, 0, 255),        # Red
            'linear': (255, 0, 255),     # Magenta
            'circular': (255, 255, 0),   # Cyan
            'irregular': (0, 255, 0),    # Green
            'unknown': (128, 128, 128)   # Gray
        }
        
        # Output directory
        self.output_dir = "ADVANCED_DEFECT_ANALYSIS"
        os.makedirs(self.output_dir, exist_ok=True)
        
    def normalize_image(self, image):
        """Apply ImageNet normalization for better feature detection."""
        # Convert to float and normalize to [0, 1]
        image_norm = image.astype(np.float32) / 255.0
        
        # Apply ImageNet normalization
        for i in range(3):
            image_norm[:, :, i] = (image_norm[:, :, i] - self.mean[i]) / self.std[i]
        
        # Convert back to displayable range
        image_norm = np.clip(image_norm, -2.0, 2.0)  # Clip extreme values
        image_norm = (image_norm + 2.0) / 4.0  # Normalize to [0, 1]
        image_norm = (image_norm * 255).astype(np.uint8)
        
        return image_norm
    
    def multi_scale_edge_detection(self, gray_image):
        """Apply multi-scale edge detection for robust feature extraction."""
        edge_maps = []
        
        for scale in self.edge_scales:
            # Apply Gaussian blur at current scale
            blurred = cv2.GaussianBlur(gray_image, (scale['blur'], scale['blur']), 0)
            
            # Canny edge detection
            edges_canny = cv2.Canny(blurred, scale['canny_low'], scale['canny_high'])
            
            # Sobel edge detection
            sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
            sobel = np.sqrt(sobelx**2 + sobely**2)
            sobel = np.uint8(sobel / sobel.max() * 255)
            edges_sobel = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY)[1]
            
            # Combine Canny and Sobel
            combined_edges = cv2.bitwise_or(edges_canny, edges_sobel)
            edge_maps.append(combined_edges)
        
        # Combine all scales with weighted sum
        final_edges = np.zeros_like(edge_maps[0], dtype=np.float32)
        weights = [0.4, 0.35, 0.25]  # Give more weight to fine details
        
        for edge_map, weight in zip(edge_maps, weights):
            final_edges += edge_map.astype(np.float32) * weight
        
        final_edges = np.clip(final_edges, 0, 255).astype(np.uint8)
        return final_edges, edge_maps
    
    def advanced_morphological_processing(self, binary_image):
        """Apply advanced morphological operations for better contour extraction."""
        processed_images = {}
        
        # Fine-scale processing (preserve small details)
        fine_processed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, 
                                        self.morph_kernels['fine'], iterations=1)
        fine_processed = cv2.morphologyEx(fine_processed, cv2.MORPH_OPEN, 
                                        self.morph_kernels['fine'], iterations=1)
        processed_images['fine'] = fine_processed
        
        # Medium-scale processing (connect nearby features)
        medium_processed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, 
                                          self.morph_kernels['medium'], iterations=2)
        medium_processed = cv2.morphologyEx(medium_processed, cv2.MORPH_OPEN, 
                                          self.morph_kernels['medium'], iterations=1)
        processed_images['medium'] = medium_processed
        
        # Coarse-scale processing (major structures)
        coarse_processed = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, 
                                          self.morph_kernels['coarse'], iterations=3)
        processed_images['coarse'] = coarse_processed
        
        # Combine processed images intelligently
        combined = np.maximum.reduce([processed_images['fine'], 
                                    processed_images['medium'] * 0.7,
                                    processed_images['coarse'] * 0.4])
        combined = (combined > 127).astype(np.uint8) * 255
        
        return combined, processed_images
    
    def classify_defect_advanced(self, contour):
        """Advanced defect classification using multiple geometric features."""
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 'unknown'
        
        # Calculate advanced geometric features
        hull = cv2.convexHull(contour)
        hull_area = cv2.contourArea(hull)
        solidity = area / hull_area if hull_area > 0 else 0
        
        # Circularity (4π * area / perimeter²)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Aspect ratio from bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h if h != 0 else 1
        
        # Extent (area / bounding rectangle area)
        rect_area = w * h
        extent = area / rect_area if rect_area > 0 else 0
        
        # Classification logic based on research parameters
        if area < self.defect_classes['micro']['max_area']:
            return 'micro'
        elif circularity > self.defect_classes['circular']['circularity_min'] and \
             self.defect_classes['circular']['min_area'] <= area <= self.defect_classes['circular']['max_area']:
            return 'circular'
        elif aspect_ratio > self.defect_classes['linear']['aspect_ratio_min'] or aspect_ratio < 1/self.defect_classes['linear']['aspect_ratio_min']:
            return 'linear'
        elif area > self.defect_classes['large']['min_area']:
            return 'large'
        elif solidity > 0.7 and extent > 0.6:
            return 'medium'
        elif area >= self.defect_classes['small']['min_area']:
            return 'small'
        else:
            return 'irregular'
    
    def filter_contours_stratified(self, contours, image_shape):
        """Apply stratified filtering based on defect classification."""
        valid_defects = []
        height, width = image_shape[:2]
        margin = 15  # Increased margin for better edge handling
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Basic size filter
            if area < 10 or area > width * height * 0.1:  # Max 10% of image
                continue
            
            # Position filter (avoid image edges)
            x, y, w, h = cv2.boundingRect(contour)
            if (x < margin or y < margin or 
                x + w > width - margin or 
                y + h > height - margin):
                continue
            
            # Shape quality filter
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            if hull_area > 0:
                solidity = area / hull_area
                if solidity < 0.1:  # Very irregular shapes
                    continue
            
            # Classify and apply class-specific filters
            defect_class = self.classify_defect_advanced(contour)
            class_params = self.defect_classes.get(defect_class, {})
            
            # Apply class-specific area constraints
            if 'min_area' in class_params and area < class_params['min_area']:
                continue
            if 'max_area' in class_params and area > class_params['max_area']:
                continue
            
            valid_defects.append(contour)
        
        return valid_defects
    
    def create_professional_mask(self, image, defects):
        """Create professional-grade highlighted mask with advanced visualization."""
        highlighted = image.copy()
        overlay = np.zeros_like(image)
        defect_info = []
        
        for i, contour in enumerate(defects):
            # Classify defect
            defect_class = self.classify_defect_advanced(contour)
            color = self.class_colors.get(defect_class, self.class_colors['unknown'])
            
            # Create precise mask for this defect
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [contour], 255)
            
            # Apply advanced blending
            overlay[mask > 0] = color
            
            # Calculate defect metrics
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            M = cv2.moments(contour)
            
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
            
            # Additional metrics
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = area / hull_area if hull_area > 0 else 0
            
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h != 0 else 1
            
            defect_info.append({
                'id': i + 1,
                'class': defect_class,
                'area': int(area),
                'perimeter': round(perimeter, 2),
                'center': (cx, cy),
                'solidity': round(solidity, 3),
                'aspect_ratio': round(aspect_ratio, 3),
                'bounding_box': (x, y, w, h),
                'color': color
            })
            
            print(f"   Defect {i+1}: {defect_class.upper()} - Area = {int(area)} pixels, "
                  f"Center = ({cx}, {cy}), Solidity = {solidity:.3f}")
        
        # Advanced blending with gamma correction
        alpha = 0.6
        gamma = 1.2
        
        # Apply gamma correction for better visibility
        highlighted_gamma = np.power(highlighted / 255.0, 1/gamma)
        overlay_gamma = np.power(overlay / 255.0, 1/gamma)
        
        # Blend with gamma correction
        blended = highlighted_gamma * (1 - alpha) + overlay_gamma * alpha
        highlighted = (np.power(blended, gamma) * 255).astype(np.uint8)
        
        return highlighted, defect_info
    
    def create_advanced_comparison(self, original, highlighted, edge_maps, processed_maps):
        """Create comprehensive comparison view with all processing stages."""
        h, w = original.shape[:2]
        
        # Resize for comparison (target width for each image)
        target_width = 300
        scale = target_width / w
        new_height = int(h * scale)
        
        # Resize all images
        original_small = cv2.resize(original, (target_width, new_height))
        highlighted_small = cv2.resize(highlighted, (target_width, new_height))
        
        # Create edge detection comparison
        final_edges = edge_maps[0]  # Combined edges
        edges_colored = cv2.applyColorMap(final_edges, cv2.COLORMAP_JET)
        edges_small = cv2.resize(edges_colored, (target_width, new_height))
        
        # Create morphology comparison  
        morph_combined = processed_maps.get('medium', np.zeros_like(final_edges))
        morph_colored = cv2.applyColorMap(morph_combined, cv2.COLORMAP_PLASMA)
        morph_small = cv2.resize(morph_colored, (target_width, new_height))
        
        # Arrange in 2x2 grid
        top_row = np.hstack([original_small, highlighted_small])
        bottom_row = np.hstack([edges_small, morph_small])
        comparison = np.vstack([top_row, bottom_row])
        
        # Add professional labels
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        color = (255, 255, 255)
        
        # Labels with black background for better readability
        labels = ["Original", "Highlighted", "Edge Detection", "Morphology"]
        positions = [(10, 25), (target_width + 10, 25), 
                    (10, new_height + 25), (target_width + 10, new_height + 25)]
        
        for label, pos in zip(labels, positions):
            # Black background
            (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
            cv2.rectangle(comparison, (pos[0]-2, pos[1]-text_height-2), 
                         (pos[0]+text_width+2, pos[1]+baseline), (0, 0, 0), -1)
            # White text
            cv2.putText(comparison, label, pos, font, font_scale, color, thickness)
        
        return comparison
    
    def process_image_advanced(self, image_path, save_results=True):
        """Process image with advanced steel defect detection techniques."""
        # Load and validate image
        if not os.path.exists(image_path):
            print(f"❌ Error: Image file '{image_path}' not found")
            return None
            
        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Error: Could not load image '{image_path}'")
            return None
            
        print(f"📸 Image loaded: {image.shape[1]}x{image.shape[0]} pixels")
        
        # Apply advanced preprocessing
        normalized_image = self.normalize_image(image)
        gray = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)
        
        # Multi-scale edge detection
        print("🔍 Applying multi-scale edge detection...")
        final_edges, edge_maps = self.multi_scale_edge_detection(gray)
        
        # Advanced morphological processing
        print("🔧 Advanced morphological processing...")
        processed_edges, processed_maps = self.advanced_morphological_processing(final_edges)
        
        # Find and filter contours
        contours, _ = cv2.findContours(processed_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_defects = self.filter_contours_stratified(contours, image.shape)
        
        print(f"🎯 Found {len(valid_defects)} high-confidence defects")
        
        if len(valid_defects) == 0:
            print("❌ No defects detected with current parameters")
            return {
                'defects_found': 0,
                'defect_info': [],
                'files_saved': []
            }
        
        # Create professional highlighting
        print("🎨 Creating professional visualization...")
        highlighted, defect_info = self.create_professional_mask(image, valid_defects)
        
        # Create comprehensive comparison
        comparison = self.create_advanced_comparison(image, highlighted, 
                                                  [final_edges] + edge_maps, processed_maps)
        
        if save_results:
            # Save results with professional naming
            base_name = Path(image_path).stem
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            files_saved = []
            
            # Save highlighted result
            highlighted_path = os.path.join(self.output_dir, f"advanced_highlighted_{base_name}_{timestamp}.jpg")
            cv2.imwrite(highlighted_path, highlighted)
            files_saved.append(highlighted_path)
            print(f"✅ Saved advanced highlighted image: {highlighted_path}")
            
            # Save comprehensive comparison
            comparison_path = os.path.join(self.output_dir, f"advanced_analysis_{base_name}_{timestamp}.jpg")
            cv2.imwrite(comparison_path, comparison)
            files_saved.append(comparison_path)
            print(f"✅ Saved comprehensive analysis: {comparison_path}")
            
            # Save technical data
            tech_path = os.path.join(self.output_dir, f"advanced_data_{base_name}_{timestamp}.json")
            with open(tech_path, 'w') as f:
                json.dump({
                    'image_path': image_path,
                    'timestamp': datetime.now().isoformat(),
                    'image_size': {'width': image.shape[1], 'height': image.shape[0]},
                    'processing_method': 'Advanced Steel Defect Detection',
                    'defects_found': len(valid_defects),
                    'defect_details': defect_info,
                    'processing_parameters': {
                        'normalization': 'ImageNet standard',
                        'edge_scales': len(self.edge_scales),
                        'morphology_kernels': list(self.morph_kernels.keys()),
                        'classification_classes': list(self.defect_classes.keys())
                    }
                }, f, indent=2)
            files_saved.append(tech_path)
            print(f"✅ Saved technical analysis: {tech_path}")
            
            return {
                'defects_found': len(valid_defects),
                'defect_info': defect_info,
                'files_saved': files_saved
            }
        else:
            return {
                'defects_found': len(valid_defects),
                'defect_info': defect_info,
                'highlighted_image': highlighted,
                'comparison_image': comparison
            }

def main():
    """Main function with advanced command line interface."""
    parser = argparse.ArgumentParser(description='Advanced Steel Defect Detection and Highlighting')
    parser.add_argument('image_path', nargs='?', help='Path to the image to process')
    parser.add_argument('--no-save', action='store_true', help='Don\'t save results to disk')
    parser.add_argument('--output-dir', default='ADVANCED_DEFECT_ANALYSIS', 
                       help='Output directory for results')
    
    args = parser.parse_args()
    
    # Initialize advanced highlighter
    highlighter = AdvancedDefectHighlighter()
    if args.output_dir != 'ADVANCED_DEFECT_ANALYSIS':
        highlighter.output_dir = args.output_dir
        os.makedirs(highlighter.output_dir, exist_ok=True)
    
    print("🔬 Advanced Steel Defect Detection System")
    print("=" * 50)
    print("📊 Features: Multi-scale analysis, Advanced morphology, Professional visualization")
    print("=" * 50)
    
    if args.image_path:
        # Process single image
        print(f"🔍 Processing: {args.image_path}")
        print("=" * 50)
        
        result = highlighter.process_image_advanced(args.image_path, save_results=not args.no_save)
        
        if result and result['defects_found'] > 0:
            print(f"\n📊 ADVANCED ANALYSIS SUMMARY:")
            print(f"✅ Total defects detected: {result['defects_found']}")
            
            # Defect class summary
            class_counts = {}
            for defect in result['defect_info']:
                defect_class = defect['class']
                class_counts[defect_class] = class_counts.get(defect_class, 0) + 1
            
            print(f"📋 Defect classification:")
            for defect_class, count in sorted(class_counts.items()):
                print(f"   • {defect_class.capitalize()}: {count} defects")
            
            if not args.no_save:
                print(f"📁 Results saved in: {os.path.abspath(highlighter.output_dir)}")
        
    else:
        # Display usage information
        print("📋 ADVANCED SYSTEM CAPABILITIES:")
        print("• Multi-scale edge detection for robust feature extraction")
        print("• ImageNet normalization for enhanced defect visibility")
        print("• Advanced morphological processing with multiple kernel sizes")
        print("• Stratified defect classification (micro, small, medium, large, linear, circular)")
        print("• Professional-grade visualization with gamma correction")
        print("• Comprehensive technical analysis and reporting")
        print("\n🚀 USAGE:")
        print("  python advanced_defect_highlighter.py <image_path>")
        print("\n📊 SUPPORTED DEFECT CLASSES:")
        for defect_class, params in highlighter.defect_classes.items():
            print(f"  • {defect_class.capitalize()}: {params}")

if __name__ == "__main__":
    main()
