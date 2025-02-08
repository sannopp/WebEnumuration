@REM put folder path in "input.txt" file

@echo off
setlocal EnableDelayedExpansion

for /f "delims=" %%i in ('type input.txt') do (
  set line=%%i
  set a=!line:~-15!
  @REM echo xcopy !line! 
  echo New Folder\!a!
  xcopy "!line!" "New Folder\!a!\"   /E /H /C /I /S /q
)

pause

