#!/bin/bash

# Check arg
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <FONTTYPE>"
  echo "  FONTTYPE: color, flat or hc"
  exit 1
fi

if [ "$1" = 'color' ]; then
  FONTTYPE='Color'
elif [ "$1" = 'flat' ]; then
  FONTTYPE='Flat'
elif [ "$1" = 'hc' ]; then
  FONTTYPE='High Contrast'
fi

# On error, exit immediately.
set -e

pushd build
TTFFILENAME=$(echo "FluentEmoji${FONTTYPE}.ttf" | sed 's/ //g')

pushd build
maximum_color --bitmaps --output_file "${TTFFILENAME}" "${TTFFILENAME}"
mv build/"${TTFFILENAME}" ../../dist
popd

# Move the final font file to the build directory and clean up.
rm -rf build *.svg
popd
rm -rf venv
