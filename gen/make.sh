#!/bin/bash
# 使い方: bash gen/make.sh content/week1.json [id ...]
# 完成品は videos/<id>.mp4 と videos/<id>_cover.jpg に入る
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
JSON=$(realpath "$1"); shift
WORK=${WORK:-/tmp/crownbell_work}
mkdir -p "$WORK" "$ROOT/videos"
python3 -I "$ROOT/gen/build_html.py" "$JSON" "$WORK" > /dev/null
IDS=${@:-$(python3 -I -c "import json,sys;print(' '.join(v['id'] for v in json.load(open(sys.argv[1]))))" "$JSON")}
for id in $IDS; do
  kind=$(python3 -I -c "import json,sys;print([v.get('audio', v['kind']) for v in json.load(open(sys.argv[1])) if v['id']==sys.argv[2]][0])" "$JSON" "$id")
  seed=$(python3 -I -c "import sys;print(sum(map(ord,sys.argv[1]))%997)" "$id")
  dur=$(python3 -I -c "import json,sys;print([v.get('dur',10000) for v in json.load(open(sys.argv[1])) if v['id']==sys.argv[2]][0])" "$JSON" "$id")
  (cd "$ROOT/gen" && node render.js "$WORK" "$id" 60 $dur)
  DUR_S=$(python3 -I -c "print($dur/1000)") python3 -I "$ROOT/gen/audio.py" "$kind" "$seed" "$WORK/$id.wav"
  ffmpeg -v error -y -i "$WORK/${id}_v.mp4" -i "$WORK/$id.wav" -c:v copy -c:a aac -b:a 192k \
    -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -movflags +faststart -shortest "$ROOT/videos/$id.mp4"
  ffmpeg -v error -y -ss 1.6 -i "$ROOT/videos/$id.mp4" -frames:v 1 -q:v 2 "$ROOT/videos/${id}_cover.jpg"
  echo "done $id"
done
