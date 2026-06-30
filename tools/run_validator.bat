@echo off
REM Convenience script to run the repository validator on Windows

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

echo Running repository validator...
echo Project root: %PROJECT_ROOT%
echo.

cd %PROJECT_ROOT%

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate" (
    call venv\Scripts\activate
) else if exist ".venv\Scripts\activate" (
    call .venv\Scripts\activate
)

REM Run the validator
python tools\repository_validator.py %*

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

if %EXIT_CODE% equ 0 (
    echo.
    echo [PASS] Repository validation PASSED
) else (
    echo.
    echo [FAIL] Repository validation FAILED
)

exit /b %EXIT_CODE%