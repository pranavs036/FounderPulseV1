#!/bin/bash

# NorthStar AI Docker Stop Script

echo "🛑 Stopping NorthStar AI services..."

# Stop all services
docker-compose down

# Remove volumes (optional - uncomment if you want to reset data)
# echo "🗑️  Removing volumes..."
# docker-compose down -v

echo "✅ All services stopped"
echo ""
echo "To start again: ./docker-start.sh"
echo "To reset all data: docker-compose down -v"
