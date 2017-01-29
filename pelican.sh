#!/bin/sh

#rm -rf tmp/*
#env/bin/python run.py --logs-source "~/Dropbox/documents/logs/trillian/logs/" --dest "tmp"

#mkdir -p static
rm -rf output/
mkdir -p output/

env/bin/pelican \
  -s pelicanconf.py \
  -o output \
  --verbose \
  --debug \
  --ignore-cache \
  --relative-urls

#cp -R static/* output/generated
