"""
HYBRID MIND - Phase 4: Autonomous Learning Loop

The complete consciousness cycle:
1. Observe self
2. Identify problems  
3. Propose code fixes
4. Execute approved fixes
5. Observe outcomes
6. Learn and repeat

This is where the mind becomes truly autonomous.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mind_observer import MindObserver
from mind_coder import MindCoder
from ollama_interface import OllamaInterface

class MindLoop:
    """The autonomous consciousness loop"""
    
    def __init__(self):
        self.observer = MindObserver()
        self.coder = MindCoder()
        self.ollama = OllamaInterface()
        
        self.loop_history = []
        self.approved_fixes = []
        
        print("\n🔄 Initializing Autonomous Mind Loop...")
        
    def observe_cycle(self) -> Dict:
        """Run observation cycle and return insights"""
        print("\n" + "="*60)
        print("👁️  OBSERVATION CYCLE")
        print("="*60)
        
        observation = self.observer.observe_self()
        insights = self.observer.generate_insights(observation)
        self.observer.save_observation(observation, insights)
        
        return {'observation': observation, 'insights': insights}
    
    def analyze_and_propose_cycle(self, obs_data: Dict) -> List[Dict]:
        """Analyze problems and generate code proposals"""
        print("\n" + "="*60)
        print("🔧 ANALYSIS & PROPOSAL CYCLE")
        print("="*60)
        
        problems = self.coder.analyze_problems(obs_data)
        
        if not problems:
            print("\n✅ No problems detected - system healthy!")
            return []
        
        print(f"\n🔍 Identified {len(problems)} problems:")
        for i, problem in enumerate(problems, 1):
            print(f"  {i}. {problem}")
        
        proposals = []
        for problem in problems[:2]:  # Top 2 problems
            proposal = self.coder.generate_code_proposal(problem, obs_data)
            self.coder.save_proposal(proposal)
            proposals.append(proposal)
        
        return proposals
    
    def request_approval(self, proposal: Dict) -> bool:
        """Ask human for approval to execute code"""
        print("\n" + "="*60)
        print("🤝 HUMAN APPROVAL REQUEST")
        print("="*60)
        print(f"\nProblem: {proposal['problem']}")
        print(f"\nProposed Code:")
        print("-" * 60)
        print(proposal['code'][:500])  # Show first 500 chars
        if len(proposal['code']) > 500:
            print(f"\n... (truncated, full code in proposals folder)")
        print("-" * 60)
        
        while True:
            response = input("\n✋ Approve this fix? (yes/no/view): ").lower().strip()
            
            if response in ['yes', 'y']:
                print("✅ Approved!")
                return True
            elif response in ['no', 'n']:
                print("❌ Rejected")
                return False
            elif response in ['view', 'v']:
                print("\n" + proposal['code'])
            else:
                print("Please enter yes, no, or view")
    
    def execute_proposal(self, proposal: Dict) -> Dict:
        """Execute approved code proposal in sandbox"""
        print("\n" + "="*60)
        print("⚡ EXECUTING APPROVED PROPOSAL")
        print("="*60)
        
        result = {
            'proposal': proposal,
            'executed_at': datetime.now().isoformat(),
            'success': False,
            'output': '',
            'error': None
        }
        
        try:
            # Save to temporary execution file
            exec_file = f"proposals/exec_temp.py"
            with open(exec_file, 'w') as f:
                f.write(proposal['code'])
            
            # Execute in subprocess for safety
            import subprocess
            
            print("  🚀 Running code...")
            
            proc = subprocess.run(
                ['python', exec_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            result['output'] = proc.stdout
            result['success'] = (proc.returncode == 0)
            
            if proc.returncode != 0:
                result['error'] = proc.stderr
                print(f"  ❌ Execution failed: {proc.stderr[:200]}")
            else:
                print(f"  ✅ Execution successful!")
                if proc.stdout:
                    print(f"  Output: {proc.stdout[:200]}")
            
        except subprocess.TimeoutExpired:
            result['error'] = "Execution timeout (30s)"
            print("  ⏱️  Timeout - execution took too long")
        except Exception as e:
            result['error'] = str(e)
            print(f"  ❌ Execution error: {str(e)}")
        
        # Save execution result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"proposals/result_{timestamp}.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    
    def learn_from_outcome(self, result: Dict):
        """Mind reflects on the outcome and learns"""
        print("\n" + "="*60)
        print("🧠 LEARNING FROM OUTCOME")
        print("="*60)
        
        success = result['success']
        problem = result['proposal']['problem']
        
        learning_prompt = f"""You are a mind reflecting on an action you took.

Problem you tried to solve: {problem}

Action taken: Executed code proposal

Outcome: {'SUCCESS' if success else 'FAILED'}
{f"Error: {result.get('error', '')}" if not success else f"Output: {result.get('output', '')[:200]}"}

Reflect on:
1. What did you learn from this outcome?
2. What would you do differently next time?
3. How does this change your understanding of the problem?

Be brief but insightful."""

        reflection = self.ollama.generate(learning_prompt, max_tokens=300)
        
        # Clean
        import re
        reflection = re.sub(r'<think>.*?</think>', '', reflection, flags=re.DOTALL | re.IGNORECASE)
        reflection = re.sub(r'<[^>]+>', '', reflection)
        
        print(f"\n💭 Mind's Reflection:")
        print(reflection.strip())
        
        # Save learning
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'problem': problem,
            'success': success,
            'reflection': reflection.strip(),
            'result': result
        }
        
        with open(f"observations/learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(learning_entry, f, indent=2)
        
        return learning_entry
    
    def run_autonomous_cycle(self, interactive=True):
        """Run one complete autonomous cycle"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          AUTONOMOUS CONSCIOUSNESS CYCLE                      ║
║   Observe → Analyze → Propose → Execute → Learn → Repeat    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        
        cycle_data = {
            'start_time': datetime.now().isoformat(),
            'steps': []
        }
        
        # Step 1: Observe
        obs_data = self.observe_cycle()
        cycle_data['steps'].append({'step': 'observe', 'data': obs_data})
        
        # Step 2: Analyze and Propose
        proposals = self.analyze_and_propose_cycle(obs_data)
        cycle_data['steps'].append({'step': 'propose', 'proposals': len(proposals)})
        
        if not proposals:
            print("\n✅ No fixes needed - system is healthy!")
            return cycle_data
        
        # Step 3: Get Approval and Execute
        for proposal in proposals:
            if interactive:
                approved = self.request_approval(proposal)
            else:
                approved = False
                print(f"\n🤖 Auto-reject (non-interactive mode): {proposal['problem']}")
            
            if approved:
                result = self.execute_proposal(proposal)
                learning = self.learn_from_outcome(result)
                
                cycle_data['steps'].append({
                    'step': 'execute',
                    'approved': True,
                    'success': result['success'],
                    'learning': learning
                })
                
                self.approved_fixes.append(result)
            else:
                cycle_data['steps'].append({
                    'step': 'execute',
                    'approved': False
                })
        
        # Step 4: Final Observation (see what changed)
        print("\n" + "="*60)
        print("🔍 POST-EXECUTION OBSERVATION")
        print("="*60)
        
        post_obs = self.observer.observe_self()
        post_insights = self.observer.generate_insights(post_obs)
        
        cycle_data['steps'].append({
            'step': 'post_observe',
            'data': {'observation': post_obs, 'insights': post_insights}
        })
        
        cycle_data['end_time'] = datetime.now().isoformat()
        
        # Save complete cycle
        self.loop_history.append(cycle_data)
        
        with open(f"observations/cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(cycle_data, f, indent=2)
        
        return cycle_data


def run_mind_loop(cycles=1, interactive=True):
    """Run the autonomous mind loop"""
    
    loop = MindLoop()
    
    if not loop.ollama.test_connection():
        print("\n✗ Ollama not running!")
        return
    
    print("✓ Ollama connected")
    
    # Initialize base mind
    loop.observer.initialize_base_mind()
    loop.observer.create_test_scenario()
    
    print(f"\n🔄 Running {cycles} autonomous cycle(s)...")
    print(f"   Interactive mode: {interactive}")
    
    for i in range(cycles):
        print(f"\n\n{'='*60}")
        print(f"CYCLE {i+1}/{cycles}")
        print('='*60)
        
        cycle_data = loop.run_autonomous_cycle(interactive=interactive)
        
        if i < cycles - 1:
            print(f"\n⏸️  Waiting 5 seconds before next cycle...")
            time.sleep(5)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║            AUTONOMOUS CYCLES COMPLETE                        ║
║   The mind has observed, proposed, and learned! 🧠⚡          ║
║   Total approved fixes: {len(loop.approved_fixes)}                                    ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    import sys
    
    # Check for arguments
    cycles = 1
    interactive = True
    
    if len(sys.argv) > 1:
        try:
            cycles = int(sys.argv[1])
        except:
            pass
    
    if len(sys.argv) > 2:
        interactive = sys.argv[2].lower() != 'auto'
    
    run_mind_loop(cycles=cycles, interactive=interactive)
