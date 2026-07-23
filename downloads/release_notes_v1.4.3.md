# SpoLyrics v1.4.3 Release Notes

## ⚡ Key Improvements & Fixes

- 🛡️ **SQLite Thread Safety & Concurrency**: Resolved database lock contention and connection leaks in lyrics caching by introducing thread-safe `db_lock` context manager wrappers.
- 🔒 **PowerShell Path Injection Defense**: Escaped single quotes (`.replace("'", "''")`) in Windows auto-start and Start Menu shortcut generation scripts to support Windows user paths containing quotes.
- 🚀 **Event Loop Optimization**: Refactored media action dispatchers (`play_pause`, `next`, `prev`) to reuse the active background `asyncio` event loop via `asyncio.run_coroutine_threadsafe`, eliminating per-keypress thread spawning.
- 🔋 **Reduced Idle CPU Usage**: Optimized ghost mode unlock polling rate from 40ms to 100ms.
- 🧹 **Code Cleanup**: Removed duplicate DPI awareness log calls and redundant tray icon fallback blocks.
