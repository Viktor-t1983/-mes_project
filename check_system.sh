#!/bin/bash
echo "🔧 MES System Quick Check"
echo "========================="

# Check API
echo -n "API Health: "
curl -s http://localhost:8000/api/v1/health | grep -q healthy && echo "✅ OK" || echo "❌ FAILED"

# Check documentation
echo -n "Documentation: "
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q 200 && echo "✅ OK" || echo "❌ FAILED"

# Check Git status
echo -n "Git Status: "
if git status --porcelain | grep -q .; then
    echo "❌ Uncommitted changes"
else
    echo "✅ Clean"
fi

# Check synchronization
echo -n "GitHub Sync: "
git fetch origin >/dev/null 2>&1
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main 2>/dev/null)
if [ "$LOCAL" = "$REMOTE" ]; then
    echo "✅ Synchronized"
else
    echo "❌ Out of sync"
fi

echo ""
echo "Quick access:"
echo "  API Docs: http://localhost:8000/docs"
echo "  GitHub:   https://github.com/Viktor-t1983/-mes_project"
