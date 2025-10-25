@echo off
echo.
echo 🔧 LAUNCHING FIXED GLYPHWHEEL ENGINE 🔧
echo.
echo This version fixes the entropy oscillation problem!
echo No more endless stress test loops.
echo.
echo Starting in 3 seconds...
timeout /t 3 >nul
echo.

python glyphwheel_app_fixed.py

pause
