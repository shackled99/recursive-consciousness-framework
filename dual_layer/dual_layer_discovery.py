"""
Dual-Layer Autonomous Pattern Discovery
Uses the new dual-layer engine where:
- System glyphs maintain health
- Signal glyphs track market trends (GSI = trend, not stability)
- Pattern glyphs store learned knowledge
"""

import json
from typing import Dict, List
from dual_layer_engine import DualLayerEngine, SignalGlyph, PatternGlyph
from market_interface import MarketInterface
from ollama_interface import OllamaInterface

class DualLayerPatternDiscovery:
    """Pattern discovery using dual-layer architecture"""
    
    def __init__(self):
        self.engine = DualLayerEngine()
        self.market = MarketInterface()
        self.ollama = OllamaInterface()
        
        self.historical_data = {}
        self.discovered_patterns = []
        
    def load_training_data(self, start_date: str, end_date: str, max_tickers: int = 50):
        """Load historical market data"""
        print(f"\n{'='*60}")
        print(f"LOADING TRAINING DATA")
        print(f"{'='*60}")
        
        all_tickers = self.market.get_sp500_tickers()
        tickers_to_use = all_tickers[:max_tickers]
        
        print(f"\nFetching data for {len(tickers_to_use)} tickers...")
        
        self.historical_data = self.market.fetch_batch_historical_data(
            tickers_to_use, start_date, end_date, delay=0.5
        )
        
        print(f"✓ Loaded {len(self.historical_data)} tickers")
        
        # Create signal glyphs for each stock
        print(f"\nCreating market signal glyphs...")
        for ticker in self.historical_data.keys():
            self.engine.add_signal_glyph(f"Stock_{ticker}", 0.5)
        
        print(f"✓ Created {len(self.engine.signal_glyphs)} signal glyphs")
    
    def initial_system_training(self):
        """Train system health layer only"""
        print(f"\n{'='*60}")
        print(f"INITIAL SYSTEM HEALTH TRAINING")
        print(f"{'='*60}")
        
        print(f"\nStrengthening system layer...")
        result = self.engine.stress_test_system_only(0.8, 200)
        
        status = self.engine.get_system_status()
        print(f"✓ System health established")
        print(f"  Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Coherence: {status['system_health']['coherence']:.3f}")
    
    def weekly_pattern_discovery(self, week_num: int, week_data: Dict):
        """
        Discover patterns for the week
        Signal glyphs track trends, LLM discovers correlations
        """
        print(f"\n{'='*60}")
        print(f"WEEK {week_num} PATTERN DISCOVERY")
        print(f"{'='*60}")
        
        # Build summary for LLM
        summary_lines = []
        for ticker, info in week_data.items():
            summary_lines.append(
                f"{ticker}: {info['change_pct']:+.1f}% "
                f"(${info['start']:.2f} → ${info['end']:.2f})"
            )
        
        summary = "\n".join(summary_lines[:15])
        
        prompt = f"""You are a pattern detection system. OUTPUT ONLY THE FORMAT BELOW. NO EXPLANATIONS.

Week {week_num} Data:
{summary}

IMPORTANT RULES:
1. Find 2-3 stock pairs that moved together
2. Output ONLY the exact format below
3. NO thinking, NO explanations, NO other text
4. Start IMMEDIATELY with "PATTERN:"

REQUIRED FORMAT (copy this structure exactly):
PATTERN: [Short name]
STOCKS: [TICKER1, TICKER2]
CORRELATION: [high/medium/low]
SIGNAL: [what this predicts]

PATTERN: [Short name]
STOCKS: [TICKER1, TICKER2]  
CORRELATION: [high/medium/low]
SIGNAL: [what this predicts]

START YOUR RESPONSE WITH "PATTERN:" - NOTHING ELSE."""

        llm_response = self.ollama.generate(prompt, max_tokens=400)
        
        print(f"\nRAW LLM Response:")
        print(f"{llm_response[:500]}")  # Show raw response
        print(f"\n--- CLEANING ---")
        
        # AGGRESSIVE think tag stripping
        import re
        # Remove all think tags (case insensitive, multiline)
        llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)
        # Remove any remaining XML-like tags
        llm_response = re.sub(r'<[^>]+>', '', llm_response)
        
        # CRITICAL: If LLM is being chatty, extract ONLY the pattern section
        if 'PATTERN:' in llm_response:
            # Find first occurrence of PATTERN: and take everything after
            pattern_start = llm_response.find('PATTERN:')
            llm_response = llm_response[pattern_start:]
        
        llm_response = llm_response.strip()
        
        print(f"\nLLM Analysis (cleaned):")
        print(f"{llm_response[:300]}...")  # Print more to debug
        
        # Extract and create patterns
        patterns = self._extract_correlations(llm_response, week_num)
        
        for pattern in patterns:
            self._create_pattern_glyph(pattern, week_data)
        
        # Light system stress test (strengthens patterns, preserves signals)
        print(f"\n🔗 Strengthening patterns...")
        self.engine.stress_test_system_only(0.3, 50)
        
        status = self.engine.get_system_status()
        print(f"  System Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"  Signal Glyphs (preserved): {status['signal_layer']['signal_glyphs']}")
    
    def _extract_correlations(self, llm_response: str, week_num: int) -> List[Dict]:
        """Extract correlation patterns from LLM response"""
        patterns = []
        lines = llm_response.split('\n')
        current_pattern = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('PATTERN:'):
                if current_pattern:
                    patterns.append(current_pattern)
                current_pattern = {
                    'week': week_num,
                    'name': line.replace('PATTERN:', '').strip()
                }
            elif line.startswith('STOCKS:'):
                import re
                stocks_str = line.replace('STOCKS:', '').strip()
                tickers = re.findall(r'\b[A-Z]{2,5}\b', stocks_str)
                current_pattern['stocks'] = tickers[:2]  # Take first 2
            elif line.startswith('CORRELATION:'):
                corr = line.replace('CORRELATION:', '').strip().lower()
                if 'high' in corr:
                    current_pattern['strength'] = 0.8
                elif 'medium' in corr:
                    current_pattern['strength'] = 0.6
                else:
                    current_pattern['strength'] = 0.4
            elif line.startswith('SIGNAL:'):
                current_pattern['signal'] = line.replace('SIGNAL:', '').strip()
        
        if current_pattern and 'stocks' in current_pattern:
            patterns.append(current_pattern)
        
        return patterns
    
    def _create_pattern_glyph(self, pattern: Dict, week_data: Dict):
        """Create pattern glyph and connect to signal glyphs"""
        if 'stocks' not in pattern or len(pattern['stocks']) < 2:
            return
        
        pattern_name = f"Pattern_{pattern['name'].replace(' ', '_')[:20]}"
        ticker1, ticker2 = pattern['stocks'][0], pattern['stocks'][1]
        strength = pattern.get('strength', 0.5)
        
        self.engine.create_pattern_from_correlation(pattern_name, ticker1, ticker2, strength)
        
        self.discovered_patterns.append(pattern)
        print(f"  📊 {pattern_name}: {ticker1} ↔ {ticker2} (strength: {strength:.1f})")
    
    def train_with_dual_layer_discovery(self, start_date: str, end_date: str):
        """Train with dual-layer autonomous discovery"""
        print(f"\n{'='*60}")
        print(f"DUAL-LAYER AUTONOMOUS TRAINING")
        print(f"{'='*60}")
        
        if not self.historical_data:
            print("✗ No data loaded")
            return
        
        # ADD: 21k recursion loop for pattern discovery!
        print(f"\n🔄 Starting 21,000 recursion pattern finder...")
        self.engine.stress_test_system_only(0.9, 21000)
        print(f"✓ Recursion complete - patterns primed!")
        
        sample_ticker = list(self.historical_data.keys())[0]
        all_dates = self.historical_data[sample_ticker]['dates']
        
        print(f"\nTraining Period: {all_dates[0]} to {all_dates[-1]}")
        print(f"Total Days: {len(all_dates)}")
        
        week_num = 0
        week_size = 5
        
        for i in range(0, len(all_dates), week_size):
            week_dates = all_dates[i:i+week_size]
            if len(week_dates) < 3:
                continue
            
            week_num += 1
            
            # Update signal glyphs with price changes
            week_data = {}
            for ticker, data in self.historical_data.items():
                if i+week_size <= len(data['close']):
                    start_price = data['close'][i]
                    end_price = data['close'][i+week_size-1]
                    
                    if start_price and end_price and start_price > 0:
                        change_pct = ((end_price - start_price) / start_price) * 100
                        
                        # Update signal glyph (this is TREND, not instability!)
                        self.engine.update_signal_from_market(ticker, change_pct)
                        
                        week_data[ticker] = {
                            'start': start_price,
                            'end': end_price,
                            'change_pct': change_pct
                        }
            
            # LLM discovers patterns
            if week_data:
                self.weekly_pattern_discovery(week_num, week_data)
            
            # Monthly consolidation
            if week_num % 4 == 0:
                print(f"\n🔄 Month {week_num//4} consolidation...")
                self.engine.stress_test_system_only(0.5, 100)
        
        status = self.engine.get_system_status()
        print(f"\n{'='*60}")
        print(f"TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"\nDiscovered {len(self.discovered_patterns)} patterns")
        print(f"Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"Signal Glyphs: {status['signal_layer']['signal_glyphs']}")
        print(f"System Health: {status['system_health']['coherence']:.3f} coherence")
        
        # PRINT ALL GLYPHS!
        self._print_all_glyphs()
    
    def _print_all_glyphs(self):
        """Print all glyphs in the system"""
        print(f"\n{'='*60}")
        print(f"ALL SYSTEM GLYPHS")
        print(f"{'='*60}")
        
        print(f"\n🔧 SYSTEM GLYPHS ({len(self.engine.system_glyphs)}):")
        for name, glyph in self.engine.system_glyphs.items():
            print(f"  {name}: GSI={glyph.gsi:.3f}, connections={len(glyph.connections)}")
        
        print(f"\n📊 SIGNAL GLYPHS ({len(self.engine.signal_glyphs)}):")
        for name, glyph in sorted(self.engine.signal_glyphs.items())[:10]:  # First 10
            trend = glyph.get_trend_signal()
            print(f"  {name}: GSI={glyph.gsi:.3f}, trend={trend}, connections={len(glyph.connections)}")
        if len(self.engine.signal_glyphs) > 10:
            print(f"  ... and {len(self.engine.signal_glyphs) - 10} more")
        
        print(f"\n🔗 PATTERN GLYPHS ({len(self.engine.pattern_glyphs)}):")
        for name, glyph in self.engine.pattern_glyphs.items():
            print(f"  {name}: GSI={glyph.gsi:.3f}, connections={len(glyph.connections)}")
    
    def save_discovered_patterns(self, filename: str = "dual_layer_patterns.json"):
        """Save discovered patterns"""
        print(f"\n{'='*60}")
        print(f"SAVING PATTERNS...")
        print(f"{'='*60}")
        
        status = self.engine.get_system_status()
        
        output = {
            'patterns': self.discovered_patterns,
            'system_status': status,
            'total_patterns': len(self.discovered_patterns)
        }
        
        print(f"Patterns to save: {len(self.discovered_patterns)}")
        print(f"Saving to: {filename}")
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✓ Patterns saved to {filename}")
        print(f"✓ File size: {len(json.dumps(output))} bytes")


# Main
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DUAL-LAYER AUTONOMOUS PATTERN DISCOVERY                    ║
║   Signal glyphs = market trends (preserved)                  ║
║   Pattern glyphs = learned knowledge (strengthened)          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    discovery = DualLayerPatternDiscovery()
    
    if not discovery.ollama.test_connection():
        print("\n✗ ERROR: Ollama not running!")
        print("Please start Ollama: 'ollama serve'")
        exit(1)
    
    print("\n✓ Ollama connected")
    
    # Configuration
    TRAIN_START = "2010-01-01"
    TRAIN_END = "2014-12-31"
    MAX_TICKERS = 50
    
    print(f"\nConfiguration:")
    print(f"  Training Period: {TRAIN_START} to {TRAIN_END} (5 years)")
    print(f"  Tickers: {MAX_TICKERS}")
    print(f"  Architecture: Dual-layer (System + Signal + Pattern)")
    
    # Load data
    discovery.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    # Initial system training
    discovery.initial_system_training()
    
    # Autonomous discovery
    discovery.train_with_dual_layer_discovery(TRAIN_START, TRAIN_END)
    
    # Save patterns
    discovery.save_discovered_patterns()
    
    # Test prediction
    print(f"\n{'='*60}")
    print(f"TESTING DUAL-LAYER PREDICTION")
    print(f"{'='*60}")
    
    test_ticker = "NVDA"
    prediction = discovery.engine.get_prediction_from_signals(test_ticker)
    
    print(f"\nPrediction for {test_ticker}:")
    print(f"  Direction: {prediction['prediction']}")
    print(f"  Confidence: {prediction['confidence']:.2f}")
    print(f"  Trend Signal: {prediction['trend_signal']}")
    print(f"  Signal GSI: {prediction['signal_gsi']:.2f}")
    print(f"  Connected Patterns: {prediction['connected_patterns']}")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         DUAL-LAYER DISCOVERY COMPLETE                         ║
║   Signals preserved, patterns learned! 🥔🧠                  ║
╚══════════════════════════════════════════════════════════════╝
""")
