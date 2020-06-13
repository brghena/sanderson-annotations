sanderson-annotations
=====================

Reads Brandon Sanderson's book annotations and formats as an epub book.

http://brandonsanderson.com/about-the-annotation-system-introduction/

Install
-------
    sudo pip install -r requirements.txt


Automatically Download Annotations and Create Ebook
---------------------------------------------------
    ./run.sh


Download Annotation Data from a Specific Book
---------------------------------------------
Requires a link to any page in the annotations

    ./get_book.py 'Elantris Annotations' 'Brandon Sanderson' http://www.brandonsanderson.com/annotation-elantris-introduction/ epub/elantris-data/


Create Ebook from a Specific Book
---------------------------------
Requires annotations to already be downloaded

    ./gen_epub.py epub/elantris-data/ epub/elantris-annotations/

The book is generated at epub/elantris-annotations.epub

