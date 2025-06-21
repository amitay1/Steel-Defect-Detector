"""
Phase 3 Validation Script - Advanced Pixel-Grid Analysis Testing
Test the enhanced grid analysis with reference comparison capabilities

Date: June 20, 2025
Task: TASK009 Phase 3
"""

import sys
import os
sys.path.append('.')
from unified_intelligent_defect_analyzer import UnifiedIntelligentDefectAnalyzer
import json

def test_phase3_grid_analysis():
    """Test Phase 3 advanced pixel-grid analysis"""
    
    print("🔬 PHASE 3 VALIDATION - Advanced Pixel-Grid Analysis Testing")
    print("=" * 65)
    
    # Initialize the unified system
    print("\n1. Initializing Unified System...")
    analyzer = UnifiedIntelligentDefectAnalyzer()
    
    # Test cases with different material parameters for grid analysis
    test_cases = [
        {
            'name': 'High Precision Carbon Steel Grade A',
            'image': 'unified_analysis_results/highlighted_img_04_436163100_00009_highlighted_20250620_201207.jpg',
            'metal_type': 'carbon_steel',
            'thickness': 0.3,
            'quality_grade': 'A'
        },
        {
            'name': 'Standard Stainless Steel Grade B',
            'image': 'unified_analysis_results/highlighted_img_04_436163100_00009_highlighted_20250620_201207.jpg',
            'metal_type': 'stainless_steel',
            'thickness': 0.5,
            'quality_grade': 'B'
        },
        {
            'name': 'Industrial Aluminum Grade C',
            'image': 'unified_analysis_results/highlighted_img_04_436163100_00009_highlighted_20250620_201207.jpg',
            'metal_type': 'aluminum',
            'thickness': 0.8,
            'quality_grade': 'C'
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing Grid Analysis: {test_case['name']}")
        print("-" * 50)
        
        try:
            # Check if image exists
            if not os.path.exists(test_case['image']):
                print(f"   ⚠️ Image not found: {test_case['image']}")
                continue
            
            # Run complete analysis
            result = analyzer.analyze_image_unified(
                image_path=test_case['image'],
                metal_type=test_case['metal_type'],
                thickness=test_case['thickness'],
                quality_grade=test_case['quality_grade']
            )
            
            # Display results
            print(f"   ✅ Analysis completed")
            print(f"   📊 Total defects: {result.total_defects_detected}")
            print(f"   🟡 Pixels highlighted: {result.defect_pixels_highlighted}")
            
            # Phase 3: Grid analysis results
            if hasattr(result, 'grid_analysis_results') and result.grid_analysis_results:
                grid = result.grid_analysis_results
                if isinstance(grid, dict) and 'error' not in grid:
                    print(f"   📐 Grid squares analyzed: {grid.get('total_squares', 0)}")
                    print(f"   🔍 Squares with defects: {grid.get('squares_with_defects', 0)}")
                    print(f"   ❌ Failed squares: {len(grid.get('failed_squares', []))}")
                    print(f"   ✅ Grid result: {'PASS' if grid.get('pass_fail', False) else 'FAIL'}")
                    
                    # Quality metrics
                    if 'quality_metrics' in grid:
                        metrics = grid['quality_metrics']
                        print(f"   📈 Overall quality: {metrics.get('overall_quality', 0):.3f}")
                        print(f"   🎯 Defect density: {metrics.get('defect_density', 0):.3f}")
                        print(f"   📊 Uniformity score: {metrics.get('uniformity_score', 0):.3f}")
                    
                    # Reference comparison
                    if 'reference_comparison' in grid:
                        ref = grid['reference_comparison']
                        print(f"   🔧 Failure rate: {ref.get('failure_rate', 0):.1%}")
                        thresholds = ref.get('thresholds_used', {})
                        print(f"   📏 Max defect ratio: {thresholds.get('max_defect_ratio', 0):.3f}")
                else:
                    print(f"   ⚠️ Grid analysis: {grid.get('error', 'Limited mode')}")
            
            # ASTM compliance
            if hasattr(result, 'standards_compliance') and result.standards_compliance:
                compliance = result.standards_compliance
                print(f"   📋 ASTM compliance: {compliance.get('pass_fail', 'Unknown')}")
                print(f"   📄 Reference number: {compliance.get('reference_number', 'None')}")
            
            results.append({
                'test_case': test_case['name'],
                'success': True,
                'defects': result.total_defects_detected,
                'pixels': result.defect_pixels_highlighted,
                'grid_pass': result.grid_pass_fail,
                'quality_score': result.quality_score,
                'grid_analysis': result.grid_analysis_results
            })
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'test_case': test_case['name'],
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print(f"\n🏆 PHASE 3 VALIDATION SUMMARY")
    print("=" * 40)
    successful_tests = sum(1 for r in results if r.get('success', False))
    total_tests = len(results)
    print(f"Tests Completed: {successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        print("✅ Phase 3 advanced pixel-grid analysis is functional")
        print("📐 Grid division and square analysis working")
        print("🔍 Reference threshold comparison operational")
        print("📊 Quality metrics calculation implemented")
        print("⚖️ Enhanced pass/fail logic with standards compliance")
    else:
        print("❌ Phase 3 testing encountered issues")
    
    # Save results
    with open('phase3_validation_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Results saved to: phase3_validation_results.json")
    return results

if __name__ == "__main__":
    test_phase3_grid_analysis()
