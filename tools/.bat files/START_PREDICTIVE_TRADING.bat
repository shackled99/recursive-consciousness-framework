@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL PREDICTIVE TRADING SYSTEM v2                    ║
echo ║   Forward-Looking Pattern Analysis + Active Rebalancing     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Starting Predictive Trading Simulation...
echo.
echo NEW FEATURES:
echo   • Momentum detection (price + GSI trends)
echo   • Volatility as opportunity signal (NVDA/TSLA style)
echo   • Active sell-to-reinvest rebalancing
echo   • Aggressive 40%% position sizing on high-conviction plays
echo   • Forward-looking predictions (not just reactions!)
echo.
echo This will:
echo   1. Load historical data (2015-2019)
echo   2. Train Glyphwheel with 21k recursion
echo   3. Run PREDICTIVE backtest with active trading
echo   4. Compare vs Warren Buffett buy-and-hold
echo.
pause

python glyphwheel_predictive_trader.py

echo.
echo ════════════════════════════════════════════════════════════════
echo Results saved to: glyphwheel_predictive_results.json
echo ════════════════════════════════════════════════════════════════
echo.
pause
