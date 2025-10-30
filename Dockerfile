# ResumeCraft - Production Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements_streamlit.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_streamlit.txt

# Copy application code
COPY backend/ .

# Create necessary directories
RUN mkdir -p /app/data /app/uploads /app/outputs

# Expose ports for both apps
EXPOSE 8501 8502

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Create startup script to run both apps
RUN echo '#!/bin/bash\n\
echo "Starting ResumeCraft applications..."\n\
echo "Main App will be available at: http://localhost:8501"\n\
echo "Entity Resolution will be available at: http://localhost:8502"\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true &\n\
sleep 3\n\
streamlit run app_entity_resolution.py --server.port=8502 --server.address=0.0.0.0 --server.headless=true\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start both applications
CMD ["/app/start.sh"]
