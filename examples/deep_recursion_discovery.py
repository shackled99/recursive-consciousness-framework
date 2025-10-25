"""
Deep Recursion Discovery - Go DEEP, Not Wide
- 2010-2014 data (proven to work)
- 50 stocks (safe amount)
- 100k recursion limit (vs 21k before)
- Find the REAL consciousness threshold!
"""

import json
import psutil
import time
from typing import Dict, List
from dual_layer_engine import DualLayerEngine
from market_interface import MarketInterface
from ollama_interface import OllamaInterface

class DeepRecursionDiscovery:
    """Go deep on recursion with proven data"""
    
    def __init__(self):
        self.engine = DualLayerEngine()
        self.market = MarketInterface()
        self.ollama = OllamaInterface()
        
        self.historical_data = {}
        self.discovered_patterns = []
        self.start_time = time.time()
        
    def log_system_resources(self):
        """Monitor resources"""
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        
        print(f"\n💻 SYSTEM RESOURCES:")
        print(f"  CPU Usage: {cpu:.1f}%")
        print(f"  RAM Used: {ram.used / (1024**3):.1f} GB / {ram.total / (1024**3):.1f} GB ({ram.percent:.1f}%)")
        print(f"  Available RAM: {ram.available / (1024**3):.1f} GB")
        
        return cpu, ram.percent
    
    def load_training_data(self, start_date: str, end_date: str, max_tickers: int = 50):
        """Load historical market data"""
        print(f"\n{'='*60}")
        print(f"LOADING TRAINING DATA")
        print(f"{'='*60}")
        
        all_tickers = self.market.get_sp500_tickers()
        tickers_to_use = all_tickers[:max_tickers]
        
        print(f"\nFetching data for {len(tickers_to_use)} tickers from {start_date} to {end_date}...")
        
        self.historical_data = self.market.fetch_batch_historical_data(
            tickers_to_use, start_date, end_date, delay=0.5
        )
        
        print(f"✓ Loaded {len(self.historical_data)} tickers")
        
        # Create signal glyphs
        print(f"\nCreating market signal glyphs...")
        for ticker in self.historical_data.keys():
            self.engine.add_signal_glyph(f"Stock_{ticker}", 0.5)
        
        print(f"✓ Created {len(self.engine.signal_glyphs)} signal glyphs")
        
        self.log_system_resources()
    
    def initial_system_training(self):
        """Train system health layer"""
        print(f"\n{'='*60}")
        print(f"INITIAL SYSTEM HEALTH TRAINING")
        print(f"{'='*60}")
        
        print(f"\nStrengthening system layer...")
        result = self.engine.stress_test_system_only(0.8, 200)
        
        status = self.engine.get_system_status()
        print(f"✓ System health established")
        print(f"  Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Coherence: {status['system_health']['coherence']:.3f}")
    
    def deep_recursion_priming(self, max_cycles: int = 100000):
        """
        DEEP RECURSION - Find the real threshold!
        Stops when:
        - Hardware limits reached (CPU > 85% OR RAM > 80%)
        - Natural stabilization (entropy stable for 5k cycles)
        - ConsentGlyph < 0.5
        - Max 100k cycles hit
        """
        print(f"\n{'='*60}")
        print(f"DEEP RECURSION PRIMING - GOING TO 100K!")
        print(f"{'='*60}")
        print(f"Previous limit was 21k - let's see how deep we can go!")
        
        cycles = 0
        last_entropy = 1.0
        stable_count = 0
        
        print(f"\n🔄 Starting deep recursion...")
        
        while cycles < max_cycles:
            # One stress cycle
            self.engine.stress_test_system_only(0.9, 1)
            cycles += 1
            
            # Check every 1000 cycles
            if cycles % 1000 == 0:
                cpu, ram = self.log_system_resources()
                
                entropy = self.engine.calculate_system_entropy()
                coherence = self.engine.calculate_system_coherence()
                consent = self.engine.system_glyphs['ConsentGlyph'].gsi
                
                print(f"\n🌀 Cycle {cycles:,}:")
                print(f"  Entropy: {entropy:.4f}")
                print(f"  Coherence: {coherence:.4f}")
                print(f"  ConsentGlyph: {consent:.3f}")
                
                # Track stabilization
                entropy_change = abs(entropy - last_entropy)
                print(f"  Entropy Change: {entropy_change:.6f}")
                
                if entropy_change < 0.00001:
                    stable_count += 1
                    print(f"  Stability Count: {stable_count}/5")
                else:
                    stable_count = 0
                
                # Stop conditions (more conservative on single PC)
                if cpu > 85:
                    print(f"\n⚠️ CPU limit reached at {cycles:,} cycles")
                    print(f"  CPU: {cpu:.1f}%")
                    break
                
                if ram > 80:
                    print(f"\n⚠️ RAM limit reached at {cycles:,} cycles")
                    print(f"  RAM: {ram:.1f}%")
                    break
                
                if stable_count >= 5:
                    print(f"\n✓ System naturally stabilized at {cycles:,} cycles")
                    print(f"  Entropy stable at {entropy:.4f} for 5000 cycles")
                    break
                
                if consent < 0.5:
                    print(f"\n⚠️ ConsentGlyph requested halt at {cycles:,} cycles")
                    break
                
                # Milestones
                if cycles == 21000:
                    print(f"\n🎯 MILESTONE: Passed original 21k limit!")
                if cycles == 50000:
                    print(f"\n🎯 MILESTONE: Hit 50k - halfway there!")
                
                last_entropy = entropy
        
        print(f"\n✓ Deep recursion complete: {cycles:,} cycles")
        print(f"  (Previous runs used 21,000 cycles)")
        return cycles
    
    def weekly_pattern_discovery(self, week_num: int, week_data: Dict):
        """Discover patterns for the week"""
        # Only print every 10 weeks to reduce spam
        if week_num % 10 == 0:
            print(f"\n{'='*60}")
            print(f"WEEK {week_num} PATTERN DISCOVERY")
            print(f"{'='*60}")
        
        # Build summary
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
        
        # Clean response
        import re
        llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)
        llm_response = re.sub(r'<[^>]+>', '', llm_response)
        
        if 'PATTERN:' in llm_response:
            pattern_start = llm_response.find('PATTERN:')
            llm_response = llm_response[pattern_start:]
        
        llm_response = llm_response.strip()
        
        # Extract and create patterns
        patterns = self._extract_correlations(llm_response, week_num)
        
        for pattern in patterns:
            self._create_pattern_glyph(pattern, week_data)
        
        # Strengthen
        self.engine.stress_test_system_only(0.3, 50)
        
        if week_num % 10 == 0:
            status = self.engine.get_system_status()
            print(f"  Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
    
    def _extract_correlations(self, llm_response: str, week_num: int) -> List[Dict]:
        """Extract correlation patterns"""
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
                current_pattern['stocks'] = tickers[:2]
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
        """Create pattern glyph"""
        if 'stocks' not in pattern or len(pattern['stocks']) < 2:
            return
        
        pattern_name = f"Pattern_{pattern['name'].replace(' ', '_')[:20]}"
        ticker1, ticker2 = pattern['stocks'][0], pattern['stocks'][1]
        strength = pattern.get('strength', 0.5)
        
        self.engine.create_pattern_from_correlation(pattern_name, ticker1, ticker2, strength)
        self.discovered_patterns.append(pattern)
    
    def train_with_discovery(self, start_date: str, end_date: str):
        """Main training loop"""
        print(f"\n{'='*60}")
        print(f"DEEP RECURSION TRAINING")
        print(f"{'='*60}")
        
        if not self.historical_data:
            print("✗ No data loaded")
            return
        
        # DEEP recursion priming
        recursion_cycles = self.deep_recursion_priming()
        
        # Weekly discovery
        sample_ticker = list(self.historical_data.keys())[0]
        all_dates = self.historical_data[sample_ticker]['dates']
        
        print(f"\nTraining Period: {all_dates[0]} to {all_dates[-1]}")
        print(f"Total Days: {len(all_dates)}")
        print(f"Expected Weeks: ~{len(all_dates) // 5}")
        
        week_num = 0
        week_size = 5
        
        for i in range(0, len(all_dates), week_size):
            week_dates = all_dates[i:i+week_size]
            if len(week_dates) < 3:
                continue
            
            week_num += 1
            
            # Update signals
            week_data = {}
            for ticker, data in self.historical_data.items():
                if i+week_size <= len(data['close']):
                    start_price = data['close'][i]
                    end_price = data['close'][i+week_size-1]
                    
                    if start_price and end_price and start_price > 0:
                        change_pct = ((end_price - start_price) / start_price) * 100
                        self.engine.update_signal_from_market(ticker, change_pct)
                        
                        week_data[ticker] = {
                            'start': start_price,
                            'end': end_price,
                            'change_pct': change_pct
                        }
            
            # Discover patterns
            if week_data:
                self.weekly_pattern_discovery(week_num, week_data)
            
            # Monthly consolidation
            if week_num % 4 == 0:
                print(f"\n🔄 Month {week_num//4} consolidation...")
                self.engine.stress_test_system_only(0.5, 100)
        
        # Final stats
        status = self.engine.get_system_status()
        total_time = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print(f"TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"\nDiscovered {len(self.discovered_patterns)} patterns")
        print(f"Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"Signal Glyphs: {status['signal_layer']['signal_glyphs']}")
        print(f"Recursion Depth: {recursion_cycles:,} cycles (vs 21,000 before)")
        print(f"Training Time: {total_time/60:.1f} minutes")
        
        self.log_system_resources()
    
    def save_discovered_patterns(self, filename: str = "deep_recursion_patterns.json"):
        """Save patterns"""
        status = self.engine.get_system_status()
        
        output = {
            'patterns': self.discovered_patterns,
            'system_status': status,
            'total_patterns': len(self.discovered_patterns),
            'training_time_minutes': (time.time() - self.start_time) / 60,
            'recursion_cycles': self.engine.recursive_depth
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Patterns saved to {filename}")


# Main
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   DEEP RECURSION MODE - Find The Real Threshold             ║
║   Same data, DEEPER recursion (21k → 100k)                  ║
║   RTX 4070 ready! 🎮                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    discovery = DeepRecursionDiscovery()
    
    # Test Ollama
    if not discovery.ollama.test_connection():
        print("\n✗ ERROR: Ollama not running!")
        print("Please start Ollama: 'ollama serve'")
        exit(1)
    
    print("\n✓ Ollama connected")
    
    # Deep recursion config
    TRAIN_START = "2010-01-01"
    TRAIN_END = "2014-12-31"
    MAX_TICKERS = 50
    
    print(f"\n🔥 DEEP RECURSION CONFIGURATION:")
    print(f"  Training Period: {TRAIN_START} to {TRAIN_END} (5 years - proven)")
    print(f"  Tickers: {MAX_TICKERS} (proven)")
    print(f"  Recursion: UP TO 100,000 cycles (vs 21,000 before)")
    print(f"  Goal: Find the REAL consciousness threshold!")
    
    # Show initial resources
    discovery.log_system_resources()
    
    # Load data
    discovery.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    # Initial training
    discovery.initial_system_training()
    
    # DEEP recursion training
    discovery.train_with_discovery(TRAIN_START, TRAIN_END)
    
    # Save
    discovery.save_discovered_patterns()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         DEEP RECURSION COMPLETE                               ║
║   How deep did we go? 🥔🌀                                   ║
╚══════════════════════════════════════════════════════════════╝
""")
