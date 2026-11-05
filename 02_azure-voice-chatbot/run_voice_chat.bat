@echo off
chcp 65001 >nul
cd /d "%~dp0"
call ..\.venv\Scripts\activate
set PYTHONIOENCODING=utf-8
python main.py
pause