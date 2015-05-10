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
    
    # get the dropdown menu with the urls
    res = content.find("select", "category-posts-dropdown")
    if res == None:
        print("Error: Could not find dropdown menu at url '" + str(self.url) + "'")
        sys.exit(1)

    # get the individual links
    urls = [option.get("value") for option in res.find_all("option")]
    #XXX:TESTING
    urls = urls[0:5]

    # parse out chapters
    chap_num = 1
    for chapter_url in urls:
        if chapter_url == '':
            continue
        self.chapters.append(Chapter(chapter_url, chap_num))
        chap_num += 1

    # actually load the test for each chapter
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
  def __init__(self, url, number):
    super(Chapter, self).__init__(url, number)

  def load(self):
    print('Downloading chapter from ' + str(self.url))
    content = fetch(self.url)

    # get the chapter title
    title_block = content.find("h1", "post-title")
    if title_block != None:
        # split off "Annotation <Title>" from chapter name
        self.title = ' '.join(title_block.string.split()[2:])
    else:
        # don't know why that wouldn't work...
        self.title = self.url.split('/')[-2]

    # find body
    self.body = content.find("article")
    if self.body == None:
        print("Error: Could not find article text at url '" + str(self.url) + "'")
        sys.exit(1)

    # remove all unwanted tags
    #   takes a couple of steps as I keep finding more cruft
    for tag in self.body.find_all(['a', 'script', 'select', 'span', 'h1', 'hr']):
        tag.extract()
    for tag in self.body.find_all("p", "post-meta"):
        tag.extract()
    for tag in self.body.find_all("p", "readtherest"):
        tag.extract()

    # replace article tag with paragraph tag instead
    self.body.name = "p"

    # mark spoilers!
    for tag in self.body.find_all("div", "sh-link"):
        spoiler_paragraph = content.new_tag("p")
        spoiler_tag = content.new_tag("b")
        spoiler_tag.string = "Spoilers Below"
        spoiler_paragraph.append(spoiler_tag)
        tag.replace_with(spoiler_tag)
        # remove div surrounding spoiler contents
        div = self.body.find("div", "sh-content")
        if div == None:
            print("Error: No div string found at url '" + str(self.url) + "'")
            sys.exit(1)
        else:
            div.unwrap()

    # remove remaining irrelevant divs
    for tag in self.body.find_all("div"):
        tag.extract()

    # remove the warnings that this is an annotation and not a book
    warning = self.body.find(text=re.compile("The following is an author"))
    if warning != None:
        warning.parent.parent.extract()
    warning = self.body.find(text=re.compile("You can navigate between"))
    if warning != None:
        warning.parent.extract()

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
    print('Usage: get_book.py title author root_url savedir')
    sys.exit(1)

  title = sys.argv[1]
  author = sys.argv[2]
  root_url = sys.argv[3]
  savedir = sys.argv[4]
  annotation = Annotation(title, author, root_url)
  annotation.load()
  annotation.save(savedir)

