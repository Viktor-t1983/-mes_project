#!/bin/bash
echo "🚀 Starting MES Development..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi
docker-compose -f docker-compose.dev.yml up --build
