#!/usr/bin/python

import data
from bs4 import BeautifulSoup
import json
import re
import sys
import urllib2
import urlparse

def fetch(url):
  raw = urllib2.urlopen(url).read()
  return BeautifulSoup(raw)

class Annotation(data.Annotation):
  def __init__(self, title, author, root_url):
    super(Annotation, self).__init__(title, author, root_url)

  def load(self):
    content = fetch(self.url)
    # parse out chapters
    post = content.find('div', class_='post')
    chap_num = 1
    for link in post.find_all('a', href=re.compile('/annotation/.+')):
      title = link.get_text()
      address = link.get('href')
      address = urlparse.urljoin(self.url, address)
      #print "%s: %s" % (address, title)
      self.chapters.append(Chapter(title, address, chap_num))
      chap_num += 1

    for chapter in self.chapters:
      chapter.load()

  def save(self, dirname):
    # generate data
    data = {
      'title': self.title,
      'author': self.author,
      'url': self.url,
      'chapters': [],
    }

    for chapter in self.chapters:
      chap_data = chapter.save(dirname)
      data['chapters'].append(chap_data)

    # write data
    f = open(self.filename(dirname), 'w')
    json.dump(data, f)
    f.close()

    return data

class Chapter(data.Chapter):
  def __init__(self, title, url, number):
    super(Chapter, self).__init__(title, url, number)

  def load(self):
    print "Fetching %s" % self.url
    content = fetch(self.url)
    # parse out chapters
    post = content.find('div', class_='post')

    #print "Annotation for %s: %s" % (self.title, post)
    # load h1 class='article_title'
    self.title = post.find('h1', class_='article_title').get_text()
    # load div class='article_content'
    self.body = post.find('div', class_='article_content')
    # strip out <a> and <script>
    for tag in self.body.find_all(['a', 'script']):
      tag.extract()
    #print "Annotation for %s: %s" % (self.title, self.body)

  def save(self, dirname):
    f = open(self.filename(dirname), 'w')
    text = unicode(self.body)
    # fix weird characters
    text.replace('\ufffd', '\'')
    f.write(text.encode('UTF-8'))
    f.close()

    return {
      'title': self.title,
      'url': self.url,
      'number': self.number,
    }

if __name__ == '__main__':
  if len(sys.argv) != 5:
    print "Usage: get_book.py title author root_url savedir"
    sys.exit(1)

  title = sys.argv[1]
  author = sys.argv[2]
  root_url = sys.argv[3]
  savedir = sys.argv[4]
  annotation = Annotation(title, author, root_url)
  annotation.load()
  annotation.save(savedir)

