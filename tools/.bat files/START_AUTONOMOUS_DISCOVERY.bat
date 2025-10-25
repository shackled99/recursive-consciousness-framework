@echo off
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║   AUTONOMOUS PATTERN DISCOVERY SYSTEM                        ║
echo ║   LLM discovers patterns → GlyphWheel learns connections     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo WHAT THIS DOES:
echo   1. Loads 5 years of historical data (2010-2015)
echo   2. Every WEEK, LLM analyzes market movements
echo   3. LLM discovers patterns like:
echo      - "When NVDA rises, AMD follows 2 days later"
echo      - "Tech stocks correlate with NASDAQ"
echo      - "October has high volatility"
echo   4. Stores patterns as GLYPHS
echo   5. Stress tests connect patterns to stocks
echo   6. Result: GlyphWheel has LEARNED PATTERNS!
echo.
echo REQUIREMENTS:
echo   ⚠️  Ollama must be running!
echo   Run: ollama serve
echo.
echo This will take 10-30 minutes depending on your system.
echo The LLM will analyze ~260 weeks of data.
echo.
pause

python autonomous_pattern_discovery.py

echo.
echo ════════════════════════════════════════════════════════════════
echo Pattern discovery complete!
echo Check: discovered_patterns.json
echo ════════════════════════════════════════════════════════════════
echo.
pause
