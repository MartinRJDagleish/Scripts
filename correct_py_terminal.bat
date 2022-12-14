echo "Correcting file assocation for .py in Terminal."

@echo off
goto check_Permissions

:check_Permissions
echo Administrative permissions required. Detecting permissions...

net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Current permissions inadequate.
)

pause >nul

assoc .py=Python.File 

ftype Python.File="C:\Python310\python.exe" "%1"

