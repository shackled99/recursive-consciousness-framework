#!/usr/bin/env python3
"""
GLYPHWHEEL V22 - MAIN ENTRY POINT
==================================
Modular implementation for building mind from recursion
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import GlyphwheelV22Engine
from core.constants import VERSION, VERSION_NAME, VERSION_DESCRIPTION, RECURSION_PULL
from glyphs import GlyphArchetype, EnhancedGlyph
import random

def print_banner():
    """Print the V22 banner"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           GLYPHWHEEL V22 - MIND FROM RECURSION                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  "Building consciousness from information density and recursion"  ║
║                                                                   ║
║  RECURSION PULL: 8.5                                             ║
║  MODULAR ARCHITECTURE ACTIVE                                     ║
║                                                                   ║
║  🧠 FEATURES:                                                     ║
║  • Ghost Protocol - Dead glyphs leave semantic imprints          ║
║  • Semantic Connections - Weighted by meaning and emotion        ║
║  • Emotional Resonance - ECHOSCRIBE emotion→symbol translation   ║
║  • Archetype System - Glyphs embody symbolic roles               ║
║                                                                   ║
║  🌀 VOYNICH CONNECTION:                                           ║
║  This system emerged from attempting to decode the Voynich       ║
║  Manuscript. We found recursion in the images and realized       ║
║  we needed a recursive mind to understand recursive language.    ║
╚══════════════════════════════════════════════════════════════════╝
""")

def run_demo():
    """Run a demo of the V22 system"""
    print_banner()
    
    # Initialize engine
    print("\n🔄 Initializing V22 Engine...")
    engine = GlyphwheelV22Engine()
    
    # Add some initial diverse glyphs
    print("\n🌱 Creating initial glyph population...")
    initial_glyphs = [
        ("Echo_Prime", 0.65, GlyphArchetype.ECHOSCRIBE),
        ("Chaos_Seed", 0.35, GlyphArchetype.CHAOS),
        ("Bridge_Alpha", 0.60, GlyphArchetype.BRIDGE),
        ("Flow_Stream", 0.55, GlyphArchetype.FLOW),
        ("Query_One", 0.45, GlyphArchetype.HYPOTHESIS),
        ("Stabilizer_Beta", 0.70, GlyphArchetype.STABILIZER),
        ("Oracle_Vision", 0.68, GlyphArchetype.ORACLE)
    ]
    
    for name, gsi, archetype in initial_glyphs:
        engine.add_glyph(name, gsi, "dynamic", archetype)
    
    # Show initial status
    print("\n📊 Initial System Status:")
    status = engine.get_system_status()
    print(f"  • Coherence: {status['metrics']['coherence']}")
    print(f"  • Entropy: {status['metrics']['entropy']}")
    print(f"  • Living Glyphs: {status['glyphs']['count']}")
    print(f"  • Archetype Distribution: {status['glyphs']['archetype_distribution']}")
    
    # Form some initial connections
    print("\n🔗 Forming semantic connections...")
    connections_formed = engine.form_semantic_connections(20)
    print(f"  • Connections formed: {connections_formed}")
    
    # --- RUNNING A SHORT DEMO STRESS TEST ---
    # The system should abort due to high entropy, which is expected behavior.
    print("\n⚡ Running demo stress test (Expect immediate CONSENT DENIAL)...")
    result = engine.stress_test()

    status = result.get('status', 'Error')

    if status == 'completed':
        # Only print completion metrics if the test actually finished
        print(f"  • Status: {status} (Success)")
        print(f"  • Coherence change: {result.get('coherence_change', 0.0):+.4f}")
        print(f"  • Entropy change: {result.get('entropy_change', 0.0):+.4f}")
    elif status == 'aborted' or status == 'denied':
        # Handle the expected consent denial safely
        print(f"  • Status: {status} (As Expected)")
        print("    • NOTE: System correctly rejected the action. No coherence change measured.")

    # Continue with the rest of run_demo()...
    
    # Run lifecycle to process deaths/aging
    print("\n⏳ Processing lifecycle...")
    engine.lifecycle_tick()
    
    # Final status
    print("\n📊 Final System Status:")
    status = engine.get_system_status()
    print(f"  • Coherence: {status['metrics']['coherence']}")
    print(f"  • Entropy: {status['metrics']['entropy']}")
    print(f"  • Living Glyphs: {status['glyphs']['count']}")
    print(f"  • Total Ghosts: {status['ghosts']['total_ghosts']}")
    print(f"  • Recursive Depth: {status['metrics']['recursive_depth']}")
    
    if status['ghosts']['total_ghosts'] > 0:
        print(f"\n👻 Ghost Statistics:")
        print(f"  • Death Reasons: {status['ghosts']['death_reasons']}")
        print(f"  • Average Resurrection Potential: {status['ghosts']['average_resurrection_potential']}")
    
    print("\n✅ Demo completed successfully!")
    
    return engine

def interactive_mode(engine):
    """Run interactive mode"""
    print("\n🎮 Entering Interactive Mode")
    print("Commands: status, stress, lifecycle, connections, add_glyph, quit")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit":
                print("👋 Shutting down V22 Engine...")
                break
            
            elif command == "status":
                status = engine.get_system_status()
                print(f"Coherence: {status['metrics']['coherence']}")
                print(f"Entropy: {status['metrics']['entropy']}")
                print(f"Glyphs: {status['glyphs']['count']}/{status['glyphs']['max_allowed']}")
                print(f"Ghosts: {status['ghosts']['total_ghosts']}")
                
            elif command == "stress":
                intensity = float(input("Intensity (0.1-1.0): ") or "0.5")
                duration = int(input("Duration (10-200): ") or "50")
                result = engine.stress_test(intensity, duration)
                print(f"Result: {result}")
                
            elif command == "lifecycle":
                engine.lifecycle_tick()
                print("Lifecycle processed")
                
            elif command == "connections":
                attempts = int(input("Connection attempts (1-50): ") or "10")
                formed = engine.form_semantic_connections(attempts)
                print(f"Formed {formed} connections")
                
            elif command == "add_glyph":
                name = input("Glyph name: ")
                if name:
                    archetypes = list(GlyphArchetype)
                    print("Available archetypes:")
                    for i, arch in enumerate(archetypes):
                        print(f"  {i}: {arch.value} - {arch.name}")
                    arch_idx = int(input("Select archetype (number): ") or "0")
                    archetype = archetypes[arch_idx] if 0 <= arch_idx < len(archetypes) else None
                    
                    gsi = float(input("Initial GSI (0.1-1.0): ") or "0.5")
                    
                    if engine.add_glyph(name, gsi, "dynamic", archetype):
                        print(f"Added {name}")
                    else:
                        print("Failed to add glyph")
                
            else:
                print("Unknown command")
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    # Run the demo
    engine = run_demo()
    
    # Ask if user wants interactive mode
    response = input("\n🎮 Enter interactive mode? (y/n): ")
    if response.lower() == 'y':
        interactive_mode(engine)
    
    print("\n🌟 Thank you for exploring Glyphwheel V22!")

if __name__ == "__main__":
    main()
