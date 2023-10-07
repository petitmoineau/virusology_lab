Dim WshShell, strCurDir
Set WshShell = CreateObject("WScript.Shell")
strCurDir    = WshShell.CurrentDirectory
WshShell.Run strCurDir & "\installer.bat", 0

Set WshShell = Nothing