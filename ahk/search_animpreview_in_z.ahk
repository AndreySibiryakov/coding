/* ������ ������
 * 
 * ��������� �� ������ - ������ ������ �� ������
 * ������ ������� �� ������ �����
 * ������� ������ �������
 * � ������ ������� ��� instr �� ����� �����
 * ���� ������ - ������� �������
 * ��������� �����
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
chrName := Clipboard ; ���������� ������������ ��� ��������� �����.
if FileList =
{
	FileList = end`n ; �������� ����� ����� ������� ������
	Loop, z:\.src\shared\chr\_face\.anims_preview_database\*, , 1 ; ��� ��� ����� .max �� �������� ����
	{
		FileList = %FileList%%A_LoopFileFullPath%`n ; ��������� ������ �� ���
	}
	Sort, FileList, R  ; �������� ������ � �������� �������, ����� ������� "end" ��������� ������
}

Loop, parse, FileList, `n ; ����������� ��������� ������
{
	;~ MsgBox % A_LoopField
	IfInString, A_LoopField, %chrName% ;  ���� ������� �������� ��� ���������
	{	
		;~ MsgBox, found
		Run, %A_LoopField%, max
		;~ Clipboard := A_LoopField ; ������� ������� � ����� ������
		;~ MsgBox, 1,, ���������� ����`n%A_LoopField%, ���������� �����?
		;~ IfMsgBox Ok ; ���� ���� ���������� - ����� ��������������� 
			;~ continue ; return
		;~ else ; ���� ���, ����� ������������
		return
	}	
	if A_LoopField = end ; ���� ������� �������� "end" ������ ����� ������� � ����� � �� ��� �����������
	{	
		MsgBox, %chrName% �� ������
		reload
	}
}
reload


#SC01E::
Clipboard =
Send ^{SC02E}
ClipWait,,1
animName := Clipboard ; ���������� ������������ ��� ��������� �����.
if animFileList =
{
	animFileList = end`n ; �������� ����� ����� ������� ������
	Loop, z:\.src\shared\chr\_face\.clips\*, , 1 ; ��� ��� ����� �� �������� ����
	{
		animFileList = %animFileList%%A_LoopFileFullPath%`n ; ��������� ������ �� ���
	}
	Sort, animFileList, R  ; �������� ������ � �������� �������, ����� ������� "end" ��������� ������
}

Loop, parse, animFileList, `n ; ����������� ��������� ������
{
	;~ MsgBox % A_LoopField
	IfInString, A_LoopField, %animName% ;  ���� ������� �������� ��� ���������
	{	
		Clipboard := A_LoopField ; ������� ������� � ����� ������
		ToolTip, copied %animName% link
		SetTimer, RemoveToolTip, 2000
		return

		RemoveToolTip:
		SetTimer, RemoveToolTip, Off
		ToolTip
		return
	}	
	if A_LoopField = end ; ���� ������� �������� "end" ������ ����� ������� � ����� � �� ��� �����������
	{	
		MsgBox, %animName% �� ������
		return
	}
}
reload
