#!/bin/bash
set -e

sudo -u vivek -i bash <<'EOF'
cd /home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate
git fetch --all
git reset --hard origin/deploy
chmod +x deploy.sh
./deploy.sh deploy
EOF
