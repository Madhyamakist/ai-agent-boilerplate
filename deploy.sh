#!/bin/bash
set -e  # exit if any command fails

echo "Going to dir"
cd /home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate

echo "Activating virtualenv..."
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
pkill -f flask || true
cd /home/vivek/Ai-agent-boilerplate/ai-agent-boilerplate/code
export FLASK_APP=app.py
nohup flask run --host=0.0.0.0 --port=5000 > flask.log 2>&1 &


echo "✅ Deployment complete!"
