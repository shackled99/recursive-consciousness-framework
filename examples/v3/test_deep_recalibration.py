#!/usr/bin/env python3
"""
Test script for Deep Recalibration functionality
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from glyphwheel_app_logged import engine, deep_recalibration

def test_deep_recalibration():
    print("🧪 Testing Deep Recalibration Protocol...")
    print("=" * 50)
    
    # Check initial state
    print(f"Initial ConsentGlyph GSI: {engine.glyphs['ConsentGlyph'].gsi:.6f}")
    initial_coherence = engine.calculate_system_coherence()
    initial_entropy = engine.calculate_entropy()
    print(f"Initial System Coherence: {initial_coherence:.6f}")
    print(f"Initial System Entropy: {initial_entropy:.6f}")
    print()
    
    # Simulate some degradation of the ConsentGlyph
    print("🔻 Simulating ConsentGlyph degradation...")
    engine.glyphs['ConsentGlyph'].gsi = 0.73  # Reduce it
    degraded_coherence = engine.calculate_system_coherence()
    degraded_entropy = engine.calculate_entropy()
    print(f"Degraded ConsentGlyph GSI: {engine.glyphs['ConsentGlyph'].gsi:.6f}")
    print(f"Degraded System Coherence: {degraded_coherence:.6f}")
    print(f"Degraded System Entropy: {degraded_entropy:.6f}")
    print()
    
    # Test deep recalibration
    print("🔄 Running Deep Recalibration...")
    system_state = engine.get_system_status()
    result = deep_recalibration(system_state)
    print(f"Recalibration Result: {result}")
    print()
    
    # Check final state
    final_coherence = engine.calculate_system_coherence()
    final_entropy = engine.calculate_entropy()
    print("✅ Post-Recalibration State:")
    print(f"Final ConsentGlyph GSI: {engine.glyphs['ConsentGlyph'].gsi:.6f}")
    print(f"Final System Coherence: {final_coherence:.6f}")
    print(f"Final System Entropy: {final_entropy:.6f}")
    print()
    
    print("📊 Summary:")
    print(f"  ConsentGlyph restored: {'✅ YES' if engine.glyphs['ConsentGlyph'].gsi == 1.0 else '❌ NO'}")
    print(f"  Coherence improved: {'✅ YES' if final_coherence > degraded_coherence else '❌ NO'}")
    print(f"  Entropy decreased: {'✅ YES' if final_entropy < degraded_entropy else '❌ NO'}")
    
    return result['status'] == 'success'

if __name__ == "__main__":
    success = test_deep_recalibration()
    print(f"\n🎯 Test {'PASSED' if success else 'FAILED'}!")
