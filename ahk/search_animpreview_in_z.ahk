/* логика поиска
 * 
 * прохожусь по файлам - создаю список из нужных
 * список состоит из полных путей
 * вызываю каждую строчку
 * в каждой строчке ищу instr по части слова
 * если нахожу - копирую строчку
 * прекращаю поиск
 */
#SingleInstance ignore
scriptTip := "Search For Animation Preview, Link`npress windows + ` for preview`npress windows + a for link"
Menu, Tray, Tip, %scriptTip%
Menu, Tray, Icon, d:\.docs\backgrounds_for_ico\ico\anim_prev_tray.ico,1,1

#NoEnv

#SC029::
Clipboard =
Send ^{SC02E}
ClipWait,,1
chrName := Clipboard ; присваиваю скопированое имя персонажа перем.
if FileList =
{
	FileList = end`n ; добавляю метку конец вначало списка
	Loop, z:\.src\shared\chr\_face\.anims_preview_database\*, , 1 ; ищу все файлы .max по заданому пути
	{
		FileList = %FileList%%A_LoopFileFullPath%`n ; составляю список из них
	}
	Sort, FileList, R  ; сортирую список в обратном порядке, чтобы строчка "end" оказалась вконце
}

Loop, parse, FileList, `n ; обрабатываю построчно список
{
	;~ MsgBox % A_LoopField
	IfInString, A_LoopField, %chrName% ;  если строчка содержит имя персонажа
	{	
		;~ MsgBox, found
		Run, %A_LoopField%, max
		;~ Clipboard := A_LoopField ; копирую строчку в буфер обмена
		;~ MsgBox, 1,, Скопирован путь`n%A_LoopField%, продолжить поиск?
		;~ IfMsgBox Ok ; если путь правильный - поиск останавливается 
			;~ continue ; return
		;~ else ; если нет, поиск продолжается
		return
	}	
	if A_LoopField = end ; если строчка содержит "end" значит поиск подошел к концу и не дал результатов
	{	
		MsgBox, %chrName% не найден
		reload
	}
}
reload


#SC01E::
Clipboard =
Send ^{SC02E}
ClipWait,,1
animName := Clipboard ; присваиваю скопированое имя персонажа перем.
if animFileList =
{
	animFileList = end`n ; добавляю метку конец вначало списка
	Loop, z:\.src\shared\chr\_face\.clips\*, , 1 ; ищу все файлы по заданому пути
	{
		animFileList = %animFileList%%A_LoopFileFullPath%`n ; составляю список из них
	}
	Sort, animFileList, R  ; сортирую список в обратном порядке, чтобы строчка "end" оказалась вконце
}

Loop, parse, animFileList, `n ; обрабатываю построчно список
{
	;~ MsgBox % A_LoopField
	IfInString, A_LoopField, %animName% ;  если строчка содержит имя персонажа
	{	
		Clipboard := A_LoopField ; копирую строчку в буфер обмена
		ToolTip, copied %animName% link
		SetTimer, RemoveToolTip, 2000
		return

		RemoveToolTip:
		SetTimer, RemoveToolTip, Off
		ToolTip
		return
	}	
	if A_LoopField = end ; если строчка содержит "end" значит поиск подошел к концу и не дал результатов
	{	
		MsgBox, %animName% не найден
		return
	}
}
reload
