@echo off
REM ============================================================
REM  Nexora - Voice Laptop Program (Test Version v1)
REM  Double-click this file to run Nexora on Windows.
REM  It checks Python, installs the needed libraries, then runs.
REM ============================================================
title Nexora

echo.
echo  ==========================================
echo    NEXORA - Voice Laptop Program (Test v1)
echo  ==========================================
echo.

REM ---- 1. Check Python ----
python --version >nul 2>&1
if %errorlevel% neq 0 goto nopython

for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  Python mila: %%v
echo.

REM ---- 2. Install libraries (quiet, one time) ----
echo  Libraries check / install ho rahi hain, thoda intezar karein...
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 echo  Note: kuch libraries install nahi huin - Nexora phir bhi chalega, sirf woh feature band rahega jinki library missing hai.
python -m pip install pyaudio >nul 2>&1
if %errorlevel% neq 0 echo  Note: PyAudio (mic ke liye) install nahi hua - awaaz sunna band rahega, typed commands chalengi.
echo.

REM ---- 3. Run Nexora ----
echo  Nexora shuru ho raha hai...
cd /d "%~dp0"
python nexora.py
if %errorlevel% neq 0 goto runerror

exit /b 0

:nopython
echo  MASLA: Is laptop par Python nahi mila.
echo.
echo  Hal (sirf ek dafa):
echo    1. Chrome mein python.org kholein aur Python download karein (free).
echo    2. Install karte waqt neeche wale box "Add python.exe to PATH" par
echo       lazmi tick lagayein.
echo    3. Phir is file (run_nexora.bat) ko dobara double-click karein.
echo.
pause
exit /b 1

:runerror
echo.
echo  Nexora chalne mein masla aaya. Upar wala message parh lein.
pause
exit /b 1
