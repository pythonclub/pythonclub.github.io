# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import random

from pelican import signals


def is_published(article):
    """ Return if article is published"""
    return getattr(article, 'status', 'published') == 'published'


def get_articles(generator):
    skip_articles = generator.settings.get('SKIP_ARTICLES', 0)
    articles = generator.context['articles']
    return articles[skip_articles:]


def register_articles(generator, metadata):
    articles = filter(is_published, get_articles(generator))
    articles_number = len(articles)

    random_articles_number = generator.settings.get('RANDOM_ARTICLES', 3)

    # we should return only articles number that exists
    sample_number = random_articles_number
    if articles_number < random_articles_number:
        sample_number = articles_number

    random_articles = random.sample(articles, sample_number)
    generator.context['random_articles'] = random_articles


def register():
    signals.page_generator_context.connect(register_articles)
