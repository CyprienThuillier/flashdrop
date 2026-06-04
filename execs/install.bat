@echo off
title Flashdrop Installer
echo -- Welcome to the Flashdrop Installer --
echo ----------------------------------------

set /p APP_PASSWORD="Set your Flashdrop Access Password: "

echo Generating secure secret key...
for /f "delims=" %%i in ('powershell -Command "[Convert]::ToBase64String((1..32 | ForEach-Object { [byte](Get-Random -Min 0 -Max 256) }))"') do set SECRET_KEY=%%i

echo Creating .env file...
echo SECRET_KEY=%SECRET_KEY% > .env
echo PASSWORD=%APP_PASSWORD% >> .env

echo Creating folders...
if not exist certs mkdir certs
if not exist uploads mkdir uploads

echo Generating local SSL certificates...
where openssl >nul 2>nul
if %ERRORLEVEL% equ 0 (
    openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/key.pem -out certs/cert.pem -days 365 -subj "/CN=localhost" 2>nul
) else (
    echo [WARNING] OpenSSL not found. You will need to generate certs/cert.pem and certs/key.pem manually.
)

echo Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ----------------------------------------
echo Installation complete!
echo To start Flashdrop, execute the run.bat file.
pause