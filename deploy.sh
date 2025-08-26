#!/bin/bash
set -e  # exit if any command fails

echo "Pulling latest code..."
cd ~
cd ~/Ai-agent-boilerplate
git pull origin deploy

echo "Activating virtualenv..."
cd ai-agent-boilerplate
source venv/bin/activate

echo "Setup .env file"
cd code
echo -n > .env
cat <<EOF > .env
DEBUG=True
GROQ_API_KEY=${GROQ_API_KEY}
GROQ_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct
# PostgreSQL Database Configuration
# Local PostgreSQL connection (adjust username/password as needed)
DATABASE_URL=postgresql://postgres:${POSTGRES_PASSWORD}@localhost:5432/
EOF

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Restarting service..."
pkill -f flask
export FLASK_APP=app.py
nohup flask run --host=0.0.0.0 --port=5000


echo "✅ Deployment complete!"
