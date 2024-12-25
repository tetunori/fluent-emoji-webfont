#!/bin/bash

CSSFILENAME="fluentColorEmoji.css"
echo -n >| ${CSSFILENAME}

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
  
  # WOFFFILENAME="FluentColorEmoji${FILENUM}.woff"
  # fonttools ttLib ${FILENAME} --flavor woff -o ${WOFFFILENAME}
  WOFF2FILENAME="FluentColorEmoji${FILENUM}.woff2"
  fonttools ttLib ${FILENAME} --flavor woff2 -o ../dist/${WOFF2FILENAME}

  UNICODERANGE=$( \
    echo $(find -maxdepth 1 -name '*.svg' | head -n $((20*i)) | tail -n 20) \
    | sed "s/.\/emoji_u/U+/g" \
    | sed "s/_/, U+/g" \
    | sed "s/.svg/,/g" \
    | sed "s/U+0*/U+/g" \
    | sed -z "s/,\n/;\n/g" \
  )

  echo "
  /* [${FILENUM}] */
  @font-face {
    font-family: 'fluentcojloremoji';
    font-display: swap;
    src: url('./dist/${WOFF2FILENAME}') format('woff2');
    unicode-range: ${UNICODERANGE}
  }" >> ${CSSFILENAME}
done

mv ${CSSFILENAME} ../dist 