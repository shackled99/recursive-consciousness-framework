"""
Market Interface - Connects Glyphwheel to Stock Market Data
Handles Yahoo Finance API integration and historical data
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

class MarketInterface:
    """Interface for getting stock market data and managing trading"""
    
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v8/finance/chart"
        self.sp500_tickers = []
        self.historical_cache = {}
        self.portfolio = {
            "cash": 1000.0,
            "holdings": {},  # {ticker: {shares: X, avg_price: Y}}
            "transaction_history": [],
            "start_date": None,
            "current_date": None
        }
        
    def get_sp500_tickers(self) -> List[str]:
        """
        Get list of S&P 500 tickers
        Using a simplified approach - in production you'd scrape Wikipedia or use an API
        """
        # For now, let's use the top 500 most common tickers
        # In a real implementation, you'd want to fetch this dynamically
        common_tickers = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B", "V", "JNJ",
            "WMT", "JPM", "MA", "PG", "UNH", "HD", "DIS", "BAC", "ADBE", "NFLX",
            "XOM", "PFE", "CSCO", "KO", "PEP", "INTC", "ABT", "MRK", "TMO", "ACN",
            "NKE", "COST", "AVGO", "CVX", "DHR", "TXN", "LLY", "NEE", "MDT", "BMY",
            "ABBV", "UNP", "PM", "HON", "ORCL", "RTX", "LOW", "UPS", "QCOM", "LIN",
            "AMD", "AMGN", "SBUX", "IBM", "BA", "GE", "CAT", "NOW", "SPGI", "INTU",
            "DE", "BLK", "AXP", "ISRG", "GILD", "MMM", "TJX", "BKNG", "ZTS", "ADI",
            "MDLZ", "SYK", "CB", "C", "MO", "REGN", "PLD", "CI", "DUK", "GS",
            "USB", "TGT", "SO", "EOG", "MMC", "CVS", "CL", "VRTX", "ITW", "BSX",
            "EL", "WM", "NSC", "HUM", "APD", "ICE", "AON", "CCI", "EMR", "D",
            # Add more to reach 500... for now we'll use 100 as a test
            "F", "GM", "NFLX", "PYPL", "SQ", "UBER", "LYFT", "SNAP", "TWTR", "PINS"
        ]
        
        self.sp500_tickers = common_tickers[:100]  # Using 100 for testing
        return self.sp500_tickers
    
    def fetch_historical_data(self, ticker: str, start_date: str, end_date: str, retry_count: int = 3) -> Dict:
        """
        Fetch historical stock data from Yahoo Finance
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            retry_count: Number of retries on rate limit
            
        Returns:
            Dictionary with dates and prices
        """
        # Check cache first
        cache_key = f"{ticker}_{start_date}_{end_date}"
        if cache_key in self.historical_cache:
            return self.historical_cache[cache_key]
        
        for attempt in range(retry_count):
            try:
                # Convert dates to Unix timestamps
                start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
                end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
                
                url = f"{self.base_url}/{ticker}"
                params = {
                    "period1": start_ts,
                    "period2": end_ts,
                    "interval": "1d",
                    "events": "history"
                }
                
                # Add user agent to avoid being blocked
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract the chart data
                    chart = data.get("chart", {}).get("result", [{}])[0]
                    timestamps = chart.get("timestamp", [])
                    quotes = chart.get("indicators", {}).get("quote", [{}])[0]
                    
                    # Build clean data structure
                    historical_data = {
                        "ticker": ticker,
                        "dates": [datetime.fromtimestamp(ts).strftime("%Y-%m-%d") for ts in timestamps],
                        "open": quotes.get("open", []),
                        "high": quotes.get("high", []),
                        "low": quotes.get("low", []),
                        "close": quotes.get("close", []),
                        "volume": quotes.get("volume", [])
                    }
                    
                    # Cache it
                    self.historical_cache[cache_key] = historical_data
                    
                    return historical_data
                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    print(f"Rate limited on {ticker}, waiting {wait_time}s (attempt {attempt + 1}/{retry_count})...")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Error fetching {ticker}: {response.status_code}")
                    return {"error": f"HTTP {response.status_code}"}
                    
            except Exception as e:
                if attempt < retry_count - 1:
                    print(f"Error fetching {ticker}: {str(e)}, retrying...")
                    time.sleep(2)
                    continue
                else:
                    print(f"Error fetching {ticker}: {str(e)}")
                    return {"error": str(e)}
        
        return {"error": "Max retries exceeded"}
    
    def fetch_batch_historical_data(self, tickers: List[str], start_date: str, end_date: str, 
                                   delay: float = 2.0) -> Dict[str, Dict]:
        """
        Fetch historical data for multiple tickers with rate limiting
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            delay: Delay between requests to avoid rate limiting
            
        Returns:
            Dictionary mapping tickers to their historical data
        """
        batch_data = {}
        
        for i, ticker in enumerate(tickers):
            print(f"Fetching {ticker} ({i+1}/{len(tickers)})...")
            data = self.fetch_historical_data(ticker, start_date, end_date)
            
            if "error" not in data:
                batch_data[ticker] = data
            
            # Rate limiting
            if i < len(tickers) - 1:
                time.sleep(delay)
        
        return batch_data
    
    def initialize_paper_trading(self, start_date: str, starting_cash: float = 1000.0):
        """
        Initialize paper trading portfolio
        
        Args:
            start_date: Starting date for simulation
            starting_cash: Starting cash amount
        """
        self.portfolio = {
            "cash": starting_cash,
            "holdings": {},
            "transaction_history": [],
            "start_date": start_date,
            "current_date": start_date,
            "initial_cash": starting_cash
        }
        print(f"Paper trading initialized with ${starting_cash} on {start_date}")
    
    def execute_trade(self, ticker: str, action: str, shares: int, price: float, date: str) -> Dict:
        """
        Execute a paper trade
        
        Args:
            ticker: Stock ticker
            action: "BUY" or "SELL"
            shares: Number of shares
            price: Price per share
            date: Date of transaction
            
        Returns:
            Transaction result
        """
        total_cost = shares * price
        
        if action == "BUY":
            if total_cost > self.portfolio["cash"]:
                return {
                    "success": False,
                    "reason": "insufficient_funds",
                    "required": total_cost,
                    "available": self.portfolio["cash"]
                }
            
            # Execute buy
            self.portfolio["cash"] -= total_cost
            
            if ticker not in self.portfolio["holdings"]:
                self.portfolio["holdings"][ticker] = {"shares": 0, "avg_price": 0}
            
            # Update average price
            holding = self.portfolio["holdings"][ticker]
            total_shares = holding["shares"] + shares
            total_value = (holding["shares"] * holding["avg_price"]) + total_cost
            holding["avg_price"] = total_value / total_shares
            holding["shares"] = total_shares
            
        elif action == "SELL":
            if ticker not in self.portfolio["holdings"]:
                return {"success": False, "reason": "no_holdings"}
            
            holding = self.portfolio["holdings"][ticker]
            if holding["shares"] < shares:
                return {
                    "success": False,
                    "reason": "insufficient_shares",
                    "required": shares,
                    "available": holding["shares"]
                }
            
            # Execute sell
            self.portfolio["cash"] += total_cost
            holding["shares"] -= shares
            
            # Remove if no shares left
            if holding["shares"] == 0:
                del self.portfolio["holdings"][ticker]
        
        # Record transaction
        transaction = {
            "date": date,
            "ticker": ticker,
            "action": action,
            "shares": shares,
            "price": price,
            "total": total_cost,
            "cash_after": self.portfolio["cash"]
        }
        self.portfolio["transaction_history"].append(transaction)
        
        return {"success": True, "transaction": transaction}
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """
        Calculate total portfolio value
        
        Args:
            current_prices: Dictionary mapping tickers to current prices
            
        Returns:
            Total portfolio value (cash + holdings)
        """
        holdings_value = 0
        for ticker, holding in self.portfolio["holdings"].items():
            if ticker in current_prices:
                holdings_value += holding["shares"] * current_prices[ticker]
        
        return self.portfolio["cash"] + holdings_value
    
    def get_portfolio_performance(self, current_prices: Dict[str, float]) -> Dict:
        """
        Calculate portfolio performance metrics
        
        Args:
            current_prices: Current stock prices
            
        Returns:
            Performance metrics
        """
        initial_value = self.portfolio["initial_cash"]
        current_value = self.get_portfolio_value(current_prices)
        
        total_return = current_value - initial_value
        return_pct = (total_return / initial_value) * 100
        
        return {
            "initial_value": initial_value,
            "current_value": current_value,
            "total_return": total_return,
            "return_percentage": return_pct,
            "cash": self.portfolio["cash"],
            "holdings_count": len(self.portfolio["holdings"]),
            "total_transactions": len(self.portfolio["transaction_history"])
        }
    
    def calculate_returns_comparison(self, historical_data: Dict[str, Dict], 
                                    start_date: str, end_date: str) -> Dict:
        """
        Calculate what Warren Buffett-style buy-and-hold would have returned
        
        Args:
            historical_data: Historical price data
            start_date: Start date
            end_date: End date
            
        Returns:
            Comparison metrics
        """
        # Simple buy-and-hold strategy: invest equally in all available stocks at start
        initial_cash = self.portfolio["initial_cash"]
        
        available_tickers = [t for t in historical_data.keys() 
                           if len(historical_data[t].get("dates", [])) > 0]
        
        if not available_tickers:
            return {"error": "No data available"}
        
        investment_per_stock = initial_cash / len(available_tickers)
        
        total_end_value = 0
        
        for ticker in available_tickers:
            data = historical_data[ticker]
            dates = data.get("dates", [])
            closes = data.get("close", [])
            
            if not dates or not closes:
                continue
            
            # Find closest dates
            start_idx = 0
            end_idx = len(dates) - 1
            
            start_price = closes[start_idx]
            end_price = closes[end_idx]
            
            if start_price and end_price and start_price > 0:
                shares = investment_per_stock / start_price
                end_value = shares * end_price
                total_end_value += end_value
        
        buy_hold_return = total_end_value - initial_cash
        buy_hold_pct = (buy_hold_return / initial_cash) * 100
        
        return {
            "strategy": "buy_and_hold",
            "initial_investment": initial_cash,
            "final_value": total_end_value,
            "total_return": buy_hold_return,
            "return_percentage": buy_hold_pct,
            "stocks_held": len(available_tickers)
        }


# Test function
if __name__ == "__main__":
    print("Testing Market Interface...")
    
    market = MarketInterface()
    
    # Test getting tickers
    tickers = market.get_sp500_tickers()
    print(f"✓ Loaded {len(tickers)} tickers")
    print(f"  First 10: {tickers[:10]}")
    
    # Test fetching historical data for one stock
    print("\nTesting historical data fetch for AAPL...")
    data = market.fetch_historical_data("AAPL", "2020-01-01", "2020-01-31")
    
    if "error" not in data:
        print(f"✓ Fetched {len(data['dates'])} days of data")
        print(f"  First date: {data['dates'][0]}, Close: ${data['close'][0]:.2f}")
        print(f"  Last date: {data['dates'][-1]}, Close: ${data['close'][-1]:.2f}")
    else:
        print(f"✗ Error: {data['error']}")
    
    # Test paper trading
    print("\nTesting paper trading...")
    market.initialize_paper_trading("2020-01-01", 1000.0)
    
    # Execute test trade
    result = market.execute_trade("AAPL", "BUY", 5, 100.0, "2020-01-01")
    if result["success"]:
        print("✓ Test trade executed successfully")
        print(f"  Cash remaining: ${market.portfolio['cash']:.2f}")
    
    print("\n✓ Market Interface test complete!")
