#!/bin/bash
set -e

cd /home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate

# pull latest code
git fetch --all
git reset --hard origin/deploy  # or origin/main depending on your branch

# run your deployment script
chmod +x deploy.sh
./deploy.sh deploy
