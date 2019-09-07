#Persistent
; ALT + h to start the application
!h::realtime_python_http_server()

; Download WatchFolder.ahk and put it in the same folder as the script
#Include WatchFolder.ahk

; Start the application and listen for changes in project folder and subfolders
realtime_python_http_server() {
	FolderPath := "C:\Users\userName\Dropbox\Personal\Dev\AutoHotKey"
	Run, python -m http.server 8000,,min
	WatchFolder(FolderPath, "rebuild_python_http_server", SubTree := True, Watch := 0x016)
}

; When a file is updated, Close existing process and run it again
rebuild_python_http_server(Folder, Changes) {
	Process, Close, python.exe
	Run, python -m http.server 8000,,min
}