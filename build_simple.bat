@echo off
echo ==========================================
echo    Poo AI - Simple Build (No Music)
echo ==========================================
echo.

python -m pip install --upgrade pip

echo Installing core dependencies...
pip install PySide6 SpeechRecognition edge-tts openai pyautogui pywin32 psutil watchdog requests pyttsx3 numpy Pillow pyperclip keyboard beautifulsoup4 markdown qasync aiohttp pyyaml

echo.
echo Installing optional dependencies...
pip install PyPDF2 python-docx openpyxl deep-translator screen-brightness-control pywhatkit winshell comtypes pycaw

echo.
echo Generating icon...
python build/generate_icon.py

echo.
echo Building EXE...
pyinstaller --name "PooAI" --onefile --windowed --icon=gui/assets/icon.ico --add-data "gui/assets;gui/assets" --hidden-import PySide6 --hidden-import speech_recognition --hidden-import edge_tts --hidden-import openai --hidden-import pyttsx3.drivers --hidden-import pyttsx3.drivers.sapi5 --hidden-import psutil --hidden-import pyautogui --hidden-import requests --hidden-import bs4 --hidden-import pyperclip --hidden-import keyboard --hidden-import win32com --hidden-import win32com.client --hidden-import comtypes --hidden-import pycaw main.py

echo.
echo ==========================================
echo    BUILD COMPLETE!
echo ==========================================
echo EXE location: dist\PooAI.exe
echo.
pause
