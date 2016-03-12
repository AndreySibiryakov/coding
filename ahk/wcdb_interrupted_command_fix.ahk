#Persistent

IfExist, d:\svn\ue3\sqlite3.exe
	sqliteExe = d:\svn\ue3\sqlite3.exe
else
	InputBox, sqliteExe, Enter path to sqlite.exe
	if ErrorLevel
		ExitApp

InputBox, wcdbPath, wc.db clear work queue, Does the following:`n“select * from work_queue”`n“delete from work_queue”`nEnter path to the wc.db, Error
if ErrorLevel
    ExitApp
else
	run, %comspec% /k %sqliteExe% %wcdbPath% "select * from work_queue"&&%sqliteExe% %wcdbPath%  "delete from work_queue"
ExitApp