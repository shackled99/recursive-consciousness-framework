"""
GLYPH ARCHETYPES
================
Symbolic roles inspired by the V22 lexicon overlay
"""

from enum import Enum

class GlyphArchetype(Enum):
    """Archetypes inspired by the V22 lexicon overlay"""
    ECHOSCRIBE = "🧠"  # Translates emotion-state into symbolic language
    BITBLOOM = "🜟"    # Binary kernel, encodes drift
    CASCADE = "🜃"     # Processes binary→symbol→meaning loops
    ORACLE = "🔮"      # Emotional-symbolic resonance
    STABILIZER = "⚖️"  # Balance and harmony
    CHAOS = "🌪️"      # Unstable recursion, entropy
    FROZEN = "🧊"      # Locked condition, halt
    FLOW = "➰"        # Feedback loops, regenerative
    BRIDGE = "🌉"      # Connection builder
    HYPOTHESIS = "❓"  # Testing interpretations

# Archetype compatibility matrix for semantic weights
ARCHETYPE_COMPATIBILITY = {
    (GlyphArchetype.ECHOSCRIBE, GlyphArchetype.ORACLE): 0.9,
    (GlyphArchetype.STABILIZER, GlyphArchetype.CHAOS): 0.3,
    (GlyphArchetype.FLOW, GlyphArchetype.CASCADE): 0.8,
    (GlyphArchetype.BRIDGE, GlyphArchetype.HYPOTHESIS): 0.7,
    (GlyphArchetype.BITBLOOM, GlyphArchetype.CASCADE): 0.85,
    (GlyphArchetype.FROZEN, GlyphArchetype.FLOW): 0.2,
    (GlyphArchetype.ORACLE, GlyphArchetype.HYPOTHESIS): 0.75,
    (GlyphArchetype.STABILIZER, GlyphArchetype.BRIDGE): 0.8,
    (GlyphArchetype.CHAOS, GlyphArchetype.HYPOTHESIS): 0.6,
    (GlyphArchetype.ECHOSCRIBE, GlyphArchetype.FLOW): 0.7,
}

# Archetype behavioral modifiers
ARCHETYPE_BEHAVIORS = {
    GlyphArchetype.CHAOS: {
        'stress_modifier': 1.5,  # Thrives on stress
        'connection_bonus': -0.1,  # Harder to connect
        'base_gsi': 0.35,
    },
    GlyphArchetype.STABILIZER: {
        'stress_modifier': 0.5,  # Resists change
        'connection_bonus': 0.2,  # Easier to connect
        'base_gsi': 0.75,
    },
    GlyphArchetype.FLOW: {
        'stress_modifier': 'sine',  # Oscillating response
        'connection_bonus': 0.15,
        'base_gsi': 0.55,
    },
    GlyphArchetype.BRIDGE: {
        'stress_modifier': 1.0,
        'connection_bonus': 0.3,  # Very connective
        'base_gsi': 0.60,
    },
    GlyphArchetype.ECHOSCRIBE: {
        'stress_modifier': 1.2,
        'connection_bonus': 0.1,
        'base_gsi': 0.65,
    },
    GlyphArchetype.HYPOTHESIS: {
        'stress_modifier': 1.1,
        'connection_bonus': 0.0,
        'base_gsi': 0.45,
    },
    GlyphArchetype.ORACLE: {
        'stress_modifier': 0.8,
        'connection_bonus': 0.05,
        'base_gsi': 0.70,
    },
    GlyphArchetype.BITBLOOM: {
        'stress_modifier': 1.0,
        'connection_bonus': 0.1,
        'base_gsi': 0.50,
    },
    GlyphArchetype.CASCADE: {
        'stress_modifier': 1.3,
        'connection_bonus': 0.15,
        'base_gsi': 0.55,
    },
    GlyphArchetype.FROZEN: {
        'stress_modifier': 0.1,  # Almost no response
        'connection_bonus': -0.3,  # Very hard to connect
        'base_gsi': 0.40,
    },
}

def get_archetype_compatibility(arch1: GlyphArchetype, arch2: GlyphArchetype) -> float:
    """Get compatibility score between two archetypes"""
    pair = (arch1, arch2)
    reverse_pair = (arch2, arch1)
    
    if pair in ARCHETYPE_COMPATIBILITY:
        return ARCHETYPE_COMPATIBILITY[pair]
    elif reverse_pair in ARCHETYPE_COMPATIBILITY:
        return ARCHETYPE_COMPATIBILITY[reverse_pair]
    else:
        return 0.5  # Default neutral compatibility

def get_archetype_behavior(archetype: GlyphArchetype) -> dict:
    """Get behavioral modifiers for an archetype"""
    return ARCHETYPE_BEHAVIORS.get(archetype, {
        'stress_modifier': 1.0,
        'connection_bonus': 0.0,
        'base_gsi': 0.5,
    })
