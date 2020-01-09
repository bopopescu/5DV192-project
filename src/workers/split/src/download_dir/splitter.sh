#!/bin/bash
mkdir $2

ffmpeg -i $1 -vcodec copy -map 0  -reset_timestamps 1 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*1)" -f segment -segment_time 10 $2/$2_%03d.mp4

cd $2
for file in $PWD/*; do
  echo file "'./"$(basename $file)"'" >> $3.txt
done
echo $2
