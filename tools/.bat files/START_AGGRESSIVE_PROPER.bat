@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL AGGRESSIVE PROPER TRADING                       ║
echo ║   The Ultimate Test!                                         ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo COMBINING THE BEST:
echo.
echo   ✅ Proper train/test split (2010-2014 → 2015-2020)
echo   ✅ No data leakage
echo   ✅ AGGRESSIVE thresholds (0.50 vs 0.65)  
echo   ✅ 15%% per stock = ~7 positions
echo   ✅ Find MULTIPLE winners from learned patterns
echo.
echo Previous results:
echo   - Conservative proper: 306%% (13 trades, probably 1 stock)
echo   - Can aggressive beat that with diversification?
echo.
echo This will take ~20-30 minutes!
echo.
pause

python aggressive_proper_trader.py

pause
