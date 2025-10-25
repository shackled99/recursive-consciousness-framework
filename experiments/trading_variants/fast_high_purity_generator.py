"""
Fast High Purity Pattern Generator
Uses a two-pass approach:
1. Quick pass: Identify which weeks had 95%+ predictions
2. Pattern discovery: Only run LLM on those high-quality weeks
"""

import json
from typing import Dict, List
from dual_layer_engine import DualLayerEngine
from market_interface import MarketInterface
from ollama_interface import OllamaInterface

class FastHighPurityGenerator:
    """Fast version - identify high-purity signals first, then discover patterns"""
    
    STRENGTH_THRESHOLD = 0.95
    
    def __init__(self):
        self.engine = DualLayerEngine()
        self.market = MarketInterface()
        self.ollama = OllamaInterface()
        
        self.historical_data = {}
        self.high_quality_weeks = []  # Weeks with 95%+ predictions
        self.high_purity_patterns = []
        
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
        
        # Create signal glyphs
        for ticker in self.historical_data.keys():
            self.engine.add_signal_glyph(f"Stock_{ticker}", 0.5)
        
        print(f"✓ Created {len(self.engine.signal_glyphs)} signal glyphs")
    
    def initial_antifragile_training(self):
        """Run the 21,000 recursion antifragile stress test"""
        print(f"\n{'='*60}")
        print(f"ANTIFRAGILE SYSTEM INITIALIZATION")
        print(f"Running 21,000 recursion stress test...")
        print(f"{'='*60}\n")
        
        print(f"🔄 Starting deep recursion training...")
        result = self.engine.stress_test_system_only(0.9, 21000)
        
        status = self.engine.get_system_status()
        print(f"\n✓ 21k recursion complete!")
        print(f"  System Entropy: {status['system_health']['entropy']:.3f}")
        print(f"  System Coherence: {status['system_health']['coherence']:.3f}")
        print(f"  System strengthened and ready for pattern discovery 🥔⚡")
    
    def identify_high_quality_weeks(self):
        """
        PASS 1: Quickly scan all weeks and identify which ones had 95%+ predictions
        Don't run LLM yet - just mark the weeks
        """
        print(f"\n{'='*60}")
        print(f"PASS 1: IDENTIFYING HIGH-QUALITY WEEKS")
        print(f"Scanning for weeks with 95%+ confident correct predictions")
        print(f"{'='*60}")
        
        sample_ticker = list(self.historical_data.keys())[0]
        all_dates = self.historical_data[sample_ticker]['dates']
        
        week_num = 0
        week_size = 5
        total_predictions = 0
        high_quality_predictions = 0
        
        print(f"\nScanning {len(all_dates)} dates across {len(self.historical_data)} tickers...")
        print(f"Expected total predictions: ~{len(all_dates) // week_size * len(self.historical_data)}\n")
        
        for i in range(0, len(all_dates) - week_size*2, week_size):
            week_num += 1
            
            # Update signals for this week
            week_data = {}
            for ticker, data in self.historical_data.items():
                if i+week_size <= len(data['close']):
                    start_price = data['close'][i]
                    end_price = data['close'][i+week_size-1]
                    
                    if start_price and end_price and start_price > 0:
                        change_pct = ((end_price - start_price) / start_price) * 100
                        self.engine.update_signal_from_market(ticker, change_pct)
                        week_data[ticker] = {'change_pct': change_pct, 'start': start_price, 'end': end_price}
            
            # Quick prediction check (no LLM)
            week_has_quality = False
            week_quality_tickers = []
            
            for ticker in self.historical_data.keys():
                if i+week_size*2 <= len(self.historical_data[ticker]['close']):
                    pred = self.engine.get_prediction_from_signals(ticker)
                    total_predictions += 1
                    
                    # Get actual result
                    actual_start = self.historical_data[ticker]['close'][i+week_size]
                    actual_end = self.historical_data[ticker]['close'][i+week_size*2-1]
                    
                    if actual_start and actual_end and actual_start > 0:
                        actual_change = ((actual_end - actual_start) / actual_start) * 100
                        actual_direction = 'bullish' if actual_change > 0 else 'bearish'
                        was_correct = (pred['prediction'] == actual_direction)
                        
                        # Check if high quality
                        if pred['confidence'] >= self.STRENGTH_THRESHOLD and was_correct:
                            high_quality_predictions += 1
                            week_has_quality = True
                            week_quality_tickers.append({
                                'ticker': ticker,
                                'confidence': pred['confidence'],
                                'prediction': pred['prediction'],
                                'actual_change': actual_change
                            })
            
            # Save week if it has quality predictions
            if week_has_quality:
                self.high_quality_weeks.append({
                    'week_num': week_num,
                    'date_index': i,
                    'week_data': week_data,
                    'quality_tickers': week_quality_tickers
                })
            
            # Progress every 50 weeks
            if week_num % 50 == 0:
                quality_rate = (high_quality_predictions / total_predictions * 100) if total_predictions > 0 else 0
                print(f\"  Week {week_num}: {len(self.high_quality_weeks)} quality weeks found, \"\n                      f\"{high_quality_predictions}/{total_predictions} predictions were 95%+ ({quality_rate:.1f}%)\")\n        \n        print(f\"\\n{'='*60}\")\n        print(f\"PASS 1 COMPLETE\")\n        print(f\"{'='*60}\")\n        print(f\"Total weeks scanned: {week_num}\")\n        print(f\"Total predictions made: {total_predictions}\")\n        print(f\"High-quality predictions (95%+): {high_quality_predictions}\")\n        print(f\"Weeks with quality predictions: {len(self.high_quality_weeks)}\")\n        \n        quality_rate = (high_quality_predictions / total_predictions * 100) if total_predictions > 0 else 0\n        print(f\"\\nQuality rate: {quality_rate:.2f}%\")\n        print(f\"Expected FCI accuracy after retraining: ~{quality_rate:.1f}%\")\n    \n    def discover_patterns_from_quality_weeks(self):\n        \"\"\"\n        PASS 2: Run LLM pattern discovery ONLY on the weeks we identified\n        Much faster since we skip the 99% of weeks with no quality signals\n        \"\"\"\n        print(f\"\\n{'='*60}\")\n        print(f\"PASS 2: PATTERN DISCOVERY FROM QUALITY WEEKS\")\n        print(f\"Running LLM analysis on {len(self.high_quality_weeks)} weeks\")\n        print(f\"{'='*60}\\n\")\n        \n        for idx, week_info in enumerate(self.high_quality_weeks):\n            week_num = week_info['week_num']\n            week_data = week_info['week_data']\n            quality_tickers = week_info['quality_tickers']\n            \n            if (idx + 1) % 10 == 0:\n                print(f\"  Processing quality week {idx+1}/{len(self.high_quality_weeks)}...\")\n            \n            # Build summary focusing on the quality tickers\n            summary_lines = []\n            for qt in quality_tickers:\n                summary_lines.append(\n                    f\"{qt['ticker']}: VERIFIED {qt['confidence']:.1%} confidence, \"\n                    f\"predicted {qt['prediction']}, actual {qt['actual_change']:+.1f}%\"\n                )\n            \n            # Add other tickers for context\n            for ticker, info in list(week_data.items())[:10]:\n                if ticker not in [qt['ticker'] for qt in quality_tickers]:\n                    summary_lines.append(f\"{ticker}: {info['change_pct']:+.1f}%\")\n            \n            summary = \"\\n\".join(summary_lines)\n            \n            prompt = f\"\"\"Week {week_num} had VERIFIED high-confidence predictions.\n\n{summary}\n\nFind 2-3 stock correlations that explain these successful predictions.\n\nREQUIRED FORMAT:\nPATTERN: [name]\nSTOCKS: [TICKER1, TICKER2]\nCORRELATION: high\nSIGNAL: [prediction]\n\nSTART WITH \"PATTERN:\"\"\" \n\n            llm_response = self.ollama.generate(prompt, max_tokens=400)\n            \n            # Clean response\n            import re\n            llm_response = re.sub(r'<think>.*?</think>', '', llm_response, flags=re.DOTALL | re.IGNORECASE)\n            llm_response = re.sub(r'<[^>]+>', '', llm_response)\n            \n            if 'PATTERN:' in llm_response:\n                pattern_start = llm_response.find('PATTERN:')\n                llm_response = llm_response[pattern_start:]\n            \n            # Extract patterns\n            patterns = self._extract_patterns(llm_response, week_num)\n            \n            for pattern in patterns:\n                pattern['verified_confidence'] = max([qt['confidence'] for qt in quality_tickers])\n                pattern['strength'] = 0.95\n                self.high_purity_patterns.append(pattern)\n                \n                # Create glyph\n                if 'stocks' in pattern and len(pattern['stocks']) >= 2:\n                    pattern_name = f\"HighPurity_{pattern['name'].replace(' ', '_')[:20]}\"\n                    ticker1, ticker2 = pattern['stocks'][0], pattern['stocks'][1]\n                    self.engine.create_pattern_from_correlation(pattern_name, ticker1, ticker2, 0.95)\n        \n        print(f\"\\n✓ Discovered {len(self.high_purity_patterns)} high-purity patterns\")\n    \n    def _extract_patterns(self, llm_response: str, week_num: int) -> List[Dict]:\n        \"\"\"Extract patterns from LLM response\"\"\"\n        patterns = []\n        lines = llm_response.split('\\n')\n        current = {}\n        \n        for line in lines:\n            line = line.strip()\n            if line.startswith('PATTERN:'):\n                if current:\n                    patterns.append(current)\n                current = {'week': week_num, 'name': line.replace('PATTERN:', '').strip()}\n            elif line.startswith('STOCKS:'):\n                import re\n                tickers = re.findall(r'\\b[A-Z]{2,5}\\b', line)\n                current['stocks'] = tickers[:2]\n            elif line.startswith('SIGNAL:'):\n                current['signal'] = line.replace('SIGNAL:', '').strip()\n        \n        if current and 'stocks' in current:\n            patterns.append(current)\n        \n        return patterns\n    \n    def save_patterns(self, filename: str = \"high_purity_patterns.json\"):\n        \"\"\"Save high-purity patterns\"\"\"\n        output = {\n            'patterns': self.high_purity_patterns,\n            'quality_weeks': self.high_quality_weeks,\n            'config': {\n                'strength_threshold': self.STRENGTH_THRESHOLD,\n                'total_quality_weeks': len(self.high_quality_weeks),\n                'total_patterns': len(self.high_purity_patterns)\n            }\n        }\n        \n        with open(filename, 'w') as f:\n            json.dump(output, f, indent=2)\n        \n        print(f\"\\n✓ Saved to {filename}\")\n\n\nif __name__ == \"__main__\":\n    print(\"\"\"\n╔══════════════════════════════════════════════════════════════╗\n║                                                              ║\n║       FAST HIGH PURITY PATTERN GENERATOR                     ║\n║   Two-pass approach: Scan first, discover second             ║\n║                                                              ║\n╚══════════════════════════════════════════════════════════════╝\n\"\"\")\n    \n    generator = FastHighPurityGenerator()\n    \n    if not generator.ollama.test_connection():\n        print(\"\\n✗ Ollama not running!\")\n        exit(1)\n    \n    print(f\"✓ Ollama connected\")\n    print(f\"✓ Threshold: {generator.STRENGTH_THRESHOLD:.1%}\\n\")\n    \n    # Full 14 years\n    generator.load_training_data(\"2010-01-01\", \"2024-12-31\", max_tickers=50)\n    \n    # Pass 1: Fast scan (no LLM)\n    generator.identify_high_quality_weeks()\n    \n    # Pass 2: Pattern discovery on quality weeks only\n    generator.discover_patterns_from_quality_weeks()\n    \n    # Save\n    generator.save_patterns()\n    \n    print(\"\"\"\n╔══════════════════════════════════════════════════════════════╗\n║         HIGH PURITY PATTERNS COMPLETE! 🥔✨                  ║\n╚══════════════════════════════════════════════════════════════╝\n\"\"\")\n