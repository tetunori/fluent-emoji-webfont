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
rm -rf venv

# Create clean Python environment.
python -m venv --upgrade-deps venv

if [ -f venv/bin/activate ]; then
  source venv/bin/activate # For Mac, Linux
else
  source venv/Scripts/activate # For Windows
fi

pip install nanoemoji
pip install brotli # Add for conversion of woff2

if [ -d venv/Lib/site-packages/nanoemoji ]; then
  git apply --directory venv/Lib/site-packages/nanoemoji nanoemoji.patch # For Windows
else
  git apply --directory venv/lib/*/site-packages/nanoemoji nanoemoji.patch # For Mac, Linux
fi

pushd build
TTFFILENAME=$(echo "FluentEmoji${FONTTYPE}.ttf" | sed 's/ //g')

pushd build
maximum_color --bitmaps --output_file "${TTFFILENAME}" "${TTFFILENAME}"
mv build/"${TTFFILENAME}" ../../dist
popd

# Move the final font file to the build directory and clean up.
rm -rf build
popd
rm -rf venv
