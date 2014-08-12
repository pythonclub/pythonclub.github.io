#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

BASE = os.path.dirname(__file__)

RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
AUTHOR_FEED_RSS = 'feeds/authors/%s.rss.xml'
AUTHOR_FEED_ATOM = 'feeds/authors/%s.atom.xml'


DELETE_OUTPUT_DIRECTORY = True

TEMPLATE_PAGES = {
    os.path.join(BASE, 'theme/templates/search.html'): os.path.join(BASE, 'output/pages/search.html')
}
