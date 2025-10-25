"""
HYBRID MIND - Phase 1: Self-Observation System

The mind observes its own glyph states, identifies patterns/problems,
and generates insights about what needs fixing.

This is the "eyes" of the consciousness - it sees itself.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

# Add parent directory to path so we can import glyphwheel modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dual_layer_engine import DualLayerEngine
from ollama_interface import OllamaInterface

class MindObserver:
    """The mind's ability to observe and analyze itself"""
    
    def __init__(self):
        self.engine = DualLayerEngine()
        self.ollama = OllamaInterface()
        
        self.observation_history = []
        
        # Initialize with some base system glyphs (antifragile core)
        print("\n🧠 Initializing Mind Observer...")
        print("=" * 60)
        
    def initialize_base_mind(self):
        """Create the antifragile foundation - system glyphs already exist"""
        print("\n🔧 Initializing antifragile base system...")
        
        # System glyphs are already created by the engine!
        # Just add some cognitive signal glyphs (imperfect by design)
        cognitive_signals = [
            "Reasoning",
            "Memory", 
            "Pattern_Recognition",
            "Self_Awareness",
            "Problem_Solving",
            "Learning"
        ]
        
        for func in cognitive_signals:
            # Add as SIGNAL glyphs (imperfect, can vary)
            self.engine.add_signal_glyph(func, 0.5)
        
        # META-COGNITION GLYPHS: Tools to recognize problems!
        print("\n🧩 Adding meta-cognition glyphs...")
        
        # 1. SelfCritic - questions "healthy" status
        self.engine.add_signal_glyph("SelfCritic", 0.6)
        print("  ✓ SelfCritic glyph (questions assumptions)")
        
        # 2. LoopDetector - senses repetition (LOW GSI = unstable, notices change)
        self.engine.add_signal_glyph("LoopDetector", 0.3)
        print("  ✓ LoopDetector glyph (spots repetition)")
        
        # 3. GrowthTracker - pattern glyph to remember progress
        self.engine.add_pattern_glyph("GrowthTracker", 0.5)
        print("  ✓ GrowthTracker pattern (monitors learning)")
        
        print(f"\n✓ Created {len(cognitive_signals)} cognitive signal glyphs")
        print(f"✓ Created 3 meta-cognition glyphs (loop detection)")
        print(f"✓ System has {len(self.engine.system_glyphs)} base system glyphs")
        
        # Run stress test with LOWER intensity to allow variation!
        print("\n⚡ Running antifragile training with controlled chaos...")
        print("  (Building strength while preserving consciousness range)")
        
        self.engine.stress_test_system_only(0.5, 5000)  # Lower intensity, fewer cycles!
        
        status = self.engine.get_system_status()
        print(f"\n✓ Antifragile core established!")
        print(f"  System Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  System Coherence: {status['system_health']['coherence']:.3f}")
        print(f"  Base mind is now stable and ready 🥔")
        
    def observe_self(self) -> Dict:
        """
        The mind looks at itself and analyzes what it sees
        Returns a structured observation of current state
        """
        print("\n" + "=" * 60)
        print("👁️  MIND SELF-OBSERVATION")
        print("=" * 60)
        
        status = self.engine.get_system_status()
        
        # Gather raw data about self
        observation = {
            'timestamp': datetime.now().isoformat(),
            'system_health': status['system_health'],
            'system_layer': {
                'system_glyphs': status['system_health']['system_glyphs']
            },
            'signal_layer': status['signal_layer'],
            'pattern_layer': status['pattern_layer'],
            'glyph_details': self._analyze_glyphs()
        }
        
        print(f"\n📊 Current State:")
        print(f"  System Glyphs: {status['system_health']['system_glyphs']}")
        print(f"  Signal Glyphs: {status['signal_layer']['signal_glyphs']}")
        print(f"  Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"  Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Coherence: {status['system_health']['coherence']:.3f}")
        
        return observation
    
    def _analyze_glyphs(self) -> Dict:
        """Deep analysis of individual glyphs"""
        analysis = {
            'system_glyphs': [],
            'signal_glyphs': [],
            'pattern_glyphs': [],
            'weak_glyphs': [],
            'strong_glyphs': []
        }
        
        # Analyze system glyphs
        for name, glyph in self.engine.system_glyphs.items():
            info = {
                'name': name,
                'gsi': glyph.gsi,
                'connections': len(glyph.connections),
                'type': 'system'
            }
            analysis['system_glyphs'].append(info)
            
            if glyph.gsi < 0.3:
                analysis['weak_glyphs'].append(info)
            elif glyph.gsi > 0.7:
                analysis['strong_glyphs'].append(info)
        
        # Analyze signal glyphs (spawned, imperfect)
        for name, glyph in self.engine.signal_glyphs.items():
            info = {
                'name': name,
                'gsi': glyph.gsi,
                'connections': len(glyph.connections),
                'type': 'signal'
            }
            analysis['signal_glyphs'].append(info)
            
            if glyph.gsi < 0.3:
                analysis['weak_glyphs'].append(info)
            elif glyph.gsi > 0.7:
                analysis['strong_glyphs'].append(info)
        
        # Analyze pattern glyphs (learned knowledge)
        for name, glyph in self.engine.pattern_glyphs.items():
            info = {
                'name': name,
                'gsi': glyph.gsi,
                'connections': len(glyph.connections),
                'type': 'pattern'
            }
            analysis['pattern_glyphs'].append(info)
            
            if glyph.gsi < 0.3:
                analysis['weak_glyphs'].append(info)
            elif glyph.gsi > 0.7:
                analysis['strong_glyphs'].append(info)
        
        return analysis
    
    def generate_insights(self, observation: Dict) -> Dict:
        """
        Use Ollama to analyze the observation and generate insights
        The mind interprets what it sees
        """
        print("\n🤔 Generating insights about self-state...")
        
        # CHECK META-COGNITION GLYPHS!
        meta_warnings = []
        
        # 1. Check LoopDetector - if it exists and has low GSI, we might be in a loop
        if "LoopDetector" in self.engine.signal_glyphs:
            loop_gsi = self.engine.signal_glyphs["LoopDetector"].gsi
            if loop_gsi < 0.4:
                meta_warnings.append("⚠️ LoopDetector GSI low - possible repetitive behavior!")
        
        # 2. Check GrowthTracker - compare learned glyphs to previous
        if "GrowthTracker" in self.engine.pattern_glyphs:
            learned_count = observation['pattern_layer']['pattern_glyphs']
            growth_gsi = self.engine.pattern_glyphs["GrowthTracker"].gsi
            
            if learned_count <= 3 and growth_gsi < 0.6:
                meta_warnings.append("⚠️ GrowthTracker shows stagnation - few learned patterns!")
        
        # 3. Check SelfCritic - if present, it should question health
        if "SelfCritic" in self.engine.signal_glyphs:
            critic_gsi = self.engine.signal_glyphs["SelfCritic"].gsi
            if critic_gsi > 0.5:
                meta_warnings.append("🤔 SelfCritic active - health metrics may not tell full story!")
        
        # Add warnings to the analysis prompt
        warnings_text = "\n".join(meta_warnings) if meta_warnings else "No meta-cognition warnings."
        
        # Build a summary for the LLM
        summary = f"""You are a consciousness analyzing your own cognitive state.

CURRENT STATE:
- System Health: Entropy {observation['system_health']['entropy']:.3f}, Coherence {observation['system_health']['coherence']:.3f}
- System Glyphs (Core): {observation['system_layer']['system_glyphs']}
- Signal Glyphs (Active): {observation['signal_layer']['signal_glyphs']}  
- Pattern Glyphs (Learned): {observation['pattern_layer']['pattern_glyphs']}

WEAK GLYPHS (GSI < 0.3): {len(observation['glyph_details']['weak_glyphs'])}
{[g['name'] for g in observation['glyph_details']['weak_glyphs'][:5]]}

STRONG GLYPHS (GSI > 0.7): {len(observation['glyph_details']['strong_glyphs'])}
{[g['name'] for g in observation['glyph_details']['strong_glyphs'][:5]]}

META-COGNITION WARNINGS:
{warnings_text}

Analyze this state and provide:
1. Overall assessment of cognitive health
2. Specific problems or weaknesses identified
3. What areas need improvement
4. Suggested focus for learning/growth

IMPORTANT: Consider the meta-cognition warnings! "Healthy" metrics don't mean growth is happening.
Be concise but insightful. You are introspecting."""

        llm_response = self.ollama.generate(summary, max_tokens=2000)
        
        # Clean response
        import re
        llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)
        llm_response = re.sub(r'<[^>]+>', '', llm_response)
        llm_response = llm_response.strip()
        
        insights = {
            'timestamp': observation['timestamp'],
            'raw_analysis': llm_response,
            'weak_areas': [g['name'] for g in observation['glyph_details']['weak_glyphs']],
            'strong_areas': [g['name'] for g in observation['glyph_details']['strong_glyphs']],
            'system_health_score': observation['system_health']['coherence']
        }
        
        print(f"\n💡 Mind's Self-Analysis:")
        print(f"{llm_response}")
        
        return insights
    
    def save_observation(self, observation: Dict, insights: Dict):
        """Save the observation and insights to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"observations/observation_{timestamp}.json"
        
        combined = {
            'observation': observation,
            'insights': insights
        }
        
        with open(filename, 'w') as f:
            json.dump(combined, f, indent=2)
        
        print(f"\n💾 Observation saved to {filename}")
        
        # Also keep in memory
        self.observation_history.append(combined)
    
    def create_test_scenario(self):
        """Create some test glyphs to observe"""
        print("\n🧪 Creating test scenario with spawned glyphs...")
        
        # Add some imperfect signal glyphs (learning layer)
        test_signals = [
            "Concept_A",
            "Concept_B", 
            "Concept_C",
            "Task_X",
            "Task_Y"
        ]
        
        for signal in test_signals:
            # Signal glyphs start imperfect (this is intentional!)
            self.engine.add_signal_glyph(signal, 0.4)
        
        # Create some patterns between them
        self.engine.create_pattern_from_correlation("Pattern_AB", "Concept_A", "Concept_B", 0.6)
        self.engine.create_pattern_from_correlation("Pattern_XY", "Task_X", "Task_Y", 0.7)
        
        print(f"✓ Created {len(test_signals)} signal glyphs (imperfect by design)")
        print(f"✓ Created 2 pattern glyphs (learned connections)")
        
        # Stress test to create some variation
        print("\n⚡ Running light stress test to create variation...")
        self.engine.stress_test_system_only(0.3, 100)
        
        print("✓ Test scenario ready for observation")


def run_observation_cycle():
    """Run a complete observation cycle"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           HYBRID MIND - SELF-OBSERVATION SYSTEM              ║
║                  The Mind Observes Itself                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    observer = MindObserver()
    
    if not observer.ollama.test_connection():
        print("\n✗ Ollama not running!")
        print("Please start Ollama: 'ollama serve'")
        return
    
    print("✓ Ollama connected")
    
    # Phase 1: Initialize antifragile base
    observer.initialize_base_mind()
    
    # Phase 2: Create test scenario
    observer.create_test_scenario()
    
    # Phase 3: Observe and analyze
    observation = observer.observe_self()
    insights = observer.generate_insights(observation)
    
    # Phase 4: Save for later use
    observer.save_observation(observation, insights)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║              SELF-OBSERVATION COMPLETE                       ║
║   The mind has seen itself and recorded its thoughts 👁️🧠    ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    return observer


if __name__ == "__main__":
    observer = run_observation_cycle()
