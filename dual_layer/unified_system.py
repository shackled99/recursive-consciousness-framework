"""
Unified Hybrid System - Web UI + Chat Interface + Ollama
All working with the same Glyphwheel instance!
"""

import sys
import threading
import webbrowser
import time

# Import existing components
try:
    from glyphwheel_optimized import OptimizedGlyphwheelEngine, run_server
    from ollama_interface import OllamaInterface
    from system_observer import SystemObserver
    from hybrid_mind import HybridMind
    from chat_interface import GlyphwheelChat
    print("✓ All components imported")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)


def start_unified_system():
    """Start the complete unified hybrid system"""
    
    print("=" * 60)
    print("GLYPHWHEEL UNIFIED HYBRID SYSTEM")
    print("=" * 60)
    print("\nInitializing unified system with:")
    print("  • Web UI (localhost:8080)")
    print("  • Chat Interface (this terminal)")
    print("  • Ollama Integration")
    print("  • Shared Glyphwheel Instance")
    print()
    
    # Check Ollama
    print("Checking Ollama...")
    ollama = OllamaInterface()
    
    if not ollama.test_connection():
        print("⚠ Ollama not connected - chat features will be limited")
        ollama = None
    else:
        models = ollama.list_models()
        print(f"✓ Ollama connected: {models}")
    
    # Create shared Glyphwheel instance
    print("\nInitializing Glyphwheel...")
    from glyphwheel_optimized import engine as shared_engine
    print(f"✓ Glyphwheel ready ({len(shared_engine.glyphs)} glyphs)")
    
    # Start web server in background thread
    print("\nStarting web server on port 8080...")
    web_thread = threading.Thread(target=run_server, args=(8080,), daemon=True)
    web_thread.start()
    time.sleep(2)  # Give server time to start
    print("✓ Web UI running at http://localhost:8080")
    
    # Try to open browser
    try:
        webbrowser.open('http://localhost:8080')
        print("✓ Opened browser")
    except:
        print("  (Open http://localhost:8080 manually)")
    
    # Setup observer and hybrid mind if Ollama available
    if ollama:
        print("\nStarting hybrid intelligence layer...")
        observer = SystemObserver(shared_engine, sample_interval=0.1)
        observer.start()
        print("✓ Observer monitoring")
        
        mind = HybridMind(shared_engine, ollama, observer)
        print("✓ Hybrid mind connected")
        
        print("\n" + "=" * 60)
        print("UNIFIED SYSTEM READY!")
        print("=" * 60)
        print()
        print("You now have:")
        print("  🌐 Web UI at http://localhost:8080")
        print("  💬 Chat interface below")
        print("  🧠 Ollama reasoning layer")
        print("  ⚡ All sharing one Glyphwheel instance!")
        print()
        print("Actions in web UI will be visible to chat!")
        print("Chat commands will update web UI!")
        print()
        
        # Start chat interface
        chat = GlyphwheelChat(mind)
        chat.start()
        
        # Cleanup
        observer.stop()
    else:
        print("\n" + "=" * 60)
        print("WEB UI MODE (Ollama not available)")
        print("=" * 60)
        print()
        print("Web UI running at http://localhost:8080")
        print("Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nShutting down...")


if __name__ == "__main__":
    try:
        start_unified_system()
    except KeyboardInterrupt:
        print("\n\nShutting down gracefully...")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
