#!/usr/bin/env python3
"""
TEST SCRIPT FOR V22 SETUP
=========================
Quick test to verify all modules are working
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports"""
    print("🔍 Testing imports...")
    
    try:
        from core.engine import GlyphwheelV22Engine
        print("  ✅ Core engine imported")
    except Exception as e:
        print(f"  ❌ Core engine import failed: {e}")
        return False
    
    try:
        from glyphs import GlyphArchetype, EnhancedGlyph, GlyphGhost, GhostRegistry
        print("  ✅ Glyph modules imported")
    except Exception as e:
        print(f"  ❌ Glyph modules import failed: {e}")
        return False
    
    try:
        from systems import SystemMonitor
        print("  ✅ System monitor imported")
    except Exception as e:
        print(f"  ❌ System monitor import failed: {e}")
        return False
    
    try:
        from api.handlers import create_handler_factory
        print("  ✅ API handlers imported")
    except Exception as e:
        print(f"  ❌ API handlers import failed: {e}")
        return False
    
    return True

def test_engine():
    """Test engine creation and basic operations"""
    print("\n🔧 Testing engine...")
    
    from core.engine import GlyphwheelV22Engine
    from glyphs import GlyphArchetype
    
    try:
        engine = GlyphwheelV22Engine()
        print("  ✅ Engine created")
        
        # Test adding a glyph
        success = engine.add_glyph("TestGlyph", 0.5, "dynamic", GlyphArchetype.ORACLE)
        if success:
            print("  ✅ Glyph added successfully")
        else:
            print("  ❌ Failed to add glyph")
            return False
        
        # Test coherence calculation
        coherence = engine.calculate_system_coherence()
        print(f"  ✅ Coherence calculated: {coherence:.3f}")
        
        # Test lifecycle
        engine.lifecycle_tick()
        print("  ✅ Lifecycle tick executed")
        
        # Test process_lifecycle (compatibility)
        engine.process_lifecycle()
        print("  ✅ Process lifecycle executed")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Engine test failed: {e}")
        return False

def test_archetypes():
    """Test all archetypes are defined"""
    print("\n🎭 Testing archetypes...")
    
    from glyphs import GlyphArchetype
    
    required_archetypes = [
        'ECHOSCRIBE', 'BITBLOOM', 'CASCADE', 'ORACLE', 
        'STABILIZER', 'CHAOS', 'FROZEN', 'FLOW', 
        'BRIDGE', 'HYPOTHESIS'
    ]
    
    for arch_name in required_archetypes:
        try:
            arch = getattr(GlyphArchetype, arch_name)
            print(f"  ✅ {arch_name}: {arch.value}")
        except AttributeError:
            print(f"  ❌ Missing archetype: {arch_name}")
            return False
    
    return True

def test_monitor():
    """Test system monitor"""
    print("\n💻 Testing system monitor...")
    
    from systems import SystemMonitor
    
    try:
        monitor = SystemMonitor()
        print("  ✅ Monitor created")
        
        # Test update method
        monitor.update()
        print("  ✅ Monitor update executed")
        
        # Test get parameters
        params = monitor.get_adaptive_parameters()
        print(f"  ✅ CPU: {params['cpu_percent']:.1f}%, RAM: {params['ram_percent']:.1f}%")
        print(f"  ✅ Recursion limit: {params['recursion_limit']}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Monitor test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("╔══════════════════════════════════════════╗")
    print("║       GLYPHWHEEL V22 SYSTEM TEST         ║")
    print("╚══════════════════════════════════════════╝")
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_engine():
        all_passed = False
    
    if not test_archetypes():
        all_passed = False
    
    if not test_monitor():
        all_passed = False
    
    print("\n" + "="*40)
    if all_passed:
        print("✨ ALL TESTS PASSED! System is ready.")
        print("\nYou can now run:")
        print("  python web/server.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("="*40)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
