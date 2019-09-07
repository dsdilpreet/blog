#Persistent
#Include WatchFolder.ahk

WatchFolder("C:\Users\dilpreet\Downloads", "move_log_files", SubTree := False, Watch := 0x01)

move_log_files(Folder, Changes) {
	FormatTime, CurrentDateTime,, dd-MM-yyyy-HHmmss
	Loop, Files, C:\Users\dilpreet\Downloads\*diag*.csv
	{	
		; Move and rename the file with current date and time.
		; For example. diag.csv will become 07-09-2019-203332_diag.csv
		FileMove, %A_LoopFileLongPath%, %A_MyDocuments%\Logs\%CurrentDateTime%_%A_LoopFileName%
	}
}