#!/bin/bash

echo "-- Welcome to the Flashdrop Installer --"
echo "----------------------------------------"

echo -n "Set your Flashdrop Access Password (typing will be hidden): "
read -s APP_PASSWORD
echo ""

SECRET_KEY=$(openssl rand -hex 24)

echo "Creating .env file..."
echo "SECRET_KEY=$SECRET_KEY" > .env
echo "PASSWORD=$APP_PASSWORD" >> .env

echo "Creating folders..."
mkdir -p certs uploads

echo "Generating local SSL certificates..."
openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/key.pem -out certs/cert.pem -days 365 -subj "/CN=localhost" 2>/dev/null

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "----------------------------------------"
echo "Installation complete!"
echo "To start Flashdrop, execute the run.sh file."