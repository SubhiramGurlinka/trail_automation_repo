@echo off
REM get path of bat file
set mypath=%~dp0
set pubpass=%1

git pull

git branch --show-current | find "main" && echo ERROR: on main! test prop normally from branch && EXIT /B 1

REM delete previous prop, if any
del "%mypath%\propagation\*.fxf"

echo prop from branch:
git branch --show-current

REM switch to folder that contains BFSitePropTool.exe
cd ..\_PropTool
start "prop-test" /WAIT /B /D "%mypath%" BFSitePropTool.exe --config-file prop-test.cfg --publisher-password %pubpass%

set propexitcode=%errorlevel%

echo prop test Exit Code is %propexitcode%

cd "%mypath%"

if not exist "%mypath%\propagation\Updates.fxf" (
    echo Updates.fxf does not exist!
    EXIT /B 1

) else (
    if %propexitcode% NEQ 0 (
        echo ERROR!
        EXIT /B %propexitcode%
    ) else (
    echo Success!
    )
)
