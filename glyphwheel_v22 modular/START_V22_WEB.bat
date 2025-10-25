@echo off
echo Starting Glyphwheel V22 Web Interface...
echo.
cd /d "%~dp0"
python web/server.py %*
pause
