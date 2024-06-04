cd "%~dp0"
@echo off

"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\smartcardreader.exe" stop

copy "jpcsc.dll" "%windir%\jpcsc.dll" > nul
copy "smartcardreader.exe" "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\" > nul

SET tmpVar=0

IF NOT EXIST "%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\smartcardreader.exe" (SET tmpVar=1)
IF NOT EXIST "%windir%\jpcsc.dll" (SET tmpVar=1)

cls

"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup\smartcardreader.exe"

if %tmpVar%==0 (GOTO success)
color 47
echo Yukleme ugursuz tamamlandi. Xahish edirik 'install.bat' fayli uzerinde sag klikleyin ve 'Run as adminstrator' sechin.
timeout 80

goto finish
:success
color 17
echo Yukleme ugurla tamamlandi.
timeout 8


:finish
