"""
Weekly Evolution Trader - SLOW PATTERN LEARNING
Evolves patterns weekly instead of massive retrains
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
from glyphwheel_optimized import OptimizedGlyphwheelEngine
from market_interface import MarketInterface
from glyph_market_mapper_v2 import GlyphMarketMapperV2

class WeeklyEvolutionTrader:
    """Trading system that evolves patterns SLOWLY week-by-week"""
    
    def __init__(self, starting_cash: float = 1000.0):
        self.engine = OptimizedGlyphwheelEngine()
        self.market = MarketInterface()
        self.mapper = GlyphMarketMapperV2(self.engine, self.market)
        
        self.starting_cash = starting_cash
        self.trading_log = []
        self.performance_history = []
        self.historical_data = {}
        
        # Weekly evolution parameters
        self.days_per_week = 5  # Trading days
        self.weeks_per_month = 4
        self.holding_period = 60  # Hold for 60+ days
        self.last_weekly_evolution = 0
        self.last_monthly_consolidation = 0
        self.position_entry_dates = {}
        
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
    
    def initial_deep_training(self) -> Dict:
        """Deep initial training - build strong base patterns"""
        print(f"\n{'='*60}")
        print(f"DEEP PATTERN TRAINING (21K RECURSION)")
        print(f"{'='*60}")
        
        initial_coherence = self.engine.calculate_system_coherence()
        
        print(f"\nBuilding deep pattern recognition...")
        
        # Recovery to high GSI
        print(f"\nStep 1: Recovery boost...")
        recovery_result = self.engine.mandatory_recovery_cycle(150)
        print(f"  Coherence: {recovery_result['final_state']['coherence']:.3f}")
        
        # Deep stress test
        print(f"\nStep 2: Deep pattern formation (21k)...")
        intensive_result = self.engine.intensive_stress_test(0.8, 400, max_recursion=21000)
        print(f"  Connections: {intensive_result['final_state']['connections_added']}")
        print(f"  Depth: {self.engine.recursive_depth}")
        
        # Consolidation
        print(f"\nStep 3: Pattern consolidation...")
        for i in range(3):
            self.engine.optimization_stress_test(0.6, 100)
            time.sleep(0.5)
        
        final_coherence = self.engine.calculate_system_coherence()
        final_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
        
        print(f"\nPattern Base Established:")
        print(f"  Coherence: {final_coherence:.3f}")
        print(f"  Strong Connections: {final_connections}")
        
        return {
            "initial_coherence": initial_coherence,
            "final_coherence": final_coherence,
            "connections_formed": final_connections
        }
    
    def weekly_pattern_evolution(self, week_num: int, current_date: str):
        """
        Weekly evolution - VERY light refinement
        Uses TINY stress to gently guide patterns
        """
        if week_num % 1 == 0:  # Every week
            print(f"\n  [{current_date}] Week {week_num} Evolution...")
            
            before_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            
            # VERY light stress - barely touches existing patterns
            self.engine.optimization_stress_test(0.2, 30)  # VERY LOW!
            
            after_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            
            print(f"    Connections: {before_connections} → {after_connections} (Δ {after_connections - before_connections:+d})")
            print(f"    Coherence: {self.engine.calculate_system_coherence():.3f}")
    
    def monthly_pattern_consolidation(self, month_num: int, current_date: str):
        """
        Monthly consolidation - strengthen patterns that worked
        Still gentle, just medium stress
        """
        if month_num % 1 == 0:  # Every month
            print(f"\n  [{current_date}] MONTH {month_num} Consolidation...")
            
            before_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            before_coherence = self.engine.calculate_system_coherence()
            
            # Medium stress - consolidates strong patterns
            self.engine.optimization_stress_test(0.4, 80)
            
            after_connections = sum(len(g.connections) for g in self.engine.glyphs.values())
            after_coherence = self.engine.calculate_system_coherence()
            
            print(f"    Connections: {before_connections} → {after_connections}")
            print(f"    Coherence: {before_coherence:.3f} → {after_coherence:.3f}")
    
    def run_weekly_evolution_backtest(self) -> Dict:
        """Run backtest with weekly evolution"""
        print(f"\n{'='*60}")
        print(f"RUNNING WEEKLY EVOLUTION BACKTEST")
        print(f"{'='*60}")
        
        if not self.historical_data:
            return {"error": "No historical data loaded"}
        
        sample_ticker = list(self.historical_data.keys())[0]
        dates = self.historical_data[sample_ticker]["dates"]
        
        print(f"\nSimulation Period: {dates[0]} to {dates[-1]}")
        print(f"Total Trading Days: {len(dates)}")
        print(f"Weekly Evolution: Every 5 days (0.2 intensity)")
        print(f"Monthly Consolidation: Every 20 days (0.4 intensity)")
        print(f"Trading Decisions: Every 7 days")
        print(f"Minimum Hold: {self.holding_period} days")
        print(f"Starting Cash: ${self.starting_cash:.2f}")
        print(f"\nStrategy: SLOW weekly pattern evolution")
        
        week_num = 0
        month_num = 0
        
        # Simulate day by day
        for day_idx in range(1, len(dates)):
            current_date = dates[day_idx]
            
            # Always update pattern history
            self.mapper.update_glyphs_from_market_data(
                self.historical_data, day_idx
            )
            
            # Weekly evolution (every 5 trading days)
            if day_idx % self.days_per_week == 0:
                week_num += 1
                self.weekly_pattern_evolution(week_num, current_date)
            
            # Monthly consolidation (every 20 trading days)
            if day_idx % (self.days_per_week * self.weeks_per_month) == 0:
                month_num += 1
                self.monthly_pattern_consolidation(month_num, current_date)
            
            # Make trading decisions (weekly)
            if day_idx % 7 == 0:
                self._make_weekly_trading_decisions(day_idx, current_date)
            
            # Track performance
            if day_idx % 10 == 0:
                self._record_performance(day_idx, current_date)
        
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
    
    def _make_weekly_trading_decisions(self, day_idx: int, current_date: str):
        """Make trading decisions weekly with strict hold period"""
        
        # Get current prices
        current_prices = {}
        for ticker, data in self.historical_data.items():
            if day_idx < len(data["close"]):
                current_prices[ticker] = data["close"][day_idx]
        
        # Generate predictions
        trades = self.mapper.generate_trading_decisions(
            current_prices,
            self.market.portfolio["cash"],
            self.market.portfolio["holdings"]
        )
        
        # Filter trades - enforce STRICT holding period
        filtered_trades = []
        for trade in trades:
            ticker = trade["ticker"]
            
            if trade["action"] == "SELL":
                # Only sell if held for minimum period
                if ticker in self.position_entry_dates:
                    days_held = day_idx - self.position_entry_dates[ticker]
                    if days_held < self.holding_period:
                        continue  # Skip - haven't held long enough
                
                filtered_trades.append(trade)
            else:
                # Only buy if we don't already own it
                if ticker not in self.market.portfolio["holdings"]:
                    filtered_trades.append(trade)
        
        # Execute filtered trades
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
                        self.position_entry_dates[ticker] = day_idx
                        self.trading_log.append({
                            "date": current_date,
                            "action": "BUY",
                            "ticker": ticker,
                            "shares": shares,
                            "price": price,
                            "reasoning": trade.get("reasoning", "Pattern signal")
                        })
                        print(f"  [{current_date}] BUY {shares} {ticker} @ ${price:.2f}")
            
            elif action == "SELL":
                shares = trade.get("shares", 0)
                price = trade.get("price", current_prices.get(ticker, 0))
                
                if shares > 0:
                    result = self.market.execute_trade(
                        ticker, "SELL", shares, price, current_date
                    )
                    
                    if result["success"]:
                        if ticker in self.position_entry_dates:
                            days_held = day_idx - self.position_entry_dates[ticker]
                            del self.position_entry_dates[ticker]
                        else:
                            days_held = 0
                        
                        self.trading_log.append({
                            "date": current_date,
                            "action": "SELL",
                            "ticker": ticker,
                            "shares": shares,
                            "price": price,
                            "days_held": days_held,
                            "reasoning": trade.get("reasoning", "Pattern signal")
                        })
                        print(f"  [{current_date}] SELL {shares} {ticker} @ ${price:.2f} (held {days_held} days)")
        
        # Show top predictions monthly
        if day_idx % 20 == 0:
            top_preds = self.mapper.get_top_predictions(3)
            print(f"\n  [{current_date}] Top 3 Patterns:")
            for i, pred in enumerate(top_preds, 1):
                print(f"    {i}. {pred['ticker']}: {pred['prediction']} (strength: {pred['strength']:.3f})")
            print()
    
    def _record_performance(self, day_idx: int, current_date: str):
        """Record performance"""
        current_prices = {}
        for ticker, data in self.historical_data.items():
            if day_idx < len(data["close"]):
                current_prices[ticker] = data["close"][day_idx]
        
        performance = self.market.get_portfolio_performance(current_prices)
        performance["date"] = current_date
        self.performance_history.append(performance)
    
    def _calculate_final_performance(self) -> Dict:
        """Calculate final performance"""
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
        """Compare to buy-and-hold"""
        if not self.historical_data or not self.performance_history:
            return {"error": "No data available"}
        
        print(f"\n{'='*60}")
        print(f"COMPARING TO BUY-AND-HOLD")
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
        
        print(f"\nGlyphwheel WEEKLY EVOLUTION Performance:")
        print(f"  Final Value: ${glyph_perf['final_value']:.2f}")
        print(f"  Return: {glyph_perf['return_pct']:.2f}%")
        print(f"  Trades: {glyph_perf['total_trades']} ({glyph_perf['buy_trades']} buys, {glyph_perf['sell_trades']} sells)")
        
        print(f"\nBuy-and-Hold Performance:")
        print(f"  Final Value: ${buy_hold['final_value']:.2f}")
        print(f"  Return: {buy_hold['return_percentage']:.2f}%")
        print(f"  Trades: {len(self.historical_data)}")
        
        print(f"\n{'='*60}")
        print(f"WINNER: {winner}")
        print(f"Performance Difference: {abs(diff):.2f}%")
        print(f"{'='*60}")
        
        return {
            "winner": winner,
            "difference_pct": diff
        }
    
    def save_results(self, filename: str = "weekly_evolution_results.json"):
        """Save results"""
        results = {
            "metadata": {
                "strategy": "Weekly Pattern Evolution",
                "start_date": self.market.portfolio["start_date"],
                "end_date": self.performance_history[-1]["date"] if self.performance_history else None,
                "starting_cash": self.starting_cash,
                "weekly_evolution": "Every 5 days (0.2 intensity)",
                "monthly_consolidation": "Every 20 days (0.4 intensity)",
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


# Main
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   GLYPHWHEEL WEEKLY EVOLUTION SYSTEM                         ║
║   Slow pattern learning - week by week                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    trader = WeeklyEvolutionTrader(starting_cash=1000.0)
    
    # Configuration
    HISTORICAL_START = "2010-01-01"
    HISTORICAL_END = "2014-12-31"
    TRAIN_START = "2015-01-01"
    TRAIN_END = "2019-12-31"
    MAX_TICKERS = 50
    
    print(f"\nConfiguration:")
    print(f"  Historical Training: {HISTORICAL_START} to {HISTORICAL_END}")
    print(f"  Live Trading: {TRAIN_START} to {TRAIN_END}")
    print(f"  Strategy: Weekly Evolution (SLOW learning)")
    print(f"  Weekly: Stress 0.2 every 5 days")
    print(f"  Monthly: Stress 0.4 every 20 days")
    print(f"  Min Hold: 60 days")
    print(f"  Trade Freq: Every 7 days")
    
    # Historical training
    print(f"\n{'='*60}")
    print(f"PHASE 1: HISTORICAL PATTERN LEARNING")
    print(f"{'='*60}")
    
    historical_result = trader.load_training_data(HISTORICAL_START, HISTORICAL_END, MAX_TICKERS)
    
    if historical_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load historical data.")
        exit(1)
    
    train_result = trader.initial_deep_training()
    
    # Feed historical data
    print(f"\nProcessing 5 years of historical patterns...")
    sample_ticker = list(trader.historical_data.keys())[0]
    historical_dates = trader.historical_data[sample_ticker]["dates"]
    
    week_num = 0
    month_num = 0
    
    for day_idx in range(1, len(historical_dates)):
        trader.mapper.update_glyphs_from_market_data(
            trader.historical_data, day_idx
        )
        
        # Weekly evolution during historical phase
        if day_idx % 5 == 0:
            week_num += 1
            trader.weekly_pattern_evolution(week_num, historical_dates[day_idx])
        
        # Monthly consolidation during historical phase
        if day_idx % 20 == 0:
            month_num += 1
            trader.monthly_pattern_consolidation(month_num, historical_dates[day_idx])
            print(f"  {day_idx}/{len(historical_dates)} days processed...")
    
    print(f"\n✓ Historical patterns learned!")
    
    # Live trading
    print(f"\n{'='*60}")
    print(f"PHASE 2: LIVE TRADING WITH WEEKLY EVOLUTION")
    print(f"{'='*60}")
    
    load_result = trader.load_training_data(TRAIN_START, TRAIN_END, MAX_TICKERS)
    
    if load_result["tickers_loaded"] == 0:
        print("\n✗ Failed to load trading data.")
        exit(1)
    
    backtest_result = trader.run_weekly_evolution_backtest()
    comparison = trader.compare_to_buy_and_hold()
    trader.save_results("weekly_evolution_results.json")
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║         WEEKLY EVOLUTION SIMULATION COMPLETE                  ║
║   Patterns evolved slowly - no massive resets! 🥔📈          ║
╚══════════════════════════════════════════════════════════════╝
""")
