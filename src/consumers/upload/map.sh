#!/bin/bash
n=0
while ! mkdir temp$n
do
    n=$((n+1))
done
ffmpeg -i 1080P.mp4 -vcodec copy -map 0  -reset_timestamps 1 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*1)" -f segment -segment_time $1 ./temp$n/output%03d.mp4

cd temp$n
for file in $PWD/*; do
  echo file "'./"$(basename $file)"'" >> output.txt
done
