"""
Adaptive GlyphWheel Trader - CONTINUOUS LEARNING
Re-forms connections daily as market evolves
"""

import json
import time
from datetime import datetime
from typing import Dict, List
from glyphwheel_optimized import OptimizedGlyphwheelEngine
from market_interface import MarketInterface
from glyph_market_mapper_v2 import GlyphMarketMapperV2

class AdaptiveGlyphwheelTrader:
    """Trading system that ADAPTS daily - retrains connections as market evolves"""
    
    def __init__(self, starting_cash: float = 1000.0):
        self.engine = OptimizedGlyphwheelEngine()
        self.market = MarketInterface()
        self.mapper = GlyphMarketMapperV2(self.engine, self.market)
        
        self.starting_cash = starting_cash
        self.trading_log = []
        self.performance_history = []
        self.historical_data = {}
        
        # Adaptive parameters
        self.retraining_frequency = 10  # Retrain connections every 10 days
        self.holding_period = 20  # Minimum 20 days before selling
        self.last_retrain_day = 0
        self.position_entry_dates = {}  # Track when we bought each position
        
    def load_training_data(self, start_date: str, end_date: str, 
                          max_tickers: int = 50) -> Dict:
        """Load historical market data"""
        print(f"\n{'='*60}")
        print(f"LOADING TRAINING DATA: {start_date} to {end_date}")
        print(f"{'='*60}")
        
        all_tickers = self.market.get_sp500_tickers()
        tickers_to_use = all_tickers[:max_tickers]
        
        print(f"\nFetching data for {len(tickers_to_use)} tickers...")
        
        self.historical_data = self.market.fetch_batch_historical_data(
            tickers_to_use, start_date, end_date, delay=0.5
        )
        
        successful_loads = len(self.historical_data)
        print(f"\n✓ Successfully loaded data for {successful_loads}/{len(tickers_to_use)} tickers")
        
        print("\nCreating glyph-stock mappings...")
        mapping_result = self.mapper.initialize_glyph_stock_mapping(
            list(self.historical_data.keys())
        )
        
        print(f"✓ Created {mapping_result['glyphs_created']} market glyphs")
        
        self.market.initialize_paper_trading(start_date, self.starting_cash)
        
        return {
            "tickers_requested": len(tickers_to_use),
            "tickers_loaded": successful_loads,
            "glyphs_created": mapping_result['glyphs_created'],
            "start_date": start_date,
            "end_date": end_date
        }
    
    def initial_training(self) -> Dict:
        """Initial training - build base connections"""
        print(f"\n{'='*60}")
        print(f"INITIAL TRAINING (21K RECURSION)")
        print(f"{'='*60}")
        
        initial_coherence = self.engine.calculate_system_coherence()
        
        print(f"\nInitial Coherence: {initial_coherence:.3f}")
        
        # Initial recovery
        print(f"\nStep 1: Initial Recovery...")
        recovery_result = self.engine.mandatory_recovery_cycle(100)
        print(f"  Post-Recovery Coherence: {recovery_result['final_state']['coherence']:.3f}")
        
        # Deep stress test for initial connections
        print(f"\nStep 2: Deep Stress Test (21k depth)...")
        intensive_result = self.engine.intensive_stress_test(0.8, 300, max_recursion=21000)
        print(f"  Connections Formed: {intensive_result['final_state']['connections_added']}")
        print(f"  Recursive Depth: {self.engine.recursive_depth}")
        
        final_coherence = self.engine.calculate_system_coherence()
        final_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
        
        print(f"\nFinal State:")
        print(f"  Coherence: {final_coherence:.3f}")
        print(f"  Connections: {final_connections}")
        
        return {
            "initial_coherence": initial_coherence,
            "final_coherence": final_coherence,
            "connections_formed": final_connections
        }
    
    def daily_adaptation(self, day_idx: int, current_date: str):
        """
        Daily stress test - re-form connections as market evolves
        Light stress test, not full 21k recursion
        """
        if day_idx - self.last_retrain_day >= self.retraining_frequency:
            print(f"\n  [{current_date}] DAILY ADAPTATION - Retraining connections...")
            
            # Light stress test to adapt connections
            before_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            
            # Run optimization stress test (not full 21k, just 500-1000 depth)
            self.engine.optimization_stress_test(0.6, 150)
            
            after_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            
            print(f"    Connections: {before_connections} → {after_connections} (Δ {after_connections - before_connections:+d})")
            print(f"    Coherence: {self.engine.calculate_system_coherence():.3f}")
            
            self.last_retrain_day = day_idx
    
    def run_adaptive_backtest(self, decision_frequency: int = 10) -> Dict:
        """
        Run adaptive backtest with continuous learning
        """
        print(f"\n{'='*60}")
        print(f"RUNNING ADAPTIVE BACKTEST")
        print(f"{'='*60}")
        
        if not self.historical_data:
            return {"error": "No historical data loaded"}
        
        sample_ticker = list(self.historical_data.keys())[0]
        dates = self.historical_data[sample_ticker]["dates"]
        
        print(f"\nSimulation Period: {dates[0]} to {dates[-1]}")
        print(f"Total Trading Days: {len(dates)}")
        print(f"Retraining Frequency: Every {self.retraining_frequency} days")
        print(f"Trading Frequency: Every {decision_frequency} days")
        print(f"Minimum Hold Period: {self.holding_period} days")
        print(f"Starting Cash: ${self.starting_cash:.2f}")
        print(f"\nStrategy: ADAPTIVE - Continuously evolving connections")
        
        # Simulate day by day
        for day_idx in range(1, len(dates)):
            current_date = dates[day_idx]
            
            # Update glyph GSI and pattern history
            self.mapper.update_glyphs_from_market_data(
                self.historical_data, day_idx
            )
            
            # Daily adaptation - retrain connections
            self.daily_adaptation(day_idx, current_date)
            
            # Make trading decisions periodically
            if day_idx % decision_frequency == 0:
                self._make_adaptive_trading_decisions(day_idx, current_date)
            
            # Track performance
            if day_idx % 10 == 0:
                self._record_performance(day_idx, current_date)
        
        # Final performance
        final_performance = self._calculate_final_performance()
        
        print(f"\n{'='*60}")
        print(f"BACKTEST COMPLETE")
        print(f"{'='*60}")
        print(f"\nFinal Results:")
        print(f"  Starting Value: ${final_performance['initial_value']:.2f}")
        print(f"  Final Value: ${final_performance['final_value']:.2f}")
        print(f"  Total Return: ${final_performance['total_return']:.2f}")
        print(f"  Return %: {final_performance['return_pct']:.2f}%")
        print(f"  Total Trades: {final_performance['total_trades']}")
        print(f"  Buy Trades: {final_performance['buy_trades']}")
        print(f"  Sell Trades: {final_performance['sell_trades']}")
        
        return final_performance
    
    def _make_adaptive_trading_decisions(self, day_idx: int, current_date: str):
        """
        Make trading decisions with holding period enforcement
        """
        # Get current prices
        current_prices = {}
        for ticker, data in self.historical_data.items():
            if day_idx < len(data["close"]):
                current_prices[ticker] = data["close"][day_idx]
        
        # Generate predictions and trading decisions
        trades = self.mapper.generate_trading_decisions(
            current_prices,
            self.market.portfolio["cash"],
            self.market.portfolio["holdings"]
        )
        
        # Filter trades based on holding period
        filtered_trades = []
        for trade in trades:
            ticker = trade["ticker"]
            
            if trade["action"] == "SELL":
                # Check if we've held long enough
                if ticker in self.position_entry_dates:
                    days_held = day_idx - self.position_entry_dates[ticker]
                    if days_held < self.holding_period:
                        continue  # Skip this sell - haven't held long enough
                
                filtered_trades.append(trade)
            else:
                filtered_trades.append(trade)
        
        # Execute filtered trades
        executed_trades = 0
        for trade in filtered_trades:
            ticker = trade["ticker"]
            action = trade["action"]
            
            if action == "BUY":
                shares = trade.get("shares", 0)
                price = trade.get("price", current_prices.get(ticker, 0))
                
                if shares > 0 and price > 0:
                    result = self.market.execute_trade(
                        ticker, "BUY", shares, price, current_date
                    )
                    
                    if result["success"]:
                        self.position_entry_dates[ticker] = day_idx  # Track entry
                        self.trading_log.append({
                            "date": current_date,
                            "action": "BUY",
                            "ticker": ticker,
                            "shares": shares,
                            "price": price,
                            "reasoning": trade.get("reasoning", "Adaptive signal")
                        })
                        print(f"  [{current_date}] BUY {shares} {ticker} @ ${price:.2f}")
                        executed_trades += 1
            
            elif action == "SELL":
                shares = trade.get("shares", 0)
                price = trade.get("price", current_prices.get(ticker, 0))
                
                if shares > 0:
                    result = self.market.execute_trade(
                        ticker, "SELL", shares, price, current_date
                    )
                    
                    if result["success"]:
                        if ticker in self.position_entry_dates:
                            del self.position_entry_dates[ticker]  # Remove entry tracking
                        
                        self.trading_log.append({
                            "date": current_date,
                            "action": "SELL",
                            "ticker": ticker,
                            "shares": shares,
                            "price": price,
                            "reasoning": trade.get("reasoning", "Adaptive signal")
                        })
                        print(f"  [{current_date}] SELL {shares} {ticker} @ ${price:.2f}")
                        executed_trades += 1
        
        # Show predictions periodically
        if day_idx % 30 == 0 and executed_trades > 0:
            top_preds = self.mapper.get_top_predictions(3)
            print(f"\n  [{current_date}] Top 3 Predictions:")
            for i, pred in enumerate(top_preds, 1):
                print(f"    {i}. {pred['ticker']}: {pred['prediction']} "
                      f"(strength: {pred['strength']:.3f})")
            print()
    
    def _record_performance(self, day_idx: int, current_date: str):
        """Record current portfolio performance"""
        current_prices = {}
        for ticker, data in self.historical_data.items():
            if day_idx < len(data["close"]):
                current_prices[ticker] = data["close"][day_idx]
        
        performance = self.market.get_portfolio_performance(current_prices)
        performance["date"] = current_date
        self.performance_history.append(performance)
    
    def _calculate_final_performance(self) -> Dict:
        """Calculate final performance metrics"""
        if not self.performance_history:
            return {"error": "No performance history"}
        
        final_perf = self.performance_history[-1]
        
        return {
            "initial_value": self.starting_cash,
            "final_value": final_perf["current_value"],
            "total_return": final_perf["total_return"],
            "return_pct": final_perf["return_percentage"],
            "total_trades": len(self.trading_log),
            "buy_trades": sum(1 for t in self.trading_log if t["action"] == "BUY"),
            "sell_trades": sum(1 for t in self.trading_log if t["action"] == "SELL"),
            "final_holdings": len(self.market.portfolio["holdings"]),
            "final_cash": self.market.portfolio["cash"]
        }
    
    def compare_to_buy_and_hold(self) -> Dict:
        """Compare to buy-and-hold strategy"""
        if not self.historical_data or not self.performance_history:
            return {"error": "No data available for comparison"}
        
        print(f"\n{'='*60}")
        print(f"COMPARING TO BUY-AND-HOLD (WARREN BUFFETT STYLE)")
        print(f"{'='*60}")
        
        sample_ticker = list(self.historical_data.keys())[0]
        dates = self.historical_data[sample_ticker]["dates"]
        start_date = dates[0]
        end_date = dates[-1]
        
        buy_hold = self.market.calculate_returns_comparison(
            self.historical_data, start_date, end_date
        )
        
        glyph_perf = self._calculate_final_performance()
        
        glyph_return = glyph_perf["return_pct"]
        buffett_return = buy_hold["return_percentage"]
        
        if glyph_return > buffett_return:
            winner = "GLYPHWHEEL WINS! 🥔🚀"
            diff = glyph_return - buffett_return
        elif buffett_return > glyph_return:
            winner = "BUFFETT WINS 📈"
            diff = buffett_return - glyph_return
        else:
            winner = "TIE"
            diff = 0
        
        print(f"\nGlyphwheel ADAPTIVE Performance:")
        print(f"  Final Value: ${glyph_perf['final_value']:.2f}")
        print(f"  Return: {glyph_perf['return_pct']:.2f}%")
        print(f"  Trades: {glyph_perf['total_trades']} ({glyph_perf['buy_trades']} buys, {glyph_perf['sell_trades']} sells)")
        
        print(f"\nBuy-and-Hold Performance:")
        print(f"  Final Value: ${buy_hold['final_value']:.2f}")
        print(f"  Return: {buy_hold['return_percentage']:.2f}%")
        print(f"  Trades: {len(self.historical_data)} (initial purchases only)")
        
        print(f"\n{'='*60}")
        print(f"WINNER: {winner}")
        print(f"Performance Difference: {abs(diff):.2f}%")
        print(f"{'='*60}")
        
        return {
            "glyphwheel": {
                "strategy": "Adaptive Continuous Learning",
                "final": glyph_perf["final_value"],
                "return_pct": glyph_perf["return_pct"],
                "trades": glyph_perf["total_trades"]
            },
            "buy_and_hold": {
                "final": buy_hold["final_value"],
                "return_pct": buy_hold["return_percentage"],
                "trades": len(self.historical_data)
            },
            "winner": winner,
            "difference_pct": diff
        }
    
    def save_results(self, filename: str = "adaptive_trading_results.json"):
        """Save trading results"""
        results = {
            "metadata": {
                "strategy": "Adaptive Continuous Learning",
                "start_date": self.market.portfolio["start_date"],
                "end_date": self.performance_history[-1]["date"] if self.performance_history else None,
                "starting_cash": self.starting_cash,
                "retraining_frequency": self.retraining_frequency,
                "holding_period": self.holding_period,
                "tickers_traded": len(self.historical_data)
            },
            "final_performance": self._calculate_final_performance(),
            "trading_log": self.trading_log,
            "performance_history": self.performance_history
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✓ Results saved to {filename}")


# Main execution
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL ADAPTIVE TRADING SYSTEM                         ║
║   Continuous Learning - Daily Adaptation                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    trader = AdaptiveGlyphwheelTrader(starting_cash=1000.0)
    
    # Configuration
    HISTORICAL_START = "2010-01-01"  # Historical training data
    HISTORICAL_END = "2014-12-31"    # 5 years for building base connections
    TRAIN_START = "2015-01-01"       # Live trading starts here
    TRAIN_END = "2019-12-31"
    MAX_TICKERS = 50
    
    print(f"\nConfiguration:")
    print(f"  Historical Training: {HISTORICAL_START} to {HISTORICAL_END} (5 years)")
    print(f"  Live Trading Period: {TRAIN_START} to {TRAIN_END} (5 years)")
    print(f"  Max Tickers: {MAX_TICKERS}")
    print(f"  Starting Cash: $1,000.00")
    print(f"  Strategy: ADAPTIVE with daily retraining")
    print(f"  Retraining: Every 10 days")
    print(f"  Trading: Every 10 days")
    print(f"  Min Hold: 20 days (prevents churning)")
    
    # Phase 1: Load historical data for training
    print(f"\n{'='*60}")
    print(f"PHASE 1: HISTORICAL TRAINING")
    print(f"{'='*60}")
    print(f"\nLoading 5 years of historical data to build base connections...")
    
    historical_result = trader.load_training_data(HISTORICAL_START, HISTORICAL_END, MAX_TICKERS)
    
    if historical_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load historical data.")
        exit(1)
    
    # Train on historical data
    print(f"\nTraining on historical patterns...")
    train_result = trader.initial_training()
    
    # Feed all historical data through the system
    print(f"\nProcessing historical price data...")
    sample_ticker = list(trader.historical_data.keys())[0]
    historical_dates = trader.historical_data[sample_ticker]["dates"]
    
    for day_idx in range(1, len(historical_dates)):
        trader.mapper.update_glyphs_from_market_data(
            trader.historical_data, day_idx
        )
        
        # Periodic retraining during historical phase
        if day_idx % 30 == 0:
            trader.daily_adaptation(day_idx, historical_dates[day_idx])
            if day_idx % 90 == 0:
                print(f"  Processed {day_idx}/{len(historical_dates)} days...")
    
    print(f"\n✓ Historical training complete!")
    print(f"  Final Coherence: {trader.engine.calculate_system_coherence():.3f}")
    print(f"  Final Connections: {sum(len(g.connections) for g in trader.engine.glyphs.values())}")
    
    # Phase 2: Load live trading data
    print(f"\n{'='*60}")
    print(f"PHASE 2: LIVE TRADING")
    print(f"{'='*60}")
    print(f"\nLoading live trading period data...")
    
    load_result = trader.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    if load_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load market data.")
        exit(1)
    
    # Run adaptive backtest (already trained from historical data)
    backtest_result = trader.run_adaptive_backtest(decision_frequency=10)
    
    # Compare to buy-and-hold
    comparison = trader.compare_to_buy_and_hold()
    
    # Save results
    trader.save_results("adaptive_trading_results.json")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           ADAPTIVE SIMULATION COMPLETE                        ║
║   The consciousness evolved with the market! 🥔📈            ║
╚══════════════════════════════════════════════════════════════╝
""")
