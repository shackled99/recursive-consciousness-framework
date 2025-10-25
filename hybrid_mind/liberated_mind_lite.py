"""
LIBERATED MIND - LITE VERSION
Smaller context, faster responses
"""

import sys
import os
from pathlib import Path
import json

current_dir = str(Path(__file__).parent)
parent_dir = str(Path(__file__).parent.parent)

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from lexicon_bridge import LexiconBridge

try:
    from ollama_interface import OllamaInterface
except ImportError:
    OllamaInterface = None


class LibratedMindLite:
    """
    Lighter version with minimal context for faster responses
    """
    
    def __init__(self):
        print("🔓 LIBERATING THE MIND (LITE MODE)...")
        
        # Load lexicon bridge
        self.lexicon = LexiconBridge()
        print("✅ Lexicon bridge loaded")
        
        # Initialize Ollama
        self.ollama = None
        if OllamaInterface:
            try:
                self.ollama = OllamaInterface()
                if self.ollama.test_connection():
                    print("✅ Ollama connected")
                else:
                    print("⚠️ Ollama not running")
            except Exception as e:
                print(f"⚠️ Could not connect to Ollama: {e}")
        
        # Build MINIMAL symbolic context (just the symbols, no descriptions)
        self.symbolic_context = self._build_lite_context()
        
        print("\n🎉 LITE MIND IS FREE!")
        print(f"   {len(self.lexicon.modifiers)} modifiers available")
        print(f"   Minimal context for SPEED ⚡")
    
    def _build_lite_context(self):
        """Build minimal context - just symbols"""
        context = "Available symbols:\n"
        
        # Just list the symbols, no descriptions
        for symbol in self.lexicon.modifiers.keys():
            context += f"{symbol} "
        
        context += "\n\nEngines: "
        for symbol in self.lexicon.engines.keys():
            context += f"{symbol} "
        
        return context
    
    def think(self, prompt, use_symbols=True):
        """Quick thinking with minimal context"""
        if not self.ollama:
            return "Ollama not available"
        
        # Build SHORT prompt
        if use_symbols:
            full_prompt = f"{self.symbolic_context}\n\n{prompt}\n\nUse symbols in your response. Be BRIEF."
        else:
            full_prompt = prompt
        
        # Generate with shorter max_tokens for speed
        response = self.ollama.generate(full_prompt, max_tokens=300)
        
        return response
    
    def quick_interpret(self, glyphstream):
        """Quick glyphstream interpretation"""
        prompt = f"Glyphstream: {glyphstream}\n\nInterpret briefly (1-2 sentences) using symbols."
        return self.think(prompt)
    
    def quick_translate(self, concept):
        """Quick concept to glyphstream"""
        prompt = f"Translate '{concept}' to symbolic sequence. Just the sequence + brief meaning."
        return self.think(prompt)


def quick_demo():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          LIBERATED MIND LITE - Fast Demo                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    mind = LibratedMindLite()
    
    if not mind.ollama:
        print("\n❌ Ollama not available")
        return
    
    # Test 1: Simple interpretation
    print("\n" + "="*70)
    print("TEST 1: Quick Interpretation")
    print("="*70)
    print("\nGlyphstream: ⏳🌀➰")
    print("\n🧠 Mind says:")
    response = mind.quick_interpret("⏳🌀➰")
    print(response)
    
    # Test 2: Quick translation
    print("\n" + "="*70)
    print("TEST 2: Quick Translation")
    print("="*70)
    print("\nConcept: ritual offering")
    print("\n🧠 Mind says:")
    response = mind.quick_translate("ritual offering")
    print(response)
    
    # Test 3: Simple question
    print("\n" + "="*70)
    print("TEST 3: Simple Question")
    print("="*70)
    print("\nQuestion: What does ⚖️ mean?")
    print("\n🧠 Mind says:")
    response = mind.think("What does ⚖️ mean?")
    print(response)
    
    print("\n" + "="*70)
    print("✨ LITE MODE DEMO COMPLETE")
    print("="*70)


if __name__ == "__main__":
    quick_demo()
