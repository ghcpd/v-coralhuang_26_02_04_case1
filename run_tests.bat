@echo off
python -m pytest tests/
if %errorlevel% neq 0 exit /b %errorlevel%