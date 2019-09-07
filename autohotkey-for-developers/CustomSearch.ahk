!s::search()
!LButton::search()

search() {
	Clipboard := ""
	Send, ^c
	ClipWait, 2
	Run, https://www.google.com/
	WinWaitActive, Google, ,10
	if ErrorLevel {
		MsgBox, Seems like google.com did not open.
		return
	}
	Send, ^v 
	Send, {Enter}
	return
}
	