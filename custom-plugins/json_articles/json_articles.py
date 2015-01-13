# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from pelican import signals


def inject_articles(generator, metadata=None):
    articles = generator.context['articles']
    site_url = generator.settings['SITEURL']

    json_articles = []

    for article in articles:
        json_articles.append({
            'title': article.title,
            'url': '{}/{}'.format(site_url, article.url)
        })

    generator.context['json_articles'] = json.dumps(json_articles)


def register():
    signals.page_generator_context.connect(inject_articles)
