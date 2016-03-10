; ������ ���������� ���������� ����� ��� facefx animsets ��� unreal engine, sherlock 8
; � ��������� � ����� ������ ������� batch analyze ��� facefx studio.

#Persistent

; ������ ����������
chrList = Albeit Alice Arthur Ashley Barman bc_pass Bernard Billy Cab cabDriver2 Charles Child Child ChildWC Conspirator Customer DeadDriver DeadPass DeadPhaeton doctor dog Driver DriverCarr DriverLC drunkard DrvrScflds Dweller Fakir Fleischer Fleischer_Pub FlowersGirl Gambler gambler2 George Guard Guard2 GuardIB Harrington Harry Hudson Informer Inspector Jeremiah Katelyn loser Mary Mechanic Mosley Mother Mycroft Oliver Orson OrsonSh Otto OttoCab Patient Peasant pedestrian Percy PhaetPass Player1 Player2 Player3 Policeman Policeman Pygmy Racist1 Racist2 Robber Sherlock shopowner Sweeper Thief Thug1 Thug3 Thug4 Toby Tom Watchman Watson Worker Worker workInjur Zacharias ZachariasNA

StringUpper, upNameList, chrList, T
nameList := RegExReplace(upNameList, " ", "|")

; ������ ������ (���)
caseList = FD|GD|IB|IN|NA|PT

; ������ ���������� ������ ��������
loop, 25
{
	num := A_Index
	if (num < 10)
		num := "0" . num
	if dList =
		dList := "cmt|misc"
	dList .= "|" . num
}

Gui, Add, ComboBox, vchrName x16 y37 w170 h50 sort H500, %nameList%
Gui, Add, ComboBox, vcaseName x196 y37 w60 h10 sort Uppercase H500, %caseList%
Gui, Add, ComboBox, vdialogueName x266 y37 w80 h20 sort Uppercase H500, %dList% ; %dialogueList%
Gui, Add, Text, x16 y10 w160 h30 , Character
Gui, Add, Text, x196 y10 w50 h30 , Case
Gui, Add, Text, x266 y10 w70 h30 , Dialogue
Gui, Add, Button, x356 y27 w60 h30 , Run
Gui, Show, w574 h76, Generate naming for SK animset
Gui, Add, Button, x426 y37 w60 h20 , Set
Gui, Add, Text, x426 y7 w60 h20 , head AS
Gui +AlwaysOnTop
return

GuiClose:
ExitApp

ButtonRun:							;		
Gui, Submit, NoHide

; ��������, ��������� �� ��� ����
if chrName =
{
	MsgBox, , ������ ����, �������� ��������� 
	Reload
}	
if caseName =
{
	MsgBox, , ������ ����, �������� �������� �����
	Reload
}
if dialogueName =
{
	MsgBox, , ������ ����, �������� ����� �������
	Reload
}

; �������, ������� ��������� ��� ������� ��������� D ����� ������� �������
if (dialogueName = "CMT" or dialogueName = "MISC")
	Dvar =
else
	Dvar = D

; ������� ������� ��� ����� _cue.upk, ������� �������� � ������ ����������
StringLower, lowCaseName, caseName
StringLower, LowDialogueName, dialogueName
StringLower, lowChrName, chrName
StringLower, lowDvar, Dvar
StringUpper, UpchrName, chrName, T

; �������� �� ���� �������� facefx animset, �������� ���
WinActivate, ahk_class #32770
if ErrorLevel
{
	MsgBox, FaceFX Window not exists
	ExitApp
}
Clipboard =
Clipboard = anim_sh8_%lowChrName%_dialogue ; ��� ������, ��������, Sherlock_FaceFX_AnimSets
Send ^v{tab}
Sleep, 50
Send ^a{Delete}
Sleep, 50
Send {tab}{tab} 
Clipboard = 
Clipboard = AS_%lowChrName%_%caseName%_%Dvar%%dialogueName%_face ; ��� facefxanimset, ��������, Sherlock_NA_D01
Sleep, 50
Send ^v 
Sleep, 50
Send {tab}{space}

Sleep, 5000
Send !f
Sleep, 1000
Send {down}{down}{Enter}

Clipboard = 
Clipboard = e:\SH8\.dialogues\%caseName%_%Dvar%%dialogueName%\anims_FBX\
Send ^V
Sleep, 500
Send {enter}


ButtonSet:							;		
Gui, Submit, NoHide

; ��������, ��������� �� ��� ����
if caseName =
{
	MsgBox, , ������ ����, �������� �������� �����
	Reload
}
if dialogueName =
{
	MsgBox, , ������ ����, �������� ����� �������
	Reload
}

; �������, ������� ��������� ��� ������� ��������� D ����� ������� �������
if (dialogueName = "CMT" or dialogueName = "MISC")
	Dvar =
else
	Dvar = D

; ������� ������� ��� ����� _cue.upk, ������� �������� � ������ ����������
StringLower, lowCaseName, caseName
StringLower, LowDialogueName, dialogueName
StringLower, lowChrName, chrName
StringLower, lowDvar, Dvar
StringUpper, UpchrName, chrName, T

; �������� �� ���� �������� facefx animset, �������� ���
WinActivate, ahk_class #32770
if ErrorLevel
{
	MsgBox, FaceFX Window not exists
	ExitApp
}
Clipboard =
Clipboard = anim_sh8_head_dialogue ; ��� ������, ��������, Sherlock_FaceFX_AnimSets
Send ^v{tab}
Sleep, 50
Send ^a{Delete}
Sleep, 50
Send {tab}{tab} 
Clipboard = 
Clipboard = AS_%caseName%_%Dvar%%dialogueName%_Head ; ��� facefxanimset, ��������, Sherlock_NA_D01
Sleep, 50
Send ^v 
Sleep, 50
Send {tab}{space}

Sleep, 5000
Send !f
Sleep, 1000
Send {down}{down}{Enter}

Clipboard = 
Clipboard = e:\SH8\.dialogues\%caseName%_%Dvar%%dialogueName%\
Send ^V
Sleep, 500
Send {enter}
return



