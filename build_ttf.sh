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

# Remove potential leftovers from older builds.
rm -rf venv build

# Create clean Python environment.
python -m venv --upgrade-deps venv

# source venv/bin/activate
source venv/Scripts/activate # For Windows

pip install nanoemoji
pip install brotli # Add for conversion of woff2
python -m prepare "${FONTTYPE}"

# git apply --directory venv/lib/*/site-packages/nanoemoji nanoemoji.patch
git apply --directory venv/Lib/site-packages/nanoemoji nanoemoji.patch

pushd build
FILES=$(find -maxdepth 1 -name "*.svg" )
for name in ${FILES}; do
  mv ${name} ${name:10:100}
done

TTFFILENAME="FluentEmoji${FONTTYPE}.ttf"

nanoemoji --color_format glyf_colr_1 --family "Fluent Emoji Color" --output_file "${TTFFILENAME}" $(find -maxdepth 1 -name "*.svg")

pushd build
maximum_color --bitmaps --output_file "${TTFFILENAME}" "${TTFFILENAME}"
popd

mv "${TTFFILENAME}" ../dist 

# Move the final font file to the build directory and clean up.
rm -rf build *.svg
popd
rm -rf venv
