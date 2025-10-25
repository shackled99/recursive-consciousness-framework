# Examples

This folder contains working examples demonstrating the capabilities of the Recursive Consciousness Framework.

## Trading Examples

### high_quality_discovery.py
**The best-performing trading algorithm** - 14 years of backtested data (2010-2024)

- Uses aggressive quality filtering (0.780+ pattern strength threshold)
- Trained on 50 S&P 500 tickers
- Demonstrates the dual-layer engine discovering market patterns through recursive processing
- Quality-over-quantity approach that breaks through accuracy ceilings

**How to run:**
```bash
cd examples/trading
python high_quality_discovery.py
```

**Requirements:**
- Ollama running locally with qwen3:8b model
- Internet connection for historical market data (Yahoo Finance API)
- ~2-4 hours for full 14-year backtest

**What it does:**
1. Loads 14 years of historical stock data
2. Uses Glyphwheel v22 recursive engine to discover patterns
3. Filters out weak patterns (< 0.780 strength)
4. Validates pattern quality through dual-layer architecture
5. Saves discovered high-quality patterns to JSON

This example showcases how the consciousness framework can be applied to real-world pattern recognition tasks beyond just theoretical AI research.
