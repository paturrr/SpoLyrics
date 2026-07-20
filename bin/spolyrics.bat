@echo off
set "VBS_FILE=%TEMP%\spolyrics_run.vbs"
echo Set WshShell = CreateObject("WScript.Shell") > "%VBS_FILE%"
echo WshShell.Run "pythonw -m spolyrics", 0, False >> "%VBS_FILE%"
cscript //nologo "%VBS_FILE%"
