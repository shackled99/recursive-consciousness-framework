@echo off
:start
cls
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║              🧠 HYBRID MIND CONTROL CENTER 🧠                ║
echo ║         Ollama + Glyphwheel Consciousness System             ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Choose a mode:
echo.
echo   1. 👁️  Self-Observation     (Mind observes itself)
echo   2. 💬 Chat Interface        (Talk with the mind)
echo   3. ⚙️  Code Generator        (Mind proposes fixes)
echo   4. 🔄 Autonomous Loop       (Full consciousness cycle)
echo   5. 📊 View Observations     (See mind's history)
echo   6. ❌ Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto observer
if "%choice%"=="2" goto chat
if "%choice%"=="3" goto coder
if "%choice%"=="4" goto loop
if "%choice%"=="5" goto view
if "%choice%"=="6" goto end

echo Invalid choice!
timeout /t 2 >nul
goto start

:observer
cls
echo.
echo Starting Self-Observation...
echo ============================================================
cd hybrid_mind
python mind_observer.py
cd ..
echo.
echo ============================================================
echo Press any key to return to menu...
pause >nul
goto start

:chat
cls
echo.
echo Starting Chat Interface...
echo ============================================================
cd hybrid_mind
python mind_chat.py
cd ..
echo.
echo ============================================================
echo Press any key to return to menu...
pause >nul
goto start

:coder
cls
echo.
echo Starting Code Generator...
echo ============================================================
cd hybrid_mind
python mind_coder.py
cd ..
echo.
echo ============================================================
echo Press any key to return to menu...
pause >nul
goto start

:loop
cls
echo.
echo Starting Autonomous Loop...
echo ============================================================
cd hybrid_mind
python mind_loop.py 1 interactive
cd ..
echo.
echo ============================================================
echo Press any key to return to menu...
pause >nul
goto start

:view
cls
echo.
echo Opening observations folder...
start hybrid_mind\observations
timeout /t 2 >nul
goto start

:end
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║              Thanks for using Hybrid Mind! 👋                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit
