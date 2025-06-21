"""
ASTM E-1932 Standards Integration Module
Implements professional quality control standards for metal defect analysis
"""

import json
import sqlite3
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

class MetalType(Enum):
    """Supported metal types per ASTM E-1932"""
    CARBON_STEEL = "Carbon Steel"
    STAINLESS_STEEL = "Stainless Steel"
    ALUMINUM = "Aluminum"
    ALLOY_STEEL = "Alloy Steel"

class QualityGrade(Enum):
    """Quality grades per ASTM E-1932"""
    GRADE_A = "Grade A"  # Premium quality - No defects >1/32" (0.8mm)
    GRADE_B = "Grade B"  # High quality - No defects >1/16" (1.6mm)
    GRADE_C = "Grade C"  # Standard quality - No defects >1/8" (3.2mm)  
    GRADE_D = "Grade D"  # Utility quality - No defects >1/4" (6.4mm)

class PassFailResult(Enum):
    """Pass/Fail determination results"""
    PASS = "PASS"
    MARGINAL = "MARGINAL"
    FAIL = "FAIL"

@dataclass
class ASTMStandards:
    """ASTM E-1932 standards lookup data"""
    metal_type: MetalType
    thickness_min: float  # inches
    thickness_max: float  # inches
    grade_a_limit: float  # inches
    grade_b_limit: float  # inches
    grade_c_limit: float  # inches
    grade_d_limit: float  # inches

@dataclass
class EnhancedDefectDetection:
    """Enhanced defect detection with ASTM standards compliance"""
    timestamp: str
    image_hash: str
    defect_type: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    defect_size_pixels: float  # Maximum dimension in pixels
    defect_size_mm: Optional[float]  # Size in millimeters (if calibrated)
    defect_size_inches: Optional[float]  # Size in inches (if calibrated)
    image_size: Tuple[int, int]  # (width, height)
    model_version: str
    
    # ASTM Standards Parameters
    metal_type: Optional[MetalType] = None
    thickness_inches: Optional[float] = None
    required_grade: Optional[QualityGrade] = None
    pixels_per_mm: Optional[float] = None  # Calibration factor
    
    # Standards Compliance Results
    standards_compliance: Optional[PassFailResult] = None
    applicable_limit_inches: Optional[float] = None
    compliance_confidence: Optional[float] = None
    
    # Original fields for backward compatibility
    user_feedback: Optional[str] = None
    is_verified: bool = False

class ASTMStandardsManager:
    """Manages ASTM E-1932 standards lookup and compliance checking"""
    
    def __init__(self):
        self.standards_table = self._initialize_standards_table()
    
    def _initialize_standards_table(self) -> Dict[MetalType, ASTMStandards]:
        """Initialize the ASTM E-1932 standards lookup table"""
        return {
            MetalType.CARBON_STEEL: ASTMStandards(
                metal_type=MetalType.CARBON_STEEL,
                thickness_min=0.125,  # 1/8"
                thickness_max=2.0,    # 2"
                grade_a_limit=1/32,   # 0.03125" = 0.8mm
                grade_b_limit=1/16,   # 0.0625" = 1.6mm
                grade_c_limit=1/8,    # 0.125" = 3.2mm
                grade_d_limit=1/4     # 0.25" = 6.4mm
            ),
            MetalType.STAINLESS_STEEL: ASTMStandards(
                metal_type=MetalType.STAINLESS_STEEL,
                thickness_min=1/16,   # 1/16"
                thickness_max=1.0,    # 1"
                grade_a_limit=1/32,   # 0.03125" = 0.8mm
                grade_b_limit=1/16,   # 0.0625" = 1.6mm
                grade_c_limit=1/8,    # 0.125" = 3.2mm
                grade_d_limit=1/4     # 0.25" = 6.4mm
            ),
            MetalType.ALUMINUM: ASTMStandards(
                metal_type=MetalType.ALUMINUM,
                thickness_min=1/16,   # 1/16"
                thickness_max=1.0,    # 1"
                grade_a_limit=1/32,   # 0.03125" = 0.8mm
                grade_b_limit=1/16,   # 0.0625" = 1.6mm
                grade_c_limit=1/8,    # 0.125" = 3.2mm
                grade_d_limit=1/4     # 0.25" = 6.4mm
            ),
            MetalType.ALLOY_STEEL: ASTMStandards(
                metal_type=MetalType.ALLOY_STEEL,
                thickness_min=0.125,  # 1/8"
                thickness_max=2.0,    # 2"
                grade_a_limit=1/32,   # 0.03125" = 0.8mm
                grade_b_limit=1/16,   # 0.0625" = 1.6mm
                grade_c_limit=1/8,    # 0.125" = 3.2mm
                grade_d_limit=1/4     # 0.25" = 6.4mm
            )
        }
    
    def get_standards(self, metal_type: MetalType) -> ASTMStandards:
        """Get ASTM standards for a specific metal type"""
        return self.standards_table[metal_type]
    
    def get_grade_limit(self, metal_type: MetalType, grade: QualityGrade) -> float:
        """Get the defect size limit for a specific metal type and grade"""
        standards = self.get_standards(metal_type)
        
        if grade == QualityGrade.GRADE_A:
            return standards.grade_a_limit
        elif grade == QualityGrade.GRADE_B:
            return standards.grade_b_limit
        elif grade == QualityGrade.GRADE_C:
            return standards.grade_c_limit
        elif grade == QualityGrade.GRADE_D:
            return standards.grade_d_limit
        else:
            raise ValueError(f"Unknown grade: {grade}")
    
    def validate_thickness(self, metal_type: MetalType, thickness: float) -> bool:
        """Check if thickness is within ASTM standard range for metal type"""
        standards = self.get_standards(metal_type)
        return standards.thickness_min <= thickness <= standards.thickness_max
    
    def determine_pass_fail(self, 
                          defect_size_inches: float,
                          metal_type: MetalType,
                          required_grade: QualityGrade) -> Tuple[PassFailResult, float]:
        """
        Determine pass/fail status based on ASTM E-1932 standards
        Returns (result, confidence_score)
        """
        limit = self.get_grade_limit(metal_type, required_grade)
        
        if defect_size_inches <= limit:
            result = PassFailResult.PASS
            confidence = 1.0
        elif defect_size_inches <= limit * 1.2:  # 20% tolerance for marginal
            result = PassFailResult.MARGINAL
            confidence = 0.7
        else:
            result = PassFailResult.FAIL
            confidence = 1.0
        
        return result, confidence
    
    def calculate_defect_size_mm(self, bbox: List[float], pixels_per_mm: float) -> float:
        """Calculate defect size in millimeters from bounding box"""
        x1, y1, x2, y2 = bbox
        width_pixels = x2 - x1
        height_pixels = y2 - y1
        max_dimension_pixels = max(width_pixels, height_pixels)
        return max_dimension_pixels / pixels_per_mm
    
    def mm_to_inches(self, size_mm: float) -> float:
        """Convert millimeters to inches"""
        return size_mm / 25.4
    
    def get_defect_color_code(self, pass_fail_result: PassFailResult) -> str:
        """Get color code for visual feedback based on pass/fail result"""
        color_map = {
            PassFailResult.PASS: "#00FF00",      # Green
            PassFailResult.MARGINAL: "#FFFF00",  # Yellow
            PassFailResult.FAIL: "#FF0000"       # Red
        }
        return color_map[pass_fail_result]
    
    def generate_compliance_report(self, detection: EnhancedDefectDetection) -> Dict[str, Any]:
        """Generate a detailed compliance report for a detection"""
        if not all([detection.metal_type, detection.required_grade, detection.defect_size_inches]):
            return {"error": "Insufficient data for compliance analysis"}
        
        standards = self.get_standards(detection.metal_type)
        applicable_limit = self.get_grade_limit(detection.metal_type, detection.required_grade)
        
        report = {
            "defect_analysis": {
                "defect_type": detection.defect_type,
                "confidence": detection.confidence,
                "size_mm": detection.defect_size_mm,
                "size_inches": detection.defect_size_inches
            },
            "material_specification": {
                "metal_type": detection.metal_type.value,
                "thickness_inches": detection.thickness_inches,
                "required_grade": detection.required_grade.value
            },
            "standards_analysis": {
                "applicable_standard": "ASTM E-1932",
                "defect_size_limit_inches": applicable_limit,
                "defect_size_limit_mm": applicable_limit * 25.4,
                "compliance_result": detection.standards_compliance.value,
                "compliance_confidence": detection.compliance_confidence
            },
            "visual_indicators": {
                "color_code": self.get_defect_color_code(detection.standards_compliance),
                "urgency_level": "High" if detection.standards_compliance == PassFailResult.FAIL else "Medium" if detection.standards_compliance == PassFailResult.MARGINAL else "Low"
            }
        }
        
        return report

class EnhancedMemoryBank:
    """Enhanced Memory Bank with ASTM standards integration"""
    
    def __init__(self, db_path: str = "enhanced_memory_bank.db"):
        self.db_path = db_path
        self.standards_manager = ASTMStandardsManager()
        self.init_enhanced_database()
    
    def init_enhanced_database(self):
        """Initialize enhanced database with ASTM standards tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Enhanced defect detections table with ASTM fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enhanced_defect_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    image_hash TEXT NOT NULL,
                    defect_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    bbox_x1 REAL NOT NULL,
                    bbox_y1 REAL NOT NULL,
                    bbox_x2 REAL NOT NULL,
                    bbox_y2 REAL NOT NULL,
                    defect_size_pixels REAL NOT NULL,
                    defect_size_mm REAL,
                    defect_size_inches REAL,
                    image_width INTEGER NOT NULL,
                    image_height INTEGER NOT NULL,
                    model_version TEXT NOT NULL,
                    
                    -- ASTM Standards fields
                    metal_type TEXT,
                    thickness_inches REAL,
                    required_grade TEXT,
                    pixels_per_mm REAL,
                    standards_compliance TEXT,
                    applicable_limit_inches REAL,
                    compliance_confidence REAL,
                    
                    -- Original fields
                    user_feedback TEXT,
                    is_verified BOOLEAN DEFAULT FALSE,
                    
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Reference images table for 8-slot system
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reference_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slot_number INTEGER NOT NULL CHECK(slot_number BETWEEN 1 AND 8),
                    metal_type TEXT NOT NULL,
                    defect_type TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    image_path TEXT NOT NULL,
                    description TEXT,
                    calibration_pixels_per_mm REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    UNIQUE(slot_number)
                )
            """)
            
            # Standards compliance history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compliance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    detection_id INTEGER NOT NULL,
                    compliance_result TEXT NOT NULL,
                    applicable_standard TEXT NOT NULL,
                    defect_size_limit REAL NOT NULL,
                    analysis_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (detection_id) REFERENCES enhanced_defect_detections (id)
                )
            """)
            
            conn.commit()
    
    def store_enhanced_detection(self, detection: EnhancedDefectDetection) -> int:
        """Store enhanced defect detection with ASTM standards data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enhanced_defect_detections 
                (timestamp, image_hash, defect_type, confidence, 
                 bbox_x1, bbox_y1, bbox_x2, bbox_y2, 
                 defect_size_pixels, defect_size_mm, defect_size_inches,
                 image_width, image_height, model_version,
                 metal_type, thickness_inches, required_grade, pixels_per_mm,
                 standards_compliance, applicable_limit_inches, compliance_confidence,
                 user_feedback, is_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                detection.timestamp, detection.image_hash, detection.defect_type,
                detection.confidence, detection.bbox[0], detection.bbox[1],
                detection.bbox[2], detection.bbox[3], detection.defect_size_pixels,
                detection.defect_size_mm, detection.defect_size_inches,
                detection.image_size[0], detection.image_size[1], detection.model_version,
                detection.metal_type.value if detection.metal_type else None,
                detection.thickness_inches, 
                detection.required_grade.value if detection.required_grade else None,
                detection.pixels_per_mm, 
                detection.standards_compliance.value if detection.standards_compliance else None,
                detection.applicable_limit_inches, detection.compliance_confidence,
                detection.user_feedback, detection.is_verified
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_compliance_statistics(self) -> Dict[str, Any]:
        """Get ASTM compliance statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Overall compliance rates
            cursor.execute("""
                SELECT standards_compliance, COUNT(*) as count
                FROM enhanced_defect_detections 
                WHERE standards_compliance IS NOT NULL
                GROUP BY standards_compliance
            """)
            compliance_distribution = dict(cursor.fetchall())
            
            # Compliance by metal type
            cursor.execute("""
                SELECT metal_type, standards_compliance, COUNT(*) as count
                FROM enhanced_defect_detections 
                WHERE metal_type IS NOT NULL AND standards_compliance IS NOT NULL
                GROUP BY metal_type, standards_compliance
            """)
            metal_compliance = {}
            for row in cursor.fetchall():
                metal_type, compliance, count = row
                if metal_type not in metal_compliance:
                    metal_compliance[metal_type] = {}
                metal_compliance[metal_type][compliance] = count
            
            return {
                "compliance_distribution": compliance_distribution,
                "metal_type_compliance": metal_compliance,
                "total_analyzed": sum(compliance_distribution.values())
            }

# Backward compatibility functions
def create_enhanced_detection_from_basic(basic_detection, 
                                       metal_type: Optional[MetalType] = None,
                                       thickness_inches: Optional[float] = None,
                                       required_grade: Optional[QualityGrade] = None,
                                       pixels_per_mm: Optional[float] = None) -> EnhancedDefectDetection:
    """Convert basic DefectDetection to EnhancedDefectDetection"""
    
    # Calculate defect size in pixels
    x1, y1, x2, y2 = basic_detection.bbox
    width_pixels = x2 - x1
    height_pixels = y2 - y1
    defect_size_pixels = max(width_pixels, height_pixels)
    
    # Calculate sizes in mm and inches if calibration is available
    defect_size_mm = None
    defect_size_inches = None
    if pixels_per_mm:
        defect_size_mm = defect_size_pixels / pixels_per_mm
        defect_size_inches = defect_size_mm / 25.4
    
    enhanced = EnhancedDefectDetection(
        timestamp=basic_detection.timestamp,
        image_hash=basic_detection.image_hash,
        defect_type=basic_detection.defect_type,
        confidence=basic_detection.confidence,
        bbox=basic_detection.bbox,
        defect_size_pixels=defect_size_pixels,
        defect_size_mm=defect_size_mm,
        defect_size_inches=defect_size_inches,
        image_size=basic_detection.image_size,
        model_version=basic_detection.model_version,
        metal_type=metal_type,
        thickness_inches=thickness_inches,
        required_grade=required_grade,
        pixels_per_mm=pixels_per_mm,
        user_feedback=basic_detection.user_feedback,
        is_verified=basic_detection.is_verified
    )
    
    # Perform ASTM compliance analysis if all required data is available
    if all([metal_type, required_grade, defect_size_inches]):
        standards_manager = ASTMStandardsManager()
        compliance_result, confidence = standards_manager.determine_pass_fail(
            defect_size_inches, metal_type, required_grade
        )
        enhanced.standards_compliance = compliance_result
        enhanced.applicable_limit_inches = standards_manager.get_grade_limit(metal_type, required_grade)
        enhanced.compliance_confidence = confidence
    
    return enhanced
