#SC02E::
Clipboard =
Send ^{SC02E}
ClipWait,,1
chrName := Clipboard ; присваиваю скопированое имя персонажа перем.
;~ Gui +Resize
Gui, Add, ListView, w700 h300 gMyListView, Name|Path
Gui, Add, Button, Default, More
; Gather a list of file names from a folder and put them into the ListView:
Loop, z:\.src\shared\chr\*%chrName%*.max, , 1
{	
	LV_Add("", A_LoopFileName, A_LoopFileFullPath)
	SingeFullPath := A_LoopFileFullPath
	SearchCount := A_Index
	;~ MsgBox, %A_Index% `n%SingeFullPath%
}
if SearchCount = 1
{
	Clipboard =
	Clipboard := SingeFullPath
	;~ MsgBox, found one match
	Reload
}
if SearchCount =
{
	MsgBox, Nothing found
	Reload
}
else
{
	LV_ModifyCol()  ; Auto-size each column to fit its contents.
	Gui, Show, AutoSize
	return

	MyListView:
	if A_GuiEvent = DoubleClick	
	{
		;~ LV_GetText(RowText, A_EventInfo)  ; Get the text from the row's first field.
		LV_GetText(RowText, A_EventInfo, 2)
		Clipboard = %RowText%
		Gui, Destroy
		reload
		;~ ToolTip You double-clicked row number %A_EventInfo%. Text: "%RowText%"
	}
	return
	
	ButtonMore:							;		
	Gui, Submit
	
	StringTrimRight, chrName, chrName, 1
	LV_Delete()
	Loop, z:\.src\shared\chr\*%chrName%*.max, , 1
	{	
		LV_Add("", A_LoopFileName, A_LoopFileFullPath)
	}
	LV_ModifyCol()  ; Auto-size each column to fit its contents.
	Gui, Show, AutoSize
	return

	GuiClose:  ; Indicate that the script should exit automatically when the window is closed.
	Gui, Destroy
	reload

	GuiEscape:
	Gui, Destroy
	reload
}

;~ lock chr in repository
#SC025::
Send {AppsKey}
Sleep, 400
Send {SC025}
Sleep, 200
Send skinning
Sleep, 200
Send !{SC018}
Sleep, 500
Send !{SC018}
return
