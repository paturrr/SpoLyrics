import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut("test2.lnk")
print("ARGS:", shortcut.Arguments)
