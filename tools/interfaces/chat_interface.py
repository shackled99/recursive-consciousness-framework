"""
Chat Interface - Interactive conversation with the Hybrid Glyphwheel System
"""

import sys
from typing import Optional

class GlyphwheelChat:
    """Interactive chat interface for the hybrid system"""
    
    def __init__(self, hybrid_mind):
        """
        Args:
            hybrid_mind: The HybridMind coordinator
        """
        self.mind = hybrid_mind
        self.running = False
        
        # Command shortcuts
        self.commands = {
            '/status': self.show_status,
            '/state': self.show_state,
            '/trends': self.show_trends,
            '/events': self.show_events,
            '/decision': self.show_last_decision,
            '/insights': self.show_insights,
            '/auto': self.toggle_autopilot,
            '/auto-verbose': self.autopilot_verbose,
            '/auto-forever': self.autopilot_forever,
            '/analyze': self.force_analysis,
            '/stress': self.stress_test,
            '/recover': self.recovery_cycle,
            '/intensive': self.intensive_stress,
            '/recalibrate': self.deep_recalibration,
            '/help': self.show_help,
            '/quit': self.quit,
            '/exit': self.quit
        }
    
    def start(self):
        """Start the interactive chat"""
        self.running = True
        
        print("=" * 60)
        print("GLYPHWHEEL HYBRID SYSTEM - CHAT INTERFACE")
        print("=" * 60)
        print("\nYou are now connected to the hybrid intelligence system.")
        print("The system combines:")
        print("  • Glyphwheel (fast computational substrate)")
        print("  • Ollama LLM (reasoning and language)")
        print(f"  • Observer (monitoring at {self.mind.observer.sample_interval}s intervals)")
        print("\nType '/help' for commands or just chat naturally.")
        print("Type '/quit' to exit.\n")
        
        # Show initial status
        print(self.mind.observer.get_summary())
        print()
        
        # Main chat loop
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.startswith('/'):
                    command = user_input.split()[0].lower()
                    if command in self.commands:
                        self.commands[command]()
                    else:
                        print(f"Unknown command: {command}")
                        print("Type '/help' for available commands")
                else:
                    # Natural conversation
                    response = self.mind.chat(user_input)
                    print(f"\nSystem: {response}\n")
            
            except KeyboardInterrupt:
                print("\n\nInterrupted. Type '/quit' to exit.\n")
            except EOFError:
                self.quit()
            except Exception as e:
                print(f"\nError: {e}\n")
    
    def show_status(self):
        """Show system status"""
        print("\n" + self.mind.status() + "\n")
    
    def show_state(self):
        """Show current system state"""
        state = self.mind.observer.get_current_state()
        print("\n=== CURRENT STATE ===")
        print(f"Glyphs: {state['glyph_count']}")
        print(f"Average GSI: {state['avg_gsi']:.3f}")
        print(f"Range: {state['min_gsi']:.3f} - {state['max_gsi']:.3f}")
        print(f"Entropy: {state['entropy']:.3f}")
        print(f"Coherence: {state['coherence']:.3f}")
        print(f"Connections: {state['connection_count']} ({state['avg_connections_per_glyph']:.1f} per glyph)")
        print(f"Weak glyphs: {len(state['weak_glyphs'])}")
        print(f"Strong glyphs: {len(state['strong_glyphs'])}")
        print()
    
    def show_trends(self):
        """Show system trends"""
        trends = self.mind.observer.get_trends()
        if trends.get('status') == 'insufficient_data':
            print("\nNot enough data for trend analysis yet.\n")
            return
        
        print("\n=== SYSTEM TRENDS ===")
        for metric, data in trends.items():
            if isinstance(data, dict):
                trend_arrow = "↑" if data['trend'] > 0.01 else "↓" if data['trend'] < -0.01 else "→"
                print(f"{metric.upper()}: {data['current']:.3f} {trend_arrow} (avg: {data['avg']:.3f})")
        print()
    
    def show_events(self):
        """Show recent significant events"""
        events = self.mind.observer.get_recent_events(10)
        if not events:
            print("\nNo significant events recorded yet.\n")
            return
        
        print("\n=== RECENT EVENTS ===")
        for event in events[-5:]:  # Show last 5
            print(f"[{event['timestamp'][-12:-4]}] {event['type']}: {event['description']}")
        print()
    
    def show_last_decision(self):
        """Show the last decision made"""
        print("\n" + self.mind.explain_last_decision() + "\n")
    
    def show_insights(self):
        """Get AI insights about system behavior"""
        print("\nGenerating insights...\n")
        insights = self.mind.get_insights()
        print(f"System: {insights}\n")
    
    def toggle_autopilot(self):
        """Toggle autonomous decision-making (quiet mode)"""
        if self.mind.auto_pilot:
            self.mind.auto_pilot = False
            print("\nAuto-pilot DISABLED\n")
        else:
            self.mind.autonomous_loop(duration=60, quiet=True)
    
    def autopilot_verbose(self):
        """Run autonomous mode with full output"""
        if self.mind.auto_pilot:
            self.mind.auto_pilot = False
            print("\nAuto-pilot DISABLED\n")
        else:
            self.mind.autonomous_loop(duration=60, quiet=False)
    
    def autopilot_forever(self):
        """Run autonomous mode forever (until Ctrl+C)"""
        if self.mind.auto_pilot:
            self.mind.auto_pilot = False
            print("\nAuto-pilot DISABLED\n")
        else:
            print("\n🔄 Starting INFINITE autonomous mode!")
            print("   The system will run until you press Ctrl+C\n")
            self.mind.autonomous_loop(duration=0, quiet=True)
    
    def force_analysis(self):
        """Force an immediate analysis and decision"""
        print("\nAnalyzing system state...\n")
        decision = self.mind.analyze_and_decide()
        print(f"Analysis: {decision['analysis']}")
        print(f"Action: {decision['action']}")
        print(f"Result: {decision['execution_result'].get('result', 'N/A')}\n")
    
    def stress_test(self):
        """Run optimization stress test"""
        print("\nRunning optimization stress test...\n")
        result = self.mind.glyphwheel.optimization_stress_test(0.7, 150)
        print(f"Status: {result['status']}")
        print(f"Test Type: {result['test_type']}")
        print(f"Coherence Change: {result['final_state']['coherence_change']:.3f}")
        print(f"Connections Added: {result['final_state']['connections_added']}")
        print(f"Antifragile Behavior: {result['antifragile_behavior']}")
        print(f"Effectiveness: {result['optimization_effectiveness']}\n")
    
    def intensive_stress(self):
        """Run intensive stress test"""
        print("\nRunning INTENSIVE stress test...\n")
        result = self.mind.glyphwheel.intensive_stress_test(0.8, 200)
        print(f"Status: {result['status']}")
        print(f"Test Type: {result['test_type']}")
        print(f"Coherence Change: {result['final_state']['coherence_change']:.3f}")
        print(f"Connections Added: {result['final_state']['connections_added']}")
        print(f"Antifragile Behavior: {result['antifragile_behavior']}")
        print(f"Intensity Effectiveness: {result['intensity_effectiveness']}\n")
    
    def recovery_cycle(self):
        """Run recovery cycle"""
        print("\nRunning recovery cycle...\n")
        result = self.mind.glyphwheel.mandatory_recovery_cycle(60)
        print(f"Coherence: {result['final_state']['coherence']:.3f}")
        print(f"Entropy: {result['final_state']['entropy']:.3f}")
        print(f"Recovery Effectiveness: {result['final_state']['recovery_effectiveness']}\n")
    
    def deep_recalibration(self):
        """Run deep recalibration to reset ConsentGlyph to 1.0"""
        print("\nRunning deep recalibration...\n")
        # Import the function from glyphwheel_optimized
        from glyphwheel_optimized import deep_recalibration
        system_state = self.mind.glyphwheel.get_system_status()
        result = deep_recalibration(system_state)
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        if result['consent_gsi_restored']:
            print(f"ConsentGlyph: {result['old_gsi']:.3f} → {result['new_gsi']:.3f}")
            print(f"Coherence: {result['system_coherence']:.3f}")
            print(f"Entropy: {result['system_entropy']:.3f}")
        print()
    
    def show_help(self):
        """Show help message"""
        print("""
=== GLYPHWHEEL CHAT COMMANDS ===

System Status:
  /status      - Full system status report
  /state       - Current system state snapshot
  /trends      - Recent trends in system metrics
  /events      - Recent significant events

AI Reasoning:
  /decision    - Show last decision made
  /insights    - Get AI insights about system behavior
  /analyze     - Force immediate analysis and decision

Manual Actions:
  /stress      - Run optimization stress test (0.7 intensity, 150 cycles)
  /intensive   - Run intensive stress test (0.8 intensity, 200 cycles)
  /recover     - Run recovery cycle (60 iterations)
  /recalibrate - Deep recalibration (reset ConsentGlyph to 1.0)

Control:
  /auto          - Run 60s autonomous mode (quiet - just dots)
  /auto-verbose  - Run 60s autonomous mode (full output)
  /auto-forever  - Run INFINITE autonomous mode (until Ctrl+C)
  /help          - Show this help message
  /quit, /exit   - Exit chat interface

Note: Press Ctrl+C during /auto to stop early!

Natural Chat:
  Just type normally to have a conversation with the system.
  Ask questions like:
    - "What are you experiencing right now?"
    - "Why did you spawn those glyphs?"
    - "Can you explain the connection pattern?"
    - "What should I focus on?"
""")
    
    def quit(self):
        """Exit the chat"""
        print("\nShutting down chat interface...")
        self.running = False
        print("Goodbye!\n")


def start_chat(glyphwheel_engine, ollama_interface, system_observer):
    """
    Convenience function to start chat with all components
    
    Args:
        glyphwheel_engine: The Glyphwheel engine
        ollama_interface: The Ollama interface
        system_observer: The system observer
    """
    from hybrid_mind import HybridMind
    
    # Create hybrid mind
    mind = HybridMind(glyphwheel_engine, ollama_interface, system_observer)
    
    # Start observer
    if not system_observer.running:
        system_observer.start()
    
    # Create and start chat
    chat = GlyphwheelChat(mind)
    chat.start()


# Example usage
if __name__ == "__main__":
    print("""
Chat Interface Module

To use:
    from chat_interface import start_chat
    start_chat(glyphwheel_engine, ollama_interface, system_observer)

Or:
    from chat_interface import GlyphwheelChat
    from hybrid_mind import HybridMind
    
    mind = HybridMind(engine, ollama, observer)
    chat = GlyphwheelChat(mind)
    chat.start()
""")
