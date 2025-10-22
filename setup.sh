#!/bin/bash

# ResumeCraft Setup Script
# This script automates the setup process for ResumeCraft

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              ResumeCraft - Setup Script                      ║"
echo "║      AI-Powered Resume Management System                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✅ Python version $python_version detected"
echo ""

# Navigate to backend directory
cd backend || exit

# Create virtual environment
echo "🔨 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "   (This may take a few minutes...)"
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi
echo ""

# Setup environment file
echo "⚙️  Setting up environment configuration..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping..."
else
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  IMPORTANT: Please edit .env and add your OpenAI API key"
fi
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p temp
echo "✅ Directories created"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   Setup Complete! 🎉                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file and add your OpenAI API key:"
echo "   nano .env"
echo ""
echo "2. Run the example usage script:"
echo "   python example_usage.py"
echo ""
echo "3. Start the API server:"
echo "   python main.py"
echo ""
echo "4. Access API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "Happy recruiting! 🚀"
echo ""
