#! /usr/bin/env python

import sys

print("Checking requirements...")

try:
    from bs4 import BeautifulSoup
except ImportError:
    print('Could not import Beautiful Soup 4')
    print('pip install --user BeautifulSoup4')
    sys.exit(1)

try:
    import genshi
except ImportError:
    print('Could not import Genshi')
    print('pip install --user genshi')
    sys.exit(1)

try:
    import lxml
except ImportError:
    print('Could not import lxml')
    print('pip install --user lxml')
    sys.exit(1)

try:
    import unidecode
except ImportError:
    print('Could not import unidecode')
    print('pip install --user unidecode')
    sys.exit(1)

try:
    import titlecase
except ImportError:
    print('Could not import titlecase')
    print('pip install --user titlecase')
    sys.exit(1)

