sanderson-annotations
=====================

Reads Brandon Sanderson's book annotations and formats as an epub book.

Install
-------
You need python-epub-builder (http://python-epub-builder.googlecode.com/svn/trunk) and it's dependencies.

Download Annotation Data
------------------------
$ mkdir -p /tmp/epub/elantris-data
$ ./get_book.py 'Elantris Annotations' 'Brandon Sanderson' http://www.brandonsanderson.com/annotation/book/elantris/ /tmp/epub/elantris-data/

Create Ebook
------------
$ mkdir -p /tmp/epub/elantris-annotations
$ ./gen_epub.py /tmp/epub/elantris-data/ /tmp/epub/elantris-annotations/
Book is at /tmp/epub/elantris-annotations.epub

