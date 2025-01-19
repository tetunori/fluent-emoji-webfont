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

if [ -f venv/bin/activate ]; then
  source venv/bin/activate # For Mac, Linux
else
  source venv/Scripts/activate # For Windows
fi

pip install nanoemoji
pip install brotli # Add for conversion of woff2
python -m prepare "${FONTTYPE}"

if [ -d venv/Lib/site-packages/nanoemoji ]; then
  git apply --directory venv/Lib/site-packages/nanoemoji nanoemoji.patch # For Windows
else
  git apply --directory venv/lib/*/site-packages/nanoemoji nanoemoji.patch # For Mac, Linux
fi

pushd build
FILES=$(find . -maxdepth 1 -name "*.svg" | sort)
for name in ${FILES}; do
  mv ${name} ${name:10:100}
done

FILES=$(find . -maxdepth 1 -name "*.svg" | sort)

TTFFILENAME=$(echo "FluentEmoji${FONTTYPE}.ttf" | sed 's/ //g')

nanoemoji --color_format glyf_colr_1 --family "Fluent Emoji ${FONTTYPE}" --output_file "${TTFFILENAME}" ${FILES} > /dev/null
popd
