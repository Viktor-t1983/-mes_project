#!/bin/bash
# Database Migration Script
set -euo pipefail

echo "Running Database Migrations"
alembic upgrade head

echo "Migrations completed successfully"
