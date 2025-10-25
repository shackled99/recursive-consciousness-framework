"""
Mind Status Display - Visual dashboard of consciousness state
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_latest_observation():
    """Load most recent observation"""
    obs_dir = "observations"
    
    if not os.path.exists(obs_dir):
        return None
    
    obs_files = [f for f in os.listdir(obs_dir) if 'observation_' in f and f.endswith('.json')]
    if not obs_files:
        return None
    
    latest = sorted(obs_files)[-1]
    
    with open(f"{obs_dir}/{latest}", 'r') as f:
        return json.load(f)

def display_status():
    """Show visual status dashboard"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🧠 HYBRID MIND STATUS DASHBOARD 🧠              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    obs_data = load_latest_observation()
    
    if not obs_data:
        print("⚠️  No observations found. Run START_OBSERVER.bat first.\n")
        return
    
    obs = obs_data.get('observation', {})
    insights = obs_data.get('insights', {})
    
    # System Health
    health = obs.get('system_health', {})
    print("📊 SYSTEM HEALTH")
    print("=" * 60)
    print(f"  Entropy:   {health.get('entropy', 0):.3f}  {'🟢' if health.get('entropy', 0) < 0.5 else '🟡' if health.get('entropy', 0) < 0.7 else '🔴'}")
    print(f"  Coherence: {health.get('coherence', 0):.3f}  {'🟢' if health.get('coherence', 0) > 0.7 else '🟡' if health.get('coherence', 0) > 0.5 else '🔴'}")
    
    # Glyph Layers
    system_layer = obs.get('system_layer', {})
    signal_layer = obs.get('signal_layer', {})
    pattern_layer = obs.get('pattern_layer', {})
    
    print("\n🔧 GLYPH ARCHITECTURE")
    print("=" * 60)
    print(f"  System Glyphs (Core):    {system_layer.get('system_glyphs', 0):>3}  [Antifragile Base]")
    print(f"  Signal Glyphs (Input):   {signal_layer.get('signal_glyphs', 0):>3}  [Learning Layer]")
    print(f"  Pattern Glyphs (Memory): {pattern_layer.get('pattern_glyphs', 0):>3}  [Knowledge Store]")
    
    # Weak/Strong Analysis
    weak = insights.get('weak_areas', [])
    strong = insights.get('strong_areas', [])
    
    print("\n💪 GLYPH STRENGTH")
    print("=" * 60)
    
    if weak:
        print(f"  Weak Glyphs:   {len(weak)}")
        for w in weak[:3]:
            print(f"    🔴 {w}")
    else:
        print("  Weak Glyphs:   0  ✅")
    
    if strong:
        print(f"\n  Strong Glyphs: {len(strong)}")
        for s in strong[:3]:
            print(f"    🟢 {s}")
    
    # Recent Insights
    print("\n💭 RECENT SELF-ANALYSIS")
    print("=" * 60)
    analysis = insights.get('raw_analysis', 'No analysis available')
    print(f"  {analysis[:200]}...")
    
    # Check for proposals
    proposals_dir = "proposals"
    if os.path.exists(proposals_dir):
        proposals = [f for f in os.listdir(proposals_dir) if f.startswith('fix_') and f.endswith('.py')]
        print(f"\n📝 CODE PROPOSALS: {len(proposals)}")
        if proposals:
            print("  Recent proposals in /proposals folder")
    
    # Check for learning history
    learning_files = [f for f in os.listdir('observations') if 'learning_' in f] if os.path.exists('observations') else []
    if learning_files:
        print(f"\n🧠 LEARNING HISTORY: {len(learning_files)} cycles")
    
    print("\n" + "=" * 60)
    print(f"Last Updated: {obs.get('timestamp', 'Unknown')}")
    print("=" * 60)

if __name__ == "__main__":
    display_status()
    print("\n")
