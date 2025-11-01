# 🐳 Docker Setup Guide for NorthStar AI

Complete Docker setup for running NorthStar AI with all services containerized.

## 🚀 Quick Start

```bash
# 1. Set up environment
cp docker.env .env
# Edit .env and add your GOOGLE_API_KEY

# 2. Start everything
./docker-start.sh

# 3. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

## 📋 Prerequisites

- Docker Desktop installed and running
- Valid Google API key

## 🔧 Setup Steps

### 1. Environment Configuration

```bash
# Copy environment template
cp docker.env .env

# Edit .env file and add your API key
nano .env
```

Required environment variables:
```bash
GOOGLE_API_KEY=your-google-api-key-here
```

### 2. Start All Services

```bash
# Start everything with one command
./docker-start.sh
```

This will:
- Build all Docker images
- Start MongoDB, Backend, and Frontend
- Check service health
- Display access URLs

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **MongoDB**: localhost:27017

## 🛠️ Docker Services

### MongoDB
- **Image**: mongo:7.0
- **Port**: 27017
- **Database**: growth_copilot_db
- **Credentials**: admin/password123
- **Persistent Volume**: mongodb_data

### Backend API
- **Port**: 8001
- **Health Check**: /api/health
- **Dependencies**: MongoDB
- **Environment**: Python 3.11

### Frontend
- **Port**: 3000 (mapped to container port 80)
- **Build**: React production build
- **Web Server**: Nginx
- **Dependencies**: Backend API

## 📜 Available Scripts

### Start Services
```bash
./docker-start.sh
```

### Stop Services
```bash
./docker-stop.sh
```

### View Logs
```bash
./docker-logs.sh
```

### Manual Commands
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up --build -d
```

## 🔍 Troubleshooting

### Services Not Starting
```bash
# Check Docker is running
docker info

# Check service status
docker-compose ps

# View logs for specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mongodb
```

### Reset Everything
```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Remove all images (optional)
docker-compose down --rmi all

# Start fresh
./docker-start.sh
```

### Backend Connection Issues
```bash
# Check if backend is responding
curl http://localhost:8001/api/health

# Check backend logs
docker-compose logs backend
```

### Frontend Not Loading
```bash
# Check if frontend container is running
docker-compose ps frontend

# Check frontend logs
docker-compose logs frontend
```

## 🗄️ Data Persistence

- **MongoDB Data**: Stored in Docker volume `mongodb_data`
- **Sample Data**: Available in `sample_data/` directory
- **Reset Data**: Use `docker-compose down -v` to reset all data

## 🔧 Development Mode

For development with live reloading:

```bash
# Backend development
cd backend
docker run -it --rm -p 8001:8001 -v $(pwd):/app -w /app python:3.11-slim bash
pip install -r requirements.txt
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Frontend development
cd frontend
docker run -it --rm -p 3000:3000 -v $(pwd):/app -w /app node:18-alpine sh
npm install
npm start
```

## 📊 Monitoring

### Health Checks
- **Backend**: http://localhost:8001/api/health
- **Frontend**: http://localhost:3000/health
- **MongoDB**: `docker-compose exec mongodb mongosh --eval "db.runCommand('ping')"`

### Resource Usage
```bash
# View resource usage
docker stats

# View container details
docker-compose ps
```

## 🚀 Production Deployment

For production deployment, update the docker-compose.yml:

```yaml
# Add to docker-compose.yml
services:
  frontend:
    environment:
      - REACT_APP_BACKEND_URL=https://your-backend-domain.com
```

## 📝 Notes

- All services are connected via Docker network
- MongoDB data persists between restarts
- Frontend is built as production React app
- Backend includes health checks
- All services have restart policies

## 🆘 Support

If you encounter issues:
1. Check Docker Desktop is running
2. Verify .env file has correct API key
3. Check service logs: `./docker-logs.sh`
4. Reset everything: `docker-compose down -v && ./docker-start.sh`
