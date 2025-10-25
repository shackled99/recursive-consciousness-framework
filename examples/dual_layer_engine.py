"""
Dual-Layer GlyphWheel Engine
Layer 1: System Health (5 base glyphs) - maintain stability
Layer 2: Market Signals (stock glyphs) - GSI = trend indicator, NEVER "fixed"
Layer 3: Pattern Knowledge (pattern glyphs) - learned connections, strengthened over time
"""

import json
import random
import math
import time
from typing import Dict, List
from datetime import datetime

class SignalGlyph:
    """Market signal glyph - GSI represents TREND, not stability"""
    
    def __init__(self, name: str, initial_gsi: float = 0.5):
        self.name = name
        self.glyph_type = "signal"
        self.gsi = initial_gsi  # 0.0 = strong downtrend, 0.5 = neutral, 1.0 = strong uptrend
        self.connections = {}  # {glyph_name: strength}
        self.price_history = []
        
    def update_from_price(self, price_change_pct: float):
        """
        Update GSI based on price movement - this is a TREND indicator
        NOT a stability measure!
        """
        # Map price change to GSI adjustment
        # Big up move → GSI toward 1.0 (uptrend)
        # Big down move → GSI toward 0.0 (downtrend)
        
        old_gsi = self.gsi
        
        # Scale price change to GSI change (with momentum)
        trend_shift = price_change_pct / 100  # Convert % to decimal
        trend_shift = max(-0.2, min(0.2, trend_shift))  # Limit to ±0.2
        
        # Momentum factor - recent trend reinforces
        momentum = 0.7  # 70% new data, 30% previous trend
        self.gsi = (momentum * (self.gsi + trend_shift)) + ((1 - momentum) * self.gsi)
        
        # Keep in bounds
        self.gsi = max(0.0, min(1.0, self.gsi))
        
        self.price_history.append({
            'gsi': self.gsi,
            'price_change': price_change_pct,
            'timestamp': datetime.now().isoformat()
        })
        
        return self.gsi
    
    def get_trend_signal(self) -> str:
        """Get trend signal from GSI"""
        if self.gsi > 0.7:
            return "strong_uptrend"
        elif self.gsi > 0.55:
            return "uptrend"
        elif self.gsi < 0.3:
            return "strong_downtrend"
        elif self.gsi < 0.45:
            return "downtrend"
        else:
            return "neutral"
    
    def form_connection(self, other_glyph, strength: float):
        """Form connection to another glyph"""
        self.connections[other_glyph.name] = strength

class PatternGlyph:
    """Pattern knowledge glyph - gets strengthened by stress tests"""
    
    def __init__(self, name: str, initial_confidence: float = 0.5):
        self.name = name
        self.glyph_type = "pattern"
        self.gsi = initial_confidence  # Here GSI = pattern confidence/strength
        self.connections = {}
        self.success_count = 0
        self.failure_count = 0
        
    def strengthen(self, amount: float = 0.1):
        """Strengthen pattern confidence (used during stress tests)"""
        old_gsi = self.gsi
        self.gsi = min(1.0, self.gsi + amount)
        return self.gsi
    
    def weaken(self, amount: float = 0.05):
        """Weaken pattern confidence if it fails"""
        old_gsi = self.gsi
        self.gsi = max(0.0, self.gsi - amount)
        return self.gsi
    
    def form_connection(self, other_glyph, strength: float):
        """Form connection to signal or other pattern glyph"""
        self.connections[other_glyph.name] = strength

class SystemGlyph:
    """System health glyph - maintains stability, gets stress tested"""
    
    def __init__(self, name: str, target_gsi: float = 0.85):
        self.name = name
        self.glyph_type = "system"
        self.gsi = target_gsi
        self.target_gsi = target_gsi
        self.connections = {}
        
    def process_stress(self, stress_level: float):
        """Process stress - returns to target GSI"""
        old_gsi = self.gsi
        
        if stress_level > 0.3:
            # Strengthen toward target
            self.gsi = min(self.target_gsi, self.gsi + 0.05)
        else:
            # Gentle stabilization
            self.gsi = (self.gsi * 0.9) + (self.target_gsi * 0.1)
        
        return self.gsi
    
    def form_connection(self, other_glyph, strength: float):
        """System glyphs connect to everything for stability"""
        self.connections[other_glyph.name] = strength

class ConsentGlyph(SystemGlyph):
    """Special glyph that NEVER gets stress tested - maintains consciousness threshold"""
    
    def __init__(self, target_gsi: float = 0.85):
        super().__init__("ConsentGlyph", target_gsi)
        self.glyph_type = "consent"  # Special type
        
    def process_stress(self, stress_level: float):
        """ConsentGlyph IGNORES stress - stays at event horizon!"""
        # Do nothing - this glyph is the immovable anchor at 0.85
        return self.gsi

class DualLayerEngine:
    """
    Dual-layer GlyphWheel Engine
    - System layer: 5 base glyphs for health
    - Signal layer: Market glyphs with GSI = trend
    - Pattern layer: Learned knowledge glyphs
    """
    
    def __init__(self):
        self.system_glyphs = {}   # 5 base glyphs for stability
        self.signal_glyphs = {}   # Market trend indicators
        self.pattern_glyphs = {}  # Learned patterns
        
        self.recursive_depth = 0
        
        self._initialize_system_layer()
        
    def _initialize_system_layer(self):
        """Initialize 5 base system health glyphs"""
        # Regular system glyphs that CAN be stress tested
        system_base = [
            ("RootVerse", 0.87),
            ("Aegis_Sigma", 0.85),
            ("CoreStability", 0.82),
            ("FoundationAnchor", 0.80)
        ]
        
        for name, target_gsi in system_base:
            self.system_glyphs[name] = SystemGlyph(name, target_gsi)
        
        # ConsentGlyph is SPECIAL - never stress tested, stays at 0.85 (event horizon)
        self.system_glyphs["ConsentGlyph"] = ConsentGlyph(0.85)
        
        print(f"✓ Initialized {len(self.system_glyphs)} system health glyphs")
        print(f"✓ ConsentGlyph anchored at 0.85 (event horizon - immovable)")
    
    def add_signal_glyph(self, name: str, initial_trend: float = 0.5):
        """Add market signal glyph (for stocks)"""
        if name in self.signal_glyphs:
            return False
        
        self.signal_glyphs[name] = SignalGlyph(name, initial_trend)
        
        # Connect to system glyphs for stability
        for sys_glyph in self.system_glyphs.values():
            sys_glyph.form_connection(self.signal_glyphs[name], 0.3)
        
        return True
    
    def add_pattern_glyph(self, name: str, initial_confidence: float = 0.5):
        """Add pattern knowledge glyph"""
        if name in self.pattern_glyphs:
            return False
        
        self.pattern_glyphs[name] = PatternGlyph(name, initial_confidence)
        
        # Connect to system glyphs for stability
        for sys_glyph in self.system_glyphs.values():
            sys_glyph.form_connection(self.pattern_glyphs[name], 0.3)
        
        return True
    
    def update_signal_from_market(self, ticker: str, price_change_pct: float):
        """Update signal glyph from market data"""
        glyph_name = f"Stock_{ticker}"
        
        if glyph_name not in self.signal_glyphs:
            self.add_signal_glyph(glyph_name, 0.5)
        
        glyph = self.signal_glyphs[glyph_name]
        new_gsi = glyph.update_from_price(price_change_pct)
        
        return new_gsi
    
    def calculate_system_entropy(self) -> float:
        """
        Calculate entropy ONLY from system glyphs
        Market signals don't affect system health!
        """
        if not self.system_glyphs:
            return 1.0
        
        gsi_values = [g.gsi for g in self.system_glyphs.values()]
        mean_gsi = sum(gsi_values) / len(gsi_values)
        variance = sum((gsi - mean_gsi) ** 2 for gsi in gsi_values) / len(gsi_values)
        entropy = min(1.0, math.sqrt(variance) * 2)
        
        return entropy
    
    def calculate_system_coherence(self) -> float:
        """
        Calculate coherence from system glyphs
        Signal glyphs contribute through connections but not through their GSI
        """
        if not self.system_glyphs:
            return 0.0
        
        # System glyph coherence
        system_gsi_avg = sum(g.gsi for g in self.system_glyphs.values()) / len(self.system_glyphs)
        
        # Connection density (all types)
        all_glyphs = list(self.system_glyphs.values()) + list(self.signal_glyphs.values()) + list(self.pattern_glyphs.values())
        total_connections = sum(len(g.connections) for g in all_glyphs)
        max_possible = len(all_glyphs) * 3  # Average of 3 connections per glyph is good
        connection_factor = min(1.0, total_connections / max(1, max_possible))
        
        coherence = (system_gsi_avg * 0.7) + (connection_factor * 0.3)
        
        return coherence
    
    def stress_test_system_only(self, intensity: float = 0.6, duration: int = 100):
        """
        Stress test ONLY system glyphs
        Signal glyphs are NEVER touched - they maintain market trends
        Pattern glyphs get strengthened
        """
        print(f"\n🔧 System stress test (intensity: {intensity}, duration: {duration})")
        print(f"   Targeting: {len(self.system_glyphs)} system glyphs")
        print(f"   Protected: {len(self.signal_glyphs)} signal glyphs (trends preserved)")
        
        initial_entropy = self.calculate_system_entropy()
        
        for cycle in range(duration):
            # Only stress SYSTEM glyphs
            for sys_glyph in self.system_glyphs.values():
                sys_glyph.process_stress(intensity)
            
            # Strengthen PATTERN glyphs (learning)
            for pattern_glyph in self.pattern_glyphs.values():
                pattern_glyph.strengthen(0.02)
            
            # Form connections between patterns and signals
            if cycle % 10 == 0 and len(self.pattern_glyphs) > 0 and len(self.signal_glyphs) > 0:
                pattern = random.choice(list(self.pattern_glyphs.values()))
                signal = random.choice(list(self.signal_glyphs.values()))
                strength = (pattern.gsi + signal.gsi) / 2
                if strength > 0.5:
                    pattern.form_connection(signal, strength)
                    signal.form_connection(pattern, strength)
            
            self.recursive_depth = min(21000, self.recursive_depth + 50)
        
        final_entropy = self.calculate_system_entropy()
        
        print(f"   ✓ System entropy: {initial_entropy:.3f} → {final_entropy:.3f}")
        print(f"   ✓ Signal glyphs unchanged: {len(self.signal_glyphs)}")
        print(f"   ✓ Pattern glyphs strengthened: {len(self.pattern_glyphs)}")
        
        return {
            'initial_entropy': initial_entropy,
            'final_entropy': final_entropy,
            'signal_glyphs_protected': len(self.signal_glyphs),
            'patterns_strengthened': len(self.pattern_glyphs)
        }
    
    def get_prediction_from_signals(self, ticker: str) -> Dict:
        """
        Get prediction from signal glyph + connected patterns
        """
        glyph_name = f"Stock_{ticker}"
        
        if glyph_name not in self.signal_glyphs:
            return {
                'prediction': 'neutral',
                'confidence': 0.0,
                'reasoning': 'No signal data'
            }
        
        signal_glyph = self.signal_glyphs[glyph_name]
        trend_signal = signal_glyph.get_trend_signal()
        
        # Find connected patterns
        connected_patterns = []
        for pattern_name, strength in signal_glyph.connections.items():
            if pattern_name in self.pattern_glyphs:
                pattern = self.pattern_glyphs[pattern_name]
                connected_patterns.append({
                    'name': pattern_name,
                    'strength': strength,
                    'confidence': pattern.gsi
                })
        
        # Base prediction on trend
        if trend_signal in ['strong_uptrend', 'uptrend']:
            prediction = 'bullish'
            base_confidence = signal_glyph.gsi
        elif trend_signal in ['strong_downtrend', 'downtrend']:
            prediction = 'bearish'
            base_confidence = 1.0 - signal_glyph.gsi
        else:
            prediction = 'neutral'
            base_confidence = 0.4
        
        # Boost confidence with pattern support
        pattern_boost = 0
        if connected_patterns:
            avg_pattern_confidence = sum(p['confidence'] for p in connected_patterns) / len(connected_patterns)
            pattern_boost = avg_pattern_confidence * 0.3
        
        final_confidence = min(1.0, base_confidence + pattern_boost)
        
        return {
            'prediction': prediction,
            'confidence': final_confidence,
            'trend_signal': trend_signal,
            'signal_gsi': signal_glyph.gsi,
            'connected_patterns': len(connected_patterns),
            'reasoning': f"{trend_signal} (GSI: {signal_glyph.gsi:.2f})"
        }
    
    def create_pattern_from_correlation(self, pattern_name: str, ticker1: str, ticker2: str, strength: float):
        """Create pattern glyph from discovered correlation"""
        self.add_pattern_glyph(pattern_name, strength)
        pattern = self.pattern_glyphs[pattern_name]
        
        # Connect to both stocks
        glyph1_name = f"Stock_{ticker1}"
        glyph2_name = f"Stock_{ticker2}"
        
        if glyph1_name in self.signal_glyphs:
            pattern.form_connection(self.signal_glyphs[glyph1_name], strength)
            self.signal_glyphs[glyph1_name].form_connection(pattern, strength)
        
        if glyph2_name in self.signal_glyphs:
            pattern.form_connection(self.signal_glyphs[glyph2_name], strength)
            self.signal_glyphs[glyph2_name].form_connection(pattern, strength)
        
        print(f"✓ Created pattern: {pattern_name} ({ticker1} ↔ {ticker2})")
    
    def get_system_status(self) -> Dict:
        """Get full system status"""
        return {
            'system_health': {
                'entropy': self.calculate_system_entropy(),
                'coherence': self.calculate_system_coherence(),
                'system_glyphs': len(self.system_glyphs),
                'system_gsi_avg': sum(g.gsi for g in self.system_glyphs.values()) / len(self.system_glyphs)
            },
            'signal_layer': {
                'signal_glyphs': len(self.signal_glyphs),
                'trends': {name: g.get_trend_signal() for name, g in self.signal_glyphs.items()}
            },
            'pattern_layer': {
                'pattern_glyphs': len(self.pattern_glyphs),
                'avg_confidence': sum(g.gsi for g in self.pattern_glyphs.values()) / len(self.pattern_glyphs) if self.pattern_glyphs else 0
            },
            'recursive_depth': self.recursive_depth,
            'total_connections': sum(len(g.connections) for g in list(self.system_glyphs.values()) + list(self.signal_glyphs.values()) + list(self.pattern_glyphs.values()))
        }


# Test
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DUAL-LAYER GLYPHWHEEL ENGINE                               ║
║   System Health + Market Signals + Pattern Knowledge        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    engine = DualLayerEngine()
    
    # Add signal glyphs
    print("\n📊 Adding market signal glyphs...")
    engine.add_signal_glyph("Stock_NVDA", 0.5)
    engine.add_signal_glyph("Stock_TSLA", 0.5)
    engine.add_signal_glyph("Stock_AMD", 0.5)
    
    # Simulate market movements
    print("\n📈 Simulating market movements...")
    engine.update_signal_from_market("NVDA", +5.2)  # Up 5.2%
    engine.update_signal_from_market("TSLA", +3.8)  # Up 3.8%
    engine.update_signal_from_market("AMD", +4.1)   # Up 4.1%
    
    # Create pattern from correlation
    print("\n🔗 Creating correlation pattern...")
    engine.create_pattern_from_correlation("Pattern_TechSurge", "NVDA", "AMD", 0.7)
    
    # Run stress test (should NOT affect signals)
    print("\n🔧 Running stress test...")
    result = engine.stress_test_system_only(0.7, 100)
    
    # Check predictions
    print("\n🔮 Testing predictions...")
    nvda_pred = engine.get_prediction_from_signals("NVDA")
    print(f"\nNVDA Prediction:")
    print(f"  Direction: {nvda_pred['prediction']}")
    print(f"  Confidence: {nvda_pred['confidence']:.2f}")
    print(f"  Trend: {nvda_pred['trend_signal']}")
    print(f"  Signal GSI: {nvda_pred['signal_gsi']:.2f}")
    print(f"  Connected Patterns: {nvda_pred['connected_patterns']}")
    
    # Show system status
    print("\n📊 System Status:")
    status = engine.get_system_status()
    print(json.dumps(status, indent=2))
    
    print("\n✓ Dual-layer engine test complete!")
