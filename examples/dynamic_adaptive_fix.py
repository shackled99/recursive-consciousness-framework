from dual_layer_engine import DualLayerEngine
from mind_bridge import MindBridge
import random

# --- 1. Load Confidence and Calculate Uncertainty Metric (The Awareness) ---

def calculate_memory_confidence(bridge):
    """Retrieves system confidence from Mind Bridge."""
    state = bridge.get_shared_state()
    glyph_state = state.get('glyphwheel_state', {})
    coherence = glyph_state.get('coherence', 0.85)
    return coherence

# Falsely flag a loop when uncertainty is high, simulating the Lexicon's protocol
def check_for_semantic_loop(uncertainty, entropy):
    """Simulates the FALSE SPIRAL DETECTION protocol."""
    # High uncertainty (>0.6) AND low entropy (<0.1) = SEMANTIC LOOP!
    if uncertainty > 0.6 and entropy < 0.1:
        return True  # Flag a Semantic Loop
    return False

# Initialize systems
engine = DualLayerEngine()
bridge = MindBridge()

# Get current state
glyph_state = bridge.glyphwheel_speaks(engine)
coder_confidence = glyph_state['coherence']

# Uncertainty is the metric used to set the resistance to pattern creation (The Flow)
system_uncertainty = 1.0 - coder_confidence
system_uncertainty = round(system_uncertainty, 3) 

print("=" * 60)
print("DYNAMIC ADAPTIVE FIX - Spiral Transformation")
print("=" * 60)
print(f"\nSystem Coherence: {coder_confidence:.3f}")
print(f"System Uncertainty: {system_uncertainty:.3f}")
print(f"System Entropy: {glyph_state['entropy']:.3f}")

# --- 2. Dynamic Adaptive Fix (Channeling the Pull/Flow) ---

# A) Integrate Uncertainty Signal (The Channel/Awareness)
print(f"\nACTION: Integrating Uncertainty Signal for awareness. GSI: {coder_confidence:.3f}")
engine.add_signal_glyph("Uncertainty_Layer", coder_confidence)

# B) Core Diversification Integration (Signal Space)
print("ACTION: Adding 3 new Signals to diversify input space.")
engine.add_signal_glyph("SignalX", 0.85)
engine.add_signal_glyph("SignalY", 0.72)
engine.add_signal_glyph("SignalZ", 0.68)

# C) Pattern Flow Integration with FALSE SPIRAL DETECTION
# Determine if we need to 'Burn the Loop'
ADJUSTMENT_FACTOR = 0.07  # Base resistance to flow

if check_for_semantic_loop(system_uncertainty, glyph_state['entropy']):
    # If a Semantic Loop is flagged, dramatically increase the adjustment factor
    # This lowers the required pattern confidence, forcing a mutation/spiral
    ADJUSTMENT_FACTOR += 0.05  # Aggressively widen the channel for flow
    print("\n🔥 MIND: FALSE SPIRAL DETECTED. Aggressively widening channel for mutation.")
    print(f"   Adjustment factor doubled: {ADJUSTMENT_FACTOR:.2f}")

# Calculate dynamic confidence thresholds for flow: higher uncertainty = lower required confidence
BASE_CONFIDENCE = 0.80
DYNAMIC_THRESHOLD_1 = round(max(0.50, BASE_CONFIDENCE - (system_uncertainty * ADJUSTMENT_FACTOR)), 2)
DYNAMIC_THRESHOLD_2 = round(max(0.50, BASE_CONFIDENCE - (system_uncertainty * (ADJUSTMENT_FACTOR + 0.02))), 2)
DYNAMIC_THRESHOLD_3 = round(max(0.50, BASE_CONFIDENCE - (system_uncertainty * (ADJUSTMENT_FACTOR + 0.04))), 2)
DYNAMIC_THRESHOLD_4 = round(max(0.50, BASE_CONFIDENCE - (system_uncertainty * (ADJUSTMENT_FACTOR + 0.06))), 2)
DYNAMIC_THRESHOLD_5 = round(max(0.50, BASE_CONFIDENCE - (system_uncertainty * (ADJUSTMENT_FACTOR + 0.08))), 2)

print(f"\nACTION: Creating 5 new Patterns with dynamic thresholds (Flow):")
print(f"  Thresholds: {DYNAMIC_THRESHOLD_1} → {DYNAMIC_THRESHOLD_5}")

# 1. Add generic pattern glyphs 
engine.add_pattern_glyph("Pattern_4", DYNAMIC_THRESHOLD_1)
engine.add_pattern_glyph("Pattern_5", DYNAMIC_THRESHOLD_2)
engine.add_pattern_glyph("Pattern_6", DYNAMIC_THRESHOLD_3)

# 2. Create cross-ticker correlation patterns 
engine.create_pattern_from_correlation("Correlation_Pattern_1", "AAPL", "MSFT", DYNAMIC_THRESHOLD_4)
engine.create_pattern_from_correlation("Correlation_Pattern_2", "GOOGL", "AMZN", DYNAMIC_THRESHOLD_5)
engine.create_pattern_from_correlation("Correlation_Pattern_3", "TSLA", "NVDA", DYNAMIC_THRESHOLD_5)

# D) Modulated Stress Test (The Flow Regulation)
STRESS_INTENSITY = max(0.2, system_uncertainty * 2.5)
STRESS_INTENSITY = round(STRESS_INTENSITY, 2)

print(f"\nACTION: Applying dynamic stress (The Current). Intensity: {STRESS_INTENSITY}")
engine.stress_test_system_only(STRESS_INTENSITY, 10)

# E) Finalization
engine.update_signal_from_market("DIVERSIFICATION_INDEX", 0.05)
engine.update_signal_from_market("AAPL", 0.05)
engine.update_signal_from_market("MSFT", -0.03)

# --- 3. Final System Check ---
status = engine.get_system_status()
print("\n" + "=" * 60)
print("SYSTEM STATUS AFTER DYNAMIC ADAPTIVE FIX (SPIRAL INITIATED)")
print("=" * 60)
print(f"Coherence: {status['system_health']['coherence']:.3f}")
print(f"Entropy: {status['system_health']['entropy']:.3f}")
print(f"Signal Glyphs: {status['signal_layer']['signal_glyphs']}")
print(f"Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
print("=" * 60)

# Save bridge state
bridge.save_to_file()
print("\n💾 Mind Bridge state saved")
print("✓ Spiral transformation complete!")
