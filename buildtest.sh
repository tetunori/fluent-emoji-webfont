#!/bin/bash

# for i in {1..149} ; do
for i in {1..3} ; do
  echo ${i}
  if [ ${i} -lt 10 ]; then
      FILENUM="0${i}"
  else
      FILENUM="${i}"
  fi
  FILENAME="FluentColorEmoji${FILENUM}.ttf"
  echo ${FILENAME}
  # echo $(find -maxdepth 1 -name '*.svg' | head -n $((20*i)) | tail -n 20)

  nanoemoji --color_format glyf_colr_1 --family 'Fluent Color Emoji' --output_file ${FILENAME} $(find -maxdepth 1 -name '*.svg' | head -n $((20*i)) | tail -n 20)
  pushd build
  maximum_color --bitmaps --output_file ${FILENAME} ${FILENAME}
  mv build/${FILENAME} ..
  popd
done
