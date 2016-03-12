#Persistent

IfExist, d:\svn\ue3\sqlite3.exe
	sqliteExe = d:\svn\ue3\sqlite3.exe
else
	InputBox, sqliteExe, Enter path to sqlite.exe
	if ErrorLevel
		ExitApp

InputBox, wcdbPath, wc.db fix, Does the following:`n"pragma integrity_check"`n"reindex nodes"`n"reindex pristine"`nEnter path to the wc.db, Error
if ErrorLevel
    ExitApp
else
	run, %comspec% /k %sqliteExe% %wcdbPath% "pragma integrity_check"&&%sqliteExe% %wcdbPath% "reindex nodes"&&%sqliteExe% %wcdbPath% "reindex pristine"
ExitApp