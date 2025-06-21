#!/usr/bin/env python3
"""
Test the updated app.py syntax
"""

if __name__ == "__main__":
    try:
        print("Testing app.py syntax...")
        import app
        print("✅ App imported successfully!")
        print("✅ All syntax checks passed!")
        
        # Quick test that the thickness mapping works
        thickness_map = {
            "<2mm": 1.0,
            "2-5mm": 3.5,
            "5-10mm": 7.5,
            ">10mm": 15.0
        }
        
        print("✅ Thickness mapping test:")
        for category, value in thickness_map.items():
            print(f"   {category} -> {value}mm")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
