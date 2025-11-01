#!/bin/bash

echo "🚀 Starting NorthStar AI Backend..."
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running!"
    echo ""
    echo "Start MongoDB first:"
    echo "  Option 1 (Docker): docker run -d -p 27017:27017 --name mongodb mongo:latest"
    echo "  Option 2 (Local):  mongod --dbpath /path/to/data"
    echo ""
    read -p "Press Enter after starting MongoDB..."
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file..."
    cat > backend/.env << 'EOF'
MONGO_URL=mongodb://localhost:27017
DB_NAME=growth_copilot_db
CORS_ORIGINS=*
GOOGLE_API_KEY=your-key-here
EOF
    echo "✓ Created backend/.env"
    echo ""
    echo "⚠️  IMPORTANT: Update GOOGLE_API_KEY in backend/.env with your actual API key!"
    echo ""
    read -p "Press Enter after updating the API key..."
fi

# Check if ai_engine.py exists
if [ ! -f "backend/ai_engine.py" ]; then
    echo "❌ ai_engine.py not found in backend/"
    echo "Make sure all files are in place"
    exit 1
fi

# Install requirements if needed
echo "📦 Checking dependencies..."
pip install -q -r backend/requirements.txt 2>/dev/null || echo "⚠️  Some dependencies may be missing"

echo ""
echo "✓ All checks passed!"
echo ""
echo "Starting server on http://localhost:8001"
echo "Press Ctrl+C to stop"
echo ""
echo "In another terminal, run: python play_with_backend.py"
echo ""

cd backend
uvicorn server:app --reload --port 8001
