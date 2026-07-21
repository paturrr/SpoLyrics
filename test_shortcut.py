import subprocess
import os
import win32com.client
ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('test2.lnk');$s.TargetPath='wscript.exe';$s.Arguments='\"C:\\Users\\Aska Kania\\test.vbs\"';$s.Save()"
subprocess.run(["powershell", "-Command", ps_script])
