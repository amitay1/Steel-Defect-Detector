#!/usr/bin/env python3
"""
Professional Web Interface for Unified Intelligent Metal Defect Analysis System
Main application file providing complete web interface for defect detection and analysis

Author: AI Assistant  
Date: June 21, 2025
"""

import gradio as gr
import os
import sys
import time
import json
import cv2
from PIL import Image
import numpy as np
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from unified_intelligent_defect_analyzer import UnifiedIntelligentDefectAnalyzer

class WebInterface:
    """Professional web interface for the unified defect analysis system"""
    
    def __init__(self):
        """Initialize the web interface"""
        self.analyzer = None
        self.initialize_system()
    
    def initialize_system(self):
        """Initialize the unified analysis system"""
        try:
            print("🚀 Initializing Unified Intelligent Defect Analysis System...")
            self.analyzer = UnifiedIntelligentDefectAnalyzer()
            print("✅ System initialized successfully")
            return True
        except Exception as e:
            print(f"❌ System initialization failed: {e}")
            return False
    
    def analyze_image(self, image, metal_type, thickness, quality_grade, progress=gr.Progress()):
        """
        Main analysis function called by Gradio interface
        
        Args:
            image: PIL Image uploaded by user
            metal_type: Selected metal type (Carbon Steel, Stainless Steel, etc.)
            thickness: Metal thickness in mm
            quality_grade: Quality grade (A, B, C, D)
            progress: Gradio progress indicator
            
        Returns:
            Tuple of (highlighted_image, analysis_report, download_files)
        """
        if image is None:
            return None, "❌ Please upload an image first", None
        
        if not self.analyzer:
            return None, "❌ System not initialized. Please refresh the page.", None
        
        try:
            # Save uploaded image temporarily
            progress(0.1, desc="Processing uploaded image...")
            temp_image_path = "temp_uploaded_image.jpg"
            image.save(temp_image_path)
              # Prepare material parameters
            progress(0.2, desc="Preparing analysis parameters...")
              # Convert thickness category to numerical value for calculations
            thickness_map = {
                "1/8 in (3.2mm)": 3.2,
                "1/4 in (6.4mm)": 6.4,
                "3/8 in (9.5mm)": 9.5,
                "1/2 in (12.7mm)": 12.7,
                "5/8 in (15.9mm)": 15.9,
                "3/4 in (19.1mm)": 19.1,
                "7/8 in (22.2mm)": 22.2,
                "1 in (25.4mm)": 25.4,
                "1-1/4 in (31.8mm)": 31.8,
                "1-1/2 in (38.1mm)": 38.1,
                "2 in (50.8mm)": 50.8,
                "3 in (76.2mm)": 76.2            }
            
            material_params = {
                'metal_type': metal_type.lower().replace(' ', '_'),
                'thickness': thickness_map.get(thickness, 6.4),  # Default to 1/4 in
                'thickness_category': thickness,  # Keep original category for display
                'quality_grade': quality_grade
            }
            
            # Run the unified analysis
            progress(0.4, desc="Running intelligent defect analysis...")
            result = self.analyzer.analyze_image_unified(
                image_path=temp_image_path,
                metal_type=material_params['metal_type'],
                thickness=material_params['thickness'],
                quality_grade=material_params['quality_grade'],
                enable_grid_analysis=True
            )
            
            # Generate highlighted image
            progress(0.7, desc="Generating highlighted defect visualization...")
            highlighted_image_path = None
            if hasattr(result, 'yellow_highlighted_image') and result.yellow_highlighted_image is not None:
                # Save the highlighted numpy array as image file
                import cv2
                highlighted_image_path = "temp_highlighted_defects.jpg"
                cv2.imwrite(highlighted_image_path, result.yellow_highlighted_image)
            elif os.path.exists("highlighted_defects.jpg"):
                highlighted_image_path = "highlighted_defects.jpg"
            
            # Generate comprehensive report
            progress(0.9, desc="Generating professional report...")
            report = self.generate_web_report(result, material_params)
            
            # Prepare download files
            download_files = self.prepare_download_files(result)
            
            progress(1.0, desc="Analysis complete!")
            
            # Load highlighted image for display
            display_image = None
            if highlighted_image_path and os.path.exists(highlighted_image_path):
                display_image = Image.open(highlighted_image_path)
              # Cleanup temp files
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
            # Don't remove the highlighted image yet - it's needed for display
            
            return display_image, report, download_files
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {str(e)}"
            print(error_msg)
            return None, error_msg, None
    
    def generate_web_report(self, result, material_params):
        """Generate formatted report for web display"""
        
        if not result:
            return "❌ No analysis results available"
        
        # Extract key metrics
        total_defects = getattr(result, 'total_defects_detected', 0)
        quality_score = getattr(result, 'quality_score', 0)
        pixels_highlighted = getattr(result, 'defect_pixels_highlighted', 0)
        
        # Get professional report if available
        professional_report = getattr(result, 'professional_report', {})
        
        # Generate HTML report
        html_report = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <h2>🔬 Metal Defect Analysis Results</h2>
            <p>Unified Intelligent Defect Analysis Results</p>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
                <h3 style="margin: 0; color: #28a745;">Defects Detected</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{total_defects}</p>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">
                <h3 style="margin: 0; color: #007bff;">Quality Score</h3>
                <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{quality_score:.1f}/100</p>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
                <h3 style="margin: 0; color: #ffc107;">Pixels Highlighted</h3>
                <p style="font-size: 18px; font-weight: bold; margin: 5px 0;">{pixels_highlighted:,}</p>
            </div>
        </div>
        """
          # Add material parameters
        thickness_display = material_params.get('thickness_category', material_params.get('thickness', 'Not specified'))
        html_report += f"""        <div style="background: #e8f4fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h3 style="color: #0056b3;">Material Parameters</h3>
            <p><strong>Metal Type:</strong> {material_params.get('metal_type', 'Not specified').replace('_', ' ').title()}</p>
            <p><strong>Thickness Category:</strong> {thickness_display}</p>
            <p><strong>Quality Grade:</strong> Grade {material_params.get('quality_grade', 'Not specified')}</p>
        </div>
        """
        
        # Add executive summary if available
        if professional_report and 'executive_summary' in professional_report:
            executive_summary = professional_report['executive_summary']
            html_report += f"""            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #856404;">
                <h3 style="color: #856404;">Executive Summary</h3>
                <pre style="white-space: pre-wrap; font-family: inherit; background: white; padding: 10px; border-radius: 5px;">{executive_summary}</pre>
            </div>
            """
        
        # Add detailed findings        if hasattr(result, 'classified_defects') and result.classified_defects:
            html_report += """
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #495057;">Identified Defects</h3>
            """
            for i, defect in enumerate(result.classified_defects, 1):
                defect_type = defect.get('type', 'Unknown')
                confidence = defect.get('confidence', 0) * 100
                html_report += f"""
                <div style="background: white; padding: 10px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #007bff;">
                    <strong>Defect #{i}:</strong> {defect_type} (Confidence: {confidence:.1f}%)
                </div>
                """
            html_report += "</div>"
        
        # Add unknown defects if any
        if hasattr(result, 'unknown_defects') and result.unknown_defects:
            html_report += f"""
            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #856404;">
                <h3 style="color: #856404;">Unknown Defects</h3>
                <p>Found {len(result.unknown_defects)} defects that require manual expert inspection</p>
            </div>
            """
        
        # Add recommendations if available
        if professional_report and 'recommendations' in professional_report:
            recommendations = professional_report['recommendations']
            html_report += """
            <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #0c5460;">
                <h3 style="color: #0c5460;">Recommendations</h3>
                <ul>
            """
            for rec in recommendations:
                html_report += f"<li>{rec}</li>"
            html_report += "</ul></div>"
        
        # Add ASTM compliance if available
        compliance_status = "Not tested"
        if hasattr(result, 'compliance_pass_fail'):
            compliance_status = "✅ Compliant" if result.compliance_pass_fail else "❌ Non-compliant"
        
        html_report += f"""
        <div style="background: #d4edda; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #155724;">
            <h3 style="color: #155724;">ASTM E-1932 Standards Compliance</h3>
            <p style="font-size: 18px; font-weight: bold;">{compliance_status}</p>
        </div>
        
        <div style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
            <p>Generated by Unified Intelligent Defect Analyzer v4.0</p>
            <p>Advanced Industrial-Grade Defect Analysis System</p>
        </div>
        </div>
        """
        
        return html_report
    
    def prepare_download_files(self, result):
        """Prepare downloadable files for the user"""
        download_files = []
        
        try:
            # Create downloads directory
            os.makedirs("downloads", exist_ok=True)
            
            # Export JSON report
            if hasattr(result, 'professional_report'):
                json_path = "downloads/defect_analysis_report.json"
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result.professional_report, f, indent=2, ensure_ascii=False, default=str)
                download_files.append(json_path)
            
            # Copy highlighted image
            if hasattr(result, 'highlighted_image_path') and result.highlighted_image_path:
                if os.path.exists(result.highlighted_image_path):
                    import shutil
                    download_path = "downloads/highlighted_defects.jpg"
                    shutil.copy2(result.highlighted_image_path, download_path)
                    download_files.append(download_path)
            
        except Exception as e:
            print(f"Error preparing download files: {e}")
        
        return download_files if download_files else None

def create_interface():
    """Create and configure the Gradio interface"""    
    # Initialize web interface
    web_interface = WebInterface()
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Arial, sans-serif !important;
    }
    .output-html {
        direction: ltr;
    }
    .gr-button-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
    }
    .gr-form {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
    }
    """
    
    # Create Gradio interface
    with gr.Blocks(css=custom_css, title="Metal Defect Analysis System") as interface:
        
        # Header
        gr.HTML("""
        <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="margin: 0; font-size: 2.5em;">🔬 Metal Defect Analysis System</h1>
            <h2 style="margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9;">Unified Intelligent Metal Defect Analysis System</h2>
            <p style="margin: 10px 0 0 0; font-size: 1em; opacity: 0.8;">Advanced AI-powered system for detecting and analyzing metal defects</p>
        </div>        """)
        
        with gr.Row():
            # Input column
            with gr.Column(scale=1):
                gr.HTML("<h3>🖼️ Image Upload & Parameters</h3>")
                
                # Image upload
                image_input = gr.Image(
                    label="Upload metal image for analysis",
                    type="pil",
                    height=300                )
                
                # Material parameters
                with gr.Group():
                    gr.HTML("<h4>Material Parameters</h4>")
                    
                    metal_type = gr.Dropdown(
                        choices=["Carbon Steel", "Stainless Steel", "Aluminum", "Alloy Steel"],
                        label="Metal Type",                        value="Carbon Steel"
                    )
                    
                    thickness = gr.Dropdown(
                        choices=[
                            "1/8 in (3.2mm)", "1/4 in (6.4mm)", "3/8 in (9.5mm)", 
                            "1/2 in (12.7mm)", "5/8 in (15.9mm)", "3/4 in (19.1mm)",
                            "7/8 in (22.2mm)", "1 in (25.4mm)", "1-1/4 in (31.8mm)",
                            "1-1/2 in (38.1mm)", "2 in (50.8mm)", "3 in (76.2mm)"
                        ],
                        label="Thickness Category",
                        value="1/4 in (6.4mm)"
                    )
                    
                    quality_grade = gr.Dropdown(
                        choices=["A", "B", "C", "D"],
                        label="Required Quality Grade",
                        value="B"
                    )
                
                # Analyze button
                analyze_btn = gr.Button(
                    "🚀 Analyze Defects",
                    variant="primary",
                    size="lg"
                )
            
            # Output column
            with gr.Column(scale=2):
                gr.HTML("<h3>🎯 Analysis Results</h3>")
                
                # Highlighted image output
                highlighted_output = gr.Image(
                    label="Image with defects highlighted in yellow",
                    height=400
                )                
                # Analysis report
                report_output = gr.HTML(
                    label="Detailed Analysis Report"
                )
                
                # Download files
                download_output = gr.File(
                    label="Download Files",
                    file_count="multiple",
                    visible=False
                )
        
        # Examples section
        gr.HTML("<h3>🔍 Examples</h3>")
        gr.HTML("""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
            <p><strong>How to use the system:</strong></p>
            <ol>
                <li>Upload an image of a metal surface</li>
                <li>Select the metal type, thickness and required quality grade</li>                <li>Click "Analyze Defects"</li>
                <li>Get results with defects highlighted in yellow and detailed report</li>
            </ol>
            <p><strong>Types of defects the system detects:</strong> Scratches, holes, oil spots, water stains, rolling defects and more...</p>
        </div>
        """)
        
        # Set up the analysis function
        analyze_btn.click(
            fn=web_interface.analyze_image,
            inputs=[image_input, metal_type, thickness, quality_grade],
            outputs=[highlighted_output, report_output, download_output]
        )
    
    return interface

def main():
    """Main function to launch the web interface"""
    
    print("🚀 Launching Unified Intelligent Metal Defect Analysis Web Interface")
    print("=" * 70)
    
    # Create and launch interface
    interface = create_interface()
    
    # Launch with appropriate settings
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
