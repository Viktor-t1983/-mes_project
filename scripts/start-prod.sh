#!/bin/bash
echo "Starting MES Production"
if [ -z "\" ]; then
    echo "DATABASE_URL not set"
    exit 1
fi
python main.py
