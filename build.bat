@echo off
echo ==========================================
echo    Poo AI Assistant - Build Script
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Install Python 3.12+
    pause
    exit /b 1
)

REM Install dependencies
echo [1/5] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller pillow

REM Generate icon
echo [2/5] Generating app icon...
python build/generate_icon.py

REM Build with PyInstaller
echo [3/5] Building EXE with PyInstaller...
pyinstaller --clean --noconfirm PooAI.spec

REM Create installer directory
echo [4/5] Preparing installer files...
mkdir dist\installer 2>nul
copy dist\PooAI.exe dist\installer\
copy README.md dist\installer\
copy requirements.txt dist\installer\
xcopy /E /I gui\assets dist\installer\gui\assets 2>nul

REM Create simple launcher
echo @echo off > dist\installer\Start_PooAI.bat
echo start PooAI.exe >> dist\installer\Start_PooAI.bat

echo.
echo ==========================================
echo    BUILD COMPLETE!
echo ==========================================
echo.
echo EXE Location: dist\PooAI.exe
echo Installer Files: dist\installer\
echo.
echo To create installer, install Inno Setup and run:
echo   build\create_installer.iss
echo.
pause
