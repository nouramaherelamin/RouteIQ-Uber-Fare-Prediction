@echo off
cd /d "%~dp0"
python -m flask --app routeiq_web_app.app run --debug
