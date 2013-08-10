# Annotation data module

import os

class Annotation(object):
  def __init__(self, title, author, root_url):
    self.title = title
    self.author = author
    self.url = root_url
    self.chapters = []

  def name(self):
    return 'Annotation for %s by %s' % (
      self.title, self.author)

  def display(self):
    print '%s (loaded from %s)' % (
      self.name(), self.url)

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

  def name(self):
    return 'Chapter %02d: %s' % (self.number, self.title)

  def display(self):
    print '%s' % self.name()
    print '  %s...' % str(self.body)[0:100]

  def filename(self, datadir):
    return os.path.join(datadir, 'chap_%02d.txt' % self.number)

