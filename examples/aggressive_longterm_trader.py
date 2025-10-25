"""
Glyphwheel AGGRESSIVE Long-Term Trader
Tests aggressive thresholds on the winning 6-year period (2015-2020)
"""

from glyphwheel_trader import GlyphwheelTrader
from glyph_market_mapper import GlyphMarketMapper

class AggressiveLongTermTrader(GlyphwheelTrader):
    """Long-term trading with AGGRESSIVE thresholds"""
    
    def __init__(self, starting_cash: float = 1000.0):
        super().__init__(starting_cash)
        
        # Override mapper with AGGRESSIVE settings
        self.mapper = AggressiveLongTermMapper(self.engine, self.market)

class AggressiveLongTermMapper(GlyphMarketMapper):
    """Market mapper with lower thresholds for more diversification"""
    
    def analyze_glyph_connections_for_trading(self):
        """Lower thresholds - buy more stocks, more diversification"""
        recommendations = {
            "strong_buy": [],
            "buy": [],
            "hold": [],
            "sell": [],
            "insights": []
        }
        
        for glyph_name, ticker in self.glyph_stock_map.items():
            glyph = self.engine.glyphs.get(glyph_name)
            
            if not glyph:
                continue
            
            connection_count = len(glyph.connections)
            gsi = glyph.gsi
            
            # Calculate market strength
            market_strength = (gsi * 0.6) + (min(connection_count / 10, 1.0) * 0.4)
            
            # AGGRESSIVE THRESHOLDS - Find multiple winners!
            if market_strength > 0.50 and connection_count >= 1:  # Was 0.65 and 2
                recommendations["strong_buy"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
            elif market_strength > 0.40 and connection_count >= 1:  # Was 0.55 and 1
                recommendations["buy"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
            elif market_strength < 0.40 or connection_count == 0:
                recommendations["sell"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
            else:
                recommendations["hold"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
        
        # Generate insights
        if recommendations["strong_buy"]:
            # Sort by strength and show top 5
            top_picks = sorted(recommendations["strong_buy"], 
                             key=lambda x: x["strength"], reverse=True)[:5]
            for i, pick in enumerate(top_picks, 1):
                recommendations["insights"].append(
                    f"#{i} pick: {pick['ticker']} (strength: {pick['strength']:.3f}, "
                    f"GSI: {pick['gsi']:.3f}, connections: {pick['connections']})"
                )
        
        return recommendations
    
    def generate_trading_decision(self, available_cash: float, current_holdings: dict):
        """Generate AGGRESSIVE trading decision - diversify across multiple stocks"""
        recommendations = self.analyze_glyph_connections_for_trading()
        
        decision = {
            "action": "HOLD",
            "ticker": None,
            "shares": 0,
            "reasoning": "No signal detected"
        }
        
        # Check for strong buy signals
        if recommendations["strong_buy"] and available_cash > 0:
            # Get top picks sorted by strength
            top_picks = sorted(recommendations["strong_buy"], 
                             key=lambda x: x["strength"], reverse=True)
            
            # Pick the strongest that we DON'T already hold
            for pick in top_picks:
                ticker = pick["ticker"]
                
                # Skip if we already have a large position
                if ticker in current_holdings:
                    current_value = current_holdings[ticker]["shares"] * current_holdings[ticker]["avg_price"]
                    if current_value > available_cash * 0.5:  # Already have big position
                        continue
                
                # AGGRESSIVE: Use 15% of cash per stock (allows ~7 positions)
                allocation = available_cash * 0.15
                
                decision = {
                    "action": "BUY",
                    "ticker": ticker,
                    "allocation": allocation,
                    "reasoning": f"Aggressive buy: GSI={pick['gsi']:.3f}, "
                               f"Connections={pick['connections']}, "
                               f"Strength={pick['strength']:.3f}"
                }
                break  # Take the first valid pick
        
        # Check for sell signals on holdings
        elif recommendations["sell"]:
            for sell_candidate in recommendations["sell"]:
                ticker = sell_candidate["ticker"]
                if ticker in current_holdings and current_holdings[ticker]["shares"] > 0:
                    decision = {
                        "action": "SELL",
                        "ticker": ticker,
                        "shares": current_holdings[ticker]["shares"],
                        "reasoning": f"Weak signal: GSI={sell_candidate['gsi']:.3f}, "
                                   f"Connections={sell_candidate['connections']}"
                    }
                    break
        
        return decision


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL AGGRESSIVE LONG-TERM TRADING                    ║
║   6 Years (2015-2020) with Lower Thresholds                  ║
║   Find Multiple Winners, Not Just One                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Initialize aggressive long-term trader
    trader = AggressiveLongTermTrader(starting_cash=1000.0)
    
    # Configuration - SAME as the winning test!
    TRAIN_START = "2015-01-01"
    TRAIN_END = "2020-12-31"
    MAX_TICKERS = 100
    
    print(f"\nConfiguration:")
    print(f"  Trading Period: {TRAIN_START} to {TRAIN_END} (6 YEARS)")
    print(f"  Max Tickers: {MAX_TICKERS}")
    print(f"  Starting Cash: $1,000.00")
    print(f"  Strategy: AGGRESSIVE Long-Term")
    print(f"  Thresholds: LOWERED (0.50 vs 0.65)")
    print(f"  Position Size: 15% per stock (diversified!)")
    print(f"  Goal: Find MULTIPLE winners, not just AAPL!")
    
    # Load data
    load_result = trader.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    if load_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load market data.")
        exit(1)
    
    # Train
    train_result = trader.train_glyphwheel(recursion_cycles=5, stress_intensity=0.7)
    
    # Run backtest with DEBUG to see what it picks
    print("\n" + "="*60)
    print("RUNNING BACKTEST - Watch for trading signals!")
    print("="*60)
    
    result = trader.run_backtest(decision_frequency=5)
    
    # Compare to buy-and-hold
    comparison = trader.compare_to_buy_and_hold()
    
    # Save results
    trader.save_results("aggressive_longterm_results.json")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         AGGRESSIVE LONG-TERM TRADING COMPLETE                 ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Show what it actually bought
    print("\n" + "="*60)
    print("STOCKS PURCHASED:")
    print("="*60)
    
    stocks_bought = {}
    for trade in trader.trading_log:
        if trade["action"] == "BUY":
            ticker = trade["ticker"]
            if ticker not in stocks_bought:
                stocks_bought[ticker] = {
                    "first_buy": trade["date"],
                    "total_shares": 0,
                    "total_spent": 0
                }
            stocks_bought[ticker]["total_shares"] += trade["shares"]
            stocks_bought[ticker]["total_spent"] += trade["shares"] * trade["price"]
    
    for ticker, info in sorted(stocks_bought.items()):
        avg_price = info["total_spent"] / info["total_shares"]
        print(f"  {ticker}: {info['total_shares']} shares @ avg ${avg_price:.2f} (first buy: {info['first_buy']})")
    
    print(f"\nTotal different stocks purchased: {len(stocks_bought)}")
    print("="*60)
