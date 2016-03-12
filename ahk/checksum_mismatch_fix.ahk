#Persistent

;~ набрать в терминале, который вызывается по cmd
;~ d:
;~ cd d:\svn\ue3\Binaries\ORBIS\
;~ svn update --set-depth empty
;~ svn update --set-depth infinity


InputBox, cMPath, checksum mismatch fix,Does the following:`nsvn update --set-depth empty`nsvn update --set-depth infinity`nEnter the path to the folder
if ErrorLevel
    ExitApp
else
	run, %comspec% /k svn update --set-depth empty %cMPath%&&svn update --set-depth infinity %cMPath%
ExitApp