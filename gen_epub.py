#!/usr/bin/python

import data
import json
import sys

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

class Chapter(data.Chapter):
  def __init__(self, data, dirname):
    super(Chapter, self).__init__(data['title'], data['url'], data['number'])

    # read file
    f = open(self.filename(dirname))
    self.body = f.read()
    f.close()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "Usage: gen_epub.py savedir"
    sys.exit(1)

  savedir = sys.argv[1]
  annotation = Annotation(savedir)
  annotation.display()

