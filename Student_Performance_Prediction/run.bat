@echo off
title Student Performance Prediction
cd /d "%~dp0"
echo ==========================================
echo  Student Performance Prediction System
echo ==========================================
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer and try again.
  pause
  exit /b 1
)
if not exist "venv\Scripts\python.exe" (
  echo Creating virtual environment...
  python -m venv venv
)
echo Installing required packages...
call venv\Scripts\python.exe -m pip install --upgrade pip
call venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo Package installation failed. Check your internet connection.
  pause
  exit /b 1
)
echo Training ML model...
call venv\Scripts\python.exe train_model.py
if errorlevel 1 (
  echo Model training failed.
  pause
  exit /b 1
)
echo Starting web application...
echo Open http://127.0.0.1:5000 in your browser.
start "" http://127.0.0.1:5000
call venv\Scripts\python.exe app.py
pause
