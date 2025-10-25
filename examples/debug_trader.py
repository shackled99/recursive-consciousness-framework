"""
DEBUG Version - See why Glyphwheel won't buy NVDA, TSLA, etc.
Shows ALL stock ratings, not just the ones it buys
"""

from aggressive_longterm_trader import AggressiveLongTermTrader
import json

class DebugTrader(AggressiveLongTermTrader):
    """Debug version that shows us EVERYTHING"""
    
    def run_backtest(self, decision_frequency: int = 5):
        """Run backtest with FULL DEBUG output"""
        
        print(f"\n{'='*60}")
        print(f"RUNNING DEBUG BACKTEST")
        print(f"{'='*60}")
        
        if not self.historical_data:
            return {"error": "No historical data loaded"}
        
        # Get date range
        sample_ticker = list(self.historical_data.keys())[0]
        dates = self.historical_data[sample_ticker]["dates"]
        
        print(f"\nSimulation Period: {dates[0]} to {dates[-1]}")
        print(f"Total Trading Days: {len(dates)}")
        
        # CRITICAL: Show initial glyph state BEFORE any trades
        print(f"\n{'='*60}")
        print("INITIAL GLYPH ANALYSIS (After Training)")
        print(f"{'='*60}")
        self._detailed_glyph_analysis()
        
        # Simulate day by day
        decision_count = 0
        for day_idx in range(1, len(dates)):
            current_date = dates[day_idx]
            
            # Update glyph GSI based on market movements
            self.mapper.update_glyphs_from_market_data(self.historical_data, day_idx)
            
            # Make trading decisions periodically
            if day_idx % decision_frequency == 0:
                decision_count += 1
                
                # DETAILED analysis every 10 decisions (every ~50 days)
                if decision_count % 10 == 0:
                    print(f"\n{'='*60}")
                    print(f"DECISION #{decision_count} - {current_date}")
                    print(f"{'='*60}")
                    self._detailed_glyph_analysis()
                
                self._make_trading_decision(day_idx, current_date)
            
            # Track performance
            if day_idx % 10 == 0:
                self._record_performance(day_idx, current_date)
        
        # Final performance
        final_performance = self._calculate_final_performance()
        
        print(f"\n{'='*60}")
        print(f"BACKTEST COMPLETE")
        print(f"{'='*60}")
        
        return final_performance
    
    def _detailed_glyph_analysis(self):
        """Show detailed analysis of ALL stocks"""
        
        # Get recommendations
        recommendations = self.mapper.analyze_glyph_connections_for_trading()
        
        # Collect ALL stock data
        all_stocks = []
        
        for glyph_name, ticker in self.mapper.glyph_stock_map.items():
            glyph = self.engine.glyphs.get(glyph_name)
            if not glyph:
                continue
            
            connection_count = len(glyph.connections)
            gsi = glyph.gsi
            market_strength = (gsi * 0.6) + (min(connection_count / 10, 1.0) * 0.4)
            
            # Categorize
            if market_strength > 0.50 and connection_count >= 1:
                category = "STRONG_BUY"
            elif market_strength > 0.40 and connection_count >= 1:
                category = "BUY"
            elif market_strength < 0.40 or connection_count == 0:
                category = "SELL"
            else:
                category = "HOLD"
            
            all_stocks.append({
                "ticker": ticker,
                "gsi": gsi,
                "connections": connection_count,
                "strength": market_strength,
                "category": category
            })
        
        # Sort by strength
        all_stocks.sort(key=lambda x: x["strength"], reverse=True)
        
        # Show top 20 and key stocks
        print("\nTOP 20 STOCKS BY STRENGTH:")
        print("-" * 80)
        print(f"{'Rank':<6} {'Ticker':<8} {'GSI':<8} {'Conn':<6} {'Strength':<10} {'Category':<12}")
        print("-" * 80)
        
        for i, stock in enumerate(all_stocks[:20], 1):
            print(f"{i:<6} {stock['ticker']:<8} {stock['gsi']:<8.3f} {stock['connections']:<6} "
                  f"{stock['strength']:<10.3f} {stock['category']:<12}")
        
        # Check specifically for TSLA, NVDA, and other big names
        print(f"\n{'='*80}")
        print("KEY STOCKS ANALYSIS:")
        print(f"{'='*80}")
        
        key_tickers = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META"]
        
        for ticker in key_tickers:
            stock_data = next((s for s in all_stocks if s["ticker"] == ticker), None)
            if stock_data:
                rank = all_stocks.index(stock_data) + 1
                print(f"\n{ticker}:")
                print(f"  Rank: #{rank} out of {len(all_stocks)}")
                print(f"  GSI: {stock_data['gsi']:.3f}")
                print(f"  Connections: {stock_data['connections']}")
                print(f"  Strength: {stock_data['strength']:.3f}")
                print(f"  Category: {stock_data['category']}")
                print(f"  Qualifies for buy? {'YES ✓' if stock_data['category'] in ['STRONG_BUY', 'BUY'] else 'NO ✗'}")
            else:
                print(f"\n{ticker}: NOT IN DATASET")
        
        # Show category counts
        print(f"\n{'='*80}")
        print("CATEGORY BREAKDOWN:")
        print("-" * 80)
        strong_buy = sum(1 for s in all_stocks if s["category"] == "STRONG_BUY")
        buy = sum(1 for s in all_stocks if s["category"] == "BUY")
        hold = sum(1 for s in all_stocks if s["category"] == "HOLD")
        sell = sum(1 for s in all_stocks if s["category"] == "SELL")
        
        print(f"  STRONG_BUY: {strong_buy} stocks")
        print(f"  BUY:        {buy} stocks")
        print(f"  HOLD:       {hold} stocks")
        print(f"  SELL:       {sell} stocks")
        print(f"  TOTAL:      {len(all_stocks)} stocks")
        print("="*80)


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL DEBUG MODE                                      ║
║   See EXACTLY why it won't buy NVDA, TSLA, etc.             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Initialize debug trader
    trader = DebugTrader(starting_cash=1000.0)
    
    # Configuration
    TRAIN_START = "2015-01-01"
    TRAIN_END = "2015-03-31"  # Just 3 months for faster debug
    MAX_TICKERS = 100
    
    print(f"\nConfiguration:")
    print(f"  Trading Period: {TRAIN_START} to {TRAIN_END} (3 months for debug)")
    print(f"  Max Tickers: {MAX_TICKERS}")
    print(f"  Aggressive Thresholds: 0.50 (STRONG_BUY), 0.40 (BUY)")
    
    # Load data
    print("\n" + "="*60)
    print("LOADING DATA...")
    print("="*60)
    load_result = trader.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    if load_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load market data.")
        exit(1)
    
    print(f"✓ Loaded {load_result['tickers_loaded']} stocks")
    
    # Train
    print("\n" + "="*60)
    print("TRAINING GLYPHWHEEL...")
    print("="*60)
    train_result = trader.train_glyphwheel(recursion_cycles=5, stress_intensity=0.7)
    
    print(f"\n✓ Training complete!")
    print(f"  Final Coherence: {train_result['final_coherence']:.3f}")
    print(f"  Connections Formed: {train_result['connections_formed']}")
    print(f"  Recursive Depth: {train_result['final_recursive_depth']}")
    
    # Run debug backtest
    result = trader.run_backtest(decision_frequency=5)
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    DEBUG COMPLETE                             ║
╚══════════════════════════════════════════════════════════════╝

Now you can see EXACTLY why Glyphwheel picks what it picks!
""")
