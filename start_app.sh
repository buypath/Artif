#!/bin/bash
# Start the Streamlit web application

echo "Starting Document Processing System Web UI..."
echo "=============================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please add your ANTHROPIC_API_KEY"
    echo ""
fi

# Check if API key is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: ANTHROPIC_API_KEY not set in .env file"
    echo "Please edit .env and add your API key before using the application"
    echo ""
fi

# Create necessary directories
mkdir -p output
mkdir -p uploads

# Start Streamlit
echo "Starting Streamlit on http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
