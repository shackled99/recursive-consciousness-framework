@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   GLYPHWHEEL REFINED TRADING SYSTEM                          ║
echo ║   Pattern REINFORCEMENT (not replacement)                    ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo KEY CHANGES:
echo   • Light refinement every 20 days (0.3 intensity - subtle)
echo   • Deep reinforcement every 60 days (0.5 intensity - moderate)
echo   • 40-day minimum hold (double previous)
echo   • Trade decisions every 15 days
echo   • Won't buy if already own position
echo.
echo PHILOSOPHY:
echo   - Patterns STRENGTHEN over time
echo   - Connections REINFORCE, not replace
echo   - Low stress = keeps existing patterns
echo   - Holds winners through market noise
echo.
pause

python refined_trader.py

echo.
echo ════════════════════════════════════════════════════════════════
echo Results saved to: refined_trading_results.json
echo ════════════════════════════════════════════════════════════════
echo.
pause
