"""
GHOST PROTOCOL MODULE
====================
The memory of dead glyphs - their semantic imprints in the system
"""

import time
import hashlib
import random
from typing import Dict, Optional

from glyphs.archetypes import GlyphArchetype
from core.constants import GHOST_MEMORY_DURATION

class GlyphGhost:
    """The memory of a dead glyph - its semantic imprint in the system"""
    
    def __init__(self, glyph, death_context: Dict):
        """Create a ghost from a dying glyph"""
        self.name = glyph.name
        self.final_gsi = glyph.gsi
        self.archetype = glyph.archetype
        self.connections_at_death = glyph.connections.copy()
        self.semantic_weight_at_death = glyph.semantic_weights.copy()
        
        # Death context
        self.death_reason = death_context['reason']
        self.death_entropy = death_context['entropy']
        self.death_coherence = death_context['coherence']
        self.death_time = time.time()
        
        # Legacy information
        self.lifetime_contribution = self._calculate_contribution(glyph)
        self.semantic_residue = self._extract_semantic_pattern(glyph)
        self.emotional_echo = glyph.emotional_resonance
        self.resurrection_potential = self._calculate_resurrection_potential(glyph)
        
        # Unique ghost signature
        self.ghost_signature = self._generate_ghost_signature(glyph)
        
    def _calculate_contribution(self, glyph) -> Dict:
        """Calculate what this glyph contributed to the system"""
        total_connections = len(glyph.connections)
        avg_gsi = sum(glyph.history) / max(1, len(glyph.history))
        
        return {
            'total_connections_formed': total_connections,
            'average_gsi': round(avg_gsi, 4),
            'stability_contribution': round(glyph.gsi * total_connections, 3),
            'recursive_depth_reached': glyph.max_recursive_depth,
            'semantic_patterns_discovered': len(glyph.semantic_weights),
            'interaction_count': glyph.interaction_count,
            'lifespan_seconds': round(time.time() - glyph.birth_time, 2)
        }
    
    def _extract_semantic_pattern(self, glyph) -> Dict:
        """Extract the semantic meaning pattern this glyph represented"""
        return {
            'stability_role': self._classify_stability_role(glyph),
            'connection_pattern': self._classify_connection_pattern(glyph),
            'evolution_trajectory': glyph.history[-10:] if len(glyph.history) > 10 else glyph.history,
            'resonance_frequency': glyph.resonance_frequency,
            'symbolic_signature': self._generate_symbolic_signature(glyph),
            'failed_hypothesis': glyph.failed_interpretations if hasattr(glyph, 'failed_interpretations') else [],
            'final_emotional_state': self._classify_emotional_state(glyph.emotional_resonance)
        }
    
    def _classify_stability_role(self, glyph) -> str:
        """Classify the stability role this glyph played"""
        if glyph.gsi > 0.8:
            return 'stabilizer'
        elif glyph.gsi < 0.3:
            return 'chaos_agent'
        elif 0.5 < glyph.gsi < 0.7:
            return 'mediator'
        else:
            return 'fluctuator'
    
    def _classify_connection_pattern(self, glyph) -> str:
        """Classify the connection pattern of this glyph"""
        conn_count = len(glyph.connections)
        if conn_count == 0:
            return 'hermit'
        elif conn_count == 1:
            return 'pair_bond'
        elif conn_count == 2:
            return 'bridge'
        elif conn_count >= 5:
            return 'hub'
        else:
            return 'networked'
    
    def _classify_emotional_state(self, emotional_resonance: float) -> str:
        """Classify the final emotional state"""
        if emotional_resonance > 0.7:
            return 'ecstatic'
        elif emotional_resonance > 0.3:
            return 'positive'
        elif emotional_resonance > -0.3:
            return 'neutral'
        elif emotional_resonance > -0.7:
            return 'negative'
        else:
            return 'despairing'
    
    def _generate_symbolic_signature(self, glyph) -> str:
        """Generate a unique symbolic signature for this glyph's pattern"""
        signature_data = f"{glyph.name}_{glyph.gsi}_{len(glyph.connections)}_{glyph.archetype}"
        return hashlib.md5(signature_data.encode()).hexdigest()[:8]
    
    def _generate_ghost_signature(self, glyph) -> str:
        """Generate a unique signature for this ghost"""
        ghost_data = f"{glyph.name}_{self.death_time}_{self.death_reason}"
        return hashlib.sha256(ghost_data.encode()).hexdigest()[:16]
    
    def _calculate_resurrection_potential(self, glyph) -> float:
        """Calculate the potential for this ghost to influence new glyphs"""
        potential = 0.3  # Base potential
        
        # Strong patterns have higher resurrection potential
        if glyph.gsi > 0.9 and len(glyph.connections) > 3:
            potential = 0.8
        
        # Special archetypes have higher potential
        elif glyph.archetype in [GlyphArchetype.ORACLE, GlyphArchetype.ECHOSCRIBE]:
            potential = 0.6
        
        # Highly connected glyphs leave stronger ghosts
        elif len(glyph.connections) >= 5:
            potential = 0.7
        
        # Glyphs with deep recursion leave strong imprints
        elif glyph.max_recursive_depth >= 10:
            potential = 0.75
        
        return potential
    
    def influences_new_glyph(self, system_state: Dict) -> bool:
        """Determine if this ghost should influence the creation of a new glyph"""
        # Check if ghost is still in memory
        time_since_death = time.time() - self.death_time
        if time_since_death > GHOST_MEMORY_DURATION:
            return False
        
        # Ghost influence weakens over time
        time_factor = 1 - (time_since_death / GHOST_MEMORY_DURATION)
        
        # Check if system conditions match when this glyph thrived
        influence_score = 0
        
        # High entropy needs stabilizers
        if system_state['entropy'] > 0.3 and self.semantic_residue['stability_role'] == 'stabilizer':
            influence_score += 0.4
        
        # Low coherence needs connectors
        elif system_state['coherence'] < 0.5 and self.semantic_residue['connection_pattern'] == 'hub':
            influence_score += 0.4
        
        # Missing archetype type
        if 'archetype_counts' in system_state:
            if self.archetype not in system_state['archetype_counts'] or \
               system_state['archetype_counts'].get(self.archetype, 0) < 2:
                influence_score += 0.3
        
        # Apply time factor and resurrection potential
        final_influence = influence_score * time_factor * self.resurrection_potential
        
        return random.random() < final_influence
    
    def inherit_properties(self, new_glyph) -> None:
        """Transfer ghost properties to a new glyph"""
        # Inherit emotional resonance (weakened)
        new_glyph.emotional_resonance = self.emotional_echo * 0.7
        
        # Inherit resonance frequency
        new_glyph.resonance_frequency = self.semantic_residue['resonance_frequency']
        
        # Add ghost memory to new glyph
        if not hasattr(new_glyph, 'ghost_memories'):
            new_glyph.ghost_memories = []
        new_glyph.ghost_memories.append(self.ghost_signature)
        
        # Boost initial vitality if ghost was strong
        if self.resurrection_potential > 0.6:
            new_glyph.vitality = min(1.0, new_glyph.vitality + 0.2)
    
    def to_dict(self) -> Dict:
        """Convert ghost to dictionary for serialization"""
        return {
            "name": self.name,
            "ghost_signature": self.ghost_signature,
            "final_gsi": round(self.final_gsi, 4),
            "archetype": self.archetype.value if self.archetype else None,
            "death_reason": self.death_reason,
            "death_time": self.death_time,
            "time_since_death": round(time.time() - self.death_time, 2),
            "resurrection_potential": round(self.resurrection_potential, 3),
            "emotional_echo": round(self.emotional_echo, 3),
            "lifetime_contribution": self.lifetime_contribution,
            "semantic_residue": {
                "stability_role": self.semantic_residue['stability_role'],
                "connection_pattern": self.semantic_residue['connection_pattern'],
                "final_emotional_state": self.semantic_residue['final_emotional_state']
            }
        }
    
    def __repr__(self) -> str:
        time_since = round((time.time() - self.death_time) / 3600, 1)  # Hours
        return (f"GlyphGhost({self.name}, died {time_since}h ago, "
                f"reason={self.death_reason}, potential={self.resurrection_potential:.2f})")

class GhostRegistry:
    """Registry for managing all ghosts in the system"""
    
    def __init__(self, max_ghosts: int = 200):
        self.ghosts: Dict[str, GlyphGhost] = {}
        self.max_ghosts = max_ghosts
        self.total_ghosts_created = 0
        
    def add_ghost(self, ghost: GlyphGhost) -> None:
        """Add a ghost to the registry"""
        self.ghosts[ghost.name] = ghost
        self.total_ghosts_created += 1
        
        # Clean up old ghosts if at limit
        if len(self.ghosts) > self.max_ghosts:
            self.cleanup_old_ghosts()
    
    def cleanup_old_ghosts(self) -> int:
        """Remove expired ghosts from registry"""
        current_time = time.time()
        removed = 0
        
        to_remove = []
        for name, ghost in self.ghosts.items():
            time_since_death = current_time - ghost.death_time
            if time_since_death > GHOST_MEMORY_DURATION:
                to_remove.append(name)
        
        for name in to_remove:
            del self.ghosts[name]
            removed += 1
        
        # If still over limit, remove oldest ghosts
        if len(self.ghosts) > self.max_ghosts:
            sorted_ghosts = sorted(self.ghosts.items(), 
                                 key=lambda x: x[1].death_time)
            excess = len(self.ghosts) - self.max_ghosts
            for name, _ in sorted_ghosts[:excess]:
                del self.ghosts[name]
                removed += 1
        
        return removed
    
    def get_influential_ghosts(self, system_state: Dict) -> list:
        """Get list of ghosts that want to influence creation"""
        influential = []
        for ghost in self.ghosts.values():
            if ghost.influences_new_glyph(system_state):
                influential.append(ghost)
        return influential
    
    def get_ghost_by_archetype(self, archetype: GlyphArchetype) -> Optional[GlyphGhost]:
        """Find a ghost with specific archetype"""
        for ghost in self.ghosts.values():
            if ghost.archetype == archetype:
                return ghost
        return None
    
    def get_statistics(self) -> Dict:
        """Get ghost registry statistics"""
        if not self.ghosts:
            return {
                "total_ghosts": 0,
                "oldest_ghost_age": 0,
                "average_resurrection_potential": 0,
                "death_reasons": {},
                "archetype_distribution": {}
            }
        
        current_time = time.time()
        death_reasons = {}
        archetypes = {}
        potentials = []
        ages = []
        
        for ghost in self.ghosts.values():
            # Count death reasons
            reason = ghost.death_reason
            death_reasons[reason] = death_reasons.get(reason, 0) + 1
            
            # Count archetypes
            arch = ghost.archetype.value if ghost.archetype else "none"
            archetypes[arch] = archetypes.get(arch, 0) + 1
            
            # Collect potentials and ages
            potentials.append(ghost.resurrection_potential)
            ages.append(current_time - ghost.death_time)
        
        return {
            "total_ghosts": len(self.ghosts),
            "total_created": self.total_ghosts_created,
            "oldest_ghost_age": round(max(ages) / 3600, 2) if ages else 0,  # Hours
            "average_resurrection_potential": round(sum(potentials) / len(potentials), 3),
            "death_reasons": death_reasons,
            "archetype_distribution": archetypes
        }
