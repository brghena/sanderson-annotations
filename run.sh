#!/bin/bash

BOOKS="elantris mistborn mistborn2 mistborn3 warbreaker"

declare -A URLS
declare -A TITLES
URLS[elantris]="http://brandonsanderson.com/annotation-elantris-introduction/"
TITLES[elantris]="Elantris"
URLS[mistborn]="http://www.brandonsanderson.com/annotation-mistborn-title-page-one/"
TITLES[mistborn]="Mistborn: The Final Empire"
URLS[mistborn2]="http://brandonsanderson.com/annotation-mistborn-2-title-page/"
TITLES[mistborn2]="Mistborn: The Well of Ascension"
URLS[mistborn3]="http://brandonsanderson.com/annotation-mistborn-3-dedication/"
TITLES[mistborn3]="Mistborn: Hero of Ages"
URLS[warbreaker]="http://brandonsanderson.com/annotation-warbreaker-dedication/"
TITLES[warbreaker]="Warbreaker"

# need to check if requirements are satisfied
#   better to fail now than later
./check_requirements.py || { echo 'Requirements not satisfied'; exit 1; }

for book in $BOOKS; do
  url=${URLS[$book]}
  title=${TITLES[$book]}
  datadir="epub/${book}-data"
  epubdir="epub/${book}-annotations"

  echo "Creating annotations book for $book from $url"

  # Get data
  if [ ! -d $datadir ]; then
    mkdir -p $datadir
  fi
  ./get_book.py "$title" "Brandon Sanderson" "$url" "$datadir" || { echo 'Failed to get book data'; exit 1; }
  echo ""

  # Create book
  rm -rf $epubdir
  rm -rf epub/${book}*.epub
  mkdir -p $datadir
  echo "Creating ePub"
  ./gen_epub.py "$datadir" "$epubdir" || { echo 'Failed to generate book'; exit 1; }
  echo "Created"
done

