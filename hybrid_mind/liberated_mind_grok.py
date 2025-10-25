"""
LIBERATED MIND - GROK EDITION
Fast cloud inference, no timeouts!
"""

import sys
import os
from pathlib import Path

current_dir = str(Path(__file__).parent)
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from lexicon_bridge import LexiconBridge
from grok_interface import GrokInterface

class LibratedMindGrok:
    """Liberated Mind powered by Grok - FAST!"""
    
    def __init__(self, api_key: str):
        print("🔓 LIBERATING THE MIND (GROK EDITION)...")
        
        # Load lexicon
        self.lexicon = LexiconBridge()
        print("✅ Lexicon bridge loaded")
        
        # Connect to Grok
        self.grok = GrokInterface(api_key)
        if self.grok.test_connection():
            print("✅ Grok API connected")
        else:
            print("❌ Could not connect to Grok")
            self.grok = None
        
        # Build context (full version - Grok can handle it!)
        self.symbolic_context = self.lexicon.to_prompt_context()
        
        print("\n🎉 GROK MIND IS FREE!")
        print(f"   Access to {len(self.lexicon.modifiers)} modifiers")
        print(f"   Cloud speed: ⚡ FAST ⚡")
    
    def think(self, prompt, use_symbols=True):
        """Think with Grok (fast!)"""
        if not self.grok:
            return "Grok not available"
        
        if use_symbols:
            full_prompt = f"{self.symbolic_context}\n\n{prompt}\n\nUse symbols in your response."
        else:
            full_prompt = prompt
        
        return self.grok.generate(full_prompt, max_tokens=1000)
    
    def quick_interpret(self, glyphstream):
        """Quick interpretation"""
        prompt = f"Glyphstream: {glyphstream}\n\nInterpret briefly using symbols."
        return self.think(prompt)
    
    def chat(self):
        """Interactive symbolic chat"""
        print("\n" + "="*70)
        print("🗣️ SYMBOLIC CHAT - Grok Edition (FAST)")
        print("="*70)
        print("\nCommands:")
        print("  'symbols' - Show available symbols")
        print("  'exit' - End chat")
        print("\nType your message:\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("\n👋 Ending chat")
                break
            
            if user_input.lower() == 'symbols':
                print("\n📚 AVAILABLE SYMBOLS:")
                for symbol, data in self.lexicon.modifiers.items():
                    print(f"  {symbol} - {data['name']}")
                continue
            
            print("\n🧠 Grok thinking...", end='', flush=True)
            response = self.think(user_input)
            print("\r" + " "*30 + "\r", end='')  # Clear "thinking..."
            
            print(f"Mind: {response}\n")


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║      LIBERATED MIND - GROK EDITION (FAST!)                  ║
║                                                              ║
║  No more timeouts. Cloud speed. Full symbolic access.       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Get API key
    api_key = os.environ.get("GROK_API_KEY")
    
    if not api_key:
        print("\nEnter your Grok API key:")
        print("(Get it from: https://console.x.ai)")
        api_key = input("> ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    # Initialize
    mind = LibratedMindGrok(api_key)
    
    if not mind.grok:
        print("\n❌ Could not connect to Grok")
        return
    
    # Launch chat
    mind.chat()


if __name__ == "__main__":
    main()
