# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui/assets', 'gui/assets'),
        ('config', 'config'),
        ('core', 'core'),
        ('database', 'database'),
        ('gui', 'gui'),
        ('modules', 'modules'),
        ('plugins', 'plugins'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'edge_tts',
        'speech_recognition',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'openai',
        'ollama',
        'psutil',
        'pyautogui',
        'PIL',
        'requests',
        'bs4',
        'pyperclip',
        'keyboard',
        'win32com',
        'win32com.client',
        'comtypes',
        'pycaw',
        'winshell',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PooAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='gui/assets/icon.ico',
    version='version.txt',
)
