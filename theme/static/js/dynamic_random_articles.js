function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

function show_random_articles(element, articles, articles_number){
    articles = shuffleArray(articles);

    var paragraph = $('<p class="article-link tagline"></p>');

    for (index in articles){
        var article = articles[index];
        var article_html = '<a href="' + article.url + '">' + article.title + '</a>';
        var article_paragraph = paragraph.clone().append(article_html)
        element.append(article_paragraph);

        if (index >= articles_number -1)
            break;
    }

}
