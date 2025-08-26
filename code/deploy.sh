#!/bin/bash
set -e  # exit if any command fails

echo "Pulling latest code..."
git pull origin main

echo "Activating virtualenv..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Restarting service..."
systemctl restart myapp

echo "✅ Deployment complete!"
