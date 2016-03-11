
#Persistent

Menu, EmMenu, Add, Disgust, MenuHandler
Menu, EmMenu, Add  
Menu, EmMenu, Add, Wonder, MenuHandler
Menu, EmMenu, Add  
Menu, EmMenu, Add, Fear, MenuHandler
Menu, EmMenu, Add  
Menu, EmMenu, Add, Anger, MenuHandler
Menu, EmMenu, Add  
Menu, EmMenu, Add, Happiness, MenuHandler
Menu, EmMenu, Add  
Menu, EmMenu, Add, Sadness, MenuHandler

Menu, AmplMenu, Add, Light, MenuHandler
Menu, AmplMenu, Add  
Menu, AmplMenu, Add, Medium, MenuHandler
Menu, AmplMenu, Add  
Menu, AmplMenu, Add, Strong, MenuHandler

Menu, TimeMenu, Add, Quick, MenuHandler
Menu, TimeMenu, Add  
Menu, TimeMenu, Add, Medium, MenuHandler
Menu, TimeMenu, Add  
Menu, TimeMenu, Add, Long, MenuHandler

;~ Menu, EaseOutMenu, Add, Standart, MenuHandler
;~ Menu, EaseOutMenu, Add  
;~ Menu, EaseOutMenu, Add, Long, MenuHandler

;~ Menu, EaseInMenu, Add, Standart, MenuHandler
;~ Menu, EaseInMenu, Add  
;~ Menu, EaseInMenu, Add, Long, MenuHandler

return  ; End of script's auto-execute section.

MenuHandler:
return

MButton::
Menu, EmMenu, Show
emRId = %A_ThisMenuItem%
Menu, AmplMenu, Show
amplRId = %A_ThisMenuItem%
Menu, TimeMenu, Show 
timeRId = %A_ThisMenuItem%
;~ Menu, EaseOutMenu, Show 
;~ EORId = %A_ThisMenuItem%
;~ Menu, EaseInMenu, Show 
;~ EIRId = %A_ThisMenuItem%

if emRId = Disgust
	emId = d
if emRId = Wonder
	emId = bw
if emRId = Fear
	emId = f
if emRId = Anger
	emId = a
if emRId = Happiness
	emId = h
if emRId = Sadness
	emId = s
if amplRId = Light
	amplId = 3
if amplRId = Medium
	amplId = 5
if amplRId = Strong
	amplId = 8
if timeRId = Quick
	timeId = 3
if timeRId = Medium
	timeId = 5
if timeRId = Long
	timeId = 9
;~ if EORId = Standart
	;~ EOId = 5
;~ if EORId = Long
	;~ EOId = 7
;~ if EIRId = Standart
	;~ EIId = 6
;~ if EIRId = Long
	;~ EIId = 8


IfWinExist, ahk_class XLMAIN
{
	WinActivate

	Clipboard =
	Clipboard = /%emId%%amplId%7%timeId%5
	;~ Clipboard = /%emId%%amplId%%EIId%%timeId%%EOId%
	;~ MsgBox, /%emId%%amplId%8%timeId%5
	Send, {SC039}^{SC02F}{SC039}
}

return






















