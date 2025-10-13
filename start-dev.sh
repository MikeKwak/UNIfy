#!/bin/bash

# UNIfy Development Server Startup Script

echo "🚀 Starting UNIfy Development Environment"
echo "========================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create one with your GEMINI_API_KEY"
    exit 1
fi

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Python virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Node modules not found. Please run:"
    echo "   npm install"
    exit 1
fi

echo ""
echo "📋 Starting services..."
echo ""

# Function to kill background processes on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $FLASK_PID 2>/dev/null || true
    kill $REACT_PID 2>/dev/null || true
    wait
    echo "✅ All services stopped"
}

# Set up trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Start Flask backend
echo "🐍 Starting Flask API server..."
source .venv/bin/activate
export FLASK_PORT=5001
python app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 3

# Check if Flask is running
if kill -0 $FLASK_PID 2>/dev/null; then
    echo "✅ Flask API server started (PID: $FLASK_PID)"
    echo "   📍 API available at: http://localhost:5001"
else
    echo "❌ Failed to start Flask server"
    exit 1
fi

# Start React frontend
echo ""
echo "⚛️  Starting React development server..."
npm run dev &
REACT_PID=$!

# Wait a moment for React to start
sleep 3

# Check if React is running
if kill -0 $REACT_PID 2>/dev/null; then
    echo "✅ React dev server started (PID: $REACT_PID)"
    echo "   📍 Frontend available at: http://localhost:5173"
else
    echo "❌ Failed to start React server"
    kill $FLASK_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "🎉 UNIfy is now running!"
echo "========================================"
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:5001"
echo "API Test: http://localhost:5001/api/test"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user to interrupt
wait
