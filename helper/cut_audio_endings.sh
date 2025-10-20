#!/bin/bash

audio_duration() {
    ffprobe -v error -show_entries format=duration \
            -of default=noprint_wrappers=1:nokey=1 "$1"
}

cut_ending() {
    duration=$(audio_duration "$1" | awk '{printf "%.3f", $1 - 1.25}')
    ffmpeg -y -i "$1" -t "$duration" -acodec copy "$2"
}

input_dir="ori_assets"
output_dir="assets"

mkdir -p "$output_dir"

shopt -s nullglob
for file in "$input_dir"/*.mp3; do
    base=$(basename "$file")
    cut_ending "$file" "$output_dir/$base"
done
shopt -u nullglob
