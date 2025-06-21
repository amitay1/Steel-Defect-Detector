"""
Ultra-Accurate Reference Card Generation System - Complete Deployment
===================================================================

This script provides a complete interface for the specialized reference card generator.
It combines training, generation, and deployment into a single comprehensive system.

Key Features:
- Access to all training datasets for learning
- Ultra-accurate visual pattern analysis
- Professional-grade reference card generation
- 8-slot comparison cards with pixel-perfect accuracy
- Industrial-standard documentation

Author: Advanced Metal Defect Detection System
Version: 1.0 - Ultra-Accurate Reference Card System
Date: June 19, 2025
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import argparse
import json
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

# Ensure required packages are available
def check_and_install_requirements():
    """Check and install required packages for the reference card system."""
    required_packages = [
        "opencv-python",
        "pillow", 
        "scikit-learn",
        "scipy",
        "matplotlib",
        "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "opencv-python":
                import cv2
            elif package == "pillow":
                import PIL
            elif package == "scikit-learn":
                import sklearn
            elif package == "scipy":
                import scipy
            elif package == "matplotlib":
                import matplotlib
            elif package == "numpy":
                import numpy
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        for package in missing_packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("All required packages installed successfully!")

# Check requirements first
check_and_install_requirements()

# Now import the specialized components
try:
    from reference_card_generator_model import ReferenceCardGeneratorModel
    from reference_card_trainer import ReferenceCardTrainer
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all model files are in the same directory.")
    sys.exit(1)


class UltraAccurateReferenceCardSystem:
    """
    Complete system for ultra-accurate reference card generation.
    
    This system provides:
    - Training on real defect images
    - Professional-grade card generation
    - Quality validation and metrics
    - Industrial deployment capabilities
    """
    
    def __init__(self):
        """Initialize the complete reference card system."""
        self.base_path = Path.cwd()
        self.model = None
        self.trainer = None
        
        # Setup logging
        self._setup_logging()
        
        # Initialize system components
        self._initialize_system()
        
        self.logger.info("Ultra-Accurate Reference Card System initialized")
    
    def _setup_logging(self):
        """Setup comprehensive logging system."""
        log_dir = self.base_path / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"reference_card_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _initialize_system(self):
        """Initialize the specialized model and trainer."""
        try:
            # Initialize the ultra-accurate model
            self.model = ReferenceCardGeneratorModel()
            
            # Initialize the trainer
            self.trainer = ReferenceCardTrainer()
            
            self.logger.info("System components initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            raise
    
    def train_ultra_accurate_model(self) -> Dict:
        """
        Train the model on all available defect datasets for maximum accuracy.
        
        Returns:
            Training statistics and performance metrics
        """
        self.logger.info("Starting ultra-accurate model training...")
        
        print("🎯 Ultra-Accurate Model Training")
        print("=" * 50)
        print("Training the specialized model on all defect datasets...")
        print("This process analyzes real defect images to learn visual patterns.")
        print()
        
        # Perform comprehensive training
        training_stats = self.trainer.comprehensive_training()
        
        # Display training results
        print("✅ Training Completed Successfully!")
        print(f"   📊 Metal types trained: {len(training_stats['metal_types_trained'])}")
        print(f"   🔍 Defect types learned: {len(training_stats['defect_types_trained'])}")
        print(f"   📸 Images analyzed: {training_stats['total_images_processed']}")
        
        if training_stats['training_errors']:
            print(f"   ⚠️  Training errors: {len(training_stats['training_errors'])}")
        
        # Generate analysis report
        analysis_report = self.model.generate_analysis_report()
        print(f"   📋 Analysis report: {analysis_report}")
        
        return training_stats
    
    def generate_professional_reference_library(self) -> Dict:
        """
        Generate complete professional reference library with ultra-accurate cards.
        
        Returns:
            Library catalog with all generated cards
        """
        self.logger.info("Generating professional reference library...")
        
        print("\\n🎨 Professional Reference Library Generation")
        print("=" * 50)
        print("Creating ultra-accurate reference cards for industrial use...")
        print()
        
        # Generate the complete library
        library_catalog = self.trainer.generate_professional_reference_library()
        
        # Display generation results
        print("✅ Reference Library Generated Successfully!")
        print(f"   🎴 Total cards created: {library_catalog['total_cards']}")
        print(f"   🔧 Metal types covered: {len(library_catalog['individual_cards'])}")
        print(f"   🎯 Defect types covered: {len(library_catalog['defect_types_covered'])}")
        print(f"   📊 Comparison cards: {len(library_catalog['comparison_cards'])}")
        
        return library_catalog
    
    def generate_custom_reference_card(self, metal_type: str, defect_type: str, 
                                     grade: str = "A", thickness: float = 1.0) -> str:
        """
        Generate a custom ultra-accurate reference card.
        
        Args:
            metal_type: Type of metal (Aluminum, Carbon_Steel, etc.)
            defect_type: Type of defect
            grade: Quality grade (A, B, C)
            thickness: Material thickness in mm
            
        Returns:
            Path to the generated reference card
        """
        self.logger.info(f"Generating custom reference card: {metal_type} - {defect_type}")
        
        try:
            card_path = self.model.generate_ultra_accurate_reference_card(
                metal_type, defect_type, grade, thickness
            )
            
            print(f"✅ Custom reference card generated: {Path(card_path).name}")
            return card_path
        
        except Exception as e:
            self.logger.error(f"Failed to generate custom card: {e}")
            raise
    
    def generate_comparison_card(self, metal_type: str, defect_types: List[str]) -> str:
        """
        Generate an 8-slot comparison card with ultra-accurate visuals.
        
        Args:
            metal_type: Type of metal for the comparison card
            defect_types: List of defect types to include (up to 8)
            
        Returns:
            Path to the generated comparison card
        """
        self.logger.info(f"Generating comparison card for {metal_type}")
        
        try:
            card_path = self.model.generate_8_slot_comparison_card(metal_type, defect_types)
            
            print(f"✅ Comparison card generated: {Path(card_path).name}")
            return card_path
        
        except Exception as e:
            self.logger.error(f"Failed to generate comparison card: {e}")
            raise
    
    def validate_card_quality(self, library_path: Optional[Path] = None) -> Dict:
        """
        Validate the quality and accuracy of generated reference cards.
        
        Args:
            library_path: Path to library to validate (default: generated library)
            
        Returns:
            Validation report with quality metrics
        """
        self.logger.info("Validating reference card quality...")
        
        if library_path is None:
            library_path = self.trainer.output_path / "professional_library"
        
        print("\\n🔍 Reference Card Quality Validation")
        print("=" * 50)
        
        validation_report = self.trainer.validate_generated_cards(library_path)
        
        # Display validation results
        print("✅ Quality Validation Completed!")
        print(f"   📊 Cards validated: {validation_report['cards_validated']}")
        print(f"   ✅ Cards passed: {validation_report['cards_passed']}")
        print(f"   ❌ Cards failed: {validation_report['cards_failed']}")
        
        if validation_report['cards_validated'] > 0:
            pass_rate = (validation_report['cards_passed'] / validation_report['cards_validated']) * 100
            print(f"   📈 Pass rate: {pass_rate:.1f}%")
        
        # Display recommendations
        if validation_report['recommendations']:
            print("\\n💡 Recommendations:")
            for rec in validation_report['recommendations']:
                print(f"   • {rec}")
        
        return validation_report
    
    def deploy_for_production(self) -> Dict:
        """
        Deploy the complete system for production use.
        
        Returns:
            Deployment report with system status
        """
        self.logger.info("Deploying system for production use...")
        
        print("\\n🚀 Production Deployment")
        print("=" * 50)
        
        deployment_report = {
            "deployment_date": datetime.now().isoformat(),
            "status": "success",
            "components": {},
            "paths": {},
            "recommendations": []
        }
        
        try:
            # Train the model
            print("1. Training ultra-accurate model...")
            training_stats = self.train_ultra_accurate_model()
            deployment_report["components"]["training"] = training_stats
            
            # Generate reference library
            print("\\n2. Generating professional reference library...")
            library_catalog = self.generate_professional_reference_library()
            deployment_report["components"]["library"] = library_catalog
            
            # Validate quality
            print("\\n3. Validating reference card quality...")
            validation_report = self.validate_card_quality()
            deployment_report["components"]["validation"] = validation_report
            
            # Set up paths
            deployment_report["paths"] = {
                "library": str(self.trainer.output_path / "professional_library"),
                "individual_cards": str(self.trainer.output_path / "professional_library" / "individual_cards"),
                "comparison_cards": str(self.trainer.output_path / "professional_library" / "comparison_cards"),
                "catalog": str(self.trainer.output_path / "professional_library" / "master_catalog" / "reference_library_catalog.html")
            }
            
            # Generate deployment recommendations
            if validation_report['cards_validated'] > 0:
                pass_rate = validation_report['cards_passed'] / validation_report['cards_validated']
                if pass_rate >= 0.9:
                    deployment_report["recommendations"].append("System ready for full production deployment")
                elif pass_rate >= 0.7:
                    deployment_report["recommendations"].append("System ready for limited production use")
                else:
                    deployment_report["recommendations"].append("System needs additional training before production")
            
            print("\\n✅ Production Deployment Completed Successfully!")
            print(f"   📁 Library location: {deployment_report['paths']['library']}")
            print(f"   🌐 HTML catalog: {deployment_report['paths']['catalog']}")
            
        except Exception as e:
            deployment_report["status"] = "failed"
            deployment_report["error"] = str(e)
            self.logger.error(f"Deployment failed: {e}")
            print(f"❌ Deployment failed: {e}")
        
        # Save deployment report
        report_file = self.base_path / "deployment_report.json"
        with open(report_file, 'w') as f:
            json.dump(deployment_report, f, indent=2)
        
        print(f"   📋 Deployment report: {report_file}")
        
        return deployment_report


class ReferenceCardGUI:
    """
    Graphical user interface for the reference card generation system.
    
    Provides an intuitive interface for:
    - Training the model
    - Generating reference cards
    - Viewing generated libraries
    - Quality validation
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.system = UltraAccurateReferenceCardSystem()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Ultra-Accurate Reference Card Generator")
        self.root.geometry("800x600")
        
        # Setup GUI components
        self._setup_gui()
        
    def _setup_gui(self):
        """Setup the GUI layout and components."""
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Training tab
        training_frame = ttk.Frame(notebook)
        notebook.add(training_frame, text="🎯 Model Training")
        self._setup_training_tab(training_frame)
        
        # Generation tab
        generation_frame = ttk.Frame(notebook)
        notebook.add(generation_frame, text="🎨 Card Generation")
        self._setup_generation_tab(generation_frame)
        
        # Validation tab
        validation_frame = ttk.Frame(notebook)
        notebook.add(validation_frame, text="🔍 Quality Validation")
        self._setup_validation_tab(validation_frame)
        
        # Deployment tab
        deployment_frame = ttk.Frame(notebook)
        notebook.add(deployment_frame, text="🚀 Production Deployment")
        self._setup_deployment_tab(deployment_frame)
    
    def _setup_training_tab(self, parent):
        """Setup the model training tab."""
        ttk.Label(parent, text="Ultra-Accurate Model Training", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(parent, text="Train the model on all available defect datasets for maximum accuracy").pack(pady=5)
        
        # Training button
        ttk.Button(parent, text="Start Training", command=self._train_model).pack(pady=10)
        
        # Progress display
        self.training_progress = ttk.Progressbar(parent, mode='indeterminate')
        self.training_progress.pack(pady=5, fill='x', padx=20)
        
        # Training results
        self.training_results = tk.Text(parent, height=15, width=80)
        self.training_results.pack(pady=10, fill='both', expand=True)
        
    def _setup_generation_tab(self, parent):
        """Setup the card generation tab."""
        ttk.Label(parent, text="Professional Reference Card Generation", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Library generation
        ttk.Button(parent, text="Generate Complete Library", command=self._generate_library).pack(pady=5)
        
        # Custom card generation
        custom_frame = ttk.LabelFrame(parent, text="Custom Card Generation")
        custom_frame.pack(pady=10, fill='x', padx=20)
        
        ttk.Label(custom_frame, text="Metal Type:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.metal_var = tk.StringVar(value="Aluminum")
        metal_combo = ttk.Combobox(custom_frame, textvariable=self.metal_var, 
                                  values=["Aluminum", "Carbon_Steel", "Stainless_Steel", "Alloy_Steel"])
        metal_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(custom_frame, text="Defect Type:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.defect_var = tk.StringVar(value="pitted")
        defect_combo = ttk.Combobox(custom_frame, textvariable=self.defect_var,
                                   values=["pitted", "punching_hole", "rolled", "scratches", "silk_spot", "water_spot"])
        defect_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(custom_frame, text="Generate Custom Card", command=self._generate_custom_card).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Results display
        self.generation_results = tk.Text(parent, height=10, width=80)
        self.generation_results.pack(pady=10, fill='both', expand=True)
    
    def _setup_validation_tab(self, parent):
        """Setup the quality validation tab."""
        ttk.Label(parent, text="Reference Card Quality Validation", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Button(parent, text="Validate Generated Cards", command=self._validate_cards).pack(pady=10)
        
        # Validation results
        self.validation_results = tk.Text(parent, height=20, width=80)
        self.validation_results.pack(pady=10, fill='both', expand=True)
    
    def _setup_deployment_tab(self, parent):
        """Setup the production deployment tab."""
        ttk.Label(parent, text="Production Deployment", font=('Arial', 16, 'bold')).pack(pady=10)
        
        ttk.Label(parent, text="Deploy the complete system for production use").pack(pady=5)
        
        ttk.Button(parent, text="Deploy for Production", command=self._deploy_system).pack(pady=10)
        
        # Deployment results
        self.deployment_results = tk.Text(parent, height=15, width=80)
        self.deployment_results.pack(pady=10, fill='both', expand=True)
    
    def _train_model(self):
        """Train the model in a separate thread."""
        def train():
            self.training_progress.start()
            self.training_results.delete(1.0, tk.END)
            self.training_results.insert(tk.END, "Starting model training...\\n")
            
            try:
                stats = self.system.train_ultra_accurate_model()
                
                self.training_results.insert(tk.END, f"\\n✅ Training completed successfully!\\n")
                self.training_results.insert(tk.END, f"Metal types: {len(stats['metal_types_trained'])}\\n")
                self.training_results.insert(tk.END, f"Defect types: {len(stats['defect_types_trained'])}\\n")
                self.training_results.insert(tk.END, f"Images processed: {stats['total_images_processed']}\\n")
                
            except Exception as e:
                self.training_results.insert(tk.END, f"\\n❌ Training failed: {e}\\n")
            finally:
                self.training_progress.stop()
        
        threading.Thread(target=train, daemon=True).start()
    
    def _generate_library(self):
        """Generate the complete reference library."""
        def generate():
            self.generation_results.delete(1.0, tk.END)
            self.generation_results.insert(tk.END, "Generating professional reference library...\\n")
            
            try:
                catalog = self.system.generate_professional_reference_library()
                
                self.generation_results.insert(tk.END, f"\\n✅ Library generated successfully!\\n")
                self.generation_results.insert(tk.END, f"Total cards: {catalog['total_cards']}\\n")
                self.generation_results.insert(tk.END, f"Defect types: {len(catalog['defect_types_covered'])}\\n")
                self.generation_results.insert(tk.END, f"Comparison cards: {len(catalog['comparison_cards'])}\\n")
                
            except Exception as e:
                self.generation_results.insert(tk.END, f"\\n❌ Generation failed: {e}\\n")
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _generate_custom_card(self):
        """Generate a custom reference card."""
        metal_type = self.metal_var.get()
        defect_type = self.defect_var.get()
        
        def generate():
            self.generation_results.insert(tk.END, f"\\nGenerating {metal_type} - {defect_type} card...\\n")
            
            try:
                card_path = self.system.generate_custom_reference_card(metal_type, defect_type)
                self.generation_results.insert(tk.END, f"✅ Card generated: {Path(card_path).name}\\n")
                
            except Exception as e:
                self.generation_results.insert(tk.END, f"❌ Generation failed: {e}\\n")
        
        threading.Thread(target=generate, daemon=True).start()
    
    def _validate_cards(self):
        """Validate the generated reference cards."""
        def validate():
            self.validation_results.delete(1.0, tk.END)
            self.validation_results.insert(tk.END, "Validating reference card quality...\\n")
            
            try:
                report = self.system.validate_card_quality()
                
                self.validation_results.insert(tk.END, f"\\n✅ Validation completed!\\n")
                self.validation_results.insert(tk.END, f"Cards validated: {report['cards_validated']}\\n")
                self.validation_results.insert(tk.END, f"Cards passed: {report['cards_passed']}\\n")
                self.validation_results.insert(tk.END, f"Pass rate: {(report['cards_passed']/(report['cards_validated'] or 1))*100:.1f}%\\n")
                
                if report['recommendations']:
                    self.validation_results.insert(tk.END, "\\nRecommendations:\\n")
                    for rec in report['recommendations']:
                        self.validation_results.insert(tk.END, f"• {rec}\\n")
                
            except Exception as e:
                self.validation_results.insert(tk.END, f"\\n❌ Validation failed: {e}\\n")
        
        threading.Thread(target=validate, daemon=True).start()
    
    def _deploy_system(self):
        """Deploy the system for production."""
        def deploy():
            self.deployment_results.delete(1.0, tk.END)
            self.deployment_results.insert(tk.END, "Deploying system for production...\\n")
            
            try:
                report = self.system.deploy_for_production()
                
                if report['status'] == 'success':
                    self.deployment_results.insert(tk.END, f"\\n✅ Deployment successful!\\n")
                    self.deployment_results.insert(tk.END, f"Library path: {report['paths']['library']}\\n")
                    self.deployment_results.insert(tk.END, f"HTML catalog: {report['paths']['catalog']}\\n")
                    
                    if report['recommendations']:
                        self.deployment_results.insert(tk.END, "\\nRecommendations:\\n")
                        for rec in report['recommendations']:
                            self.deployment_results.insert(tk.END, f"• {rec}\\n")
                else:
                    self.deployment_results.insert(tk.END, f"\\n❌ Deployment failed: {report.get('error', 'Unknown error')}\\n")
                
            except Exception as e:
                self.deployment_results.insert(tk.END, f"\\n❌ Deployment failed: {e}\\n")
        
        threading.Thread(target=deploy, daemon=True).start()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Ultra-Accurate Reference Card Generation System")
    parser.add_argument("--mode", choices=["cli", "gui"], default="cli", 
                       help="Run in CLI or GUI mode")
    parser.add_argument("--action", choices=["train", "generate", "validate", "deploy", "all"], 
                       default="all", help="Action to perform (CLI mode only)")
    parser.add_argument("--metal-type", help="Specific metal type for custom generation")
    parser.add_argument("--defect-type", help="Specific defect type for custom generation")
    
    args = parser.parse_args()
    
    if args.mode == "gui":
        # Run GUI application
        app = ReferenceCardGUI()
        app.run()
    else:
        # Run CLI application
        system = UltraAccurateReferenceCardSystem()
        
        print("🏭 Ultra-Accurate Reference Card Generation System")
        print("=" * 60)
        print("Professional-grade reference cards for industrial quality control")
        print()
        
        if args.action in ["train", "all"]:
            system.train_ultra_accurate_model()
        
        if args.action in ["generate", "all"]:
            if args.metal_type and args.defect_type:
                # Generate custom card
                system.generate_custom_reference_card(args.metal_type, args.defect_type)
            else:
                # Generate complete library
                system.generate_professional_reference_library()
        
        if args.action in ["validate", "all"]:
            system.validate_card_quality()
        
        if args.action in ["deploy", "all"]:
            system.deploy_for_production()
        
        print("\\n🎯 System ready for professional use!")


if __name__ == "__main__":
    main()
