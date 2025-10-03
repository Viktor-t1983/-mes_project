#!/bin/bash
echo "🚀 Deploying MES to Production..."
docker build -t mes-app:latest .
docker run -d --name mes-production -p 8000:8000 --env-file .env.production mes-app:latest
echo "✅ MES Production deployed"
