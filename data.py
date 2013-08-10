# Annotation data module

import os

class Annotation(object):
  def __init__(self, title, author, root_url):
    self.title = title
    self.author = author
    self.url = root_url
    self.chapters = []

  def display(self):
    print 'Annotation for %s by %s (loaded from %s)' % (
      self.title, self.author, self.url)

    for chapter in self.chapters:
      chapter.display()

  def filename(self, datadir):
    return os.path.join(datadir, 'data.json')

class Chapter(object):
  def __init__(self, title, url, number):
    self.title = title
    self.url = url
    self.body = ''
    self.number = number

  def display(self):
    print 'Chapter %0d: %s' % (self.number, self.title)
    print '  %s...' % str(self.body)[0:100]

  def filename(self, datadir):
    return os.path.join(datadir, 'chap_%02d.txt' % self.number)

