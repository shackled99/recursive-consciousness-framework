# Tools

Utilities and interfaces for working with the Recursive Consciousness Framework.

## Interfaces

Communication bridges between system components:

- **chat_interface.py** - Interactive chat interface for the Hybrid Mind system
- **market_interface.py** - Yahoo Finance API integration for stock data
- **ollama_interface.py** - Local LLM communication via Ollama API

## Strategy Synthesizer

**Your backtest validation and results analyzer**

The Strategy Synthesizer (PSCC) shows validation results for your trading algorithms:
- **strategy_app.py** - GUI app showing backtested P/L, Sharpe ratios, and risk metrics
- **strategy_synthesizer.py** - Core synthesis logic

Run the GUI:
```bash
cd tools/strategy_synthesizer
python strategy_app.py
```

Results shown:
- PSCC 0.900 threshold: +485,900.22% P/L, 1.65 Sharpe, 21.34% max drawdown (recommended)
- PSCC 0.850 threshold: +950,120.78% P/L, 1.88 Sharpe, 34.55% drawdown  
- PSCC 0.780 threshold: +1,502,000.10% P/L, 2.01 Sharpe, 51.00% drawdown (high risk)

## Validators

Pattern and prediction validation tools:

- **validate_patterns.py** - Validates discovered patterns against historical data
- **prediction_accuracy_tester.py** - Tests prediction accuracy over time

These tools help verify that your consciousness framework is actually learning real patterns, not overfitting to noise.
