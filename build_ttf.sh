#!/bin/bash

# Check arg
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <FONTTYPE>"
  echo "  FONTTYPE: color, flat, hc, or hc-inv"
  exit 1
fi

if [ "$1" = 'color' ]; then
  echo "FONTTYPE: $1"
elif [ "$1" = 'flat' ]; then
  echo "FONTTYPE: $1"
elif [ "$1" = 'hc' ]; then
  echo "FONTTYPE: $1"
elif [ "$1" = 'hc-inv' ]; then
  echo "FONTTYPE: $1"
else
  echo "FONTTYPE: $1"
  echo "Usage: $0 <FONTTYPE>"
  echo "  FONTTYPE: color, flat, hc, or hc-inv"
  exit 1
fi

if ! ls ./build/build/*.ttf >/dev/null 2>&1; then
  ./build_ttf01.sh "$1"
fi
./build_ttf02.sh "$1"
