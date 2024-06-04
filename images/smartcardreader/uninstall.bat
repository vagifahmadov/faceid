@echo off

"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\smartcardreader.exe" stop

DEL /Q "%windir%\jpcsc.dll" > nul
DEL /Q "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\" > nul

SET tmpVar=0

IF EXIST "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\smartcardreader.exe" (SET tmpVar=1)
IF EXIST "%windir%\jpcsc.dll" (SET tmpVar=1)

cls

if %tmpVar%==0 (GOTO success)
color 47
echo Ugursuz oldu. Xahish edirik 'uninstall.bat' fayli uzerinde sag klikleyin ve 'Run as adminstrator' sechin.
timeout 80

goto finish
:success
color 17
echo Ugurla silindi.
timeout 8


:finish
