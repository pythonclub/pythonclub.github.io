#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'PythonClub'
SITENAME = u'PythonClub'
SITEURL = 'http://pythonclub.com.br'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
    ('Pelican', 'http://getpelican.com/'),
    ('Python.org', 'http://python.org/'),
    ('Jinja2', 'http://jinja.pocoo.org/'),
)

# Social widget
SOCIAL = (
    ('Github', 'https://github.com/pythonclub/pythonclub.github.io'),
)

STATIC_PATHS = ['images', 'extras/CNAME']

DEFAULT_PAGINATION = 10

PLUGIN_PATH = 'plugins'
# PLUGINS = ['cjk-auto-spacing', 'gzip_cache', 'neighbors', 'optimize_images', 'sitemap']

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
