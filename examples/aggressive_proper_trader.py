"""
Glyphwheel AGGRESSIVE Proper Training
Train on 2010-2014, trade AGGRESSIVELY on 2015-2020
Lower thresholds to find MULTIPLE winners from learned patterns
"""

from proper_training_trader import ProperTrainingTrader
from glyph_market_mapper import GlyphMarketMapper

class AggressiveProperTrader(ProperTrainingTrader):
    """Proper training with aggressive trading thresholds"""
    
    def __init__(self, starting_cash: float = 1000.0):
        super().__init__(starting_cash)
        
        # Override mapper with AGGRESSIVE settings AFTER initialization
        # We'll do this in load_split_data
        
    def load_split_data(self, train_start: str, train_end: str, 
                       trade_start: str, trade_end: str, max_tickers: int = 100):
        """Load data and set up aggressive mapper"""
        
        result = super().load_split_data(train_start, train_end, trade_start, trade_end, max_tickers)
        
        # NOW override with aggressive mapper
        self.mapper = AggressiveProperMapper(self.engine, self.market)
        
        # Re-initialize the glyph-stock mapping with aggressive mapper
        self.mapper.glyph_stock_map = {}
        self.mapper.stock_glyph_map = {}
        mapping_result = self.mapper.initialize_glyph_stock_mapping(
            list(self.historical_data.keys())
        )
        
        print(f"\n🔥 AGGRESSIVE MODE ACTIVATED!")
        print(f"   Lower thresholds will find MULTIPLE winners")
        
        return result

class AggressiveProperMapper(GlyphMarketMapper):
    """Aggressive mapper for proper training scenario"""
    
    def analyze_glyph_connections_for_trading(self):
        """AGGRESSIVE thresholds - find multiple winners from learned patterns"""
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
            
            # AGGRESSIVE THRESHOLDS - Lower than normal
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
        
        return recommendations
    
    def generate_trading_decision(self, available_cash: float, current_holdings: dict):
        """Generate AGGRESSIVE trading decision - diversify"""
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
            
            # Pick the strongest that we DON'T already have large positions in
            for pick in top_picks:
                ticker = pick["ticker"]
                
                # Skip if we already have a large position
                if ticker in current_holdings:
                    current_value = current_holdings[ticker]["shares"] * current_holdings[ticker]["avg_price"]
                    if current_value > available_cash * 0.5:
                        continue
                
                # AGGRESSIVE: Use 15% per stock (diversify across ~7 stocks)
                allocation = available_cash * 0.15
                
                decision = {
                    "action": "BUY",
                    "ticker": ticker,
                    "allocation": allocation,
                    "reasoning": f"Aggressive buy (learned pattern): GSI={pick['gsi']:.3f}, "
                               f"Connections={pick['connections']}, Strength={pick['strength']:.3f}"
                }
                break
        
        # Also consider regular buy signals if no strong_buy
        elif recommendations["buy"] and available_cash > 0:
            buy_picks = sorted(recommendations["buy"],
                             key=lambda x: x["strength"], reverse=True)
            
            for pick in buy_picks:
                ticker = pick["ticker"]
                
                if ticker in current_holdings:
                    current_value = current_holdings[ticker]["shares"] * current_holdings[ticker]["avg_price"]
                    if current_value > available_cash * 0.3:
                        continue
                
                # Moderate buy: 10% allocation
                allocation = available_cash * 0.10
                
                decision = {
                    "action": "BUY",
                    "ticker": ticker,
                    "allocation": allocation,
                    "reasoning": f"Moderate buy (learned pattern): GSI={pick['gsi']:.3f}, "
                               f"Connections={pick['connections']}"
                }
                break
        
        # Check for sell signals
        elif recommendations["sell"]:
            for sell_candidate in recommendations["sell"]:
                ticker = sell_candidate["ticker"]
                if ticker in current_holdings and current_holdings[ticker]["shares"] > 0:
                    decision = {
                        "action": "SELL",
                        "ticker": ticker,
                        "shares": current_holdings[ticker]["shares"],
                        "reasoning": f"Weak learned pattern: GSI={sell_candidate['gsi']:.3f}"
                    }
                    break
        
        return decision


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL AGGRESSIVE PROPER TRADING                       ║
║   Best of Both Worlds: Proper Training + Aggressive Trades   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Initialize trader
    trader = AggressiveProperTrader(starting_cash=1000.0)
    
    # Configuration
    TRAIN_START = "2010-01-01"
    TRAIN_END = "2014-12-31"
    TRADE_START = "2015-01-01"
    TRADE_END = "2020-12-31"
    MAX_TICKERS = 100
    
    print(f"\n📊 EXPERIMENT DESIGN:")
    print(f"{'='*60}")
    print(f"  Training Period: {TRAIN_START} to {TRAIN_END} (5 years)")
    print(f"  Trading Period:  {TRADE_START} to {TRADE_END} (6 years)")
    print(f"  Max Tickers: {MAX_TICKERS}")
    print(f"  Starting Cash: $1,000.00")
    print(f"\n  🎯 Strategy: Learn from past, trade AGGRESSIVELY on future")
    print(f"  🔥 Lower thresholds (0.50 vs 0.65)")
    print(f"  📈 15% per stock (diversify across ~7 winners)")
    
    # Load split data
    load_result = trader.load_split_data(
        TRAIN_START, TRAIN_END, TRADE_START, TRADE_END, MAX_TICKERS
    )
    
    if load_result["train_tickers"] == 0 or load_result["trade_tickers"] == 0:
        print("\n✗ Failed to load market data.")
        exit(1)
    
    # Train on historical patterns
    train_result = trader.train_on_historical_patterns()
    
    # Trade aggressively on future data
    print(f"\n{'='*60}")
    print(f"NOW TRADING AGGRESSIVELY ON FUTURE DATA (2015-2020)")
    print(f"Using learned patterns with lower thresholds")
    print(f"{'='*60}")
    
    backtest_result = trader.run_backtest(decision_frequency=5)
    
    # Compare to buy-and-hold
    comparison = trader.compare_to_buy_and_hold()
    
    # Save results
    trader.save_results("aggressive_proper_training_results.json")
    
    # Show what it bought
    print(f"\n{'='*60}")
    print("STOCKS PURCHASED (AGGRESSIVE MODE):")
    print(f"{'='*60}")
    
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
        print(f"  {ticker}: {info['total_shares']} shares @ avg ${avg_price:.2f} (first: {info['first_buy']})")
    
    print(f"\n✓ Total different stocks: {len(stocks_bought)}")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║       AGGRESSIVE PROPER TRAINING COMPLETE                     ║
╚══════════════════════════════════════════════════════════════╝
""")
