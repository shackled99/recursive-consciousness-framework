#!/usr/bin/env python3
"""
Quick test to see if the glyphwheel code runs without issues
"""

try:
    # Import the main module
    import sys
    sys.path.append('.')
    
    # Test basic imports
    from glyphwheelpython import GlyphwheelEngine, Glyph, run_basic_demo
    
    print("✅ All imports successful!")
    print("✅ Code should run without dependency issues")
    
    # Quick test of basic functionality
    engine = GlyphwheelEngine()
    print(f"✅ Engine created with {len(engine.glyphs)} initial glyphs")
    
    engine.add_glyph("test_glyph", 0.5)
    print(f"✅ Added test glyph, now {len(engine.glyphs)} total glyphs")
    
    coherence = engine.calculate_system_coherence()
    entropy = engine.calculate_entropy()
    print(f"✅ System metrics calculated: coherence={coherence:.3f}, entropy={entropy:.3f}")
    
    print("\n🎉 Basic functionality test PASSED!")
    print("\nYou can run the full demo with: python glyphwheelpython.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("There might be an issue with the code that needs fixing.")
