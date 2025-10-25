"""
Pattern Validation - Test Discovered Patterns on Unseen Data
Loads trained patterns and validates predictions against actual market movements
"""

import json
import os
from typing import Dict, List
# Assuming DualLayerEngine and MarketInterface are correctly defined and imported
from dual_layer_engine import DualLayerEngine
from market_interface import MarketInterface

class PatternValidator:
    """Validate discovered patterns on unseen data"""
    
    # Define the official PSCC threshold for the Filtered Confidence Index (FCI)
    # This will be auto-detected from the pattern file
    PSCC_THRESHOLD = 0.780  # Default, will be updated from config
    
    def __init__(self, patterns_file: str = "dual_layer_patterns.json"):
        self.engine = DualLayerEngine()
        self.market = MarketInterface()
        
        # Load trained patterns
        with open(patterns_file, 'r') as f:
            data = json.load(f)
            self.patterns = data['patterns']
            self.trained_status = data.get('system_status', {})
            
            # AUTO-DETECT THRESHOLD from config if available
            if 'config' in data and 'strength_threshold' in data['config']:
                self.PSCC_THRESHOLD = data['config']['strength_threshold']
                print(f"✓ Auto-detected PSCC threshold: {self.PSCC_THRESHOLD:.3f} (from pattern file config)")
            else:
                print(f"✓ Using default PSCC threshold: {self.PSCC_THRESHOLD:.3f}")
        
        print(f"✓ Loaded {len(self.patterns)} trained patterns")
        
        # Rebuild pattern glyphs from saved data
        self._rebuild_pattern_glyphs()
    
    def _rebuild_pattern_glyphs(self):
        """Recreate pattern glyphs from saved patterns"""
        print("\n🔧 Rebuilding pattern glyphs...")
        
        for pattern in self.patterns:
            if 'stocks' in pattern and len(pattern['stocks']) >= 2:
                pattern_name = f"Pattern_{pattern['name'].replace(' ', '_')[:20]}"
                ticker1, ticker2 = pattern['stocks'][0], pattern['stocks'][1]
                strength = pattern.get('strength', 0.5)
                
                # Add signal glyphs if not present
                if f"Stock_{ticker1}" not in self.engine.signal_glyphs:
                    self.engine.add_signal_glyph(f"Stock_{ticker1}", 0.5)
                if f"Stock_{ticker2}" not in self.engine.signal_glyphs:
                    self.engine.add_signal_glyph(f"Stock_{ticker2}", 0.5)
                
                # Create pattern
                # NOTE: The engine must use the original pattern's strength, not a fixed value, for glyph creation
                self.engine.create_pattern_from_correlation(pattern_name, ticker1, ticker2, strength)
        
        print(f"✓ Rebuilt {len(self.engine.pattern_glyphs)} pattern glyphs")
        print(f"✓ Rebuilt {len(self.engine.signal_glyphs)} signal glyphs")
    
    def validate_on_test_data(self, start_date: str, end_date: str, max_tickers: int = 50):
        """
        Validate patterns on unseen test data
        """
        print(f"\n{'='*60}")
        print(f"PATTERN VALIDATION ON TEST DATA")
        print(f"{'='*60}")
        print(f"Test Period: {start_date} to {end_date}")
        
        # Get tickers from patterns
        pattern_tickers = set()
        for pattern in self.patterns:
            if 'stocks' in pattern:
                pattern_tickers.update(pattern['stocks'])
        
        tickers_to_test = list(pattern_tickers)[:max_tickers]
        print(f"\nTesting {len(tickers_to_test)} tickers from patterns...")
        
        # Fetch test data
        test_data = self.market.fetch_batch_historical_data(
            tickers_to_test, start_date, end_date, delay=0.5
        )
        
        print(f"✓ Loaded test data for {len(test_data)} tickers")
        
        # Run validation
        results = self._run_validation(test_data)
        
        return results
    
    def _run_validation(self, test_data: Dict) -> Dict:
        """Run validation and track accuracy"""
        print(f"\n{'='*60}")
        print(f"RUNNING VALIDATION")
        print(f"{'='*60}")
        
        predictions = []
        correct = 0
        total = 0
        
        # Test weekly predictions
        sample_ticker = list(test_data.keys())[0]
        all_dates = test_data[sample_ticker]['dates']
        
        week_size = 5
        for i in range(0, len(all_dates) - week_size*2, week_size):
            # Use week N to predict week N+1
            current_week = all_dates[i:i+week_size]
            next_week = all_dates[i+week_size:i+week_size*2]
            
            if len(current_week) < 3 or len(next_week) < 3:
                continue
            
            # Update signals with current week data
            for ticker, data in test_data.items():
                if i+week_size <= len(data['close']):
                    start_price = data['close'][i]
                    end_price = data['close'][i+week_size-1]
                    
                    if start_price and end_price and start_price > 0:
                        change_pct = ((end_price - start_price) / start_price) * 100
                        # Assuming the engine handles mapping ticker to the correct signal glyph
                        self.engine.update_signal_from_market(ticker, change_pct)
            
            # Make predictions for next week
            for ticker in test_data.keys():
                if i+week_size*2 <= len(test_data[ticker]['close']):
                    # Get prediction
                    pred = self.engine.get_prediction_from_signals(ticker)
                    
                    # Get actual result
                    actual_start = test_data[ticker]['close'][i+week_size]
                    actual_end = test_data[ticker]['close'][i+week_size*2-1]
                    
                    if actual_start and actual_end and actual_start > 0:
                        actual_change = ((actual_end - actual_start) / actual_start) * 100
                        actual_direction = 'bullish' if actual_change > 0 else 'bearish'
                        
                        # Check if prediction was correct
                        if pred['prediction'] == actual_direction:
                            correct += 1
                        
                        total += 1
                        
                        # Save prediction result
                        predictions.append({
                            'ticker': ticker,
                            'week': f"{current_week[0]} to {current_week[-1]}",
                            'predicted': pred['prediction'],
                            'actual': actual_direction,
                            'confidence': pred['confidence'],
                            'actual_change': actual_change,
                            'correct': pred['prediction'] == actual_direction
                        })
            
            # Progress update every 10 weeks
            if (i // week_size) % 10 == 0:
                week_num = i // week_size
                accuracy = (correct / total * 100) if total > 0 else 0
                print(f"  Week {week_num}: {correct}/{total} correct ({accuracy:.1f}%)")
        
        # Final results
        accuracy = (correct / total * 100) if total > 0 else 0
        
        print(f"\n{'='*60}")
        print(f"VALIDATION RESULTS")
        print(f"{'='*60}")
        print(f"Total Predictions: {total}")
        print(f"Correct: {correct}")
        print(f"Overall Accuracy: {accuracy:.2f}%")
        
        # Breakdown by confidence (The crucial FCI calculation)
        fci_conf = [p for p in predictions if p['confidence'] >= self.PSCC_THRESHOLD]
        if fci_conf:
            fci_correct = sum(1 for p in fci_conf if p['correct'])
            fci_acc = (fci_correct / len(fci_conf) * 100)
            
            print(f"\nFiltered Confidence Index (FCI) - PSCC >= {self.PSCC_THRESHOLD:.3f}:")
            print(f"  Total Filtered Trades: {len(fci_conf)}")
            print(f"  Correct Filtered Trades: {fci_correct}")
            print(f"  FCI Accuracy: {fci_acc:.2f}%")
        
        # Show some examples
        print(f"\n{'='*60}")
        print(f"SAMPLE PREDICTIONS")
        print(f"{'='*60}")
        
        # Show 5 correct and 5 incorrect
        correct_samples = [p for p in predictions if p['correct']][:5]
        incorrect_samples = [p for p in predictions if not p['correct']][:5]
        
        print("\n✓ Correct Predictions:")
        for p in correct_samples:
            print(f"  {p['ticker']}: Predicted {p['predicted']}, "
                  f"Actual {p['actual']} ({p['actual_change']:+.1f}%), "
                  f"Confidence: {p['confidence']:.2f}")
        
        print("\n✗ Incorrect Predictions:")
        for p in incorrect_samples:
            print(f"  {p['ticker']}: Predicted {p['predicted']}, "
                  f"Actual {p['actual']} ({p['actual_change']:+.1f}%), "
                  f"Confidence: {p['confidence']:.2f}")
        
        return {
            'total': total,
            'correct': correct,
            'accuracy': accuracy,
            'predictions': predictions
        }
    
    def save_results(self, results: Dict, filename: str = "validation_results.json"):
        """Save validation results"""
        # Save in same directory as patterns
        # NOTE: Using a relative path for cross-platform compatibility
        base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
        save_path = os.path.join(base_dir, filename)

        # Create a more structured results dictionary for the output file
        save_data = {
            "validation_metadata": {
                "test_period": "2015-01-01 to 2020-12-31",
                "patterns_loaded": len(self.patterns),
                "pscc_threshold": self.PSCC_THRESHOLD
            },
            "overall_results": {
                "total_predictions": results['total'],
                "correct": results['correct'],
                "accuracy_pct": results['accuracy']
            },
            # Calculate FCI for structured output
            "fci_results": {},
            "predictions_log": results['predictions']
        }
        
        # Recalculate FCI for structured output
        fci_conf = [p for p in results['predictions'] if p['confidence'] >= self.PSCC_THRESHOLD]
        if fci_conf:
            fci_correct = sum(1 for p in fci_conf if p['correct'])
            fci_acc = (fci_correct / len(fci_conf) * 100)
            save_data["fci_results"] = {
                "total_filtered_trades": len(fci_conf),
                "correct_filtered_trades": fci_correct,
                "fci_accuracy_pct": fci_acc
            }

        with open(save_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\n✓ Results saved to {save_path}")


# Main
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           PATTERN VALIDATION - Test on Unseen Data           ║
║       Load trained patterns, make predictions, check accuracy  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Load patterns and validate
    # Check for high purity patterns first, fall back to regular patterns
    import os
    
    high_purity_path = "high_purity_patterns.json"
    regular_path = "dual_layer_patterns.json"
    
    if os.path.exists(high_purity_path):
        print("\n🎯 Found high_purity_patterns.json - using high-purity patterns!")
        patterns_path = high_purity_path
    elif os.path.exists(regular_path):
        print("\n📊 Using dual_layer_patterns.json (regular patterns)")
        patterns_path = regular_path
    else:
        print("\n✗ No pattern files found!")
        exit(1)
    
    try:
        validator = PatternValidator(patterns_path)
    except Exception as e:
        print(f"CRITICAL ERROR: Could not load patterns file. Error: {e}")
        exit()
    
    # Test on 2010-2024 (matching the 14-year training period)
    TEST_START = "2010-01-01"
    TEST_END = "2024-12-31"
    
    print(f"\nValidation Configuration:")
    print(f"  Test Period: {TEST_START} to {TEST_END} (6 years, UNSEEN)")
    print(f"  PSCC Threshold (for FCI): {validator.PSCC_THRESHOLD:.3f}")
    print(f"  Patterns Loaded: {len(validator.patterns)}")
    
    # Run validation
    results = validator.validate_on_test_data(TEST_START, TEST_END, max_tickers=50)
    
    # Save results
    validator.save_results(results, filename="validation_results.json")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║            VALIDATION COMPLETE                               ║
║    Did the patterns actually work? 🥔🔮                      ║
╚══════════════════════════════════════════════════════════════╝
""")
