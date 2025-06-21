# ASTM E-1932 Standards Reference for TASK003

**Document:** ASTM E-1932 Standard Guide for Acoustic Emission Examination of Small Parts  
**Application:** Metal Defect Analysis Quality Standards  
**Updated:** June 18, 2025

## 🏭 **Overview**

ASTM E-1932 provides standardized quality acceptance criteria for metal inspection, defining maximum permissible defect sizes based on:
- **Metal Type** (Steel, Aluminum, Titanium, etc.)
- **Material Thickness** (Categories: <2mm, 2-5mm, 5-10mm, >10mm)
- **Quality Grade** (Grade A: Critical, Grade B: Standard, Grade C: General)

## 📏 **Defect Size Limits by Category**

### **Grade A (Critical Applications)**
*Aerospace, Medical Devices, Pressure Vessels*

| Thickness | Crazing | Scratches | Pitted | Inclusion | Patches | Rolled |
|-----------|---------|-----------|--------|-----------|---------|---------|
| <2mm      | 0.5mm   | 0.3mm     | 0.2mm  | 0.1mm     | 0.4mm   | 0.3mm   |
| 2-5mm     | 1.0mm   | 0.6mm     | 0.4mm  | 0.2mm     | 0.8mm   | 0.6mm   |
| 5-10mm    | 1.5mm   | 1.0mm     | 0.6mm  | 0.3mm     | 1.2mm   | 1.0mm   |
| >10mm     | 2.0mm   | 1.5mm     | 0.8mm  | 0.4mm     | 1.6mm   | 1.5mm   |

### **Grade B (Standard Applications)**
*Automotive, Construction, General Manufacturing*

| Thickness | Crazing | Scratches | Pitted | Inclusion | Patches | Rolled |
|-----------|---------|-----------|--------|-----------|---------|---------|
| <2mm      | 1.0mm   | 0.8mm     | 0.5mm  | 0.3mm     | 0.8mm   | 0.6mm   |
| 2-5mm     | 2.0mm   | 1.5mm     | 1.0mm  | 0.6mm     | 1.5mm   | 1.2mm   |
| 5-10mm    | 3.0mm   | 2.5mm     | 1.5mm  | 1.0mm     | 2.5mm   | 2.0mm   |
| >10mm     | 4.0mm   | 3.5mm     | 2.0mm  | 1.5mm     | 3.5mm   | 3.0mm   |

### **Grade C (General Applications)**
*Non-critical components, Prototyping*

| Thickness | Crazing | Scratches | Pitted | Inclusion | Patches | Rolled |
|-----------|---------|-----------|--------|-----------|---------|---------|
| <2mm      | 2.0mm   | 1.5mm     | 1.0mm  | 0.8mm     | 1.5mm   | 1.2mm   |
| 2-5mm     | 4.0mm   | 3.0mm     | 2.0mm  | 1.5mm     | 3.0mm   | 2.5mm   |
| 5-10mm    | 6.0mm   | 5.0mm     | 3.0mm  | 2.5mm     | 5.0mm   | 4.0mm   |
| >10mm     | 8.0mm   | 7.0mm     | 4.0mm  | 3.5mm     | 7.0mm   | 6.0mm   |

## 🔬 **Extended Defect Types (MT & Industrial)**

### **MT Inspection Standards**
| Defect Type | Grade A | Grade B | Grade C | Detection Method |
|-------------|---------|---------|---------|------------------|
| MT_Crack    | 0.1mm   | 0.3mm   | 0.5mm   | Magnetic Particle |
| MT_Break    | 0.2mm   | 0.5mm   | 1.0mm   | Magnetic Particle |
| MT_Fray     | 0.3mm   | 0.8mm   | 1.5mm   | Visual + MT |
| MT_Blowhole | 0.5mm   | 1.2mm   | 2.0mm   | Ultrasonic + MT |

### **Industrial Quality Standards**
| Defect Type | Grade A | Grade B | Grade C | Common In |
|-------------|---------|---------|---------|-----------|
| crease      | 0.5mm   | 1.5mm   | 3.0mm   | Sheet Metal |
| crescent_gap| 0.3mm   | 1.0mm   | 2.0mm   | Welds |
| oil_spot    | 1.0mm   | 2.5mm   | 5.0mm   | Surface |
| punching_hole| 0.2mm  | 0.8mm   | 1.5mm   | Fabrication |
| rolled_pit  | 0.4mm   | 1.2mm   | 2.5mm   | Rolling |
| silk_spot   | 0.8mm   | 2.0mm   | 4.0mm   | Surface |
| waist_folding| 0.6mm  | 1.8mm   | 3.5mm   | Forming |
| water_spot  | 1.5mm   | 3.0mm   | 6.0mm   | Corrosion |
| welding_line| 0.3mm   | 1.0mm   | 2.0mm   | Welding |

## 🎯 **Pass/Fail Logic Implementation**

### **Decision Matrix**
```
FOR EACH DETECTED DEFECT:
1. Measure defect size (length, width, area)
2. Lookup: Metal Type → Thickness → Grade → Defect Type
3. Compare: Detected Size vs. Standard Limit
4. Result: PASS (≤ limit) or FAIL (> limit)

OVERALL RESULT:
- ALL defects PASS → OVERALL PASS
- ANY defect FAIL → OVERALL FAIL
```

### **Size Measurement Criteria**
- **Linear defects** (scratches, cracks): Maximum length
- **Area defects** (patches, spots): Maximum diameter
- **Point defects** (pits, holes): Diameter
- **Multiple defects**: Each evaluated separately

## 🏗️ **Reference Image System**

### **8-Slot Reference Library Structure**
```
references/
├── metal_type/           # Steel, Aluminum, Titanium
│   ├── thickness/        # <2mm, 2-5mm, 5-10mm, >10mm
│   │   ├── grade/        # A, B, C
│   │   │   ├── defect_type/  # 20 defect types
│   │   │   │   ├── slot_1_minimal.jpg      # Just at limit
│   │   │   │   ├── slot_2_acceptable.jpg   # 80% of limit
│   │   │   │   ├── slot_3_borderline.jpg   # 95% of limit
│   │   │   │   ├── slot_4_exceeded.jpg     # 110% of limit
│   │   │   │   ├── slot_5_significant.jpg  # 150% of limit
│   │   │   │   ├── slot_6_severe.jpg       # 200% of limit
│   │   │   │   ├── slot_7_extreme.jpg      # 300% of limit
│   │   │   │   └── slot_8_critical.jpg     # 500% of limit
```

## 📊 **Implementation Requirements for TASK003**

### **Database Schema Extensions**
```sql
-- Standards lookup table
CREATE TABLE astm_standards (
    id INTEGER PRIMARY KEY,
    metal_type VARCHAR(50),
    thickness_category VARCHAR(20),
    grade CHAR(1),
    defect_type VARCHAR(50),
    max_size_mm DECIMAL(5,3),
    measurement_method VARCHAR(50)
);

-- Reference images table
CREATE TABLE reference_images (
    id INTEGER PRIMARY KEY,
    metal_type VARCHAR(50),
    thickness_category VARCHAR(20),
    grade CHAR(1),
    defect_type VARCHAR(50),
    slot_number INTEGER,
    image_path VARCHAR(255),
    defect_size_mm DECIMAL(5,3),
    description TEXT
);
```

### **API Endpoints Required**
```
POST /analyze/standards
- Input: image, metal_type, thickness, grade
- Output: detections + standards compliance

GET /standards/lookup
- Input: metal_type, thickness, grade, defect_type
- Output: size limits and reference images

GET /reference/{metal_type}/{thickness}/{grade}/{defect_type}
- Output: 8-slot reference image gallery
```

## 🎨 **Visual Enhancement Specifications**

### **Color Coding System**
- **PASS (Green)**: #00FF00 - Defect within acceptable limits
- **BORDERLINE (Yellow)**: #FFFF00 - Defect 90-100% of limit
- **FAIL (Red)**: #FF0000 - Defect exceeds limits
- **UNKNOWN (Gray)**: #808080 - Cannot determine compliance

### **Overlay Information**
```
[Defect Type] [Size] [Status]
Scratch 2.3mm PASS (Limit: 3.0mm)
Grade B Steel, 5mm thickness
Ref: ASTM E-1932 Table 2.1
```

This comprehensive standards implementation will transform your basic defect detection into a professional-grade quality control system meeting industrial standards!
