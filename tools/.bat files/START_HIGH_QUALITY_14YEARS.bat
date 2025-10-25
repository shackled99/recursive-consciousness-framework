@echo off
echo ========================================
echo HIGH QUALITY PATTERN DISCOVERY
echo 2010-2024 | 0.780 Min Strength
echo ========================================
echo.
echo This will take 2-3 hours!
echo Only accepting HIGH QUALITY patterns (0.780+)
echo.
echo Starting...
echo.

cd /d "C:\Users\lmt04\OneDrive\Desktop\glyphwheel (2)"
python high_quality_discovery.py

echo.
echo ========================================
echo High Quality Training Complete!
echo Check if we broke 54.44%%!
echo ========================================
pause
