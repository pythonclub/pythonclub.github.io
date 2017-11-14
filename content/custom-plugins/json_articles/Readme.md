Json Articles Plugin For Pelican
========================

This plugin insert a variable called `json_articles` in the page context.

This variable contains all articles in a json format.


In settings we can define the number of random_articles:

    RANDOM_ARTICLES = 3


Usage
-----

Add `dynamic_random_articles.js` in your template, in our case, just do that:
<script src="{{ SITEURL }}/theme/js/dynamic_random_articles.js"></script>

In our sidebar.html  was inserted:

    div class="section articles-random">
        <h1 class="tagline">Não deixe de ver!</h1>
        <div id="random-articles"></div>
    </div>

We use `articles-random` class to hide it in mobile.

And then, we call the javascript function that render articles:

    $(function(){
        show_random_articles($('#random-articles'), {{ json_articles }}, {{ RANDOM_ARTICLES }});
    });

Note that we pass a element to function, this element can be changed any time.
