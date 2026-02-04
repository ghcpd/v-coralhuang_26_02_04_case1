@echo off
REM Test runner script for ClickHouse tuple parsing fix
REM This script runs the test suite on Windows with a single command

setlocal enabledelayedexpansion

echo ============================================================
echo   Running ClickHouse Tuple Parsing Fix Test Suite
echo ============================================================
echo.

REM Try to find python in .venv first, otherwise use system python
if exist ".venv\Scripts\python.exe" (
    set PYTHON_CMD=.venv\Scripts\python.exe
    echo Using Python from virtual environment: !PYTHON_CMD!
) else (
    set PYTHON_CMD=python
    echo Using system Python: !PYTHON_CMD!
)
echo.

REM Run pytest on the test file
echo Running pytest...
!PYTHON_CMD! -m pytest tests/test_clickhouse_tuple_fix.py -v --tb=short

REM Capture exit code
set EXIT_CODE=%ERRORLEVEL%

echo.
echo ============================================================
if %EXIT_CODE% equ 0 (
    echo   All tests PASSED!
) else (
    echo   Tests FAILED with exit code %EXIT_CODE%
)
echo ============================================================

exit /b %EXIT_CODE%
