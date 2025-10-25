"""
Glyphwheel AGGRESSIVE Day Trader - YOLO Mode
Forces trades with very low thresholds - high risk, high frequency
"""

from glyphwheel_day_trader import GlyphwheelDayTrader
from glyph_market_mapper import GlyphMarketMapper
from glyphwheel_optimized import OptimizedGlyphwheelEngine
from market_interface import MarketInterface

class AggressiveDayTrader(GlyphwheelDayTrader):
    """AGGRESSIVE day trading - lower thresholds, more trades"""
    
    def __init__(self, starting_cash: float = 1000.0):
        super().__init__(starting_cash)
        
        # Override mapper with AGGRESSIVE settings
        self.mapper = AggressiveMarketMapper(self.engine, self.market)

class AggressiveMarketMapper(GlyphMarketMapper):
    """Market mapper with MUCH lower trading thresholds"""
    
    def analyze_glyph_connections_for_trading(self):
        """AGGRESSIVE trading signals - much lower thresholds"""
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
            
            # AGGRESSIVE THRESHOLDS - Trade almost anything!
            if market_strength > 0.45 and connection_count >= 1:  # Was 0.65 and 2
                recommendations["strong_buy"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
            elif market_strength > 0.35 and connection_count >= 0:  # Was 0.55 and 1
                recommendations["buy"].append({
                    "ticker": ticker,
                    "glyph_name": glyph_name,
                    "gsi": gsi,
                    "connections": connection_count,
                    "strength": market_strength
                })
            elif market_strength < 0.30:  # Was 0.50
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
        """Generate AGGRESSIVE trading decision"""
        recommendations = self.analyze_glyph_connections_for_trading()
        
        decision = {
            "action": "HOLD",
            "ticker": None,
            "shares": 0,
            "reasoning": "No signal detected"
        }
        
        # Check for ANY buy signals (not just strong_buy)
        if recommendations["strong_buy"] and available_cash > 0:
            top_buy = recommendations["strong_buy"][0]
            ticker = top_buy["ticker"]
            
            # AGGRESSIVE: Use 80% of cash!
            allocation = available_cash * 0.80
            
            decision = {
                "action": "BUY",
                "ticker": ticker,
                "allocation": allocation,
                "reasoning": f"AGGRESSIVE buy: GSI={top_buy['gsi']:.3f}, "
                           f"Connections={top_buy['connections']}, "
                           f"Strength={top_buy['strength']:.3f}"
            }
        elif recommendations["buy"] and available_cash > 0:  # Also buy on regular buy signals!
            top_buy = recommendations["buy"][0]
            ticker = top_buy["ticker"]
            
            allocation = available_cash * 0.60
            
            decision = {
                "action": "BUY",
                "ticker": ticker,
                "allocation": allocation,
                "reasoning": f"Moderate buy: GSI={top_buy['gsi']:.3f}, "
                           f"Connections={top_buy['connections']}"
            }
        elif recommendations["sell"]:
            for sell_candidate in recommendations["sell"]:
                ticker = sell_candidate["ticker"]
                if ticker in current_holdings and current_holdings[ticker]["shares"] > 0:
                    decision = {
                        "action": "SELL",
                        "ticker": ticker,
                        "shares": current_holdings[ticker]["shares"],
                        "reasoning": f"Weak signal: GSI={sell_candidate['gsi']:.3f}"
                    }
                    break
        
        return decision


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL AGGRESSIVE DAY TRADING                          ║
║   YOLO Mode - High Risk, High Frequency                      ║
║   Lower Thresholds = More Trades                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Initialize aggressive trader
    trader = AggressiveDayTrader(starting_cash=1000.0)
    
    # Configuration
    TRAIN_START = "2020-01-01"
    TRAIN_END = "2020-12-31"
    MAX_TICKERS = 50
    
    print(f"\nConfiguration:")
    print(f"  Trading Period: {TRAIN_START} to {TRAIN_END}")
    print(f"  Max Tickers: {MAX_TICKERS}")
    print(f"  Starting Cash: $1,000.00")
    print(f"  Strategy: AGGRESSIVE Day Trading")
    print(f"  Thresholds: LOWERED (0.45 vs 0.65)")
    print(f"  Position Size: 80% of cash per trade!")
    
    # Load data
    load_result = trader.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    if load_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load market data.")
        exit(1)
    
    # Train
    train_result = trader.train_glyphwheel(recursion_cycles=5, stress_intensity=0.7)
    
    # Run aggressive day trading
    result = trader.run_day_trading_backtest()
    
    # Compare to buy-and-hold
    comparison = trader.compare_to_buy_and_hold()
    
    # Save results
    trader.save_day_trading_results("aggressive_day_trading_results.json")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           AGGRESSIVE DAY TRADING COMPLETE                     ║
╚══════════════════════════════════════════════════════════════╝
""")
