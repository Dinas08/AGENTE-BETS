@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
title Agente Bets - dashboard (nao feches esta janela)
echo A abrir a dashboard... (nao feches esta janela enquanto a usares)
start "" /b cmd /c "timeout /t 6 /nobreak >nul & start "" http://127.0.0.1:8501"
".venv\Scripts\python.exe" -m streamlit run dashboard.py
