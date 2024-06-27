:<<"::CMDLITERAL"
@echo off
REM the above hides the rest from BASH


REM get path of bat file
set mypath=%~dp0

REM delete previous prop, if any
del "%mypath%\propagation\fixlets.fxf"

REM switch to folder that contains BFSitePropTool.exe
cd C:\tmp\_Prop\PropTool
start "prop-verify" /WAIT /B /D "%mypath%" BFSitePropTool.exe --config-file prop-verify.cfg

set propexitcode=%errorlevel%

echo prop verify Exit Code is %propexitcode%

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

REM the following hides the rest from BASH
::CMDLITERAL
