#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

mkdir ./tmp

cp -r ../../sample/* ./tmp/
cp ../../dist/*.css ./tmp/

cd ./tmp
find -name "style.css" | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont\/dist/\.\./g"
find -name "*.css" | xargs sed -i "s/https:\/\/tetunori\.github\.io\/fluent-emoji-webfont//g"
