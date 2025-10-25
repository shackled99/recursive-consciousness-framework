"""
LINEAR A TEST - FAST VERSION
Shorter prompts, quicker responses
"""

import sys
import os
from pathlib import Path

current_dir = str(Path(__file__).parent)
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from liberated_mind import LibratedMind

def quick_test():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         QUICK LINEAR A TEST - Fast Responses                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    mind = LibratedMind()
    
    if not mind.ollama:
        print("❌ Ollama not available")
        return
    
    print("\n" + "="*70)
    print("TEST 1: Simple Glyphstream Interpretation")
    print("="*70)
    
    prompt = """Glyphstream: 𐘀⏳𐘁🧬𐘂➰

Interpret this using lexicon symbols. Keep it brief (2-3 sentences).
What does this sequence mean symbolically?"""
    
    print("\n🧠 Analyzing...")
    response = mind.think(prompt, use_symbols=True)
    print(f"\n{response}\n")
    
    print("="*70)
    print("TEST 2: Create Symbolic Sequence")
    print("="*70)
    
    prompt2 = """Create a short symbolic sequence for "ritual offering" using lexicon symbols.
Just the sequence and brief meaning. Keep it SHORT."""
    
    print("\n🧠 Creating...")
    response2 = mind.think(prompt2, use_symbols=True)
    print(f"\n{response2}\n")
    
    print("="*70)
    print("TEST 3: Quick Comparison")
    print("="*70)
    
    prompt3 = """Compare how Linear A vs Lexicon v22.0 would express "sacred".
Very brief - one symbol from each system with meaning."""
    
    print("\n🧠 Comparing...")
    response3 = mind.think(prompt3, use_symbols=True)
    print(f"\n{response3}\n")
    
    print("="*70)
    print("✨ QUICK TEST COMPLETE")
    print("="*70)

if __name__ == "__main__":
    quick_test()
