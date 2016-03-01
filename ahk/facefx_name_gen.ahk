; скрипт генерирует правильные имена для facefx animsets для unreal engine, sherlock 8
; и добавляет в буфер обмена команду batch analyze для facefx studio.

#Persistent

; список персонажей
chrList = Albeit Alice Arthur Ashley Barman bc_pass Bernard Billy Cab cabDriver2 Charles Child Child ChildWC Conspirator Customer DeadDriver DeadPass DeadPhaeton doctor dog Driver DriverCarr DriverLC drunkard DrvrScflds Dweller Fakir Fleischer Fleischer_Pub FlowersGirl Gambler gambler2 George Guard Guard2 GuardIB Harrington Harry Hudson Informer Inspector Jeremiah Katelyn loser Mary Mechanic Mosley Mother Mycroft Oliver Orson OrsonSh Otto OttoCab Patient Peasant pedestrian Percy PhaetPass Player1 Player2 Player3 Policeman Policeman Pygmy Racist1 Racist2 Robber Sherlock shopowner Sweeper Thief Thug1 Thug3 Thug4 Toby Tom Watchman Watson Worker Worker workInjur Zacharias ZachariasNA

StringUpper, upNameList, chrList, T
nameList := RegExReplace(upNameList, " ", "|")

; список кейсов (дел)
caseList = FD|GD|IB|IN|NA|PT

; создаю порядковый список диалогов
loop, 25
{
	num := A_Index
	if (num < 10)
		num := "0" . num
	if dList =
		dList := "cmt|misc"
	dList .= "|" . num
}

;~ Gui, Add, ComboBox, x15 y36 w170 h21 , Mary
;~ Gui, Add, ComboBox, x195 y36 w60 h21 , IN
;~ Gui, Add, ComboBox, x265 y36 w80 h21 , CMT
;~ Gui, Add, Text, x15 y9 w160 h30 , Character
;~ Gui, Add, Text, x195 y9 w50 h30 , Case
;~ Gui, Add, Text, x265 y9 w70 h30 , Dialogue
;~ Gui, Add, Button, x426 y27 w60 h30 , Run
;~ Gui, Add, Button, x496 y37 w60 h20 , Copy
;~ Gui, Add, Button, x566 y37 w60 h20 , Create
;~ Gui, Add, Text, x496 y7 w60 h30 , Analyze
;~ Gui, Add, Text, x566 y7 w60 h30 , FXAsset
;~ Gui, Add, Button, x636 y37 w60 h20 , Import
;~ Gui, Add, Button, x706 y37 w60 h20 , Open
;~ Gui, Add, Text, x636 y7 w60 h30 , soundsCue
;~ Gui, Add, Text, x706 y7 w60 h30 , .xlsx
;~ Gui, Add, Radio, x356 y7 w60 h20 , Radio
;~ Gui, Add, Radio, x356 y27 w60 h20 , Radio
;~ Gui, Add, Radio, x356 y47 w60 h20 , Radio
;~ ; Generated using SmartGUI Creator for SciTE
;~ Gui, Show, w784 h74, Untitled GUI
;~ return




Gui, Add, ComboBox, vchrName x16 y37 w170 h50 sort H500, %nameList%
Gui, Add, ComboBox, vcaseName x196 y37 w60 h10 sort Uppercase H500, %caseList%
Gui, Add, ComboBox, vdialogueName x266 y37 w80 h20 sort Uppercase H500, %dList% ; %dialogueList%
Gui, Add, Text, x16 y10 w160 h30 , Character
Gui, Add, Text, x196 y10 w50 h30 , Case
Gui, Add, Text, x266 y10 w70 h30 , Dialogue
Gui, Add, Button, x426 y27 w60 h30 , Run
Gui, Add, Button, x496 y37 w60 h20 , Copy
Gui, Add, Button, x566 y37 w60 h20 , Create
Gui, Add, Text, x496 y10 w60 h30 , Analyze
Gui, Add, Text, x566 y10 w60 h30 , FXAsset
Gui, Add, Button, x636 y37 w60 h20 , Import
Gui, Add, Button, x706 y37 w60 h20 , Open
Gui, Add, Button, x706 y67 w60 h20 , Commit
Gui, Add, Text, x636 y10 w60 h30 , soundsCue
Gui, Add, Text, x706 y10 w60 h30 , .xlsx
Gui, Add, Radio, x356 y7 w60 h20 vInt, INT
Gui, Add, Radio, x356 y27 w60 h20 vFra, FRA
Gui, Add, Radio, x356 y47 w60 h20 vDeu, DEU
Gui, Show, w781 h99, Generate naming for FaceFX animset
Gui +AlwaysOnTop
return

GuiClose:
ExitApp


ButtonCreate:							;		
Gui, Submit, NoHide

; перехожу на окно создания facefx animset, заполняю его
WinActivate, ahk_class #32770
if ErrorLevel
{
	MsgBox, FaceFX Window not exists
	ExitApp
}

Send ^a
Clipboard =
Send ^c
StringTrimLeft, chrName, clipboard, 4
;~ MsgBox, %chrName%
Send %chrName%_facefx
Send {tab}{Del}
Send {tab}{tab}
Send %chrName%_facefx
Send {tab}{space}
return


ButtonCopy:							;		
Gui, Submit, NoHide

if chrName =
{
	MsgBox, , пустое поле, Выберите персонажа 
	Reload
}	
;~ if caseName =
;~ {
	;~ MsgBox, , пустое поле, Выберите название кейса
	;~ Reload
;~ }
if dialogueName =
{
	MsgBox, , пустое поле, Выберите номер диалога
	Reload
}

; условие, которое добавляет или убирает приставку D перед номером диалога
if (dialogueName = "CMT" or dialogueName = "MISC")
	Dvar =
else
	Dvar = D

if caseName = 
	caseNameUnderscore =
else
	caseNameUnderscore = _

StringLower, lowCaseName, caseName
StringLower, LowDialogueName, dialogueName
StringLower, lowChrName, chrName
StringLower, lowDvar, Dvar
StringUpper, UpchrName, chrName, T

Clipboard = 
Clipboard = analyze -package "%lowCaseName%%caseNameUnderscore%%lowDvar%%LowDialogueName%_%lowChrName%_sounds_cue" -group "%UpchrName%_%caseName%%caseNameUnderscore%%Dvar%%dialogueName%" -overwrite;

ToolTip, %Clipboard%
SetTimer, RemoveToolTip, 2000
return

RemoveToolTip:
SetTimer, RemoveToolTip, Off
ToolTip

return

ButtonRun:							;		
Gui, Submit, NoHide

; проверяю, заполнены ли все поля
if chrName =
{
	MsgBox, , пустое поле, Выберите персонажа 
	Reload
}	
;~ if caseName =
;~ {
	;~ MsgBox, , пустое поле, Выберите название кейса
	;~ Reload
;~ }
if dialogueName =
{
	MsgBox, , пустое поле, Выберите номер диалога
	Reload
}

; условие, которое добавляет или убирает приставку D перед номером диалога
if (dialogueName = "CMT" or dialogueName = "MISC")
	Dvar =
else
	Dvar = D

if caseName = 
	caseNameUnderscore =
else
	caseNameUnderscore = _

;~ проверяю локализацию
local =
if Int = 1
	local = 
if Fra = 1
	local = _FRAN
if Deu = 1
	local = _DEUS


; опускаю регистр для имени _cue.upk, которые приходят в движок прописными
StringLower, lowCaseName, caseName
StringLower, LowDialogueName, dialogueName
StringLower, lowChrName, chrName
StringLower, lowDvar, Dvar
StringUpper, UpchrName, chrName, T

; перехожу на окно создания facefx animset, заполняю его
WinActivate, ahk_class #32770
if ErrorLevel
{
	MsgBox, FaceFX Window not exists
	ExitApp
}
Clipboard =
Clipboard = %chrName%_FaceFX_AnimSets%local% ; имя пакета, например, Sherlock_FaceFX_AnimSets
Send ^v{tab}
Clipboard =
Clipboard = facefx ; имя группы, facefx
Send ^v{tab}{tab} 
Clipboard = 
Clipboard = %chrName%_%caseName%%caseNameUnderscore%%Dvar%%dialogueName% ; имя facefxanimset, например, Sherlock_NA_D01
Send ^v 
Send {tab}{space}

;~ генерирую в буфер обмена команду для facefx studio, например, analyze -package "pt_dmisc_sherlock_sounds_cue"  -group "Sherlock_PT_DMISC" -overwrite;
Clipboard = 
Clipboard = analyze -package "%lowCaseName%%caseNameUnderscore%%lowDvar%%LowDialogueName%_%lowChrName%_sounds_cue" -group "%UpchrName%_%caseName%%caseNameUnderscore%%Dvar%%dialogueName%" -overwrite;
return

ButtonImport:							;		
Gui, Submit, NoHide

IfWinExist, Microsoft Excel - D%dialogueName%.xlsx
{
	WinActivate
	Send ^{SC01F}
	WinClose
}

;~ удаляю существующие файлы sounds_cue
Loop, d:\svn\ue3\SH8Game\Production\Content\Sounds\Case_%caseName%\*.upk, , 1
{
	IfInString, A_LoopFileFullPath, %dialogueName%
		FileDelete, %A_LoopFileFullPath%
}

batPath = d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\Import_Dialogs_%caseName%_D%dialogueName%.bat
batText = ..\..\..\..\Binaries\Win64\SH8Game.exe DialogImport -vCaseID=%caseName% -dialogIDs=D%dialogueName%

;~ IfExist, %batPath%
	;~ FileDelete, %batPath%
;~ FileAppend, %batText%, %batPath%

;~ Sleep, 1000
;~ MsgBox % batPath
;~ RunWait, %batPath%

;~ запускаю команду, которая импортирует spokenText в sounds_cue
;~ Run, cmd.exe, , , VarPID
;~ WinWait, ahk_pid  %VarPID%
;~ Send, cd d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\
;~ Send {Enter}
;~ Send, ..\..\..\..\Binaries\Win64\SH8Game.exe DialogImport -vCaseID=%caseName% -dialogIDs=D%dialogueName% ;-AUTO -UNATTENDED -NOPAUSE -NULLRHI
;~ Send {Enter}
;~ Sleep, 6000
;~ Send exit
;~ Send {Enter}

run, %comspec% /c d: &&cd d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\ &&..\..\..\..\Binaries\Win64\SH8Game.exe DialogImport -vCaseID=%caseName% -dialogIDs=D%dialogueName%
return


ButtonOpen:							;		
Gui, Submit, NoHide

IfExist, d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\D%dialogueName%.xlsx
	run, d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\D%dialogueName%.xlsx
else
	MsgBox, ...Case_%caseName%\D%dialogueName%.xlsx not exists
return

ButtonCommit:							;		
Gui, Submit, NoHide

IfExist, d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\D%dialogueName%.xlsx
	run, %comspec% d:&&/k cd d:\svn\ue3\SH8Game\Production\Dialogs\Case_%caseName%\&&svn update&&svn commit D%dialogueName%.xlsx -m updated_tags
else
	MsgBox, ...Case_%caseName%\D%dialogueName%.xlsx not exists
return



















