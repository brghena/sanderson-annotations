#!/usr/bin/python

from bs4 import BeautifulSoup
import data
import json
import sys
import ez_epub
import codecs
import unidecode

class Annotation(data.Annotation):
  def __init__(self, dirname):
    # read the root file
    f = open(self.filename(dirname))
    data = json.load(f)
    f.close()
    super(Annotation, self).__init__(data['title'], data['author'], data['url'])

    for chap_data in data['chapters']:
      chapter = Chapter(chap_data, dirname)
      self.chapters.append(chapter)

  def generate_epub(self):
    book = ez_epub.Book()
    book.title = self.title
    book.authors = [self.author]
    book.sections = [chapter.generate_epub() for chapter in self.chapters]
    return book

class Chapter(data.Chapter):
  def __init__(self, data, dirname):
    super(Chapter, self).__init__(data['url'], data['number'])
    self.title = unidecode.unidecode(data['title'])

    # read file
    f = codecs.open(self.filename(dirname), encoding='utf-8')
    self.body = f.read()
    f.close()

  def generate_epub(self):
    section = ez_epub.Section()
    section.title = self.title

    # replace unicode characters with ascii equivalent within the text
    text = unidecode.unidecode(BeautifulSoup(self.body).body.get_text())

    # replace two spaces after periods with one space
    #   okay, this one is a personal choice. I guess...
    text = text.replace('.  ', '. ')
    text = text.replace('!  ', '! ')
    text = text.replace('?  ', '? ')

    # remove extraneous end of line characters and record text
    for part in text.split('\n'):
      part = part.strip()
      if len(part) == 0:
        continue
      section.text.append(part)
    return section

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print 'Usage: gen_epub.py datadir epubdir'
    sys.exit(1)

  datadir = sys.argv[1]
  epubdir = sys.argv[2]

  # Strip trailing slash for stupid make()
  if epubdir[-1] == '/':
    epubdir = epubdir[:-1]

  # read data
  annotation = Annotation(datadir)
  book = annotation.generate_epub()
  print 'Starting epub generation...'
  book.make(epubdir)
  print 'Done!'

