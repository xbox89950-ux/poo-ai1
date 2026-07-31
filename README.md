# Poo AI Voice Assistant

Windows AI Voice Assistant supporting Bengali, English, and Banglish.

## Quick Start

1. Install Python 3.12+
2. `pip install -r requirements.txt`
3. `set OPENAI_API_KEY=your_key` (optional)
4. `python main.py`

## Build to EXE

### Method 1: Simple Build (Recommended)
```batch
build.bat
```

### Method 2: Single File EXE
```batch
build_onefile.bat
```

### Method 3: Manual
```batch
pip install pyinstaller pillow
python build/generate_icon.py
pyinstaller --clean --noconfirm PooAI.spec
```

## Create Windows Installer

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `build/create_installer.iss`
3. Press F9 to compile
4. Installer will be created as `dist/PooAI_Setup.exe`

## Features

- Voice & Text Commands
- Windows Automation (Apps, Volume, System)
- Code Generation with VS Code integration
- Web Search, Weather, News
- File Management (PDF, Word, Excel)
- Calculator, Currency Converter, Translation
- Music Player, Voice Recorder
- Timer, Alarm, Reminders
- System Info (CPU, RAM, Battery)
- Wi-Fi / Bluetooth Control
- OCR (Image to Text)
- Clipboard History
- Jokes, Facts, Coin Flip, Dice Roll
- Glassmorphism UI with Animations
- System Tray
- Bengali / English / Banglish Support

## Wake Words

- "Hey Poo" / "Poo" / "Hello Poo"
- "হে পু" / "পু" / "হ্যালো পু"

## Commands

- `ক্রোম খোলো` / `open chrome`
- `ভিএস কোড চালু করো` / `open vs code`
- `screenshot নাও` / `take screenshot`
- `weather in Dhaka`
- `calculate 25 * 4`
- `convert 100 USD to BDT`
- `translate hello to bn`
- `set timer 60 seconds`
- `remind me to eat at 2026-08-01 14:30`
- `play music`
- `system info`
- `wifi off`
- `brightness 70`
- `tell me a joke`
- `roll dice`
- `what time`
- `read pdf myfile.pdf`
- `ocr`
- `record voice`
- `Python দিয়ে Calculator বানাও`
