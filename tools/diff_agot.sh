#!/usr/bin/env bash
# Показывает, чем файлы патча отличаются от копий AGOT в Workshop (после обновления AGOT
# прогнать и перенести изменения). Файлы AGOT в CRLF, отсюда --strip-trailing-cr.
set -uo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGOT="$HOME/.local/share/Steam/steamapps/workshop/content/1158310/2962333032"
GAME="$HOME/.local/share/Steam/steamapps/common/Crusader Kings III/game"

for f in game_object_layers.txt effect_layers.txt skyx_skybox.txt; do
	base="$AGOT/gfx/map/map_object_data/$f"
	[ -f "$base" ] || base="$GAME/gfx/map/map_object_data/$f"
	echo "=== $f  (base: $base)"
	diff --strip-trailing-cr <(sed 's/^\xEF\xBB\xBF//; /^#/d; /^$/d' "$base") <(sed 's/^\xEF\xBB\xBF//; /^#/d; /^$/d' "$SRC/gfx/map/map_object_data/$f") || true
done
echo "=== ZOOM_STEPS и ключи, которые трогает патч, в AGOT 00_graphics.txt"
grep -n 'ZOOM_STEPS = \|LARGE_NAMES_ZOOM_STEP\|NAME_DRAW_DISTANCE\|REALM_COLOR_MAP_START\|FORT_VISIBLE\|MAX_MESHES' "$AGOT/common/defines/graphic/00_graphics.txt" | tr -d '\r'
