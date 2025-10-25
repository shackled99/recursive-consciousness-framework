@echo off
REM --- Glyphwheel V22 Launch Script ---
REM --- Change directory to the current folder ---
cd /d "%~dp0"

REM --- Execute the main Python file ---
echo Launching Glyphwheel V22 Engine...
python main.py

pause