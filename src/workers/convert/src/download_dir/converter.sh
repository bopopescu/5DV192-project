#!/bin/bash
mkdir $2
ffmpeg -i $1 -vf scale=1920:1080 -c:v libx264 -crf 35 $2/$3.mp4



