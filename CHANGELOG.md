# Changelog

## [1.3.6] - 2026-07-20

### Added
- **UI Enhancement:** Added a minimalist, ultra-thin real-time progress bar at the bottom of the lyrics window to track song duration seamlessly.

### Fixed
- **Terminal/Console Issue:** Resolved a major issue where launching the application via a Python Virtual Environment (`venv`) would force a lingering black terminal window to remain open.
- **Hybrid Launcher Implementation:** Completely replaced standard `gui_scripts` with a custom hybrid Batch and VBScript architecture (`spolyrics.bat` -> `launcher.vbs`). This bulletproof approach natively interfaces with the Windows API (`WScript.Shell`, `vbHide`) to detach and hide all console windows instantly, regardless of the user's Python environment.
- **Start Menu & Auto-Start:** The background update system now dynamically points all Start Menu and Auto-Start shortcuts to the newly implemented VBScript hidden launcher.
- **Updater Resilience:** The internal auto-updater has been fortified to locate `python.exe` more robustly, eliminating "Fatal error in launcher" occurrences during background updates.
