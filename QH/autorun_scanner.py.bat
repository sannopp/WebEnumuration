@echo off
cd C:\Tools\qhscanner
set /p input= "Enter Path: "
@REM echo Input is: "%input%"
python scanner.py "%input%"
pause
