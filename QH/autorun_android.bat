@echo off

cd C:\Tools\Android\
cmd /c "Android_scanner.bat"
set /p input= "Enter Path: "
@REM echo Input is: "%input%"
cd C:\Tools\Android\Scanner\
qhscan.exe "%input%"
pause
