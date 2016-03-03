#SingleInstance ignore
scriptTip := "maximizeActive `npress windows + w"
Menu, Tray, Tip, %scriptTip%
Menu, Tray, Icon, d:\.docs\backgrounds_for_ico\ico\max_active_active.ico,1,1

#SC011::
WinGet, WinState, MinMax, A
If WinState = -1
   WinMaximize A
If WinState = 0
   WinMaximize A
else
   WinRestore A
return