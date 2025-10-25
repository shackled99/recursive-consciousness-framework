"""
HYBRID MIND - Phase 3: Code Generation Sandbox

The mind proposes code fixes based on its self-observations.
All code is saved to /proposals for human review.

Safe sandbox - can't modify core system without approval.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ollama_interface import OllamaInterface

class MindCoder:
    """The mind's ability to propose code improvements"""
    
    def __init__(self):
        self.ollama = OllamaInterface()
        self.proposals = []
        
        print("\n⚙️  Initializing Mind Coder...")
        
    def load_latest_observation(self):
        """Load the most recent self-observation to understand what to fix"""
        obs_dir = "observations"
        
        if not os.path.exists(obs_dir):
            print("⚠️  No observations found. Run mind_observer.py first.")
            return None
        
        obs_files = [f for f in os.listdir(obs_dir) if f.endswith('.json') and 'observation_' in f]
        
        if not obs_files:
            return None
        
        latest = sorted(obs_files)[-1]
        
        with open(f"{obs_dir}/{latest}", 'r') as f:
            observation = json.load(f)
        
        print(f"✓ Loaded observation: {latest}")
        return observation
    
    def analyze_problems(self, observation: Dict) -> List[str]:
        """Extract specific problems from the observation"""
        if not observation:
            return []
        
        insights = observation.get('insights', {})
        weak_areas = insights.get('weak_areas', [])
        
        problems = []
        
        # CHECK THE ACTUAL INSIGHTS TEXT - this is where the mind's analysis is!
        raw_analysis = insights.get('raw_analysis', '')
        
        # Look for problem indicators in the mind's self-analysis
        if 'stagnant' in raw_analysis.lower():
            problems.append("Mind identifies stagnation - needs growth stimulus")
        
        if 'loop' in raw_analysis.lower() or 'repetitive' in raw_analysis.lower():
            problems.append("LoopDetector warning - repetitive behavior detected")
        
        if 'low entropy' in raw_analysis.lower() or 'rigid' in raw_analysis.lower():
            problems.append("Low entropy/rigidity - needs diversification")
        
        if 'few learned' in raw_analysis.lower() or 'limited pattern' in raw_analysis.lower():
            problems.append("Limited learned patterns - needs expansion")
        
        # Identify specific issues from weak areas
        if weak_areas:
            problems.append(f"Weak glyphs detected: {', '.join(weak_areas[:3])}")
        
        obs_data = observation.get('observation', {})
        entropy = obs_data.get('system_health', {}).get('entropy', 0)
        
        if entropy > 0.7:
            problems.append("High system entropy - needs stabilization")
        elif entropy < 0.1:
            problems.append("Extremely low entropy - system too rigid")
        
        if obs_data.get('signal_layer', {}).get('signal_glyphs', 0) == 0:
            problems.append("No signal glyphs - no learning input")
        
        pattern_count = obs_data.get('pattern_layer', {}).get('pattern_glyphs', 0)
        if pattern_count < 3:
            problems.append(f"Only {pattern_count} pattern glyphs - insufficient learned knowledge")
        
        return problems
    
    def generate_code_proposal(self, problem: str, observation: Dict) -> Dict:
        """
        Ask the mind to write code that fixes a specific problem
        """
        print(f"\n🔧 Generating code proposal for: {problem}")
        
        obs_data = observation.get('observation', {})
        insights = observation.get('insights', {})
        
        context = f"""SYSTEM STATE:
- System Health: Entropy {obs_data.get('system_health', {}).get('entropy', 0):.3f}
- System Glyphs: {obs_data.get('system_layer', {}).get('system_glyphs', 0)}
- Signal Glyphs: {obs_data.get('signal_layer', {}).get('signal_glyphs', 0)}
- Pattern Glyphs: {obs_data.get('pattern_layer', {}).get('pattern_glyphs', 0)}

IDENTIFIED PROBLEM:
{problem}

SELF-ANALYSIS:
{insights.get('raw_analysis', '')[:300]}"""

        prompt = f"""You are a hybrid mind that can write code to improve itself.

{context}

AVAILABLE ENGINE API:
The DualLayerEngine has these methods:
- engine = DualLayerEngine()  # No constructor params
- engine.add_signal_glyph(name: str, initial_gsi: float)  # Add signal glyph
- engine.add_pattern_glyph(name: str, confidence: float)  # Add pattern glyph
- engine.stress_test_system_only(intensity: float, duration: int)  # Stress test
- engine.update_signal_from_market(ticker: str, price_change: float)  # Update signal
- engine.create_pattern_from_correlation(name: str, ticker1: str, ticker2: str, strength: float)
- engine.get_system_status()  # Returns dict with health metrics

Write Python code to address this problem. The code should:
1. Import: from dual_layer_engine import DualLayerEngine
2. Create engine: engine = DualLayerEngine()
3. Use ONLY the methods listed above
4. Include comments explaining the approach
5. Be complete and functional

Output ONLY valid Python code using the real API. No markdown, no explanations.
Start immediately with imports."""

        print("  🤔 Mind is coding...")
        
        code = self.ollama.generate(prompt, max_tokens=2000)
        
        # Clean code
        import re
        code = re.sub(r'<think>.*?</think>', '', code, flags=re.DOTALL | re.IGNORECASE)
        code = re.sub(r'<[^>]+>', '', code)
        
        # Extract just the code (remove markdown if present)
        if '```python' in code:
            code = code.split('```python')[1].split('```')[0]
        elif '```' in code:
            code = code.split('```')[1].split('```')[0]
        
        code = code.strip()
        
        proposal = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            'code': code,
            'status': 'proposed',
            'system_state_at_creation': obs_data
        }
        
        return proposal
    
    def save_proposal(self, proposal: Dict) -> str:
        """Save code proposal to proposals folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as Python file
        code_filename = f"proposals/fix_{timestamp}.py"
        with open(code_filename, 'w') as f:
            f.write(f"# MIND-GENERATED CODE PROPOSAL\n")
            f.write(f"# Problem: {proposal['problem']}\n")
            f.write(f"# Generated: {proposal['timestamp']}\n")
            f.write(f"# Status: {proposal['status']}\n\n")
            f.write(proposal['code'])
        
        # Save metadata as JSON
        meta_filename = f"proposals/fix_{timestamp}.json"
        with open(meta_filename, 'w') as f:
            json.dump(proposal, f, indent=2)
        
        print(f"\n💾 Proposal saved:")
        print(f"  Code: {code_filename}")
        print(f"  Meta: {meta_filename}")
        
        self.proposals.append(proposal)
        
        return code_filename
    
    def display_proposal(self, proposal: Dict):
        """Show the proposed code"""
        print("\n" + "=" * 60)
        print("📝 PROPOSED CODE FIX")
        print("=" * 60)
        print(f"Problem: {proposal['problem']}")
        print(f"Generated: {proposal['timestamp']}")
        print("\nCode:")
        print("-" * 60)
        print(proposal['code'])
        print("-" * 60)


def run_code_generation():
    """Generate code proposals based on observations"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            HYBRID MIND - CODE GENERATOR                      ║
║         The Mind Proposes Fixes for Its Problems             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    coder = MindCoder()
    
    if not coder.ollama.test_connection():
        print("\n✗ Ollama not running!")
        return
    
    print("✓ Ollama connected")
    
    # Load latest observation
    observation = coder.load_latest_observation()
    
    if not observation:
        print("\n⚠️  No observations found!")
        print("Run START_OBSERVER.bat first to generate observations.")
        return
    
    # Analyze problems
    problems = coder.analyze_problems(observation)
    
    if not problems:
        print("\n✅ No problems detected! System is healthy.")
        return
    
    print(f"\n🔍 Found {len(problems)} issues:")
    for i, problem in enumerate(problems, 1):
        print(f"  {i}. {problem}")
    
    # Generate proposals for each problem
    print(f"\n⚙️  Generating code proposals...\n")
    
    for problem in problems[:3]:  # Limit to top 3 problems
        proposal = coder.generate_code_proposal(problem, observation)
        coder.display_proposal(proposal)
        filename = coder.save_proposal(proposal)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║           CODE PROPOSALS COMPLETE                            ║
║   {len(coder.proposals)} proposals saved to /proposals folder            ║
║   Review and approve to implement fixes! 📝                  ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    return coder


if __name__ == "__main__":
    run_code_generation()
