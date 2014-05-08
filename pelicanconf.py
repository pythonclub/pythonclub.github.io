#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'PythonClub'
AUTHOR_EMAIL = u'gravatar@pythonclub.com.br'
SITENAME = u'PythonClub'
SITEURL = 'http://pythonclub.com.br'

GITHUB_URL = 'https://github.com/pythonclub/pythonclub.github.io'
DISQUS_SITENAME = 'pythonclub'

FACEBOOK_APPID = '1487080281503641'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

DEFAULT_PAGINATION = 10

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
    ('github', 'https://github.com/pythonclub/pythonclub.github.io'),
    ('rss', '/feeds/all.atom.xml'),
)

STATIC_PATHS = ['images', 'extras/CNAME']
EXTRA_PATH_METADATA = {
    'extras/CNAME': {'path': 'CNAME'}
}

# Plugins
PLUGIN_PATH = 'plugins'
PLUGINS = ['gravatar']

# Theme
THEME = 'theme'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
