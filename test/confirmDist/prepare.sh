#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

mkdir ./tmp-woff2
mkdir ./tmp-ttf

cp -r ../../sample/* ./tmp-woff2/
cp -r ../../sample/* ./tmp-ttf/
cp ../../dist/*.css ./tmp-woff2/
cp ./ttf/*.css ./tmp-ttf/

cd ./tmp-woff2
find -name "style.css" | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont\/dist/\.\./g"
find -name "*.css" | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont//g"
cd ..

cd ./tmp-ttf
find -name "style.css" | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont\/dist/\.\./g"
