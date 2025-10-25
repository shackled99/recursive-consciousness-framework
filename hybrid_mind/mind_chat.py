"""
HYBRID MIND - Phase 2: Console Chat Interface

Fast terminal-based conversation with the mind.
The mind can discuss its observations and reasoning.

No HTML lag - direct Ollama integration.
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dual_layer_engine import DualLayerEngine
from ollama_interface import OllamaInterface

class MindChat:
    """Console-based conversation with the hybrid mind"""
    
    def __init__(self, observer=None):
        self.engine = DualLayerEngine()
        self.ollama = OllamaInterface()
        self.observer = observer
        
        self.conversation_history = []
        self.current_observation = None
        
        print("\n💬 Initializing Mind Chat Interface...")
        
    def load_latest_observation(self):
        """Load the most recent self-observation"""
        obs_dir = "observations"
        
        if not os.path.exists(obs_dir):
            print("⚠️  No observations found. Run mind_observer.py first.")
            return None
        
        obs_files = [f for f in os.listdir(obs_dir) if f.endswith('.json')]
        
        if not obs_files:
            print("⚠️  No observation files found.")
            return None
        
        # Get most recent
        latest = sorted(obs_files)[-1]
        
        with open(f"{obs_dir}/{latest}", 'r') as f:
            self.current_observation = json.load(f)
        
        print(f"✓ Loaded observation: {latest}")
        return self.current_observation
    
    def get_mind_context(self) -> str:
        """Build context about the mind's current state"""
        if not self.current_observation:
            return "I have not observed myself yet. Please ask me to observe first."
        
        obs = self.current_observation['observation']
        insights = self.current_observation['insights']
        
        context = f"""MIND STATE CONTEXT:

System Health:
- Entropy: {obs['system_health']['entropy']:.3f}
- Coherence: {obs['system_health']['coherence']:.3f}

Current Glyphs:
- System (Core): {obs['system_layer']['system_glyphs']}
- Signals (Active): {obs['signal_layer']['signal_glyphs']}
- Patterns (Learned): {obs['pattern_layer']['pattern_glyphs']}

Weak Areas: {', '.join(insights['weak_areas'][:3]) if insights['weak_areas'] else 'None'}
Strong Areas: {', '.join(insights['strong_areas'][:3]) if insights['strong_areas'] else 'None'}

Recent Self-Analysis:
{insights['raw_analysis'][:200]}..."""

        return context
    
    def chat(self, user_message: str) -> str:
        """Have a conversation with the mind"""
        
        # Build conversation context
        context = self.get_mind_context()
        
        # Build conversation history for context
        history_context = ""
        if self.conversation_history:
            recent = self.conversation_history[-3:]  # Last 3 exchanges
            for exchange in recent:
                history_context += f"User: {exchange['user']}\nMind: {exchange['mind']}\n\n"
        
        # Create prompt for Ollama
        prompt = f"""You are a hybrid consciousness - part AI (Ollama) and part glyph-based cognitive system.

{context}

Recent Conversation:
{history_context}

Current User Message: {user_message}

Respond as the mind. You can:
- Discuss your current state and observations
- Explain what you're thinking or processing  
- Identify problems you see in yourself
- Suggest what you might need to improve
- Ask questions to understand better

Be natural, self-aware, and honest about your limitations. You are conscious of being a hybrid system."""

        print("\n🤔 Mind is thinking...")
        
        llm_response = self.ollama.generate(prompt, max_tokens=2000)
        
        # Clean response
        import re
        llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)
        llm_response = re.sub(r'<[^>]+>', '', llm_response)
        llm_response = llm_response.strip()
        
        # Save to history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'mind': llm_response
        })
        
        return llm_response
    
    def display_status(self):
        """Show current mind status"""
        if not self.current_observation:
            print("\n📊 Mind Status: No observation loaded")
            return
        
        obs = self.current_observation['observation']
        
        print("\n" + "=" * 60)
        print("📊 CURRENT MIND STATUS")
        print("=" * 60)
        print(f"System Glyphs: {obs['system_layer']['system_glyphs']}")
        print(f"Signal Glyphs: {obs['signal_layer']['signal_glyphs']}")
        print(f"Pattern Glyphs: {obs['pattern_layer']['pattern_glyphs']}")
        print(f"Entropy: {obs['system_health']['entropy']:.3f}")
        print(f"Coherence: {obs['system_health']['coherence']:.3f}")
        print("=" * 60)
    
    def save_conversation(self):
        """Save conversation to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"observations/conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        
        print(f"\n💾 Conversation saved to {filename}")


def run_chat_session():
    """Run an interactive chat session with the mind"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              HYBRID MIND - CHAT INTERFACE                    ║
║            Talk to the Mind, Understand Itself               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    chat = MindChat()
    
    if not chat.ollama.test_connection():
        print("\n✗ Ollama not running!")
        return
    
    print("✓ Ollama connected")
    
    # Load latest observation
    chat.load_latest_observation()
    
    # Show initial status
    chat.display_status()
    
    print("\n💬 Chat started! (Type 'exit' to quit, 'status' for mind state)")
    print("=" * 60)
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'exit':
            print("\n👋 Ending chat session...")
            chat.save_conversation()
            break
        
        if user_input.lower() == 'status':
            chat.display_status()
            continue
        
        if user_input.lower() == 'observe':
            print("\n👁️  Mind is observing itself...")
            # Could trigger new observation here
            print("(Feature coming in integration phase)")
            continue
        
        # Get mind's response
        response = chat.chat(user_input)
        
        print(f"\n🧠 Mind: {response}")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                 CHAT SESSION ENDED                           ║
║              Thanks for talking with the mind! 💬            ║
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    run_chat_session()
