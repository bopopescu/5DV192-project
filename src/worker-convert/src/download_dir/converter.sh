#!/bin/bash
mkdir $2
ffmpeg -i $1 -vf scale=426:240 -c:v libx264 -crf 35 $2/$3



