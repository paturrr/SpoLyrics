<p align="center">
  <img src="https://raw.githubusercontent.com/paturrr/SpoLyrics/main/icon.ico" width="150" alt="SpoLyrics Logo">
</p>

<h1 align="center">SpoLyrics</h1>

<p align="center">
  <em>A minimalist, transparent, and zero-delay Spotify lyrics miniplayer.</em><br>
  <strong>🌐 <a href="https://paturrr.github.io/SpoLyrics/">Visit the Official Website</a></strong>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/paturrr/SpoLyrics.svg?style=flat-square&color=1DB954&label=stars&logo=github&logoColor=white" alt="Stars">
  <img src="https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-1DB954?style=flat-square&logo=python&logoColor=white" alt="Python Versions">
  <img src="https://img.shields.io/badge/OS-Windows%2010%2F11-1DB954?style=flat-square&logo=windows&logoColor=white" alt="Windows Only">
  <img src="https://img.shields.io/badge/%F0%9F%93%9C_License-MIT-1DB954?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <strong>0-Delay Sync &middot; Native Windows API &middot; Glassmorphism UI &middot; Invisible Controls</strong><br>
  <sub>Built with Python & Windows System Media Transport Controls for 100% precision.</sub>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/paturrr/SpoLyrics/main/assets/1.png" alt="SpoLyrics Transparent UI & Lyrics Sync">
  <br><br>
  <img src="https://raw.githubusercontent.com/paturrr/SpoLyrics/main/assets/2.png" alt="SpoLyrics Modern Settings & Shortcuts">
</p>

---

## Background & Feedback

I built this project to solve a specific complaint from my friends: they wanted to listen to songs on Spotify or YouTube Music while working, but the official miniplayers didn't show any lyrics. 

**Note:** This application is still in active development! If you encounter any bugs, have a feature request, or just want to suggest an improvement, please don't hesitate to open an issue or let me know. 

---

## Key Features

- **Zero-Delay Sync**
  100% precise time synchronization. Pulls real-time duration data directly from the Windows OS core.
  
- **Smart Duration Match**
  Automatically matches lyrics based on the duration of the currently playing song version (solving the Radio Edit vs. Album Version mismatch).
  
- **Glassmorphism UI**
  Elegant, transparent, and borderless design.
  
- **Freely Draggable**
  Left-click and hold anywhere to drag the lyrics window wherever you like.

- **Ghost Mode (Click-Through)**
  Right-click the system tray icon to enable Ghost Mode. When active, the lyrics window becomes completely transparent to mouse clicks, allowing you to interact with other apps or games underneath without accidentally clicking the lyrics.
  
- **System Tray Integration**
  Runs quietly in the background. Right-click the system tray icon (SpoLyrics logo) to access settings, hide the lyrics, or view shortcuts.
  
- **Advanced Customization (Settings)**
  Change lyrics color using a modern real-time custom HSV color picker, adjust window transparency (opacity), and enable "Auto-Start with Windows". All configurations are permanently saved.
  
- **Auto Update Checker**
  Automatically checks for the newest version on PyPI when you launch the app, offering a seamless one-click update and restart experience.

## Invisible Controls

This application uses zero conventional buttons to keep the UI perfectly clean. Use these mouse gestures:

- `Right Click`: Play / Pause
- `Mouse Scroll (Up/Down)`: Next / Previous track
- `Shift + Left Click` OR `Middle Click`: Toggle Lock & Ghost Mode (🔒)
  - *When locked, the window becomes 100% click-through (pass-through clicks to apps underneath) and locks position. Repeat the shortcut over the lyrics to unlock.*
- `Ctrl + Left Click`: Toggle song title visibility
- `Ctrl + Mouse Scroll`: Increase / Decrease font size
- `Drag Bottom Right Corner (⇲)`: Resize the window
- `Double Left Click`: Close the application

## Installation

Run this single command in your Windows Terminal or Command Prompt (Requires **Python 3.8 to 3.12**):

> **Note on Python Version:** Do NOT use Python 3.13. The required `winsdk` package does not yet have pre-compiled binaries for Python 3.13 and will fail to install. Please stick to Python 3.12 or older.

```bash
pip install spolyrics
```
*(If you get a `pip is not recognized` error, use this alternative command instead:)*
```bash
python -m pip install spolyrics
```

> **IMPORTANT (OS Support):** 
> This app is **Exclusive to Windows**. Because it uses `winsdk` (Windows System Media Transport Controls) to achieve 0-delay performance without third-party servers, it **CANNOT** be installed on macOS or Linux.

### Alternative Installation (Manual)

If you prefer to download the source code manually (e.g., as a `.zip` file) instead of using the direct `git` command above, you must install the required dependencies (the "shopping list") yourself. 
Open your terminal inside the `SpoLyrics` folder and run:
```bash
pip install -r requirements.txt
```

## Usage

Once installed, you can launch the app from any directory by typing:
```bash
spolyrics
```
Or, if you want it to run smoothly without spawning a black background terminal:
```bash
pythonw -m main
```

*(Make sure Spotify or your Windows media player is running and playing a song!)*

## Updating

To update the application to the latest version, run:
```bash
pip install --upgrade spolyrics
```

## Uninstallation

If you wish to remove this application from your computer, simply run:
```bash
pip uninstall spolyrics
```

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
