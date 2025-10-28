#!/bin/bash

# UNIfy Development Startup Script
echo "🚀 Starting UNIfy Development Environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js v18 or higher."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python v3.8 or higher."
    exit 1
fi

# Install dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

if [ ! -d "server/venv" ]; then
    echo "🐍 Setting up Python virtual environment..."
    cd server && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cd ..
fi

# Start both frontend and backend
echo "🎯 Starting frontend and backend servers..."
echo "Frontend will be available at: http://localhost:5173"
echo "Backend API will be available at: http://localhost:5000"
echo ""

# Use concurrently to run both servers
npx concurrently "cd frontend && npm run dev" "cd server && source venv/bin/activate && python app.py"

