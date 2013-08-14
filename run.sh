#!/bin/bash

BOOKS="elantris mistborn mistborn2 mistborn3"

declare -A URLS
URLS[elantris]="http://www.brandonsanderson.com/annotation/book/Elantris"
URLS[mistborn]="http://www.brandonsanderson.com/annotation/book/Mistborn"
URLS[mistborn2]="http://www.brandonsanderson.com/annotation/book/Mistborn-2"
URLS[mistborn3]="http://www.brandonsanderson.com/annotation/book/Mistborn-3"

for book in $BOOKS; do
  url=${URLS[$book]}
  datadir="/tmp/epub/${book}-data"
  epubdir="/tmp/epub/${book}-annotations"

  echo "Creating annotations book for $book from $url"

  # Get data
  if [ ! -d $datadir ]; then
    mkdir -p $datadir
    ./get_book.py "$book Annotations" "Brandon Sanderson" "$url" "$datadir"
  fi

  # Create book
  rm -rf $epubdir
  rm -rf /tmp/epub/${book}*.epub
  mkdir -p $datadir
  ./gen_epub.py "$datadir" "$epubdir"
done

