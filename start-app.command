#!/bin/bash

echo "🚀 Starting Text-to-TikTok Video Generator..."
echo ""
echo "Backend starting on http://localhost:8000"
echo "Frontend starting on http://localhost:3000"
echo "Mobile access: http://192.168.1.169:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

cd "$(dirname "$0")/backend"
source venv/bin/activate
python main.py &

BACKEND_PID=$!

cd "$(dirname "$0")/frontend"
npm run dev &
FRONTEND_PID=$!

wait $BACKEND_PID $FRONTEND_PID
