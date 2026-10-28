#!/bin/sh
# Re-run the whole first-pass analysis. Usage: analysis/run_all.sh <folder with the 12 .czi files> [python]
# Raw files are read only. Outputs go to results/.
set -e
RAW="$1"; PY="${2:-python3}"; HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="$HERE/../results"
mkdir -p "$OUT/runs" "$OUT/logs" "$OUT/clips"
find "$RAW" -maxdepth 1 -name '*.czi' -print0 | xargs -0 -P 4 -n 1 sh -c \
  '"$0" -I -W ignore "$1"/flood_wave.py "$2" "$3"/runs --qc "$1"/qc.json > "$3"/logs/"$(basename "$2" .czi)".log 2>&1' "$PY" "$HERE" _ "$OUT"
"$PY" -I -W ignore "$HERE/roi2020.py" "$RAW/Flooding expt 8 NormalWater small plant representative 10012020.czi" \
  "$HERE/../legacy/2020_Flood_Wave_deck/slide55_roi_image.png" "$OUT/roi2020_expt08.json"
"$PY" -I -W ignore "$HERE/deck_figs.py" "$OUT/runs" "$OUT/roi2020_expt08.json" "$OUT/figures" "$HERE/qc.json"
"$PY" -I -W ignore "$HERE/ref_grid.py" "$OUT/runs" "$OUT/figures/mask_qc_sheet.png"
"$PY" -I -W ignore "$HERE/make_clip.py" "$RAW/Flooding expt 8 NormalWater small plant representative 10012020.czi" \
  "$OUT/runs/expt08/expt08_maps.npz" "$HERE/qc.json" "$OUT/clips/expt08_clip.mp4" "$OUT/clips/expt08_clip_still.png" 600
