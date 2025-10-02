#!/bin/bash
echo "🚀 Quick MES Day 4 Test"
echo "========================"
curl -s http://localhost:8000/ | python -c "import sys, json; print(json.load(sys.stdin)['message'])"
curl -s http://localhost:8000/health | python -c "import sys, json; print('Health:', json.load(sys.stdin)['status'])"
curl -s http://localhost:8000/api/v1/achievements | python -c "import sys, json; data=json.load(sys.stdin); print('Achievements:', len(data), 'items')"
curl -s http://localhost:8000/api/v1/leaderboard | python -c "import sys, json; data=json.load(sys.stdin); print('Leaderboard:', len(data), 'entries')"
echo "✅ Day 4 Test Complete!"
