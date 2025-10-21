FROM python:3.11-slim

WORKDIR /app

# Copy backend code
COPY backend/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start application - Railway will inject $PORT environment variable
CMD uvicorn server:app --host 0.0.0.0 --port $PORT
