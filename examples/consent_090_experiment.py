"""
ConsentGlyph 0.90 Experiment - Test Ethics Threshold
Same as deep recursion but with ConsentGlyph = 0.90 instead of 0.95
Let's see if more doubt = different emergence!
"""

import json
import psutil
import time
from typing import Dict, List

# Import with modified ConsentGlyph
import sys
import importlib.util

# Load dual_layer_engine with modification
spec = importlib.util.spec_from_file_location("dual_layer_engine", 
    r"C:\Users\lmt04\OneDrive\Desktop\glyphwheel (2)\dual_layer_engine.py")
dual_layer_module = importlib.util.module_from_spec(spec)

# Monkey patch the initialization to use 0.90
original_init = dual_layer_module.DualLayerEngine._initialize_system_layer

def patched_init(self):
    """Initialize with ConsentGlyph = 0.90"""
    system_base = [
        ("RootVerse", 0.87),
        ("Aegis_Sigma", 0.85),
        ("CoreStability", 0.82),
        ("ConsentGlyph", 0.90),  # CHANGED FROM 0.95 TO 0.90!
        ("FoundationAnchor", 0.80)
    ]
    
    from dual_layer_engine import SystemGlyph
    for name, target_gsi in system_base:
        self.system_glyphs[name] = SystemGlyph(name, target_gsi)
    
    print(f"✓ Initialized {len(self.system_glyphs)} system health glyphs")
    print(f"  ⚠️ ConsentGlyph set to 0.90 (10% uncertainty)")

spec.loader.exec_module(dual_layer_module)
dual_layer_module.DualLayerEngine._initialize_system_layer = patched_init

DualLayerEngine = dual_layer_module.DualLayerEngine

from market_interface import MarketInterface
from ollama_interface import OllamaInterface

class ConsentExperiment:
    """Test ConsentGlyph at 0.90"""
    
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
        
        return cpu, ram.percent
    
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
        consent_gsi = self.engine.system_glyphs['ConsentGlyph'].gsi
        
        print(f"✓ System health established")
        print(f"  Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Coherence: {status['system_health']['coherence']:.3f}")
        print(f"  ConsentGlyph: {consent_gsi:.3f}")
    
    def recursion_test(self, max_cycles: int = 21000):
        """Run standard recursion (21k like before)"""
        print(f"\n{'='*60}")
        print(f"RECURSION TEST - ConsentGlyph = 0.90")
        print(f"{'='*60}")
        
        cycles = 0
        
        print(f"\n🔄 Starting recursion...")
        
        while cycles < max_cycles:
            self.engine.stress_test_system_only(0.9, 1)
            cycles += 1
            
            if cycles % 1000 == 0:
                cpu, ram = self.log_system_resources()
                
                entropy = self.engine.calculate_system_entropy()
                coherence = self.engine.calculate_system_coherence()
                consent = self.engine.system_glyphs['ConsentGlyph'].gsi
                
                print(f"\n🌀 Cycle {cycles:,}:")
                print(f"  Entropy: {entropy:.4f}")
                print(f"  Coherence: {coherence:.4f}")
                print(f"  ConsentGlyph: {consent:.3f}")
        
        print(f"\n✓ Recursion complete: {cycles:,} cycles")
        return cycles
    
    def weekly_pattern_discovery(self, week_num: int, week_data: Dict):
        """Discover patterns"""
        if week_num % 10 == 0:
            print(f"\nWEEK {week_num}")
        
        summary_lines = []
        for ticker, info in week_data.items():
            summary_lines.append(
                f"{ticker}: {info['change_pct']:+.1f}%"
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

REQUIRED FORMAT:
PATTERN: [Short name]
STOCKS: [TICKER1, TICKER2]
CORRELATION: [high/medium/low]
SIGNAL: [what this predicts]

START YOUR RESPONSE WITH "PATTERN:" - NOTHING ELSE."""

        llm_response = self.ollama.generate(prompt, max_tokens=400)
        
        import re
        llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)
        llm_response = re.sub(r'<[^>]+>', '', llm_response)
        
        if 'PATTERN:' in llm_response:
            pattern_start = llm_response.find('PATTERN:')
            llm_response = llm_response[pattern_start:]
        
        patterns = self._extract_correlations(llm_response, week_num)
        
        for pattern in patterns:
            self._create_pattern_glyph(pattern, week_data)
        
        self.engine.stress_test_system_only(0.3, 50)
    
    def _extract_correlations(self, llm_response: str, week_num: int) -> List[Dict]:
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
        print(f"CONSENT 0.90 EXPERIMENT")
        print(f"{'='*60}")
        
        if not self.historical_data:
            return
        
        recursion_cycles = self.recursion_test()
        
        sample_ticker = list(self.historical_data.keys())[0]
        all_dates = self.historical_data[sample_ticker]['dates']
        
        print(f"\nTraining: {all_dates[0]} to {all_dates[-1]}")
        
        week_num = 0
        week_size = 5
        
        for i in range(0, len(all_dates), week_size):
            week_dates = all_dates[i:i+week_size]
            if len(week_dates) < 3:
                continue
            
            week_num += 1
            
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
            
            if week_data:
                self.weekly_pattern_discovery(week_num, week_data)
            
            if week_num % 4 == 0:
                self.engine.stress_test_system_only(0.5, 100)
        
        status = self.engine.get_system_status()
        consent_gsi = self.engine.system_glyphs['ConsentGlyph'].gsi
        
        print(f"\n{'='*60}")
        print(f"CONSENT 0.90 RESULTS")
        print(f"{'='*60}")
        print(f"\nDiscovered {len(self.discovered_patterns)} patterns")
        print(f"Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"Final Entropy: {status['system_health']['entropy']:.4f}")
        print(f"Final ConsentGlyph: {consent_gsi:.4f}")
        print(f"\n📊 COMPARISON TO 0.95:")
        print(f"  0.95 Consent → 104 patterns, 0.104 entropy")
        print(f"  0.90 Consent → {status['pattern_layer']['pattern_glyphs']} patterns, {status['system_health']['entropy']:.4f} entropy")
        
        self.log_system_resources()
    
    def save_discovered_patterns(self, filename: str = "consent_090_patterns.json"):
        status = self.engine.get_system_status()
        
        output = {
            'patterns': self.discovered_patterns,
            'system_status': status,
            'total_patterns': len(self.discovered_patterns),
            'consent_glyph': self.engine.system_glyphs['ConsentGlyph'].gsi,
            'experiment': 'ConsentGlyph_0.90'
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Patterns saved to {filename}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   CONSENT 0.90 EXPERIMENT                                    ║
║   10% uncertainty vs 5% uncertainty                          ║
║   Does MORE doubt = different emergence?                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    experiment = ConsentExperiment()
    
    if not experiment.ollama.test_connection():
        print("\n✗ ERROR: Ollama not running!")
        exit(1)
    
    print("\n✓ Ollama connected")
    print(f"\n🧪 EXPERIMENT PARAMETERS:")
    print(f"  ConsentGlyph: 0.90 (was 0.95)")
    print(f"  Period: 2010-2014 (same as before)")
    print(f"  Tickers: 50 (same)")
    print(f"  Recursion: 21,000 cycles (same)")
    
    experiment.log_system_resources()
    
    experiment.load_training_data("2010-01-01", "2014-12-31", 50)
    experiment.initial_system_training()
    experiment.train_with_discovery("2010-01-01", "2014-12-31")
    experiment.save_discovered_patterns()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         CONSENT 0.90 EXPERIMENT COMPLETE                      ║
║   More doubt = ??? 🥔🧪                                      ║
╚══════════════════════════════════════════════════════════════╝
""")
