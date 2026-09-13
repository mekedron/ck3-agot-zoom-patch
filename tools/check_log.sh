#!/usr/bin/env bash
# Проверка после запуска игры: смонтирован ли мод и не ругается ли игра на его файлы.
set -uo pipefail
LOGS="$HOME/.local/share/Steam/steamapps/compatdata/1158310/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Crusader Kings III/logs"
NAME="smooth_zoom_agot_patch"

echo "== монтирование (debug.log, последний запуск)"
grep -o 'Mounted Data: .*' "$LOGS/debug.log" | grep -v '/game/dlc/' | tail -20
grep -q "Mounted Data: .*mod/$NAME" "$LOGS/debug.log" && echo "OK: $NAME смонтирован" || echo "НЕТ: $NAME не найден среди смонтированных"

echo "== error.log: слои объектов, defines, кодировка"
grep -i 'layer\|define\|utf8-bom\|map_object_data' "$LOGS/error.log" | sort | uniq -c | sort -rn | head -20
echo "(пусто = ошибок по этим темам нет)"
