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
    print('%s (loaded from %s)' % (
      self.name(), self.url))

    for chapter in self.chapters:
      chapter.display()

  def filename(self, datadir):
    return os.path.join(datadir, 'data.json')

class Chapter(object):
  def __init__(self,  url, number):
    self.title = ''
    self.url = url
    self.body = ''
    #Note: chapter number is for unique identification only and does not
    #   necessarily match the actual chapter number
    self.number = number

  def name(self):
    return str(self.title)

  def display(self):
    print('%s' % self.name())
    print('  %s...' % str(self.body)[0:100])

  def filename(self, datadir):
    return os.path.join(datadir, 'chap_%02d.txt' % self.number)

