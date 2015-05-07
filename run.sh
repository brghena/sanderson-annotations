#!/bin/bash

#BOOKS="elantris mistborn mistborn2 mistborn3"
BOOKS="mistborn"

declare -A URLS
URLS[mistborn]="http://www.brandonsanderson.com/annotation-mistborn-title-page-one/"
#URLS[elantris]="http://www.brandonsanderson.com/annotation/book/Elantris"
#URLS[mistborn]="http://www.brandonsanderson.com/annotation/book/Mistborn"
#URLS[mistborn2]="http://www.brandonsanderson.com/annotation/book/Mistborn-2"
#URLS[mistborn3]="http://www.brandonsanderson.com/annotation/book/Mistborn-3"

# need to check if requirements are satisfied
#   better to fail now than later
./check_requirements.py || { echo 'Requirements not satisfied'; exit 1; }

#XXX: TESTING ONLY
# need to clear out old files to re-run fetch
#rm -rf /tmp/epub/*

for book in $BOOKS; do
  url=${URLS[$book]}
  datadir="tmp/epub/${book}-data"
  epubdir="tmp/epub/${book}-annotations"

  echo "Creating annotations book for $book from $url"

  # Get data
  if [ ! -d $datadir ]; then
    mkdir -p $datadir
  fi
  ./get_book.py "$book Annotations" "Brandon Sanderson" "$url" "$datadir" || { echo 'Failed to get book data'; exit 1; }
  echo ""

  #XXX: TESTING
  exit 1

  # Create book
  rm -rf $epubdir
  rm -rf /tmp/epub/${book}*.epub
  mkdir -p $datadir
  echo "Creating ePub"
  ./gen_epub.py "$datadir" "$epubdir"
  echo "Created"
done

