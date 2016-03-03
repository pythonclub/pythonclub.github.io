#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os


BASE = os.path.dirname(__file__)

AUTHOR = u'PythonClub'
AUTHOR_EMAIL = u'gravatar@pythonclub.com.br'
SITENAME = u'PythonClub'
SITEURL = 'http://pythonclub.com.br'
SITELOGO = 'http://res.cloudinary.com/diu8g9l0s/image/upload/v1400201393/pythonclub/logo_275x130.png'

GITHUB_URL = 'https://github.com/pythonclub/pythonclub.github.io'
DISQUS_SITENAME = 'pythonclub'

GOOGLE_ANALYTICS = 'UA-50935105-1'
FACEBOOK_APPID = '1487080281503641'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

DEFAULT_PAGINATION = 10

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
MENUITEMS = (
    ('Arquivo', 'archives.html'),
    ('Quem Somos', 'pages/about.html'),
    # ('Autores', 'authors.html'),
    # ('Categorias', 'categories.html'),
    # ('Tags', 'tags.html'),
)

TEMPLATE_PAGES = {
    os.path.join(BASE, 'theme/templates/search.html'): os.path.join(BASE, 'output/pages/search.html')
}

# Social widget
SOCIAL = (
    ('github', 'https://github.com/pythonclub/pythonclub.github.io'),
    ('rss', 'feeds/all.atom.xml'),
)

STATIC_PATHS = ['images', 'extras/CNAME', 'extras/robots.txt']
EXTRA_PATH_METADATA = {
    'extras/CNAME': {'path': 'CNAME'},
    'extras/robots.txt': {'path': 'robots.txt'}
}

# Plugins
PLUGIN_PATHS = [
    'pelican-plugins',
    'custom-plugins'
]

PLUGINS = [
    'gravatar',
    'pelican_alias', # para criar alias para artigos
    'sitemap',
    'pelican_youtube',  # funciona somente com arquivos rst
    'pelican_vimeo',  # funciona somente com arquivos rst
    'json_articles',
    'gzip_cache'  # deve ser o ultimo plugin
    # 'pdf', # funciona somente com arquivos rst

]

RANDOM_ARTICLES = 10


SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.3
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Theme
THEME = 'theme'

# Theme Pure config
PROFILE_IMAGE_URL = "http://res.cloudinary.com/diu8g9l0s/image/upload/v1399566411/fundo_python_a6iqip.png"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Geracao de PDF
# PDF_GENERATOR = True
