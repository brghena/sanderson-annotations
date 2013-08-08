#!/usr/bin/python

from bs4 import BeautifulSoup
import re
import sys
import urllib2
import urlparse

def fetch(url):
  raw = urllib2.urlopen(url).read()
  return BeautifulSoup(raw)

class Annotation(object):
  def __init__(self, title, root_url):
    self.url = root_url
    self.chapters = []

  def load(self):
    content = fetch(self.url)
    # parse out chapters
    post = content.find('div', class_='post')
    for link in post.find_all('a', href=re.compile('/annotation/.+')):
      title = link.get_text()
      address = link.get('href')
      address = urlparse.urljoin(self.url, address)
      #print "%s: %s" % (address, title)
      self.chapters.append(Chapter(title, address))

    for chapter in self.chapters:
      chapter.load()
      return

class Chapter(object):
  def __init__(self, title, url):
    self.title = title
    self.url = url
    self.body = ''

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
    print "Annotation for %s: %s" % (self.title, self.body)
    
if __name__ == '__main__':
  if len(sys.argv) != 3:
    print "Usage: get_book.py title root_url"
    sys.exit(1)

  title = sys.argv[1]
  root_url = sys.argv[2]
  book = Annotation(title, root_url)
  book.load()

