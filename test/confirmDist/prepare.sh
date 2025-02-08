#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

mkdir ./tmp

cp ../../sample/* ./tmp/
cp ../../dist/*.css ./tmp/

cd ./tmp
find style.css | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont/\.\./g"
find *.css | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont//g"
