@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

:MENU
cls
echo ======================================================
echo   ROUTEIQ - UBER FARE PREDICTION - START MENU
echo ======================================================
echo Project folder: %CD%
echo.
echo 1. Install / repair Python packages (pip)
echo 2. Run Interactive Analytics Dashboard (Streamlit)
echo 3. Train the fare prediction model
echo 4. Run RouteIQ Prediction App (Flask)
echo 5. Run project tests
echo 6. Exit
echo.
set /p choice=Choose 1-6: 

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto DASHBOARD
if "%choice%"=="3" goto TRAIN
if "%choice%"=="4" goto FLASK
if "%choice%"=="5" goto TESTS
if "%choice%"=="6" goto END
goto MENU

:INSTALL
echo.
echo [1/3] Checking Python...
python --version
if errorlevel 1 (
  echo Python was not found. Install Python 3.13 from python.org and enable Add Python to PATH.
  pause
  goto MENU
)
if not exist ".venv\Scripts\python.exe" (
  echo [2/3] Creating a local virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo Could not create the virtual environment.
    pause
    goto MENU
  )
)
echo [3/3] Bootstrapping pip and installing packages...
".venv\Scripts\python.exe" -m ensurepip --upgrade
if errorlevel 1 (
  echo ensurepip failed. Check that your Python installation includes pip.
  pause
  goto MENU
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto INSTALLERROR
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto INSTALLERROR
echo.
echo Installation completed.
pause
goto MENU

:INSTALLERROR
echo.
echo Package installation failed. Keep the full red error message and send it for diagnosis.
pause
goto MENU

:DASHBOARD
if not exist ".venv\Scripts\python.exe" (
  echo First choose option 1 to install dependencies.
  pause
  goto MENU
)
start "RouteIQ Analytics Dashboard" /D "%~dp0" "%~dp0.venv\Scripts\python.exe" -m streamlit run analytics_project\interactive_dashboard\app.py
goto MENU

:TRAIN
if not exist ".venv\Scripts\python.exe" (
  echo First choose option 1 to install dependencies.
  pause
  goto MENU
)
cd /d "%~dp0analytics_project"
..\.venv\Scripts\python.exe -m src.uber_fare.train
set traincode=%errorlevel%
cd /d "%~dp0"
if not "%traincode%"=="0" echo Training failed. Send the full error message.
pause
goto MENU

:FLASK
if not exist ".venv\Scripts\python.exe" (
  echo First choose option 1 to install dependencies.
  pause
  goto MENU
)
start "RouteIQ Prediction App" /D "%~dp0" "%~dp0.venv\Scripts\python.exe" -m flask --app routeiq_web_app.app run --debug
goto MENU

:TESTS
if not exist ".venv\Scripts\python.exe" (
  echo First choose option 1 to install dependencies.
  pause
  goto MENU
)
".venv\Scripts\python.exe" -m pytest -q
pause
goto MENU

:END
endlocal
exit /b 0
