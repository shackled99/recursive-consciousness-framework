@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL ADAPTIVE TRADING SYSTEM                         ║
echo ║   Continuous Learning - Daily Adaptation                     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo NEW APPROACH:
echo   • Phase 1: Train on 2010-2015 historical data (5 years)
echo   • Phase 2: Trade 2015-2020 with evolved connections
echo   • Retrains every 10 days (continuous adaptation)
echo   • 20-day minimum hold (prevents churning)
echo   • Trades every 10 days (reduced frequency)
echo.
echo This fixes the over-trading problem by:
echo   1. Letting connections evolve with the market
echo   2. Preventing rapid buy-sell cycles
echo   3. Holding winners longer
echo.
pause

python adaptive_trader.py

echo.
echo ════════════════════════════════════════════════════════════════
echo Results saved to: adaptive_trading_results.json
echo ════════════════════════════════════════════════════════════════
echo.
pause
