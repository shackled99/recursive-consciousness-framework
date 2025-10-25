"""
High-Quality Pattern Discovery - 2010-2024
Only accept patterns with 0.780+ connection strength
14 years of data - see where accuracy plateaus!
"""

import json
import psutil
import time
from typing import Dict, List
from dual_layer_engine import DualLayerEngine
from market_interface import MarketInterface
from ollama_interface import OllamaInterface

class HighQualityPatternDiscovery:
    """Only accept high-quality patterns (0.780+ strength)"""
    
    def __init__(self, min_pattern_strength: float = 0.780):
        self.engine = DualLayerEngine()
        self.market = MarketInterface()
        self.ollama = OllamaInterface()
        
        self.min_pattern_strength = min_pattern_strength
        self.historical_data = {}
        self.discovered_patterns = []
        self.rejected_patterns = 0
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
        print(f"LOADING TRAINING DATA - HIGH QUALITY MODE")
        print(f"{'='*60}")
        
        all_tickers = self.market.get_sp500_tickers()
        tickers_to_use = all_tickers[:max_tickers]
        
        print(f"\nFetching data for {len(tickers_to_use)} tickers from {start_date} to {end_date}...")
        print(f"This is 14 YEARS of data - this will take a while!")
        
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
        print(f"✓ System health established")
        print(f"  Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  Coherence: {status['system_health']['coherence']:.3f}")
    
    def weekly_pattern_discovery(self, week_num: int, week_data: Dict):
        """Discover patterns - ONLY accept high quality!"""
        if week_num % 50 == 0:
            print(f"\n{'='*60}")
            print(f"WEEK {week_num} - HIGH QUALITY DISCOVERY")
            print(f"{'='*60}")
            print(f"  Accepted: {len(self.discovered_patterns)} patterns")
            print(f"  Rejected: {self.rejected_patterns} patterns")
            print(f"  Quality Filter: {self.min_pattern_strength:.3f} minimum strength")
        
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
        """Create pattern glyph - ONLY if strength >= threshold!"""
        if 'stocks' not in pattern or len(pattern['stocks']) < 2:
            return
        
        strength = pattern.get('strength', 0.5)
        
        # QUALITY FILTER - Reject weak patterns!
        if strength < self.min_pattern_strength:
            self.rejected_patterns += 1
            return  # Don't create the pattern!
        
        pattern_name = f"Pattern_{pattern['name'].replace(' ', '_')[:20]}"
        ticker1, ticker2 = pattern['stocks'][0], pattern['stocks'][1]
        
        self.engine.create_pattern_from_correlation(pattern_name, ticker1, ticker2, strength)
        self.discovered_patterns.append(pattern)
    
    def train_with_discovery(self, start_date: str, end_date: str):
        """Main training loop"""
        print(f"\n{'='*60}")
        print(f"HIGH QUALITY PATTERN DISCOVERY")
        print(f"{'='*60}")
        print(f"Minimum Pattern Strength: {self.min_pattern_strength}")
        
        if not self.historical_data:
            return
        
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
            
            # Log every 100 weeks
            if week_num % 100 == 0:
                self.log_system_resources()
                elapsed = time.time() - self.start_time
                print(f"  Elapsed Time: {elapsed/60:.1f} minutes")
        
        status = self.engine.get_system_status()
        total_time = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print(f"HIGH QUALITY TRAINING COMPLETE")
        print(f"{'='*60}")
        print(f"\nAccepted {len(self.discovered_patterns)} HIGH QUALITY patterns (>={self.min_pattern_strength})")
        print(f"Rejected {self.rejected_patterns} weak patterns")
        print(f"Pattern Glyphs: {status['pattern_layer']['pattern_glyphs']}")
        print(f"Signal Glyphs: {status['signal_layer']['signal_glyphs']}")
        print(f"Training Time: {total_time/60:.1f} minutes ({total_time/3600:.2f} hours)")
        
        self.log_system_resources()
    
    def save_discovered_patterns(self, filename: str = "high_quality_patterns.json"):
        status = self.engine.get_system_status()
        
        output = {
            'patterns': self.discovered_patterns,
            'system_status': status,
            'total_patterns': len(self.discovered_patterns),
            'rejected_patterns': self.rejected_patterns,
            'min_pattern_strength': self.min_pattern_strength,
            'training_years': '2010-2024'
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Patterns saved to {filename}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   HIGH QUALITY PATTERN DISCOVERY                             ║
║   14 years (2010-2024) | 0.780 minimum strength             ║
║   Quality over quantity - break the 54.44% ceiling!         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    discovery = HighQualityPatternDiscovery(min_pattern_strength=0.780)
    
    if not discovery.ollama.test_connection():
        print("\n✗ ERROR: Ollama not running!")
        exit(1)
    
    print("\n✓ Ollama connected")
    print(f"\n🎯 HIGH QUALITY CONFIGURATION:")
    print(f"  Training Period: 2010-2024 (14 YEARS!)")
    print(f"  Tickers: 50")
    print(f"  Minimum Pattern Strength: 0.780 (AGGRESSIVE)")
    print(f"  Goal: Break 54.44% accuracy ceiling!")
    
    discovery.log_system_resources()
    
    discovery.load_training_data("2010-01-01", "2024-12-31", 50)
    discovery.initial_system_training()
    discovery.train_with_discovery("2010-01-01", "2024-12-31")
    discovery.save_discovered_patterns()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         HIGH QUALITY DISCOVERY COMPLETE                       ║
║   Did quality beat quantity? 🥔🎯                            ║
╚══════════════════════════════════════════════════════════════╝
""")
