@echo off
echo ==========================================
echo    Poo AI - Single File Build
echo ==========================================
echo.

pip install pyinstaller pillow
python build/generate_icon.py

echo Building single-file executable...
pyinstaller ^
    --name "PooAI" ^
    --onefile ^
    --windowed ^
    --icon=gui/assets/icon.ico ^
    --add-data "gui/assets;gui/assets" ^
    --add-data "config;config" ^
    --add-data "core;core" ^
    --add-data "database;database" ^
    --add-data "gui;gui" ^
    --add-data "modules;modules" ^
    --add-data "plugins;plugins" ^
    --add-data "utils;utils" ^
    --hidden-import edge_tts ^
    --hidden-import speech_recognition ^
    --hidden-import pyttsx3.drivers ^
    --hidden-import pyttsx3.drivers.sapi5 ^
    --hidden-import openai ^
    --hidden-import ollama ^
    --hidden-import psutil ^
    --hidden-import pyautogui ^
    --hidden-import PIL ^
    --hidden-import requests ^
    --hidden-import bs4 ^
    --hidden-import pyperclip ^
    --hidden-import keyboard ^
    --hidden-import win32com ^
    --hidden-import win32com.client ^
    --hidden-import comtypes ^
    --hidden-import pycaw ^
    --hidden-import winshell ^
    --version-file=version.txt ^
    main.py

echo.
echo Single EXE created: dist\PooAI.exe
echo.
pause
