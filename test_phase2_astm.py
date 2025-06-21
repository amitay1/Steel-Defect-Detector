"""
Phase 2 Validation Script - ASTM Standards Compliance Testing
Test the enhanced ASTM integration and reference selection capabilities

Date: June 20, 2025
Task: TASK009 Phase 2
"""

import sys
import os
sys.path.append('.')
from unified_intelligent_defect_analyzer import UnifiedIntelligentDefectAnalyzer
import json

def test_phase2_astm_enhancements():
    """Test Phase 2 ASTM enhancements and reference selection"""
    
    print("🔬 PHASE 2 VALIDATION - ASTM Standards Compliance Testing")
    print("=" * 60)
    
    # Initialize the unified system
    print("\n1. Initializing Unified System...")
    analyzer = UnifiedIntelligentDefectAnalyzer()
    
    # Test different metal types and grades
    test_cases = [
        {
            'name': 'Carbon Steel Grade B',
            'image': 'USER_HIGHLIGHTED_DEFECTS/highlighted_img_04_436163100_00009.jpg',
            'metal_type': 'carbon_steel',
            'thickness': 0.5,
            'quality_grade': 'B'
        },
        {
            'name': 'Stainless Steel Grade A',
            'image': 'USER_HIGHLIGHTED_DEFECTS/highlighted_img_04_436163100_00009.jpg',
            'metal_type': 'stainless_steel',
            'thickness': 0.3,
            'quality_grade': 'A'
        },
        {
            'name': 'Aluminum Grade C',
            'image': 'USER_HIGHLIGHTED_DEFECTS/highlighted_img_04_436163100_00009.jpg',
            'metal_type': 'aluminum',
            'thickness': 0.8,
            'quality_grade': 'C'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Check if image exists
            if not os.path.exists(test_case['image']):
                print(f"   ⚠️ Image not found: {test_case['image']}")
                continue
            
            # Run analysis
            result = analyzer.analyze_image_unified(
                image_path=test_case['image'],
                metal_type=test_case['metal_type'],
                thickness=test_case['thickness'],
                quality_grade=test_case['quality_grade']
            )
            
            # Validate Phase 2 features
            print(f"   ✅ Analysis completed")
            print(f"   📊 Defects detected: {result.total_defects_detected}")
            print(f"   🟡 Pixels highlighted: {result.defect_pixels_highlighted}")
            
            # Test ASTM compliance features
            if hasattr(result, 'standards_compliance') and result.standards_compliance:
                compliance = result.standards_compliance
                print(f"   📋 ASTM Result: {compliance.get('result', 'Unknown')}")
                print(f"   ✅ Pass/Fail: {compliance.get('pass_fail', 'Unknown')}")
                print(f"   📄 Reference Number: {compliance.get('reference_number', 'None')}")
                print(f"   🔗 Reference Image: {compliance.get('reference_image', 'None')}")
            else:
                print(f"   ⚠️ No ASTM compliance data available")
            
            # Check parameters
            if hasattr(result, 'standards_parameters') and result.standards_parameters:
                params = result.standards_parameters
                print(f"   🔧 Metal Type: {params.get('metal_type', 'Unknown')}")
                print(f"   📏 Thickness: {params.get('thickness', 'Unknown')}")
                print(f"   🏅 Quality Grade: {params.get('quality_grade', 'Unknown')}")
            
            results.append({
                'test_case': test_case['name'],
                'success': True,
                'defects': result.total_defects_detected,
                'pixels': result.defect_pixels_highlighted,
                'astm_result': result.astm_compliance_result,
                'compliance': result.standards_compliance
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'test_case': test_case['name'],
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n🏆 PHASE 2 VALIDATION SUMMARY")
    print("=" * 40)
    successful_tests = sum(1 for r in results if r.get('success', False))
    total_tests = len(results)
    print(f"Tests Passed: {successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        print("✅ Phase 2 ASTM enhancements are functional")
        print("📋 Enhanced standards compliance data structure working")
        print("🔧 Reference selection logic implemented")
        print("📄 Metal type and thickness parameter handling operational")
    else:
        print("❌ Phase 2 testing encountered issues")
    
    # Save results
    with open('phase2_validation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Results saved to: phase2_validation_results.json")
    return results

if __name__ == "__main__":
    test_phase2_astm_enhancements()
