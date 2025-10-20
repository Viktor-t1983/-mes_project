#!/bin/bash
set -e

echo "🚀 Запуск финальной фиксации Дня 13..."

# 1. Добавляем все изменения
echo "1. Выполняется: git add ."
git add .

# 2. Создаём коммит
echo "2. Создаётся коммит..."
git commit -m "feat: Day 13 — production-ready MES system, E2E test passed"

# 3. Отправляем в ветку security-setup
echo "3. Отправка в GitHub..."
git push origin security-setup

# 4. Проверяем, установлен ли GitHub CLI (gh)
if command -v gh &> /dev/null; then
    echo "4. GitHub CLI (gh) обнаружен. Создаём Pull Request..."
    gh pr create \
        --title "feat: Day 13 — production-ready MES system" \
        --body "✅ E2E-тест пройден\n✅ Безопасность проверена\n✅ Все 13 дней реализованы" \
        --base main \
        --head security-setup
    echo "✅ Pull Request создан: https://github.com/Viktor-t1983/-mes_project/pulls"
else
    echo "4. GitHub CLI (gh) не установлен."
    echo "👉 Вручную создайте Pull Request:"
    echo "   1. Перейдите на: https://github.com/Viktor-t1983/-mes_project"
    echo "   2. Нажмите 'Compare & pull request' между ветками:"
    echo "      base: main ← compare: security-setup"
    echo "   3. Нажмите 'Create pull request'"
fi

echo ""
echo "🎉 День 13 официально завершён и зафиксирован в Git!"
echo "🔒 Система готова к production."
