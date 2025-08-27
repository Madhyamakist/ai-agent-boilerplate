#!/bin/bash
# update_app.sh
# Runs on VM startup, pulls latest code, and triggers deploy.sh

LOG_FILE="/var/log/update_app.log"

# Start logging
echo "==== $(date): Starting update_app.sh ====" | tee -a "$LOG_FILE"
exec >> "$LOG_FILE" 2>&1
set -ex

cd /home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate


echo "Pulling latest code..."
git -c safe.directory=/home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate fetch --all
git -c safe.directory=/home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate reset --hard origin/deploy

echo "Running deploy.sh..."
chmod +x deploy.sh
./deploy.sh deploy
