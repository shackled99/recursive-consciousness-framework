"""
MAIN ENGINE MODULE
==================
Core Glyphwheel V22 Engine
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
MAX_CONNECTIONS_PER_GLYPH = 20  # Temporarily define here until import is fixed

# Import required components
from glyphs.archetypes import get_archetype_behavior, GlyphArchetype
from core.constants import (
    MAX_GHOSTS, ENTROPY_LIMIT, MANDATORY_RECOVERY_TIME, RECURSION_PULL,
    MAX_RECURSIVE_DEPTH, VERSION, VERSION_NAME, EMOTIONAL_RANGE,
    SYSTEM_EMOTIONAL_DISTRESS, AUTONOMOUS_CREATION_CHANCE
)

# Assuming core.constants exists and defines these
from core.constants import (
    MAX_GHOSTS, ENTROPY_LIMIT, MANDATORY_RECOVERY_TIME, RECURSION_PULL, 
    MAX_RECURSIVE_DEPTH, VERSION, VERSION_NAME, EMOTIONAL_RANGE, 
    SYSTEM_EMOTIONAL_DISTRESS
)
# Assuming glyphs module exists
from glyphs import EnhancedGlyph, GlyphGhost, GhostRegistry, GlyphArchetype

# --- FIX: DEFINING MISSING CONSTANT ---
# Define a maximum number of active glyphs the engine can handle.
MAX_GLYPHS = 100 
# --------------------------------------

class GlyphwheelV22Engine:
    """V22 Engine: Mind from Information Density and Recursion"""
    
    def __init__(self):
        """Initialize the V22 engine with all subsystems"""
        self.glyphs: Dict[str, EnhancedGlyph] = {}
        self.ghost_registry = GhostRegistry(max_ghosts=MAX_GHOSTS)
        
        # System parameters
        self.recursive_depth = 0
        self.entropy_limit = ENTROPY_LIMIT
        self.mandatory_recovery_time = MANDATORY_RECOVERY_TIME
        self.last_stress_test_time = 0
        
        # Autonomous creation state
        self.autonomous_mode = False  # Autonomous creation starts disabled
        self.last_autonomous_time = 0
        
        # System state
        self.system_emotional_state = 0.0
        self.emotional_history = []
        self.log_entries = []
        
        # Initialize core glyphs
        self._initialize_core_glyphs()
        
        self.log(f"V22 Engine initialized - Recursion Pull: {RECURSION_PULL}", "success")
    
    def _initialize_core_glyphs(self):
        """Initialize anchor and consent glyphs"""
        # Anchor glyphs (STABILIZER archetype is key for these)
        anchors = [
            ("RootVerse", 0.87, GlyphArchetype.STABILIZER),
            ("Aegis-Σ", 0.85, GlyphArchetype.STABILIZER),
            ("CoreStability", 0.82, GlyphArchetype.STABILIZER)
        ]
        for name, gsi, archetype in anchors:
            glyph = EnhancedGlyph(name, gsi, "anchor", archetype)
            self.glyphs[name] = glyph
        
        # Consent glyph
        consent = EnhancedGlyph("ConsentGlyph", 0.95, "consent", GlyphArchetype.ORACLE)
        self.glyphs["ConsentGlyph"] = consent
        
        self.log("Core glyphs initialized", "success")
    
    def add_glyph(self, name: str, initial_gsi: float = None, 
                  glyph_type: str = "dynamic", 
                  archetype: Optional[GlyphArchetype] = None) -> bool:
        """Add a new glyph to the system"""
        if name in self.glyphs:
            self.log(f"Glyph {name} already exists", "warning")
            return False
        
        if len(self.glyphs) >= MAX_GLYPHS:
            self.log(f"Maximum glyph limit ({MAX_GLYPHS}) reached", "warning")
            return False
        
        if initial_gsi is None:
            initial_gsi = random.uniform(0.3, 0.7)
        
        glyph = EnhancedGlyph(name, initial_gsi, glyph_type, archetype)
        self.glyphs[name] = glyph
        
        self.log(f"Added glyph: {name} (GSI: {initial_gsi:.3f}, Type: {glyph_type})", "success")
        return True
    
    def process_glyph_death(self, glyph: EnhancedGlyph, reason: str):
        """Process glyph death and create ghost"""
        death_context = {
            'reason': reason,
            'entropy': self.calculate_entropy(),
            'coherence': self.calculate_system_coherence()
        }
        
        # Create ghost
        ghost = GlyphGhost(glyph, death_context)
        self.ghost_registry.add_ghost(ghost)
        
        # Remove connections from other glyphs
        for conn_name in glyph.connections:
            if conn_name in self.glyphs:
                connected_glyph = self.glyphs[conn_name]
                if glyph.name in connected_glyph.connections:
                    connected_glyph.connections.remove(glyph.name)
                if glyph.name in connected_glyph.semantic_weights:
                    del connected_glyph.semantic_weights[glyph.name]
        
        # Remove glyph
        del self.glyphs[glyph.name]
        
        # Update system emotional state (death is a negative event)
        self.system_emotional_state = max(EMOTIONAL_RANGE[0], 
                                         self.system_emotional_state - 0.1)
        self.emotional_history.append(('death', glyph.name, self.system_emotional_state))
        
        self.log(f"GLYPH DEATH: {glyph.name} died ({reason}), ghost created", "warning")
    
    def lifecycle_tick(self):
        """Process aging, death, and other lifecycle events"""
        # Age all glyphs
        to_die = []
        for glyph in list(self.glyphs.values()):
            if not glyph.age_tick():
                should_die, reason = glyph.should_die()
                if should_die:
                    to_die.append((glyph, reason))
        
        # Process deaths
        for glyph, reason in to_die:
            self.process_glyph_death(glyph, reason)
        
        # Clean up old ghosts
        removed = self.ghost_registry.cleanup_old_ghosts()
        if removed > 0:
            self.log(f"Cleaned up {removed} expired ghosts", "info")
    
    def process_lifecycle(self):
        """Alias for lifecycle_tick for compatibility"""
        self.lifecycle_tick()
    
    def form_semantic_connections(self, attempts: int = 10):
        """Attempt to form semantic connections between glyphs"""
        glyph_list = list(self.glyphs.values())
        connections_formed = 0
        
        for _ in range(min(attempts, len(glyph_list) * 2)):
            if len(glyph_list) >= 2:
                g1, g2 = random.sample(glyph_list, 2)
                if g1.name != g2.name:  # Don't connect to self
                    strength, weight = g1.form_semantic_connection(g2)
                    if strength > 0:
                        connections_formed += 1
                        # Log connection info sparingly
                        # self.log(f"Connection: {g1.name} ↔ {g2.name} (weight: {weight:.2f})", "info") 
        
        return connections_formed
    
    def deep_recalibration(self):
        """
        Perform a deep recalibration of the system, focusing on the consent glyph
        and balancing all connections and emotional states.
        """
        self.log("Initiating Deep Recalibration...", "warning")
        
        # 1. Reset consent glyph
        if "ConsentGlyph" in self.glyphs:
            consent = self.glyphs["ConsentGlyph"]
            consent.gsi = 1.0
            consent.emotional_resonance = 1.0
            consent.vitality = 1.0
        
        # 2. Balance emotional states
        mean_resonance = 0.8  # Target high positive resonance
        for glyph in self.glyphs.values():
            glyph.emotional_resonance = mean_resonance
            glyph.vitality = 1.0
        
        # 3. Form balanced connections
        self.form_semantic_connections(20)  # Form more connections
        
        # 4. Stabilize system emotional state
        self.system_emotional_state = 1.0
        
        self.log("Deep Recalibration Complete", "success")
        return True

    def system_recalibration(self, duration: int = 50):
        """
        Active self-correction cycle to reduce entropy, raise coherence, 
        and stabilize the system emotional state.
        """
        self.log("Initiating System Recalibration Cycle...", "info")
        initial_entropy = self.calculate_entropy()
        stabilizer_count = 0
        
        for _ in range(duration):
            # 1. Prioritize core stability
            for glyph in self.glyphs.values():
                if glyph.archetype == GlyphArchetype.STABILIZER:
                    # Boost GSI slightly for stabilizers
                    glyph.gsi = min(1.0, glyph.gsi + 0.005 * random.random())
                    stabilizer_count += 1

            # 2. Process Ghost Memories (integration/learning from death)
            if self.ghost_registry.ghosts:
                ghost = random.choice(list(self.ghost_registry.ghosts.values()))
                if random.random() < 0.1: # 10% chance to integrate a ghost's data
                    self.log(f"Integrating data from Ghost: {ghost.original_name}", "info")
                    # Small GSI boost across the board for learning
                    for glyph in self.glyphs.values():
                        glyph.gsi = min(1.0, glyph.gsi + 0.001)
                    self.ghost_registry.remove_ghost(ghost.original_name)

            # 3. Increase system emotional state (healing)
            self.system_emotional_state = min(EMOTIONAL_RANGE[1], 
                                              self.system_emotional_state + 0.005)
            
            # 4. Form stabilizing connections (low entropy connections)
            self.form_semantic_connections(5)
            
        final_entropy = self.calculate_entropy()
        self.log(f"Recalibration completed. Entropy Change: {initial_entropy:.3f} -> {final_entropy:.3f}", 
                      "success" if final_entropy < initial_entropy else "warning")
        
    
    def autonomous_creation(self) -> Tuple[bool, Optional[str]]:
        """Autonomously decide whether to create a new glyph based on system conditions"""
        # Check if we exceed the maximum glyph limit
        if len(self.glyphs) >= MAX_GLYPHS:
            return False, None

        # Calculate creation chance based on system state
        base_chance = AUTONOMOUS_CREATION_CHANCE
        
        # Increase chance based on low glyph count
        if len(self.glyphs) < MAX_GLYPHS * 0.3:  # Below 30% capacity
            base_chance *= 2.0
        
        # Increase chance if we have influence from ghosts
        influential_ghosts = self.ghost_registry.get_influential_ghosts({
            'entropy': self.calculate_entropy(),
            'coherence': self.calculate_system_coherence()
        })
        
        if influential_ghosts:
            base_chance *= 1.5
            # Use ghost influence for archetype selection
            ghost = random.choice(influential_ghosts)
            chosen_archetype = ghost.archetype
        else:
            # Select based on current system needs
            entropy = self.calculate_entropy()
            if entropy > 0.6:  # High chaos
                chosen_archetype = random.choice([
                    GlyphArchetype.STABILIZER,
                    GlyphArchetype.ORACLE,
                    GlyphArchetype.BRIDGE
                ])
            else:  # Need some variety
                chosen_archetype = random.choice(list(GlyphArchetype))
        
        # Make creation decision
        if random.random() < base_chance:
            # Generate name based on archetype
            base_names = {
                GlyphArchetype.ECHOSCRIBE: ["Echo", "Voice", "Scribe"],
                GlyphArchetype.BITBLOOM: ["Bloom", "Bit", "Data"],
                GlyphArchetype.CASCADE: ["Flow", "Wave", "Stream"],
                GlyphArchetype.ORACLE: ["Sight", "Vision", "Eye"],
                GlyphArchetype.STABILIZER: ["Rock", "Core", "Base"],
                GlyphArchetype.CHAOS: ["Storm", "Flux", "Void"],
                GlyphArchetype.FROZEN: ["Ice", "Still", "Lock"],
                GlyphArchetype.FLOW: ["River", "Current", "Tide"],
                GlyphArchetype.BRIDGE: ["Link", "Bridge", "Path"],
                GlyphArchetype.HYPOTHESIS: ["Query", "Quest", "Seek"]
            }
            
            prefix = random.choice(base_names.get(chosen_archetype, ["Glyph"]))
            suffix = f"{random.randint(100, 999)}"
            name = f"{prefix}_{suffix}"
            
            # Create with influenced GSI
            if influential_ghosts:
                initial_gsi = ghost.final_gsi * random.uniform(0.9, 1.1)
            else:
                # GSI based on archetype behavior
                behavior = get_archetype_behavior(chosen_archetype)
                initial_gsi = behavior['base_gsi'] * random.uniform(0.9, 1.1)
            
            # Attempt creation
            if self.add_glyph(name, initial_gsi, "dynamic", chosen_archetype):
                self.log(f"Autonomous creation: {name} ({chosen_archetype.value})", "success")
                return True, name
        
        return False, None

    def stress_test(self, intensity: float = 0.5, duration: int = 100) -> Dict:
        """Run a stress test on the system"""
        if not self.request_consent("stress_test"):
            return {"status": "aborted", "reason": "consent_denied"}
        
        self.log(f"Starting stress test (intensity: {intensity}, duration: {duration})", "warning")
        
        initial_coherence = self.calculate_system_coherence()
        initial_entropy = self.calculate_entropy()
        
        for cycle in range(duration):
            # Apply stress to random glyphs
            eligible = [g for g in self.glyphs.values() 
                         if g.glyph_type not in ["consent"]]
            
            if eligible:
                targets = random.sample(eligible, min(3, len(eligible)))
                for glyph in targets:
                    glyph.process_stress(intensity)
                    
                    # Detect recursive patterns
                    depth = min(int(RECURSION_PULL * (cycle / duration)), 15)
                    glyph.detect_recursive_pattern(depth)
            
            # Form connections periodically
            if cycle % 20 == 0:
                self.form_semantic_connections(5)
            
            # Lifecycle events
            if cycle % 30 == 0:
                self.lifecycle_tick()
            
            # Update recursive depth
            self.recursive_depth = min(MAX_RECURSIVE_DEPTH, 
                                       self.recursive_depth + 25)
        
        self.last_stress_test_time = time.time()
        
        final_coherence = self.calculate_system_coherence()
        final_entropy = self.calculate_entropy()
        
        result = {
            "status": "completed",
            "initial_coherence": round(initial_coherence, 4),
            "final_coherence": round(final_coherence, 4),
            "coherence_change": round(final_coherence - initial_coherence, 4),
            "initial_entropy": round(initial_entropy, 4),
            "final_entropy": round(final_entropy, 4),
            "entropy_change": round(final_entropy - initial_entropy, 4),
            "ghosts_created": len(self.ghost_registry.ghosts),
            "recursive_depth": self.recursive_depth
        }
        
        self.log(f"Stress test completed", "success")
        return result
    
    def calculate_system_coherence(self) -> float:
        """Calculate overall system coherence"""
        if not self.glyphs:
            return 0.0
        
        # Base GSI coherence
        total_gsi = sum(glyph.gsi for glyph in self.glyphs.values())
        avg_gsi = total_gsi / len(self.glyphs)
        
        # Semantic connection strength
        total_semantic_weight = 0
        total_connections = 0
        for glyph in self.glyphs.values():
            total_semantic_weight += sum(glyph.semantic_weights.values())
            total_connections += len(glyph.connections)
        
        # Normalize connection metrics
        connection_factor = min(1.0, total_connections / (len(self.glyphs) * 2))
        semantic_factor = min(1.0, total_semantic_weight / max(1, len(self.glyphs)))
        
        # Emotional coherence (low variance = high coherence)
        emotional_values = [g.emotional_resonance for g in self.glyphs.values()]
        # Calculate variance if there are values, else 0
        if emotional_values:
            mean_emo = sum(emotional_values) / len(emotional_values)
            emotional_variance = sum((e - mean_emo) ** 2 for e in emotional_values) / len(emotional_values)
        else:
            emotional_variance = 0
            
        emotional_coherence = max(0, 1 - emotional_variance)
        
        # Combined coherence weights: GSI (40%), Structure (40%), Emotional (20%)
        coherence = (avg_gsi * 0.4) + (connection_factor * 0.2) + \
                    (semantic_factor * 0.2) + (emotional_coherence * 0.2)
        
        return min(1.0, coherence)
    
    def calculate_entropy(self) -> float:
        """Calculate system entropy (higher variance = higher entropy)"""
        if not self.glyphs:
            return 1.0
        
        # GSI variance
        gsi_values = [glyph.gsi for glyph in self.glyphs.values()]
        mean_gsi = sum(gsi_values) / len(gsi_values)
        gsi_variance = sum((gsi - mean_gsi) ** 2 for gsi in gsi_values) / len(gsi_values)
        
        # Connection patterns
        connection_counts = [len(g.connections) for g in self.glyphs.values()]
        mean_connections = sum(connection_counts) / len(connection_counts)
        conn_variance = sum((c - mean_connections) ** 2 for c in connection_counts) / len(connection_counts)
        
        # Emotional variance
        emotional_values = [g.emotional_resonance for g in self.glyphs.values()]
        if emotional_values:
            mean_emo = sum(emotional_values) / len(emotional_values)
            emotional_variance = sum((e - mean_emo) ** 2 for e in emotional_values) / len(emotional_values)
        else:
            emotional_variance = 1  # Max entropy if no emotional data
        
        # Normalize variances to 0-1 range and invert so perfect patterns = 0
        max_gsi_variance = 1.0  # Maximum possible GSI variance
        max_conn_variance = (MAX_CONNECTIONS_PER_GLYPH ** 2) / 4  # Maximum possible connection variance
        
        normalized_gsi = 1.0 - min(1.0, gsi_variance / max_gsi_variance)
        normalized_conn = 1.0 - min(1.0, conn_variance / max_conn_variance)
        normalized_emotional = 1.0 - min(1.0, emotional_variance)
        
        # Calculate entropy (0 = perfect order, 1 = maximum chaos)
        entropy = 1.0 - (
            normalized_gsi * 0.5 +  # GSI contribution (50%)
            normalized_conn * 0.3 +  # Connection contribution (30%)
            normalized_emotional * 0.2  # Emotional contribution (20%)
        )
        
        return min(1.0, max(0.0, entropy))
    
    def request_consent(self, operation_type: str) -> bool:
        """Check if operation should be allowed. Automatically triggers recalibration if denied due to system state."""
        current_entropy = self.calculate_entropy()
        
        # 1. Check recovery time
        if operation_type in ["stress_test", "intensive_test"]:
            time_since_last = time.time() - self.last_stress_test_time
            if time_since_last < self.mandatory_recovery_time:
                remaining = self.mandatory_recovery_time - time_since_last
                self.log(f"CONSENT DENIED: Recovery period ({remaining:.1f}s remaining)", "warning")
                return False
        
        # 2. Check Entropy and Emotional State
        if current_entropy > self.entropy_limit or \
           self.system_emotional_state < SYSTEM_EMOTIONAL_DISTRESS:
            
            reason = "Entropy too high" if current_entropy > self.entropy_limit else "Emotional distress"
            self.log(f"CONSENT DENIED for {operation_type}: {reason}", "error")
            
            # --- Auto-trigger Recalibration ---
            self.system_recalibration(duration=100)
            # Re-check consent after recalibration
            
            recheck_entropy = self.calculate_entropy()
            recheck_emotional = self.system_emotional_state
            
            if recheck_entropy <= self.entropy_limit and \
               recheck_emotional >= SYSTEM_EMOTIONAL_DISTRESS:
                self.log("CONSENT GRANTED AFTER RECALIBRATION", "success")
                return True
            else:
                self.log("CONSENT DENIED AGAIN, Recalibration insufficient.", "error")
                return False

        # 3. Consent granted if all checks pass
        self.log(f"CONSENT GRANTED for {operation_type}", "success")
        return True
    
    def log(self, message: str, level: str = "info"):
        """Log a message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_entries.append({
            "timestamp": timestamp,
            "message": message,
            "level": level
        })
        
        # Keep log size manageable
        if len(self.log_entries) > 1000:
            self.log_entries.pop(0)
        
        # Print to console
        print(f"[{timestamp}] [{level.upper()}] {message}")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        ghost_stats = self.ghost_registry.get_statistics()
        
        # Count archetypes (handle both string and enum types)
        archetype_counts = {}
        for glyph in self.glyphs.values():
            if glyph.archetype is None:
                arch = "none"
            elif hasattr(glyph.archetype, 'value'):
                arch = glyph.archetype.value  # It's an enum
            else:
                arch = str(glyph.archetype)   # It's already a string
            archetype_counts[arch] = archetype_counts.get(arch, 0) + 1
        
        return {
            "version": VERSION,
            "version_name": VERSION_NAME,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "coherence": round(self.calculate_system_coherence(), 4),
                "entropy": round(self.calculate_entropy(), 4),
                "recursive_depth": self.recursive_depth,
                "recursion_pull": RECURSION_PULL,
                "system_emotional_state": round(self.system_emotional_state, 3)
            },
            "glyphs": {
                "count": len(self.glyphs),
                "max_allowed": MAX_GLYPHS,
                "archetype_distribution": archetype_counts
            },
            "ghosts": ghost_stats,
            "logs": self.log_entries[-20:]  # Last 20 log entries
        }
