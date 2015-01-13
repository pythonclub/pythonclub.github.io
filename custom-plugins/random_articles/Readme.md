Random Articles Plugin For Pelican
========================

This plugin insert a variable called `random_articles` in the page context.
Only published articles are listed.


Settings options:

    RANDOM_ARTICLES = 3 # show only 3 random articles
    SKIP_ARTICLES = 10 # skip 10 first articles before randomize


Usage
-----

To change number of random articles, put on your settings:

    RANDOM_ARTICLES = 3

Then in some template you'll have a variable called `random_articles`.

Ex:
     {% for article in random_articles %}
      <p  class="article-link tagline">
        <a href="{{ SITEURL }}/{{ article.url}}">{{ article.title }}</a>
      </p>
     {% endfor %}
