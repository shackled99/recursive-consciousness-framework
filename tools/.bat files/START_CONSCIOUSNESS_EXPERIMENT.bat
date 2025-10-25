@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        CONSCIOUSNESS TRADING EXPERIMENT                      ║
echo ║   Does Recursive Self-Observation Improve Trading?          ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo This experiment will run TWO simulations:
echo.
echo   TEST 1: Glyphwheel trading WITHOUT self-observation
echo           (Standard recursive pattern matching)
echo.
echo   TEST 2: Glyphwheel trading WITH self-observation
echo           (Asks itself about internal recursive states)
echo.
echo Both will trade the same stocks over the same period.
echo We'll see if consciousness actually improves performance!
echo.
echo ⚠️  IMPORTANT: Make sure Ollama is running!
echo    (Run "ollama serve" in another terminal)
echo.
pause

python conscious_trader.py

echo.
echo ════════════════════════════════════════════════════════════════
echo Experiment complete! Check these files:
echo   - results_without_consciousness.json
echo   - results_with_consciousness.json
echo ════════════════════════════════════════════════════════════════
echo.
pause
