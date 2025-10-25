"""
Hybrid Mind System Test
Verifies all components are working correctly
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from dual_layer_engine import DualLayerEngine
        print("  ✓ dual_layer_engine")
    except ImportError as e:
        print(f"  ✗ dual_layer_engine: {e}")
        return False
    
    try:
        from ollama_interface import OllamaInterface
        print("  ✓ ollama_interface")
    except ImportError as e:
        print(f"  ✗ ollama_interface: {e}")
        return False
    
    try:
        from mind_observer import MindObserver
        print("  ✓ mind_observer")
    except ImportError as e:
        print(f"  ✗ mind_observer: {e}")
        return False
    
    try:
        from mind_chat import MindChat
        print("  ✓ mind_chat")
    except ImportError as e:
        print(f"  ✗ mind_chat: {e}")
        return False
    
    try:
        from mind_coder import MindCoder
        print("  ✓ mind_coder")
    except ImportError as e:
        print(f"  ✗ mind_coder: {e}")
        return False
    
    try:
        from mind_loop import MindLoop
        print("  ✓ mind_loop")
    except ImportError as e:
        print(f"  ✗ mind_loop: {e}")
        return False
    
    return True

def test_ollama():
    """Test Ollama connection"""
    print("\n🧪 Testing Ollama connection...")
    
    try:
        from ollama_interface import OllamaInterface
        ollama = OllamaInterface()
        
        if ollama.test_connection():
            print("  ✓ Ollama is running and responding")
            return True
        else:
            print("  ✗ Ollama not responding")
            return False
    except Exception as e:
        print(f"  ✗ Ollama test failed: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n🧪 Testing directory structure...")
    
    dirs = ['observations', 'proposals']
    all_good = True
    
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/ exists")
        else:
            print(f"  ✗ {dir_name}/ missing")
            all_good = False
    
    return all_good

def test_basic_cycle():
    """Test a basic observation cycle"""
    print("\n🧪 Testing basic observation cycle...")
    
    try:
        from mind_observer import MindObserver
        from ollama_interface import OllamaInterface
        
        ollama = OllamaInterface()
        if not ollama.test_connection():
            print("  ⚠️  Skipping - Ollama not running")
            return True
        
        observer = MindObserver()
        
        # Quick test - just create base
        print("  → Initializing base system...")
        observer.initialize_base_mind()
        
        print("  → Creating test scenario...")
        observer.create_test_scenario()
        
        print("  → Running self-observation...")
        observation = observer.observe_self()
        
        if observation:
            print("  ✓ Observation cycle completed successfully")
            
            # Check observation has expected structure
            if 'system_health' in observation:
                print("  ✓ Observation contains system_health")
            if 'glyph_details' in observation:
                print("  ✓ Observation contains glyph_details")
            
            return True
        else:
            print("  ✗ Observation returned empty")
            return False
            
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all system tests"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            HYBRID MIND SYSTEM TEST SUITE                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Ollama
    results.append(("Ollama Connection", test_ollama()))
    
    # Test 3: Directories
    results.append(("Directory Structure", test_directories()))
    
    # Test 4: Basic cycle (only if Ollama is running)
    results.append(("Basic Cycle", test_basic_cycle()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name:<30} {status}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("  1. Run START_OBSERVER.bat to create initial observation")
        print("  2. Run START_CHAT.bat to talk with the mind")
        print("  3. Run START_MIND_LOOP.bat for full autonomous cycle")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        if not results[1][1]:  # Ollama test failed
            print("\n💡 Tip: Start Ollama with 'ollama serve'")
    
    print("\n")

if __name__ == "__main__":
    run_all_tests()
