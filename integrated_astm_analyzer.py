"""
Integrated ASTM Detection and Analysis System
Connects defect detection with ASTM standards and reference cards
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import os
import tempfile
from datetime import datetime

# Import all our systems
from astm_standards import (
    ASTMStandardsManager, MetalType, QualityGrade, 
    EnhancedDefectDetection, PassFailResult
)
from astm_reference_generator import ASTMReferenceGenerator
from reference_image_system import ReferenceImageManager
from max_recall_detector import MaxRecallDefectDetector
from visual_similarity_scorer import VisualSimilarityScorer

@dataclass
class IntegratedAnalysisResult:
    """Complete analysis result with ASTM compliance"""
    # Detection Results
    total_defects: int
    detected_defects: List[Dict]
    detection_confidence_avg: float
    
    # ASTM Compliance Analysis
    material_spec: Dict[str, Any]  # metal_type, grade, thickness
    astm_compliance: PassFailResult
    compliance_details: List[Dict]  # Per-defect compliance
    
    # Reference Comparison
    reference_cards_used: List[str]
    similarity_scores: Dict[str, float]
    
    # Final Assessment
    overall_status: str
    recommendations: List[str]
    quality_score: float  # 0-100

class IntegratedASTMAnalyzer:
    """Main class that integrates all ASTM systems"""
    
    def __init__(self):
        # Initialize all subsystems
        self.detector = MaxRecallDefectDetector()
        self.astm_manager = ASTMStandardsManager()
        self.reference_generator = ASTMReferenceGenerator()
        self.reference_manager = ReferenceImageManager()
        self.similarity_scorer = VisualSimilarityScorer()
        
        print("🔧 Integrated ASTM Analyzer initialized")
        print("📊 All systems connected: Detection + Standards + References + Similarity Scoring")
    
    def analyze_image_complete(self, 
                             image_path: str,
                             metal_type: MetalType,
                             thickness_inches: float,
                             required_grade: QualityGrade,
                             pixels_per_mm: float = 10.0) -> IntegratedAnalysisResult:
        """
        Complete integrated analysis:
        1. Detect defects with maximum recall
        2. Analyze against ASTM standards  
        3. Compare with reference cards
        4. Provide pass/fail determination
        """
        
        print(f"🔍 Starting integrated analysis for {metal_type.value}")
        
        # Step 1: Detect all defects
        detection_results = self.detector.detect_all_defects(image_path, return_details=True)
        
        if 'error' in detection_results:
            raise Exception(f"Detection failed: {detection_results['error']}")
        
        detected_defects = detection_results['detections']
        total_defects = len(detected_defects)
        
        print(f"✅ Step 1: Found {total_defects} defects")
        
        # Step 2: ASTM Compliance Analysis
        compliance_details = []
        overall_compliance = PassFailResult.PASS
        
        for defect in detected_defects:
            # Calculate defect size in real units
            bbox = defect['bbox']
            defect_size_pixels = max(bbox[2] - bbox[0], bbox[3] - bbox[1])
            defect_size_mm = defect_size_pixels / pixels_per_mm
            defect_size_inches = defect_size_mm / 25.4
            
            # Check ASTM compliance
            compliance_result, confidence = self.astm_manager.determine_pass_fail(
                defect_size_inches, metal_type, required_grade
            )
            
            # Update overall compliance
            if compliance_result == PassFailResult.FAIL:
                overall_compliance = PassFailResult.FAIL
            elif compliance_result == PassFailResult.MARGINAL and overall_compliance == PassFailResult.PASS:
                overall_compliance = PassFailResult.MARGINAL
            
            compliance_details.append({
                'defect_type': defect['class'],
                'defect_size_mm': defect_size_mm,
                'defect_size_inches': defect_size_inches,
                'astm_limit_inches': self.astm_manager.get_grade_limit(metal_type, required_grade),
                'compliance_result': compliance_result,
                'compliance_confidence': confidence,
                'bbox': bbox
            })
        
        print(f"✅ Step 2: ASTM compliance = {overall_compliance.value}")
          # Step 3: Reference Card Comparison
        reference_analysis = self._compare_with_reference_cards(
            detected_defects, metal_type, required_grade, image_path
        )
        
        print(f"✅ Step 3: Reference comparison completed")
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(
            compliance_details, overall_compliance, metal_type, required_grade
        )
        
        # Step 5: Calculate quality score
        quality_score = self._calculate_quality_score(
            compliance_details, overall_compliance, total_defects
        )
        
        # Create integrated result
        result = IntegratedAnalysisResult(
            total_defects=total_defects,
            detected_defects=detected_defects,
            detection_confidence_avg=detection_results['confidence_range']['avg'],
            material_spec={
                'metal_type': metal_type.value,
                'thickness_inches': thickness_inches,
                'required_grade': required_grade.value,
                'pixels_per_mm': pixels_per_mm
            },
            astm_compliance=overall_compliance,
            compliance_details=compliance_details,
            reference_cards_used=reference_analysis['cards_used'],
            similarity_scores=reference_analysis['similarity_scores'],
            overall_status=self._determine_overall_status(overall_compliance, total_defects),
            recommendations=recommendations,            quality_score=quality_score
        )
        
        print(f"🎯 Analysis complete: {result.overall_status}")
        return result
    
    def _compare_with_reference_cards(self, 
                                    detected_defects: List[Dict],
                                    metal_type: MetalType, 
                                    required_grade: QualityGrade,
                                    original_image_path: str = None) -> Dict:
        """Compare detected defects with reference cards"""
        
        cards_used = []
        similarity_scores = {}
        
        # For each unique defect type found
        unique_defect_types = set(defect['class'] for defect in detected_defects)
        
        for defect_type in unique_defect_types:
            # Try to find or generate reference card
            try:
                # Check if reference card exists
                card_path = os.path.join(
                    self.reference_generator.output_dir,
                    f"{metal_type.value.replace(' ', '_')}_{defect_type}_{required_grade.value.replace(' ', '_')}.png"
                )
                
                if not os.path.exists(card_path):
                    # Generate reference card on demand
                    from astm_reference_generator import ReferenceCardSpec
                    standards = self.astm_manager.get_standards(metal_type)
                    thickness = (standards.thickness_min + standards.thickness_max) / 2
                    
                    spec = ReferenceCardSpec(
                        metal_type=metal_type,
                        defect_type=defect_type,
                        quality_grade=required_grade,
                        thickness_inches=thickness                    )
                    
                    card_path = self.reference_generator.generate_reference_card(spec)
                    print(f"📋 Generated reference card: {os.path.basename(card_path)}")
                
                cards_used.append(card_path)
                
                # Calculate visual similarity score using SSIM
                defects_of_type = [d for d in detected_defects if d['class'] == defect_type]
                visual_similarity_scores = []
                
                if original_image_path and os.path.exists(original_image_path):
                    # Load original image
                    original_image = cv2.imread(original_image_path)
                    # Load reference card
                    reference_card = cv2.imread(card_path)
                    
                    for defect in defects_of_type:
                        # Extract defect region from original image
                        bbox = defect['bbox']
                        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
                        defect_crop = original_image[y1:y2, x1:x2]
                        
                        if defect_crop.size > 0 and reference_card is not None:
                            # Calculate visual similarity
                            similarity_score = self.similarity_scorer.get_similarity_percentage(
                                defect_crop, reference_card
                            )
                            visual_similarity_scores.append(similarity_score)
                            print(f"🔍 Visual similarity for {defect_type}: {similarity_score:.1f}%")
                    
                    # Use average visual similarity or fallback to confidence
                    if visual_similarity_scores:
                        similarity_scores[defect_type] = sum(visual_similarity_scores) / len(visual_similarity_scores)
                    else:
                        # Fallback to confidence-based scoring
                        avg_confidence = sum(d['confidence'] for d in defects_of_type) / len(defects_of_type)
                        similarity_scores[defect_type] = avg_confidence * 100  # Convert to percentage
                else:
                    # Fallback to confidence-based scoring if no image
                    avg_confidence = sum(d['confidence'] for d in defects_of_type) / len(defects_of_type)
                    similarity_scores[defect_type] = avg_confidence * 100  # Convert to percentage
                
            except Exception as e:
                print(f"⚠️ Could not process reference for {defect_type}: {str(e)}")
        
        return {
            'cards_used': cards_used,
            'similarity_scores': similarity_scores
        }
    
    def _generate_recommendations(self, 
                                compliance_details: List[Dict],
                                overall_compliance: PassFailResult,
                                metal_type: MetalType,
                                required_grade: QualityGrade) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        if overall_compliance == PassFailResult.PASS:
            recommendations.append("✅ Material meets ASTM E-1932 standards")
            recommendations.append("✅ Approved for use in specified application")
            
        elif overall_compliance == PassFailResult.MARGINAL:
            recommendations.append("⚠️ Material shows marginal compliance")
            recommendations.append("🔍 Recommend manual inspection by quality engineer")
            recommendations.append("📊 Consider testing additional samples")
            
        else:  # FAIL
            recommendations.append("❌ Material fails ASTM E-1932 standards")
            recommendations.append("🚫 NOT approved for use")
            recommendations.append("🔄 Material requires rework or rejection")
        
        # Specific defect recommendations
        fail_defects = [cd for cd in compliance_details if cd['compliance_result'] == PassFailResult.FAIL]
        if fail_defects:
            defect_types = set(fd['defect_type'] for fd in fail_defects)
            recommendations.append(f"🎯 Critical defect types: {', '.join(defect_types)}")
            
            # Process-specific recommendations
            if any('crack' in dt.lower() or 'break' in dt.lower() for dt in defect_types):
                recommendations.append("🔧 Review welding/forming processes")
            if any('spot' in dt.lower() or 'oil' in dt.lower() for dt in defect_types):
                recommendations.append("🧽 Improve surface cleaning procedures")
            if any('inclusion' in dt.lower() for dt in defect_types):
                recommendations.append("🏭 Review material sourcing and melting process")
        
        return recommendations
    
    def _calculate_quality_score(self, 
                               compliance_details: List[Dict],
                               overall_compliance: PassFailResult,
                               total_defects: int) -> float:
        """Calculate overall quality score (0-100)"""
        
        if total_defects == 0:
            return 100.0  # Perfect score for clean material
        
        # Base score from compliance
        if overall_compliance == PassFailResult.PASS:
            base_score = 85.0
        elif overall_compliance == PassFailResult.MARGINAL:
            base_score = 65.0
        else:  # FAIL
            base_score = 35.0
        
        # Adjust for defect count
        defect_penalty = min(total_defects * 2, 20)  # Max 20 point penalty
        score = base_score - defect_penalty
        
        # Adjust for defect severity
        critical_defects = sum(1 for cd in compliance_details 
                             if cd['compliance_result'] == PassFailResult.FAIL)
        severity_penalty = critical_defects * 10
        score -= severity_penalty
        
        return max(0.0, min(100.0, score))
    
    def _determine_overall_status(self, 
                                compliance: PassFailResult, 
                                total_defects: int) -> str:
        """Determine overall material status"""
        
        if total_defects == 0:
            return "PRISTINE - No defects detected"
        elif compliance == PassFailResult.PASS:
            return "ACCEPTABLE - Within ASTM standards"
        elif compliance == PassFailResult.MARGINAL:
            return "MARGINAL - Requires inspection"
        else:
            return "REJECTED - Fails ASTM standards"
    
    def generate_comprehensive_report(self, result: IntegratedAnalysisResult) -> str:
        """Generate detailed analysis report"""
        
        report_sections = []
        
        # Header
        report_sections.append(f"""
# 🏭 INTEGRATED ASTM DEFECT ANALYSIS REPORT

## 📊 **EXECUTIVE SUMMARY**
- **Material Status:** {result.overall_status}
- **ASTM Compliance:** {result.astm_compliance.value}
- **Quality Score:** {result.quality_score:.1f}/100
- **Total Defects:** {result.total_defects}
""")
        
        # Material specifications
        spec = result.material_spec
        report_sections.append(f"""
## 🔧 **MATERIAL SPECIFICATIONS**
- **Metal Type:** {spec['metal_type']}
- **Required Grade:** {spec['required_grade']}
- **Thickness:** {spec['thickness_inches']:.3f} inches
- **Calibration:** {spec['pixels_per_mm']:.1f} pixels/mm
""")
        
        # Detection results
        if result.total_defects > 0:
            report_sections.append(f"""
## 🔍 **DEFECT DETECTION RESULTS**
- **Average Detection Confidence:** {result.detection_confidence_avg:.3f}
- **Detection Method:** Maximum Recall (100% sensitivity)
""")
            
            # Defect breakdown
            defect_breakdown = {}
            for defect in result.detected_defects:
                defect_type = defect['class']
                defect_breakdown[defect_type] = defect_breakdown.get(defect_type, 0) + 1
            
            report_sections.append("### Defect Type Breakdown:")
            for defect_type, count in defect_breakdown.items():
                report_sections.append(f"- **{defect_type}:** {count}")
        
        # ASTM compliance details
        report_sections.append(f"""
## 📏 **ASTM E-1932 COMPLIANCE ANALYSIS**
""")
        
        if result.compliance_details:
            for i, detail in enumerate(result.compliance_details, 1):
                status_icon = "✅" if detail['compliance_result'] == PassFailResult.PASS else "⚠️" if detail['compliance_result'] == PassFailResult.MARGINAL else "❌"
                
                report_sections.append(f"""
### Defect {i}: {detail['defect_type']}
{status_icon} **Status:** {detail['compliance_result'].value}
- **Size:** {detail['defect_size_mm']:.2f}mm ({detail['defect_size_inches']:.4f}")
- **ASTM Limit:** {detail['astm_limit_inches']:.4f}"
- **Confidence:** {detail['compliance_confidence']:.2f}
""")
          # Reference cards used
        if result.reference_cards_used:
            report_sections.append(f"""
## 📋 **REFERENCE CARDS & VISUAL SIMILARITY**
""")
            for card in result.reference_cards_used:
                card_name = os.path.basename(card)
                report_sections.append(f"- **Card:** {card_name}")
            
            # Add visual similarity scores
            if result.similarity_scores:
                report_sections.append(f"""
### 🎯 **Visual Similarity Analysis**
""")
                for defect_type, score in result.similarity_scores.items():
                    score_icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                    report_sections.append(f"- **{defect_type}:** {score_icon} {score:.1f}% similarity to reference")
                
                avg_similarity = sum(result.similarity_scores.values()) / len(result.similarity_scores)
                report_sections.append(f"\n**Average Visual Similarity:** {avg_similarity:.1f}%")
        
        # Recommendations
        report_sections.append(f"""
## 💡 **RECOMMENDATIONS**
""")
        for rec in result.recommendations:
            report_sections.append(f"- {rec}")
        
        # Footer
        report_sections.append(f"""
---
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Analysis System:** Integrated ASTM Defect Analyzer v1.0  
**Standards:** ASTM E-1932 Metal Defect Analysis
""")
        
        return "\n".join(report_sections)

# Example usage
if __name__ == "__main__":
    analyzer = IntegratedASTMAnalyzer()
    
    # This would be called from the main application
    print("🔧 Integrated ASTM Analyzer ready for complete defect analysis")
