#!/bin/bash
# ResumeCraft - Start Both Apps

echo "🚀 Starting ResumeCraft Applications..."
echo ""

# Change to backend directory
cd "$(dirname "$0")/backend"

# Kill existing processes
echo "🛑 Stopping existing processes..."
lsof -ti:8501,8502 | xargs kill -9 2>/dev/null
sleep 2

# Start main unified app
echo "📝 Starting Main App (Port 8501)..."
./venv/bin/streamlit run app.py --server.headless=true --server.port 8501 &
MAIN_PID=$!

# Wait a moment
sleep 3

# Start Entity Resolution standalone
echo "🎯 Starting Entity Resolution (Port 8502)..."
./venv/bin/streamlit run app_entity_resolution.py --server.headless=true --server.port 8502 &
ENTITY_PID=$!

# Wait for apps to start
sleep 3

echo ""
echo "✅ Apps Started Successfully!"
echo ""
echo "📱 Access your applications:"
echo "   Main App:            http://localhost:8501"
echo "   Entity Resolution:   http://localhost:8502"
echo ""
echo "🛑 To stop apps, press Ctrl+C or run:"
echo "   lsof -ti:8501,8502 | xargs kill -9"
echo ""

# Wait for processes
wait $MAIN_PID $ENTITY_PID
