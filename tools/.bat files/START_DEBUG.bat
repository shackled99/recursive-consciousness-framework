@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL DEBUG MODE                                      ║
echo ║   See WHY it won't buy NVDA, TSLA, etc.                     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This will show you:
echo   - Top 20 stocks ranked by Glyphwheel's analysis
echo   - Exactly where AAPL, TSLA, NVDA, MSFT rank
echo   - GSI values and connection counts for each
echo   - Why some qualify and others don't
echo.
echo Running on Q1 2015 (3 months) for quick results!
echo.
pause

python debug_trader.py

pause
