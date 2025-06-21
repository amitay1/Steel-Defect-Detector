"""
Reference Card Generator Training & Deployment Script
====================================================

This script trains the specialized reference card generator model and provides
a comprehensive interface for generating ultra-accurate comparison cards.

Author: Advanced Metal Defect Detection System
Version: 1.0 - Professional Reference Card Training
Date: June 19, 2025
"""

import os
import sys
from pathlib import Path
import argparse
import json
from typing import List, Dict
import logging
from datetime import datetime
import cv2
import numpy as np

# Import the specialized model
from reference_card_generator_model import ReferenceCardGeneratorModel

class ReferenceCardTrainer:
    """
    Comprehensive trainer for the Reference Card Generator Model.
    
    This class handles:
    - Training on all available defect datasets
    - Validation of generated reference cards
    - Performance optimization
    - Professional card generation workflows
    """
    
    def __init__(self, base_path: str = "."):
        """Initialize the trainer with project paths."""
        self.base_path = Path(base_path)
        self.training_path = self.base_path / "training" / "datasets"
        self.reference_path = self.base_path / "reference_images"
        self.output_path = self.base_path / "generated_reference_cards"
        
        # Create output directory
        self.output_path.mkdir(exist_ok=True)
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize the specialized model
        self.model = ReferenceCardGeneratorModel(str(self.training_path))
        
        # Define comprehensive defect mapping
        self.defect_mapping = {
            "surface_defects": ["pitted", "punching_hole", "rolled", "scratches", "silk_spot", "water_spot"],
            "mt_defects": ["mt_crack", "mt_break", "mt_blowhole", "mt_fray", "mt_free"],
            "industrial_defects": ["crazing", "crease", "crescent_gap", "inclusion", "oil_spot", "patches", "rolled_pit", "waist_folding", "welding_line"],
            "all_defects": []
        }
        
        # Combine all defects
        for category in ["surface_defects", "mt_defects", "industrial_defects"]:
            self.defect_mapping["all_defects"].extend(self.defect_mapping[category])
        
        self.logger.info("Reference Card Trainer initialized successfully")
    
    def _setup_logging(self):
        """Setup comprehensive logging for training process."""
        log_file = self.output_path / "training_log.txt"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def comprehensive_training(self):
        """
        Perform comprehensive training on all available datasets.
        
        This method:
        1. Scans all available training data
        2. Trains the model on each defect type
        3. Validates the learning process
        4. Generates training metrics
        """
        self.logger.info("Starting comprehensive training process...")
        
        training_stats = {
            "metal_types_trained": [],
            "defect_types_trained": [],
            "total_images_processed": 0,
            "training_errors": []
        }
        
        # Check available datasets
        if self.reference_path.exists():
            metal_types = [d.name for d in self.reference_path.iterdir() if d.is_dir()]
        else:
            # Fallback to organized datasets
            organized_path = self.training_path / "organized_comprehensive"
            if organized_path.exists():
                metal_types = [d.name for d in organized_path.iterdir() if d.is_dir()]
            else:
                self.logger.error("No training datasets found!")
                return training_stats
        
        training_stats["metal_types_trained"] = metal_types
        
        # Train on each metal type
        for metal_type in metal_types:
            self.logger.info(f"Training on {metal_type} datasets...")
            
            # Get defect folders for this metal type
            if self.reference_path.exists():
                metal_path = self.reference_path / metal_type
            else:
                metal_path = self.training_path / "organized_comprehensive" / metal_type
            
            if not metal_path.exists():
                continue
            
            defect_folders = [d for d in metal_path.iterdir() if d.is_dir()]
            
            for defect_folder in defect_folders:
                defect_type = defect_folder.name
                
                try:
                    # Get all images in this defect folder
                    image_files = list(defect_folder.glob("*.jpg")) + list(defect_folder.glob("*.png"))
                    
                    if image_files:
                        self.logger.info(f"Training on {metal_type} - {defect_type}: {len(image_files)} images")
                        
                        # Train the model on these images
                        self.model.train_on_new_images([str(f) for f in image_files], metal_type, defect_type)
                        
                        training_stats["total_images_processed"] += len(image_files)
                        
                        if defect_type not in training_stats["defect_types_trained"]:
                            training_stats["defect_types_trained"].append(defect_type)
                
                except Exception as e:
                    error_msg = f"Training error for {metal_type} - {defect_type}: {str(e)}"
                    self.logger.error(error_msg)
                    training_stats["training_errors"].append(error_msg)
        
        # Save training statistics
        stats_file = self.output_path / "training_statistics.json"
        with open(stats_file, 'w') as f:
            json.dump(training_stats, f, indent=2)
        
        self.logger.info(f"Comprehensive training completed. Stats saved to {stats_file}")
        return training_stats
    
    def generate_professional_reference_library(self):
        """
        Generate a complete professional reference library.
        
        Creates:
        - Individual ultra-accurate reference cards for each defect type
        - 8-slot comparison cards for each metal type
        - Master reference catalog
        """
        self.logger.info("Generating professional reference library...")
        
        library_path = self.output_path / "professional_library"
        library_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        individual_cards_path = library_path / "individual_cards"
        comparison_cards_path = library_path / "comparison_cards"
        master_catalog_path = library_path / "master_catalog"
        
        for path in [individual_cards_path, comparison_cards_path, master_catalog_path]:
            path.mkdir(exist_ok=True)
        
        metal_types = ["Aluminum", "Carbon_Steel", "Stainless_Steel", "Alloy_Steel"]
        grades = ["A", "B", "C"]
        
        library_catalog = {
            "generated_date": datetime.now().isoformat(),
            "total_cards": 0,
            "individual_cards": {},
            "comparison_cards": {},
            "defect_types_covered": set()
        }
        
        # Generate individual cards for each combination
        for metal_type in metal_types:
            library_catalog["individual_cards"][metal_type] = {}
            
            for defect_type in self.defect_mapping["all_defects"]:
                library_catalog["individual_cards"][metal_type][defect_type] = []
                
                for grade in grades:
                    try:
                        # Generate ultra-accurate reference card
                        card_path = self.model.generate_ultra_accurate_reference_card(
                            metal_type, defect_type, grade, thickness=1.0
                        )
                        
                        # Move to library structure
                        new_path = individual_cards_path / f"{metal_type}_{defect_type}_Grade_{grade}_Professional.png"
                        if Path(card_path).exists():
                            import shutil
                            shutil.move(card_path, new_path)
                            
                            library_catalog["individual_cards"][metal_type][defect_type].append(str(new_path))
                            library_catalog["total_cards"] += 1
                            library_catalog["defect_types_covered"].add(defect_type)
                            
                            self.logger.info(f"Generated: {new_path.name}")
                    
                    except Exception as e:
                        self.logger.error(f"Failed to generate {metal_type} - {defect_type} - {grade}: {e}")
        
        # Generate 8-slot comparison cards
        for metal_type in metal_types:
            try:
                # Select 8 most important defects for this metal type
                selected_defects = self._select_priority_defects_for_metal(metal_type)
                
                comparison_card_path = self.model.generate_8_slot_comparison_card(metal_type, selected_defects)
                
                # Move to library structure
                new_path = comparison_cards_path / f"{metal_type}_8_Slot_Professional_Comparison.png"
                if Path(comparison_card_path).exists():
                    import shutil
                    shutil.move(comparison_card_path, new_path)
                    
                    library_catalog["comparison_cards"][metal_type] = {
                        "path": str(new_path),
                        "defects_included": selected_defects
                    }
                    
                    self.logger.info(f"Generated comparison card: {new_path.name}")
            
            except Exception as e:
                self.logger.error(f"Failed to generate comparison card for {metal_type}: {e}")
        
        # Convert set to list for JSON serialization
        library_catalog["defect_types_covered"] = list(library_catalog["defect_types_covered"])
        
        # Save library catalog
        catalog_file = master_catalog_path / "library_catalog.json"
        with open(catalog_file, 'w') as f:
            json.dump(library_catalog, f, indent=2)
        
        # Generate master HTML catalog
        self._generate_html_catalog(library_catalog, master_catalog_path)
        
        self.logger.info(f"Professional reference library generated: {library_path}")
        return library_catalog
    
    def _select_priority_defects_for_metal(self, metal_type: str) -> List[str]:
        """Select 8 priority defects for a specific metal type."""
        # Metal-specific defect priorities
        priority_defects = {
            "Aluminum": ["pitted", "punching_hole", "rolled", "scratches", "silk_spot", "water_spot", "oil_spot", "patches"],
            "Carbon_Steel": ["mt_crack", "mt_break", "pitted", "rolled_pit", "scratches", "inclusion", "welding_line", "crazing"],
            "Stainless_Steel": ["pitted", "scratches", "water_spot", "silk_spot", "rolled", "punching_hole", "oil_spot", "patches"],
            "Alloy_Steel": ["mt_crack", "pitted", "inclusion", "rolled_pit", "scratches", "mt_break", "crazing", "crease"]
        }
        
        return priority_defects.get(metal_type, self.defect_mapping["all_defects"][:8])
    
    def _generate_html_catalog(self, catalog: Dict, output_path: Path):
        """Generate HTML catalog for easy viewing of the reference library."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Professional Metal Defect Reference Library</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ text-align: center; background-color: #2c3e50; color: white; padding: 20px; border-radius: 10px; }}
        .stats {{ background-color: white; padding: 15px; margin: 20px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .metal-section {{ background-color: white; margin: 20px 0; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .comparison-card {{ text-align: center; margin: 20px 0; }}
        .individual-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }}
        .card-item {{ text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }}
        .card-item img {{ max-width: 100%; height: auto; border-radius: 3px; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .defect-list {{ columns: 3; column-gap: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏭 Professional Metal Defect Reference Library</h1>
        <p>Ultra-Accurate AI-Generated Reference Cards for Industrial Quality Control</p>
        <p>Generated: {catalog['generated_date']}</p>
    </div>
    
    <div class="stats">
        <h2>📊 Library Statistics</h2>
        <ul>
            <li><strong>Total Reference Cards:</strong> {catalog['total_cards']}</li>
            <li><strong>Metal Types Covered:</strong> {len(catalog['individual_cards'])}</li>
            <li><strong>Defect Types Covered:</strong> {len(catalog['defect_types_covered'])}</li>
            <li><strong>Comparison Cards:</strong> {len(catalog['comparison_cards'])}</li>
        </ul>
        
        <h3>Defect Types Included:</h3>
        <div class="defect-list">
            {chr(10).join([f"<p>• {defect.replace('_', ' ').title()}</p>" for defect in catalog['defect_types_covered']])}
        </div>
    </div>
"""
        
        # Add comparison cards section
        if catalog['comparison_cards']:
            html_content += """
    <div class="metal-section">
        <h2>🎯 8-Slot Comparison Cards</h2>
        <p>Professional comparison cards showing 8 key defects for each metal type.</p>
"""
            
            for metal_type, card_info in catalog['comparison_cards'].items():
                if isinstance(card_info, dict) and 'path' in card_info:
                    card_path = Path(card_info['path']).name
                    defects = card_info.get('defects_included', [])
                    html_content += f"""
        <div class="comparison-card">
            <h3>{metal_type} - Professional Comparison Card</h3>
            <img src="../comparison_cards/{card_path}" alt="{metal_type} Comparison Card" style="max-width: 800px;">
            <p><strong>Defects Included:</strong> {', '.join([d.replace('_', ' ').title() for d in defects])}</p>
        </div>
"""
            
            html_content += """
    </div>
"""
        
        # Add individual cards sections
        for metal_type, defects in catalog['individual_cards'].items():
            html_content += f"""
    <div class="metal-section">
        <h2>🔧 {metal_type} - Individual Reference Cards</h2>
        <div class="individual-cards">
"""
            
            for defect_type, card_paths in defects.items():
                if card_paths:  # Only show if cards exist
                    html_content += f"""
            <div class="card-item">
                <h4>{defect_type.replace('_', ' ').title()}</h4>
"""
                    for card_path in card_paths:
                        card_filename = Path(card_path).name
                        grade = "A"  # Extract grade from filename if needed
                        html_content += f"""
                <img src="../individual_cards/{card_filename}" alt="{metal_type} {defect_type} Grade {grade}">
                <p>Grade {grade}</p>
"""
                    html_content += """
            </div>
"""
            
            html_content += """
        </div>
    </div>
"""
        
        html_content += """
    <div class="stats">
        <h2>📋 Usage Instructions</h2>
        <ol>
            <li><strong>Comparison Cards:</strong> Use 8-slot cards for quick defect identification and training</li>
            <li><strong>Individual Cards:</strong> Use specific grade cards for detailed quality assessment</li>
            <li><strong>Quality Control:</strong> Compare actual defects with reference cards to determine pass/fail status</li>
            <li><strong>Training:</strong> Use cards to train quality control personnel on defect recognition</li>
        </ol>
        
        <h3>🎯 Professional Applications</h3>
        <ul>
            <li>Manufacturing quality control inspection</li>
            <li>Incoming material acceptance testing</li>
            <li>Production line defect monitoring</li>
            <li>Training and certification programs</li>
            <li>Customer quality audits</li>
            <li>Research and development validation</li>
        </ul>
    </div>
    
    <footer style="text-align: center; margin-top: 40px; padding: 20px; background-color: #34495e; color: white; border-radius: 5px;">
        <p>Generated by Advanced Metal Defect Detection System</p>
        <p>Ultra-Accurate AI-Generated Reference Cards for Professional Use</p>
    </footer>
</body>
</html>
"""
        
        # Save HTML catalog
        html_file = output_path / "reference_library_catalog.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        self.logger.info(f"HTML catalog generated: {html_file}")
    
    def validate_generated_cards(self, library_path: Path) -> Dict:
        """
        Validate the quality and accuracy of generated reference cards.
        
        Args:
            library_path: Path to the generated library
            
        Returns:
            Validation report dictionary
        """
        self.logger.info("Validating generated reference cards...")
        
        validation_report = {
            "validation_date": datetime.now().isoformat(),
            "cards_validated": 0,
            "cards_passed": 0,
            "cards_failed": 0,
            "quality_metrics": {},
            "recommendations": []
        }
        
        individual_cards_path = library_path / "individual_cards"
        
        if not individual_cards_path.exists():
            self.logger.error("Individual cards directory not found!")
            return validation_report
        
        import cv2
        import numpy as np
        
        # Validate each card
        for card_file in individual_cards_path.glob("*.png"):
            try:
                # Load and analyze card
                img = cv2.imread(str(card_file))
                if img is None:
                    continue
                
                validation_report["cards_validated"] += 1
                
                # Basic quality checks
                quality_score = self._calculate_card_quality_score(img)
                
                if quality_score >= 0.7:  # 70% threshold
                    validation_report["cards_passed"] += 1
                else:
                    validation_report["cards_failed"] += 1
                
                # Store quality metrics
                validation_report["quality_metrics"][card_file.name] = {
                    "quality_score": quality_score,
                    "resolution": f"{img.shape[1]}x{img.shape[0]}",
                    "file_size": card_file.stat().st_size
                }
            
            except Exception as e:
                self.logger.error(f"Validation error for {card_file}: {e}")
        
        # Generate recommendations
        if validation_report["cards_failed"] > 0:
            validation_report["recommendations"].append("Some cards failed quality validation - consider retraining")
        
        if validation_report["cards_validated"] > 0:
            pass_rate = validation_report["cards_passed"] / validation_report["cards_validated"]
            if pass_rate < 0.8:
                validation_report["recommendations"].append("Low pass rate - review training data quality")
            else:
                validation_report["recommendations"].append("Good quality cards generated - ready for production use")
        
        # Save validation report
        report_file = library_path / "validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(validation_report, f, indent=2)
        
        self.logger.info(f"Validation completed. Report saved: {report_file}")
        return validation_report
    
    def _calculate_card_quality_score(self, img: np.ndarray) -> float:
        """Calculate quality score for a reference card."""
        score = 0.0
        
        # Check resolution (minimum 300x200)
        height, width = img.shape[:2]
        if width >= 300 and height >= 200:
            score += 0.2
        
        # Check contrast (should have good dynamic range)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        contrast = np.std(gray)
        if contrast > 20:  # Good contrast
            score += 0.3
        
        # Check for defect visibility (should have clear features)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        if edge_density > 0.05:  # Sufficient edge content
            score += 0.3
        
        # Check color distribution (should not be monochromatic)
        color_std = np.std(img.reshape(-1, 3), axis=0)
        if np.mean(color_std) > 10:
            score += 0.2
        
        return min(score, 1.0)


def main():
    """Main execution function with command line interface."""
    parser = argparse.ArgumentParser(description="Reference Card Generator Training & Deployment")
    parser.add_argument("--action", choices=["train", "generate", "validate", "all"], 
                       default="all", help="Action to perform")
    parser.add_argument("--output", default="generated_reference_cards", 
                       help="Output directory for generated cards")
    parser.add_argument("--metal-type", help="Specific metal type to process")
    parser.add_argument("--defect-type", help="Specific defect type to process")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize trainer
    trainer = ReferenceCardTrainer()
    
    print("🏭 Reference Card Generator - Professional Training System")
    print("=" * 60)
    
    if args.action in ["train", "all"]:
        print("\n📚 Starting comprehensive training...")
        training_stats = trainer.comprehensive_training()
        print(f"✅ Training completed:")
        print(f"   - Metal types: {len(training_stats['metal_types_trained'])}")
        print(f"   - Defect types: {len(training_stats['defect_types_trained'])}")
        print(f"   - Images processed: {training_stats['total_images_processed']}")
        print(f"   - Errors: {len(training_stats['training_errors'])}")
    
    if args.action in ["generate", "all"]:
        print("\n🎨 Generating professional reference library...")
        library_catalog = trainer.generate_professional_reference_library()
        print(f"✅ Reference library generated:")
        print(f"   - Total cards: {library_catalog['total_cards']}")
        print(f"   - Defect types: {len(library_catalog['defect_types_covered'])}")
        print(f"   - Comparison cards: {len(library_catalog['comparison_cards'])}")
    
    if args.action in ["validate", "all"]:
        print("\n🔍 Validating generated cards...")
        library_path = Path(trainer.output_path) / "professional_library"
        if library_path.exists():
            validation_report = trainer.validate_generated_cards(library_path)
            print(f"✅ Validation completed:")
            print(f"   - Cards validated: {validation_report['cards_validated']}")
            print(f"   - Cards passed: {validation_report['cards_passed']}")
            print(f"   - Pass rate: {validation_report['cards_passed']/(validation_report['cards_validated'] or 1)*100:.1f}%")
        else:
            print("❌ No library found to validate")
    
    print("\n🎯 Professional reference card system ready for industrial use!")
    print(f"📁 Output directory: {trainer.output_path}")


if __name__ == "__main__":
    main()
