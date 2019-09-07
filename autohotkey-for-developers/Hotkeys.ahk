f5::chrome()
f6::vscode()

chrome() {
	Process, Exist, chrome.exe
	{
		If ! errorLevel {
			Run, chrome.exe
		}
		else {	
			SetTitleMatchMode RegEx
			WinActivate Google Chrome
		}
	}
}

vscode() {
	Process, Exist, Code.exe
	{
		If ! errorLevel {
			Run, C:\Users\userName\AppData\Local\Programs\Microsoft VS Code\code.exe
		}
		else {	
			SetTitleMatchMode RegEx
			WinActivate Visual Studio Code
		}
	}
}