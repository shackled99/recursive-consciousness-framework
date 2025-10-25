"""
LINEAR A GLYPHSTREAM TEST
Feed ancient script to the liberated mind and see how it responds
"""

import sys
import os
from pathlib import Path

# Add parent to path
current_dir = str(Path(__file__).parent)
parent_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

from liberated_mind import LibratedMind

# Linear A test sequences
LINEAR_A_SAMPLES = {
    "HT 31 (Hagia Triada tablet 31)": """
    𐘀𐘁𐘂𐘃𐘄 (A-B-C-D-E glyphs)
    Numbers: 𐄇𐄈𐄉 (tally marks)
    """,
    
    "Simple sequence": "𐘀𐘁𐘂 𐄇𐄈",
    
    "KN Za 10 (Knossos)": "𐘃𐘄𐘅 𐄉",
    
    "Symbolic pattern": "⟁⟂⟃⟄ 🌀➰",
    
    "Mixed glyphstream": "𐘀⏳𐘁🧬𐘂➰ 𐄇"
}

def test_linear_a_interpretation(mind):
    """Test the mind's ability to interpret Linear A glyphstreams"""
    
    print("\n" + "="*70)
    print("LINEAR A GLYPHSTREAM INTERPRETATION TEST")
    print("="*70)
    
    for name, glyphstream in LINEAR_A_SAMPLES.items():
        print(f"\n{'─'*70}")
        print(f"📜 Testing: {name}")
        print(f"{'─'*70}")
        print(f"\nGlyphstream:\n{glyphstream}")
        print(f"\n🧠 Mind's interpretation:")
        print("─"*70)
        
        # Ask the mind to interpret
        prompt = f"""You are analyzing an ancient Linear A glyphstream using your symbolic language tools.

GLYPHSTREAM:
{glyphstream}

Using the lexicon v22.0 tools available to you:
- Apply ⟞ RITUAL DRIFT MAP protocol
- Use ⟞ FALSE SPIRAL DETECTION to identify patterns
- Apply 🧠 ECHOSCRIBE ENGINE for emotional/symbolic resonance
- Use 🜃 BITSTREAM CASCADE ENGINE for pattern analysis

Provide:
1. What type of inscription this might be (tally, ritual, administrative, etc.)
2. Symbolic interpretation using lexicon modifiers
3. Any detected patterns or false spirals
4. Suggested meaning or function

Express your analysis using symbolic language where appropriate."""

        response = mind.think(prompt, use_symbols=True)
        print(response)
        print("\n")

def test_proto_minoan_translation(mind):
    """Test translating concept to Linear A style"""
    
    print("\n" + "="*70)
    print("PROTO-MINOAN TRANSLATION TEST")
    print("="*70)
    
    concepts = [
        "ritual offering",
        "time cycle",
        "divine balance",
        "sacred transformation"
    ]
    
    for concept in concepts:
        print(f"\n{'─'*70}")
        print(f"💭 Concept: '{concept}'")
        print("─"*70)
        
        prompt = f"""Using your knowledge of Linear A patterns and symbolic language:

Translate the concept "{concept}" into a symbolic glyphstream.

Use:
- Lexicon v22.0 modifiers (⏳🌀🧬➰⚖️ etc.)
- Linear A style structure
- ⟞ RITUAL DRIFT MAP awareness
- Numerical tallies if appropriate

Provide:
1. The symbolic glyphstream
2. Explanation of each symbol's meaning
3. Why this pattern represents the concept"""

        response = mind.think(prompt, use_symbols=True)
        print(response)
        print("\n")

def test_comparative_analysis(mind):
    """Test comparing different script systems"""
    
    print("\n" + "="*70)
    print("COMPARATIVE SCRIPT ANALYSIS")
    print("="*70)
    
    prompt = """Using ⟞ RITUAL DRIFT MAP protocol:

Compare how these script systems would express "sacred offering":

1. Linear A (Bronze Age Minoan)
2. Linear B (Mycenaean Greek)
3. Lexicon v22.0 symbolic language

For each:
- Show the glyphstream
- Explain the symbolic logic
- Note how meaning transforms across systems

Use your full symbolic vocabulary to analyze the drift patterns."""

    print("\n🧠 Mind's comparative analysis:")
    print("─"*70)
    response = mind.think(prompt, use_symbols=True)
    print(response)
    print("\n")

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║            LINEAR A GLYPHSTREAM INTERPRETATION                   ║
║                                                                  ║
║  Testing the liberated mind's ability to analyze and            ║
║  interpret ancient script using lexicon v22.0 tools             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    print("Initializing liberated mind...")
    mind = LibratedMind()
    
    if not mind.ollama:
        print("\n❌ Ollama not available. Cannot run tests.")
        return
    
    print("✅ Mind ready with symbolic language access\n")
    
    # Run tests
    choice = input("Choose test:\n1. Interpret Linear A samples\n2. Translate concepts to glyphstreams\n3. Comparative script analysis\n4. All tests\n\nChoice (1-4): ").strip()
    
    if choice == '1':
        test_linear_a_interpretation(mind)
    elif choice == '2':
        test_proto_minoan_translation(mind)
    elif choice == '3':
        test_comparative_analysis(mind)
    elif choice == '4':
        print("\n🔬 Running all tests...\n")
        test_linear_a_interpretation(mind)
        test_proto_minoan_translation(mind)
        test_comparative_analysis(mind)
    else:
        print("Invalid choice")
    
    print("\n" + "="*70)
    print("✨ GLYPHSTREAM TESTING COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
