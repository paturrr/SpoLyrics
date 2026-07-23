# SpoLyrics v1.4.2 Release Notes

## What's New
- **Security & Stability**: Eliminated Tkinter thread-safety violations in the Ghost Mode monitor. The app no longer spawns background daemon threads for input polling, preventing potential race conditions and crashes.
- **Performance**: Mouse polling loop moved entirely to the Tkinter event loop (`root.after`), making the app more lightweight.
- **Codebase Cleanliness**: Removed duplicate imports, dead code, and old testing files (`test.lnk`, `test2.lnk`, etc.). Extracted magic hex numbers into proper Win32 constants.
- **Assets**: Added high-resolution transparent logo (`icon_4x4cm.png`) for media and printing purposes.

*Update automatically via PyPI: `pip install --upgrade spolyrics`*
