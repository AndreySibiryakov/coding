#NoEnv
#SingleInstance ignore
scriptTip := "Unreal Windows Switch `npress windows + 1,2,3,4"
Menu, Tray, Tip, %scriptTip%
Menu, Tray, Icon, d:\.docs\backgrounds_for_ico\ico\unreal_window_switch_tray_bold.ico,1,1


ActivateUrealWidnow(name)
{

	WinGet, Window, List	
	DetectHiddenWindows, on
	Loop %Window%
	{
		Id:=Window%A_Index%
		windowID = ahk_id %Id%
		WinGetTitle, TVar, %windowID%
		;~ MsgBox % TVar
		IfInString, TVar, %name%
		{
			WinActivate, %TVar% ahk_exe SH8Game.exe
			return
		}
	}
}

#4::
ActivateUrealWidnow("preview")
ActivateUrealWidnow("FaceFX Studio")
return

#3::
ActivateUrealWidnow("kismet")
return

#2::
ActivateUrealWidnow("matinee")
return

#1::
ActivateUrealWidnow("content browser")
ActivateUrealWidnow("Actor Classes")
ActivateUrealWidnow("Levels")
ActivateUrealWidnow("Scene")
ActivateUrealWidnow("Layers")
return

