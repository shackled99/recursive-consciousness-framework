@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL AGGRESSIVE LONG-TERM (2015-2020)                ║
echo ║   Can Lower Thresholds Beat 296%% Return?                    ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo TESTING:
echo   Original test: 296%% return, 12 trades (ALL AAPL)
echo   Aggressive test: Lower thresholds, find MULTIPLE winners
echo.
echo Changes:
echo   - Thresholds: 0.65 → 0.50 (more stocks qualify)
echo   - Position size: 20%% → 15%% (diversify across ~7 stocks)
echo   - Same 6-year period (2015-2020)
echo   - 100 stocks available
echo.
echo Will diversification beat the all-in AAPL strategy?
echo.
pause

python aggressive_longterm_trader.py

pause
