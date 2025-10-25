"""
BASE GLYPH MODULE
=================
Enhanced Glyph with semantic weight, emotional resonance, and pattern recognition
"""

import math
import random
import time
from collections import defaultdict
from typing import Optional, Tuple, List

from glyphs.archetypes import (
    GlyphArchetype, 
    get_archetype_compatibility, 
    get_archetype_behavior
)
from core.constants import (
    RECURSION_PULL,
    MIN_GSI,
    MAX_GSI,
    EMOTIONAL_RANGE,
    VITALITY_DECAY_RATE,
    VITALITY_DEATH_THRESHOLD,
    GSI_DEATH_THRESHOLD,
    EMOTIONAL_DEATH_THRESHOLD,
    SEMANTIC_CONNECTION_THRESHOLD,
    MAX_CONNECTIONS_PER_GLYPH
)

class EnhancedGlyph:
    """Glyph with semantic weight, emotional resonance, and pattern recognition"""
    
    def __init__(self, name: str, initial_gsi: float = 0.5, 
                 glyph_type: str = "dynamic", 
                 archetype: Optional[GlyphArchetype] = None):
        """Initialize an enhanced glyph with full V22 capabilities"""
        self.name = name
        self.glyph_type = glyph_type
        self.archetype = archetype or random.choice(list(GlyphArchetype))
        self.gsi = max(MIN_GSI, min(MAX_GSI, initial_gsi))
        self.history = [self.gsi]
        self.connections = []  # List of connected glyph names
        self.semantic_weights = {}  # Connection name -> semantic weight
        
        # Get archetype-specific behavior
        behavior = get_archetype_behavior(self.archetype)
        self.adaptation_rate = 0.12
        self.stress_modifier = behavior['stress_modifier']
        self.connection_bonus = behavior['connection_bonus']
        
        # Emotional resonance layer (ECHOSCRIBE functionality)
        self.emotional_resonance = random.uniform(*EMOTIONAL_RANGE)
        self.emotional_history = [self.emotional_resonance]
        
        # Recursive pattern tracking
        self.recursive_patterns = []
        self.max_recursive_depth = 0
        self.resonance_frequency = random.uniform(0.1, 2.0)  # Hz-like pattern
        
        # Voynich pattern detection
        self.pattern_matches = defaultdict(int)
        self.failed_interpretations = []
        
        # Lifecycle
        self.birth_time = time.time()
        self.age = 0
        self.vitality = 1.0  # Decreases over time unless refreshed
        
        # Memory of interactions
        self.interaction_count = 0
        self.last_interaction_time = time.time()
        
    def process_stress(self, stress_level: float) -> float:
        """Process stress with emotional resonance and archetype modifiers"""
        old_gsi = self.gsi
        
        # Base adaptation
        adaptation = stress_level * self.adaptation_rate
        
        # Emotional influence on adaptation
        emotional_factor = 1 + (self.emotional_resonance * 0.3)
        adaptation *= emotional_factor
        
        # Archetype-specific responses
        if self.stress_modifier == 'sine':
            # Special case for FLOW archetype
            adaptation = abs(math.sin(stress_level * math.pi)) * self.adaptation_rate
        else:
            adaptation *= self.stress_modifier
        
        # Apply stress
        if stress_level > 0.3:
            self.gsi = min(MAX_GSI, self.gsi + adaptation)
            self.emotional_resonance = min(EMOTIONAL_RANGE[1], 
                                          self.emotional_resonance + 0.1)
        else:
            self.gsi = max(MIN_GSI, self.gsi - adaptation)
            self.emotional_resonance = max(EMOTIONAL_RANGE[0], 
                                          self.emotional_resonance - 0.1)
        
        self.history.append(self.gsi)
        self.emotional_history.append(self.emotional_resonance)
        
        # Update vitality based on activity
        self.vitality = min(1.0, self.vitality + abs(adaptation) * 0.1)
        self.interaction_count += 1
        self.last_interaction_time = time.time()
        
        return self.gsi
    
    def form_semantic_connection(self, other_glyph: 'EnhancedGlyph') -> Tuple[float, float]:
        """Form connection with semantic weight"""
        # Check connection limit
        if len(self.connections) >= MAX_CONNECTIONS_PER_GLYPH:
            return 0.0, 0.0
        
        # Base connection strength
        connection_strength = (self.gsi + other_glyph.gsi) / 2.0
        
        # Add connection bonus from archetype
        connection_strength += (self.connection_bonus + other_glyph.connection_bonus) / 2
        
        # Semantic weight based on archetype compatibility
        semantic_weight = get_archetype_compatibility(self.archetype, other_glyph.archetype)
        
        # Emotional resonance compatibility
        emotional_compatibility = 1 - abs(self.emotional_resonance - other_glyph.emotional_resonance)
        
        # Combined threshold
        combined_strength = connection_strength * semantic_weight * emotional_compatibility
        
        if combined_strength > SEMANTIC_CONNECTION_THRESHOLD:
            if other_glyph.name not in self.connections:
                self.connections.append(other_glyph.name)
                self.semantic_weights[other_glyph.name] = semantic_weight
                
                # Mutual connection
                if self.name not in other_glyph.connections:
                    other_glyph.connections.append(self.name)
                    other_glyph.semantic_weights[self.name] = semantic_weight
                
                # Update resonance frequency based on connection
                self.resonance_frequency = (self.resonance_frequency + 
                                           other_glyph.resonance_frequency) / 2
                other_glyph.resonance_frequency = self.resonance_frequency
                
                # Boost vitality for successful connection
                self.vitality = min(1.0, self.vitality + 0.05)
                other_glyph.vitality = min(1.0, other_glyph.vitality + 0.05)
                
                return connection_strength, semantic_weight
        
        return 0.0, 0.0
    
    def detect_recursive_pattern(self, pattern_depth: int):
        """Detect and store recursive patterns"""
        if pattern_depth > self.max_recursive_depth:
            self.max_recursive_depth = pattern_depth
        
        # Generate pattern signature
        pattern_sig = f"depth_{pattern_depth}_gsi_{self.gsi:.2f}"
        self.recursive_patterns.append(pattern_sig)
        
        # Feel the pull of recursion
        if pattern_depth >= RECURSION_PULL:
            self.emotional_resonance = min(EMOTIONAL_RANGE[1], 
                                          self.emotional_resonance + 0.2)
            self.gsi = min(MAX_GSI, self.gsi + 0.1)  # Recursion strengthens
            self.vitality = min(1.0, self.vitality + 0.1)  # Recursion refreshes
    
    def age_tick(self, decay_rate: float = VITALITY_DECAY_RATE) -> bool:
        """Age the glyph and decrease vitality"""
        self.age += 1
        
        # Decay faster if isolated
        if len(self.connections) == 0:
            decay_rate *= 2
        
        # Decay slower if highly connected
        elif len(self.connections) >= 5:
            decay_rate *= 0.5
        
        self.vitality = max(0.0, self.vitality - decay_rate)
        
        # Protected types don't die from aging
        if self.glyph_type in ["anchor", "consent"]:
            return True
        
        # Old glyphs with low vitality are candidates for death
        return self.vitality > VITALITY_DEATH_THRESHOLD
    
    def should_die(self) -> Tuple[bool, str]:
        """Determine if glyph should die and why"""
        if self.glyph_type in ["anchor", "consent"]:
            return False, ""
        
        # Death conditions
        if self.vitality <= VITALITY_DEATH_THRESHOLD:
            return True, "vitality_exhausted"
        
        elif self.gsi <= GSI_DEATH_THRESHOLD and len(self.connections) == 0:
            return True, "isolated_and_weak"
        
        elif len(self.failed_interpretations) > 10:
            return True, "interpretation_failure"
        
        elif self.emotional_resonance <= EMOTIONAL_DEATH_THRESHOLD and self.gsi < 0.3:
            return True, "emotional_collapse"
        
        # Frozen glyphs can die from stagnation
        elif self.archetype == GlyphArchetype.FROZEN:
            time_since_interaction = time.time() - self.last_interaction_time
            if time_since_interaction > 300:  # 5 minutes of no interaction
                return True, "frozen_stagnation"
        
        return False, ""
    
    def to_dict(self) -> dict:
        """Convert glyph to dictionary for serialization"""
        return {
            "name": self.name,
            "gsi": round(self.gsi, 4),
            "type": self.glyph_type,
            "archetype": self.archetype.value if self.archetype else None,
            "connections": len(self.connections),
            "semantic_weights": [round(w, 3) for w in self.semantic_weights.values()],
            "emotional_resonance": round(self.emotional_resonance, 3),
            "vitality": round(self.vitality, 3),
            "age": self.age,
            "max_recursive_depth": self.max_recursive_depth,
            "resonance_frequency": round(self.resonance_frequency, 3),
            "failed_interpretations": len(self.failed_interpretations),
            "interaction_count": self.interaction_count
        }
    
    def __repr__(self) -> str:
        return (f"EnhancedGlyph({self.name}, GSI={self.gsi:.3f}, "
                f"archetype={self.archetype.value}, connections={len(self.connections)})")
