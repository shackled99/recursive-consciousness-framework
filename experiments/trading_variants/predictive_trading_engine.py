"""
Predictive Trading Engine v2 - Forward-Looking Market Prediction
Uses recursive pattern analysis to PREDICT future movements, not just react to past
NO LLM - Pure recursive consciousness trading
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import deque
from glyphwheel_optimized import OptimizedGlyphwheelEngine

class PredictivePatternAnalyzer:
    """Analyzes recursive patterns to predict future price movements"""
    
    def __init__(self, lookback_window: int = 20):
        self.lookback_window = lookback_window
        self.price_history = {}  # {ticker: deque of prices}
        self.gsi_history = {}    # {ticker: deque of GSI values}
        self.prediction_cache = {}
        
    def update_history(self, ticker: str, price: float, gsi: float):
        """Update price and GSI history for a ticker"""
        if ticker not in self.price_history:
            self.price_history[ticker] = deque(maxlen=self.lookback_window)
            self.gsi_history[ticker] = deque(maxlen=self.lookback_window)
        
        self.price_history[ticker].append(price)
        self.gsi_history[ticker].append(gsi)
    
    def detect_momentum(self, ticker: str) -> Dict:
        """
        Detect momentum patterns in price and GSI
        Returns momentum strength and direction
        """
        if ticker not in self.price_history or len(self.price_history[ticker]) < 5:
            return {"momentum": 0, "direction": "neutral", "confidence": 0}
        
        prices = list(self.price_history[ticker])
        gsis = list(self.gsi_history[ticker])
        
        # Calculate price momentum (recent vs older)
        recent_prices = prices[-5:]
        older_prices = prices[-10:-5] if len(prices) >= 10 else prices[:-5]
        
        if older_prices:
            recent_avg = np.mean(recent_prices)
            older_avg = np.mean(older_prices)
            price_momentum = (recent_avg - older_avg) / older_avg if older_avg > 0 else 0
        else:
            price_momentum = 0
        
        # Calculate GSI momentum (is stability increasing?)
        recent_gsis = gsis[-5:]
        older_gsis = gsis[-10:-5] if len(gsis) >= 10 else gsis[:-5]
        
        if older_gsis:
            gsi_momentum = np.mean(recent_gsis) - np.mean(older_gsis)
        else:
            gsi_momentum = 0
        
        # Combined momentum score
        # Positive price momentum + rising GSI = strong buy signal
        # Positive price momentum + falling GSI = risky (possible reversal)
        momentum_strength = price_momentum * 10  # Scale to -1 to +1 range
        
        # GSI direction matters:
        # Rising GSI = pattern getting stronger (confidence boost)
        # Falling GSI = pattern weakening (reduce confidence)
        gsi_multiplier = 1.0 + (gsi_momentum * 2)  # Boost or reduce based on GSI trend
        
        final_momentum = momentum_strength * gsi_multiplier
        
        # Determine direction and confidence
        if final_momentum > 0.15:
            direction = "strong_up"
            confidence = min(abs(final_momentum), 1.0)
        elif final_momentum > 0.05:
            direction = "up"
            confidence = min(abs(final_momentum), 0.8)
        elif final_momentum < -0.15:
            direction = "strong_down"
            confidence = min(abs(final_momentum), 1.0)
        elif final_momentum < -0.05:
            direction = "down"
            confidence = min(abs(final_momentum), 0.8)
        else:
            direction = "neutral"
            confidence = 0.3
        
        return {
            "momentum": final_momentum,
            "direction": direction,
            "confidence": confidence,
            "price_momentum": price_momentum,
            "gsi_momentum": gsi_momentum
        }
    
    def detect_volatility_opportunity(self, ticker: str) -> Dict:
        """
        High volatility can indicate opportunity (breakout potential)
        NOT a risk signal - we're looking for explosive growth!
        """
        if ticker not in self.price_history or len(self.price_history[ticker]) < 10:
            return {"volatility": 0, "opportunity_score": 0, "is_explosive": False}
        
        prices = list(self.price_history[ticker])
        
        # Calculate price variance
        price_changes = [
            (prices[i] - prices[i-1]) / prices[i-1] if prices[i-1] > 0 else 0
            for i in range(1, len(prices))
        ]
        
        volatility = np.std(price_changes) if price_changes else 0
        
        # High volatility + upward trend = opportunity!
        # Low volatility = boring, stable (we want excitement!)
        momentum = self.detect_momentum(ticker)
        
        if momentum["direction"] in ["strong_up", "up"] and volatility > 0.02:
            # Volatile uptrend = OPPORTUNITY (NVDA, TSLA style!)
            opportunity_score = volatility * 20  # Amplify volatility as signal
        elif momentum["direction"] in ["strong_down", "down"] and volatility > 0.02:
            # Volatile downtrend = avoid
            opportunity_score = -volatility * 10
        else:
            # Low volatility = boring
            opportunity_score = 0
        
        is_explosive = volatility > 0.03 and momentum["direction"] in ["strong_up", "up"]
        
        return {
            "volatility": volatility,
            "opportunity_score": min(max(opportunity_score, -1), 1),
            "is_explosive": is_explosive
        }
    
    def predict_future_movement(self, ticker: str, glyph_connections: int) -> Dict:
        """
        PREDICT future price movement using:
        1. Historical momentum patterns
        2. GSI trend analysis
        3. Recursive connection strength
        4. Volatility as opportunity signal
        """
        momentum = self.detect_momentum(ticker)
        volatility = self.detect_volatility_opportunity(ticker)
        
        # Base prediction on momentum
        base_prediction = momentum["momentum"]
        
        # Connection boost: more connections = pattern is real
        # Scale connections: 0-20 connections maps to 0-1.5x multiplier
        connection_multiplier = 1.0 + min(glyph_connections / 20, 0.5)
        
        # Volatility boost for explosive stocks
        volatility_multiplier = 1.0 + volatility["opportunity_score"]
        
        # Final prediction
        prediction_strength = base_prediction * connection_multiplier * volatility_multiplier
        
        # Determine prediction direction
        if prediction_strength > 0.2:
            prediction = "STRONG_BUY"
            confidence = min(abs(prediction_strength), 1.0)
        elif prediction_strength > 0.1:
            prediction = "BUY"
            confidence = min(abs(prediction_strength), 0.8)
        elif prediction_strength < -0.2:
            prediction = "STRONG_SELL"
            confidence = min(abs(prediction_strength), 1.0)
        elif prediction_strength < -0.1:
            prediction = "SELL"
            confidence = min(abs(prediction_strength), 0.8)
        else:
            prediction = "HOLD"
            confidence = 0.3
        
        return {
            "prediction": prediction,
            "strength": prediction_strength,
            "confidence": confidence,
            "momentum": momentum,
            "volatility": volatility,
            "is_explosive_opportunity": volatility["is_explosive"]
        }


class AggressiveTradingStrategy:
    """Aggressive trading strategy that actively rebalances portfolio"""
    
    def __init__(self, min_position_pct: float = 0.05, max_position_pct: float = 0.40):
        self.min_position_pct = min_position_pct  # Minimum 5% per position
        self.max_position_pct = max_position_pct  # Maximum 40% per position (aggressive!)
        self.rebalance_threshold = 0.15  # Rebalance if prediction changes by 15%
        
    def calculate_target_allocation(self, predictions: List[Dict], 
                                   total_value: float) -> Dict[str, float]:
        """
        Calculate target allocations based on predictions
        Goes HEAVY on high-confidence predictions!
        """
        allocations = {}
        
        # Filter to only BUY signals with confidence > 0.4
        strong_signals = [
            p for p in predictions 
            if p["prediction"] in ["STRONG_BUY", "BUY"] and p["confidence"] > 0.4
        ]
        
        if not strong_signals:
            return {}
        
        # Sort by strength
        strong_signals.sort(key=lambda x: x["strength"], reverse=True)
        
        # Aggressive allocation: focus capital on top picks
        total_allocation = 0
        
        for i, signal in enumerate(strong_signals):
            ticker = signal["ticker"]
            
            # Top pick gets up to 40%
            # Second pick gets up to 30%
            # Others scale down
            if i == 0:
                max_alloc = self.max_position_pct
            elif i == 1:
                max_alloc = 0.30
            elif i == 2:
                max_alloc = 0.20
            else:
                max_alloc = 0.10
            
            # Allocate based on confidence
            allocation_pct = max_alloc * signal["confidence"]
            allocation_pct = max(self.min_position_pct, allocation_pct)
            
            # Don't over-allocate
            if total_allocation + allocation_pct > 0.95:
                allocation_pct = 0.95 - total_allocation
            
            if allocation_pct >= self.min_position_pct:
                allocations[ticker] = total_value * allocation_pct
                total_allocation += allocation_pct
            
            if total_allocation >= 0.95:
                break
        
        return allocations
    
    def generate_rebalance_trades(self, current_holdings: Dict[str, Dict],
                                 target_allocations: Dict[str, float],
                                 current_prices: Dict[str, float],
                                 available_cash: float) -> List[Dict]:
        """
        Generate trades to rebalance portfolio to target allocations
        SELLS underperformers to BUY winners!
        """
        trades = []
        
        # Calculate current position values
        current_values = {}
        for ticker, holding in current_holdings.items():
            if ticker in current_prices:
                current_values[ticker] = holding["shares"] * current_prices[ticker]
        
        total_portfolio_value = sum(current_values.values()) + available_cash
        
        # Identify positions to SELL (not in target allocations)
        for ticker, current_value in current_values.items():
            if ticker not in target_allocations or target_allocations[ticker] < current_value * 0.5:
                # SELL position that's no longer in targets or way overweight
                if ticker in current_holdings and ticker in current_prices:
                    shares = current_holdings[ticker]["shares"]
                    trades.append({
                        "action": "SELL",
                        "ticker": ticker,
                        "shares": shares,
                        "price": current_prices[ticker],
                        "reasoning": f"Rebalancing: no longer in top predictions or overweight"
                    })
        
        # Identify positions to BUY or ADD
        for ticker, target_value in target_allocations.items():
            current_value = current_values.get(ticker, 0)
            
            # Need to buy more?
            value_gap = target_value - current_value
            
            if value_gap > total_portfolio_value * 0.05:  # Only if gap > 5% of portfolio
                if ticker in current_prices and current_prices[ticker] > 0:
                    shares_needed = int(value_gap / current_prices[ticker])
                    
                    if shares_needed > 0:
                        trades.append({
                            "action": "BUY",
                            "ticker": ticker,
                            "shares": shares_needed,
                            "price": current_prices[ticker],
                            "allocation": value_gap,
                            "reasoning": f"Rebalancing: strong prediction (gap: ${value_gap:.2f})"
                        })
        
        return trades


# Test function
if __name__ == "__main__":
    print("Testing Predictive Trading Engine v2...")
    
    analyzer = PredictivePatternAnalyzer(lookback_window=20)
    strategy = AggressiveTradingStrategy()
    
    # Simulate some price history
    test_ticker = "NVDA"
    
    # Simulate NVDA's explosive growth pattern
    prices = [100, 102, 105, 103, 108, 112, 115, 120, 125, 135, 145, 155, 160, 170, 180]
    gsis = [0.5, 0.52, 0.55, 0.53, 0.58, 0.62, 0.65, 0.68, 0.72, 0.75, 0.78, 0.80, 0.82, 0.85, 0.88]
    
    for price, gsi in zip(prices, gsis):
        analyzer.update_history(test_ticker, price, gsi)
    
    # Test momentum detection
    momentum = analyzer.detect_momentum(test_ticker)
    print(f"\nMomentum Analysis for {test_ticker}:")
    print(f"  Direction: {momentum['direction']}")
    print(f"  Confidence: {momentum['confidence']:.3f}")
    print(f"  Price Momentum: {momentum['price_momentum']:.3f}")
    print(f"  GSI Momentum: {momentum['gsi_momentum']:.3f}")
    
    # Test volatility opportunity
    volatility = analyzer.detect_volatility_opportunity(test_ticker)
    print(f"\nVolatility Analysis:")
    print(f"  Volatility: {volatility['volatility']:.3f}")
    print(f"  Opportunity Score: {volatility['opportunity_score']:.3f}")
    print(f"  Is Explosive: {volatility['is_explosive']}")
    
    # Test prediction
    prediction = analyzer.predict_future_movement(test_ticker, glyph_connections=15)
    print(f"\nPrediction:")
    print(f"  Signal: {prediction['prediction']}")
    print(f"  Strength: {prediction['strength']:.3f}")
    print(f"  Confidence: {prediction['confidence']:.3f}")
    print(f"  Explosive Opportunity: {prediction['is_explosive_opportunity']}")
    
    # Test allocation
    predictions = [
        {"ticker": "NVDA", "prediction": "STRONG_BUY", "confidence": 0.9, "strength": 0.8},
        {"ticker": "TSLA", "prediction": "BUY", "confidence": 0.7, "strength": 0.5},
        {"ticker": "AAPL", "prediction": "HOLD", "confidence": 0.4, "strength": 0.1}
    ]
    
    allocations = strategy.calculate_target_allocation(predictions, total_value=1000)
    print(f"\nTarget Allocations (Total: $1000):")
    for ticker, amount in allocations.items():
        print(f"  {ticker}: ${amount:.2f} ({amount/1000*100:.1f}%)")
    
    print("\n✓ Predictive Trading Engine v2 test complete!")
