Title: Material do Tutorial: Web Scraping na Nuvem
Date: 2015-11-13 10:04
Author: elias
Slug: material-do-tutorial-web-scraping-na-nuvem


## Roteiro

* Introdução a web scraping com [Scrapy](http://scrapy.org/)
* Conceitos do Scrapy
* Hands-on: crawler para versões diferentes dum site de citações
* Rodando no [Scrapy Cloud](http://scrapinghub.com/platform/)

O tutorial é 90% Scrapy e 10% Scrapy Cloud.

> **Nota:** Scrapy Cloud é o serviço PaaS da Scrapinghub, a empresa em que
> trabalho e que é responsável pelo desenvolvimento do Scrapy.

### Precisa de ajuda?

Pergunte no [Stackoverflow em Português usando a tag
scrapy](http://pt.stackoverflow.com/tags/scrapy) ou pergunte em inglês no
[Stackoverflow em inglês](http://stackoverflow.com/tags/scrapy) ou na [lista de
e-mail scrapy-users](https://groups.google.com/forum/#!forum/scrapy-users).


## Introdução a web scraping com Scrapy

### O que é Scrapy?

[Scrapy](http://scrapy.org/) é um framework para crawlear web sites e extrair dados estruturados que
podem ser usados para uma gama de aplicações úteis (data mining, arquivamento,
etc).

*Scraping:*
: extrair dados do conteúdo da página

*Crawling:*
: seguir links de uma página a outra

Se você já fez extração de dados de páginas Web antes em Python, são grandes as
chances de você ter usado algo como requests + beautifulsoup. Essas tecnologias
ajudam a fazer *scraping*.

A grande vantagem de usar Scrapy é que tem suporte de primeira classe a
*crawling*.

Por exemplo, ele permite configurar o tradeoff de **politeness vs speed** (sem
precisar escrever código pra isso) e já vem com uma configuração útil de
fábrica para crawling habilitada: suporte a cookies, redirecionamento tanto via
HTTP header quanto via tag HTML `meta`, tenta de novo requisições que falham,
evita requisições duplicadas, etc.

Além disso, o framework é altamente extensível, permite seguir combinando
componentes e crescer um projeto de maneira gerenciável.

### Instalando o Scrapy

Recomendamos usar virtualenv, e instalar o Scrapy com:

    pip install scrapy

A dependência chatinha é normalmente o [lxml](http://lxml.de/) (que precisa de
algumas bibliotecas C instaladas). Caso tenha dificuldade, [consulte as
instruções específicas por
plataforma](http://doc.scrapy.org/en/latest/intro/install.html#intro-install-platform-notes)
ou peça ajuda nos canais citados acima.

Para verificar se o Scrapy está instalado corretamente, rode o comando:

    scrapy version

A saída que obtenho rodando este comando no meu computador é:

    $ scrapy version
    2015-11-14 19:58:56 [scrapy] INFO: Scrapy 1.0.3 started (bot: scrapybot)
    2015-11-14 19:58:56 [scrapy] INFO: Optional features available: ssl, http11
    2015-11-14 19:58:56 [scrapy] INFO: Overridden settings: {}
    Scrapy 1.0.3


### Rodando um spider

Para ter uma noção inicial de como usar o Scrapy, vamos começar rodando um
spider de exemplo.

Crie um arquivo **youtube_spider.py** com o seguinte conteúdo:


    import scrapy


    def first(sel, xpath):
        return sel.xpath(xpath).extract_first()


    class YoutubeChannelLister(scrapy.Spider):
        name = 'channel-lister'
        youtube_channel = 'portadosfundos'
        start_urls = ['https://www.youtube.com/user/%s/videos' % youtube_channel]

        def parse(self, response):
            for sel in response.css("ul#channels-browse-content-grid > li"):
                yield {
                    'link': response.urljoin(first(sel, './/h3/a/@href')),
                    'title': first(sel, './/h3/a/text()'),
                    'views': first(sel, ".//ul/li[1]/text()"),
                }


Agora, rode o spider com o comando:

    scrapy runspider youtube_spider.py -o portadosfundos.csv

O scrapy vai procurar um spider no arquivo **youtube_spider.py** e
escrever os dados no arquivo CSV **portadosfundos.csv**.

Caso tudo deu certo, você verá o log da página sendo baixada, os dados sendo
extraídos, e umas estatísticas resumindo o processo no final, algo como:

    ...
    2015-11-14 20:14:21 [scrapy] DEBUG: Crawled (200) <GET https://www.youtube.com/user/portadosfundos/videos> (referer: None)
    2015-11-14 20:14:22 [scrapy] DEBUG: Scraped from <200 https://www.youtube.com/user/portadosfundos/videos>
    {'views': u'323,218 views', 'link': u'https://www.youtube.com/watch?v=qSqPkRi-UiE', 'title': u'GAR\xc7ONS'}
    2015-11-14 20:14:22 [scrapy] DEBUG: Scraped from <200 https://www.youtube.com/user/portadosfundos/videos>
    {'views': u'1,295,054 views', 'link': u'https://www.youtube.com/watch?v=yXc8KCxyEyQ', 'title': u'SUCESSO'}
    2015-11-14 20:14:22 [scrapy] DEBUG: Scraped from <200 https://www.youtube.com/user/portadosfundos/videos>
    {'views': u'1,324,448 views', 'link': u'https://www.youtube.com/watch?v=k9CbDcOT1e8', 'title': u'BIBLIOTECA'}
    ...
    {'downloader/request_bytes': 239,
     'downloader/request_count': 1,
     'downloader/request_method_count/GET': 1,
     'downloader/response_bytes': 27176,
     'downloader/response_count': 1,
     'downloader/response_status_count/200': 1,
     'item_scraped_count': 30,
    ...
    2015-11-14 20:14:22 [scrapy] INFO: Spider closed (finished)

Ao final, verifique os resultados abrindo o arquivo CSV no seu editor de
planilhas favorito.

Se você quiser os dados em JSON, basta mudar a extensão do arquivo de saída:

    scrapy runspider youtube_spider.py -o portadosfundos.json

Outro formato interessante que o Scrapy suporta é [JSON lines](http://jsonlines.org):

    scrapy runspider youtube_spider.py -o portadosfundos.jl

Esse formato usa um item JSON em cada linha -- isso é muito útil para arquivos
grandes, porque fica fácil de concatenar dois arquivos ou acrescentar novas
entradas a um arquivo já existente.


## Conceitos do Scrapy

## Spiders

Conceito central no Scrapy,
[spiders](http://doc.scrapy.org/en/latest/topics/spiders.html) são classes que
herdam de
[``scrapy.Spider``](http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy-spider),
definindo de alguma maneira as requisições iniciais do crawl e como proceder
para tratar os resultados dessas requisições.

Um exemplo simples de spider é:

    import scrapy

    class SpiderSimples(scrapy.Spider):
        name = 'meuspider'

        def start_requests(self):
            return [scrapy.Request('http://example.com')]

        def parse(self, response):
            self.log('Visitei o site: %s' % response.url)

Se você rodar o spider acima com o comando ``scrapy runspider``, deverá ver no
log as mensagens:

    2015-11-14 21:11:13 [scrapy] DEBUG: Crawled (200) <GET http://example.com> (referer: None)
    2015-11-14 21:11:13 [meuspider] DEBUG: Visitei o site: http://example.com

Como iniciar um crawl a partir de uma lista de URLs é uma tarefa comum,
o Scrapy permite você usar o atribute de classe `start_urls` em vez de
definir o método ``start_requests()`` a cada vez:

    import scrapy

    class SpiderSimples(scrapy.Spider):
        name = 'meuspider'
        start_urls = ['http://example.com']

        def parse(self, response):
            self.log('Visitei o site: %s' % response.url)

## Callbacks e próximas requisições

Repare o método ``parse()``, ele recebe um objeto *response* que representa uma
resposta HTTP, é o que chamamos de um **callback**. Os métodos **callbacks** no
Scrapy são
[generators](https://pythonhelp.wordpress.com/2012/09/03/generator-expressions/)
(ou retornam uma lista ou iterável) de objetos que podem ser:

* dados extraídos (dicionários Python ou objetos que herdam de scrapy.Item)
* requisições a serem feitas a seguir (objetos scrapy.Request)

O motor do Scrapy itera sobre os objetos resultantes dos callbacks e os
encaminha para o pipeline de dados ou para a fila de próximas requisições a
serem feitas.

Exemplo:

    import scrapy

    class SpiderSimples(scrapy.Spider):
        name = 'meuspider'
        start_urls = ['http://example.com']

        def parse(self, response):
            self.log('Visitei o site: %s' % response.url)
            yield {'url': response.url, 'tamanho': len(response.body)}

            proxima_url = 'http://www.google.com.br'
            self.log('Agora vou para: %s' % proxima_url)
            yield scrapy.Request(proxima_url, self.handle_google)

        def handle_google(self, response):
            self.log('Visitei o google via URL: %s' % response.url)


Antes de rodar o código acima, experimente ler o código e prever
o que ele vai fazer. Depois, rode e verifique se ele fez mesmo
o que você esperava.

Você deverá ver no log algo como:

    2015-11-14 21:32:53 [scrapy] DEBUG: Crawled (200) <GET http://example.com> (referer: None)
    2015-11-14 21:32:53 [meuspider] DEBUG: Visitei o site: http://example.com
    2015-11-14 21:32:53 [scrapy] DEBUG: Scraped from <200 http://example.com>
    {'url': 'http://example.com', 'tamanho': 1270}
    2015-11-14 21:32:53 [meuspider] DEBUG: Agora vou para: http://www.google.com.br
    2015-11-14 21:32:53 [scrapy] DEBUG: Crawled (200) <GET http://www.google.com.br> (referer: http://example.com)
    2015-11-14 21:32:54 [meuspider] DEBUG: Visitei o google via URL: http://www.google.com.br
    2015-11-14 21:32:54 [scrapy] INFO: Closing spider (finished)


### Settings

Outro conceito importante do Scrapy são as **settings** (isto é, configurações).
As **settings** oferecem uma maneira de configurar componentes do Scrapy, podendo
ser setadas de várias maneiras, tanto via linha de comando, variáveis de ambiente
em um arquivo **settings.py** no caso de você estar usando um projeto Scrapy ou ainda
diretamente no spider definindo um atributo de classe `custom_settings`.

Exemplo setando no código do spider um delay de 1.5 segundos entre cada
requisição:

    class MeuSpider(scrapy.Spider):
        name = 'meuspider'

        custom_settings = {
            'DOWNLOAD_DELAY': 1.5,
        }

Para setar uma setting diretamente na linha de comando com `scrapy runspider`,
use opção `-s`:

    scrapy runspider meuspider.py -s DOWNLOAD_DELAY=1.5

Uma setting útil durante o desenvolvimento é a *HTTPCACHE_ENABLED*, que
habilita uma cache das requisições HTTP -- útil para evitar baixar as
mesmas páginas várias vezes enquanto você refina o código de extração.

> **Dica:** na versão atual do Scrapy, a cache por padrão só funciona caso você
> esteja dentro de um projeto, que é onde ele coloca um diretório
> `.scrapy/httpcache` para os arquivos de cache. Caso você queira usar a cache
> rodando o spider com `scrapy runspider`, você pode usar um truque "enganar" o
> Scrapy criando um arquivo vazio com o nome `scrapy.cfg` no diretório atual, e
> o Scrapy criará a estrutura de diretórios `.scrapy/httpcache` no diretório
> atual.

Bem, por ora você já deve estar familiarizado com os conceitos importantes do
Scrapy, está na hora de partir para exemplos mais realistas.


## Hands-on: crawler para versões diferentes dum site de citações

Vamos agora criar um crawler para um site de frases e citações, feito
para esse tutorial e disponível em: <http://spidyquotes.herokuapp.com>

> *Nota:* O código-fonte do site está disponível em:
> <https://github.com/eliasdorneles/spidyquotes>

### Descrição dos objetivos:

O site contém uma lista de citações com autor e tags, paginadas com 10 citações
por páginas. Queremos obter todas as citações, juntamente com os respectivos
autores e lista de tags.

Existem 4 variações do site, com o mesmo conteúdo mas usando markup HTML diferente.

* Versão com markup HTML semântico: <http://spidyquotes.herokuapp.com/>
* Versão com leiaute em tabelas: <http://spidyquotes.herokuapp.com/tableful/>
* Versão com os dados dentro do código Javascript: <http://spidyquotes.herokuapp.com/js/>
* Versão com AJAX e scroll infinito: <http://spidyquotes.herokuapp.com/scroll>

Para ver as diferenças entre cada versão do site, acione a opção "Exibir
código-fonte" (<kbd>Ctrl</kbd>-<kbd>U</kbd>) do menu de contexto do seu
browser.

> **Nota:** cuidado com a opção "Inspecionar elemento" do browser para inspecionar
> a estrutura do markup. Diferentemente do resultado da opção "Exibir
> código-fonte" Usando essa ferramenta, o código que você vê representa as
> estruturas que o browser cria para a página, e nem sempre mapeiam diretamente
> ao código HTML que veio na requisição HTTP (que é o que você obtém quando usa
> o Scrapy), especialmente se a página estiver usando Javascript ou AJAX. Outro
> exemplo é o elemento `<tbody>` que é adicionado automaticamente pelos
> browsers em todas as tabelas, mesmo quando não declarado no markup.


### Spider para a versão com HTML semântico

Para explorar a página (e a API de scraping do Scrapy), você pode usar
o comando `scrapy shell URL`:

    scrapy shell http://spidyquotes.herokuapp.com/

Esse comando abre um shell Python (ou [IPython](http://ipython.org), se você o
tiver instalado no mesmo virtualenv) com o objeto `response`, o mesmo que você
obteria num método **callback**. Recomendo usar o IPython porque fica mais fácil
de explorar as APIs sem precisar ter que abrir a documentação a cada vez.

Exemplo de exploração com o shell:

    >>> # olhando o fonte HTML, percebi que cada citação está num <div class="quote">
    >>> # vamos pegar o primeiro dele, e ver como extrair o texto:
    >>> quote = response.css('.quote')[0]
    >>> quote
        <Selector xpath=u"descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' quote ')]" data=u'<div class="quote" itemscope itemtype="h'>
    >>> print quote.extract()
    <div class="quote" itemscope itemtype="http://schema.org/CreativeWork">
            <span itemprop="text">“We accept the love we think we deserve.”</span>
            <small itemprop="author">Stephen Chbosky</small>
            <div class="tags">
                Tags:
                <meta itemprop="keywords" content="inspirational,love"> 
                
                <a href="/tag/inspirational/page/1/">inspirational</a>
                
                <a href="/tag/love/page/1/">love</a>
                
            </div>
        </div>
    >>> print quote.css('span').extract_first()
    <span itemprop="text">“We accept the love we think we deserve.”</span>
    >>> print quote.css('span::text').extract_first()  # texto
    “We accept the love we think we deserve.”
    >>> quote.css('small::text').extract_first()  # autor
        u'Stephen Chbosky'
    >>> 
    >>> # para a lista de tags, usamos .extract() em vez de .extract_first()
    >>> quote.css('.tags a::text').extract()
        [u'inspirational', u'love']
    >>> 


Com o resultado da exploração inicial acima, podemos começar escrevendo um
spider assim, num arquivo `quote_spider.py`:

    import scrapy


    class QuotesSpider(scrapy.Spider):
        name = 'quotes'
        start_urls = [
            'http://spidyquotes.herokuapp.com/'
        ]

        def parse(self, response):
            for quote in response.css('.quote'):
                yield {
                    'texto': quote.css('span::text').extract_first(),
                    'autor': quote.css('small::text').extract_first(),
                    'tags': quote.css('.tags a::text').extract(),
                }

Se você rodar esse spider com:

    scrapy runspider quote_spider.py -o quotes.csv

Você obterá os dados das citações da primeira página no arquivo `quotes.csv`.
Só está faltando agora seguir o link para a próxima página, o que você também
pode descobrir com mais alguma exploração no shell:

    >>> response.css('li.next')
        [<Selector xpath=u"descendant-or-self::li[@class and contains(concat(' ', normalize-space(@class), ' '), ' next ')]" data=u'<li class="next">\n                <a hre'>]
    >>> response.css('li.next a')
        [<Selector xpath=u"descendant-or-self::li[@class and contains(concat(' ', normalize-space(@class), ' '), ' next ')]/descendant-or-self::*/a" data=u'<a href="/page/2/">Next <span aria-hidde'>]
    >>> response.css('li.next a::attr("href")').extract_first()
        u'/page/2/'
    >>> # o link é relativo, temos que joinear com a URL da resposta:
    >>> response.urljoin(response.css('li.next a::attr("href")').extract_first())
        u'http://spidyquotes.herokuapp.com/page/2/'

Juntando isso com o spider, ficamos com:

    import scrapy


    class QuotesSpider(scrapy.Spider):
        name = 'quotes'
        start_urls = [
            'http://spidyquotes.herokuapp.com/'
        ]

        def parse(self, response):
            for quote in response.css('.quote'):
                yield {
                    'texto': quote.css('span::text').extract_first(),
                    'autor': quote.css('small::text').extract_first(),
                    'tags': quote.css('.tags a::text').extract(),
                }
            link_next = response.css('li.next a::attr("href")').extract_first()
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))

Agora, se você rodar esse spider novamente com:

    scrapy runspider quote_spider.py

Perceberá que ainda assim ele vai extrair apenas os items da primeira página, e a segunda página
vai falhar com um código HTTP 429, com a seguinte mensagem no log:

    2015-11-15 00:06:15 [scrapy] DEBUG: Crawled (429) <GET http://spidyquotes.herokuapp.com/page/2/> (referer: http://spidyquotes.herokuapp.com/)
    2015-11-15 00:06:15 [scrapy] DEBUG: Ignoring response <429 http://spidyquotes.herokuapp.com/page/2/>: HTTP status code is not handled or not allowed
    2015-11-15 00:06:15 [scrapy] INFO: Closing spider (finished)

<center>
  ![](http://httpstatusdogs.com/wp-content/uploads/2011/12/429.jpg)
</center>

O status HTTP 429 é usado para indicar que o servidor está recebendo muitas
requisições do mesmo cliente num curto período de tempo.

No caso do nosso site, podemos simular o problema no próprio browser se
apertarmos o botão atualizar várias vezes no mesmo segundo:

<center>
  ![](http://i.imgur.com/V3arr9E.jpg)
</center>

Neste caso, a mensagem no próprio site já nos diz o problema e a solução: o máximo de
requisições permitido é uma a cada segundo, então podemos resolver o problema setando
a configuração `DOWNLOAD_DELAY` para 1.5, deixando uma margem decente para podermos
fazer crawling sabendo que estamos respeitando a política.

Como esta é uma necessidade comum para alguns sites, o Scrapy também permite
você configurar este comportamento diretamente no spider, setando o atributo de
classe `download_delay`:

    import scrapy


    class QuotesSpider(scrapy.Spider):
        name = 'quotes'
        start_urls = [
            'http://spidyquotes.herokuapp.com/'
        ]
        download_delay = 1.5

        def parse(self, response):
            for quote in response.css('.quote'):
                yield {
                    'texto': quote.css('span::text').extract_first(),
                    'autor': quote.css('small::text').extract_first(),
                    'tags': quote.css('.tags a::text').extract(),
                }
            link_next = response.css('li.next a::attr("href")').extract_first()
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))

### Usando extruct para microdata

Se você é um leitor perspicaz, deve ter notado que o markup HTML tem umas
marcações adicionais ao HTML normal, usando atributos `itemprop` e `itemtype`.
Trata-se de um mecanismo chamado
[Microdata](https://en.wikipedia.org/wiki/Microdata_(HTML)), [especificado pela
W3C](http://www.w3.org/TR/microdata/) e feito justamente para facilitar a
tarefa de extração automatizada. Vários sites suportam este tipo de marcação,
alguns exemplos famosos são [Yelp](http://www.yelp.com), [The
Guardian](http://www.theguardian.co.uk), [LeMonde](http://lemonde.fr), etc.

Quando um site tem esse tipo de marcação para o conteúdo que você está
interessado, você pode usar o extrator de microdata da biblioteca
[extruct](https://pypi.python.org/pypi/extruct).

Instale a biblioteca extruct com:

    pip install extruct

Veja como fica o código usando a lib:

    import scrapy
    from extruct.w3cmicrodata import LxmlMicrodataExtractor


    class QuotesSpider(scrapy.Spider):
        name = "quotes-microdata"
        start_urls = ['http://spidyquotes.herokuapp.com/']
        download_delay = 1.5

        def parse(self, response):
            extractor = LxmlMicrodataExtractor()
            items = extractor.extract(response.body_as_unicode(), response.url)['items']

            for it in items:
                yield it['properties']

            link_next = response.css('li.next a::attr("href")').extract_first()
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))

Usando microdata você reduz sobremaneira os problemas de mudanças de leiaute,
pois o desenvolvedor do site ao colocar o markup microdata se compromete a
mantê-lo atualizado.

### Lidando com leiaute de tabelas:

Agora, vamos extrair os mesmos dados mas para um markup faltando bom-gosto:
<http://spidyquotes.herokuapp.com/tableful/>

Para lidar com esse tipo de coisa, a dica é: **aprenda XPath**, vale a pena!

Comece aqui: <http://www.slideshare.net/scrapinghub/xpath-for-web-scraping>

> *O domínio de XPath diferencia os gurus dos gafanhotos. -- Elias Dorneles, 2014*

Como o markup HTML dessa página não uma estrutura boa, em vez de fazer scraping
baseado nas classes CSS ou ids dos elementos, com XPath podemos fazer baseando-se
na estrutura e nos padrões presentes no conteúdo.

Por exemplo, se você abrir o shell para a página
<http://spidyquotes.herokuapp.com/tableful>, usando a expressão a seguir
retorna os os nós `tr` (linhas da tabela) que contém os textos das citações,
usando uma condição para pegar apenas linhas que estão imediatamente antes de
linhas cujo texto comece com `"Tags: "`:

    >>> response.xpath('//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]')
    [<Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>,
     <Selector xpath='//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]' data=u'<tr style="border-bottom: 0px; ">\n      '>]

Para extrair os dados, precisamos de alguma exploração:

    >>> quote = response.xpath('//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]')[0]
    >>> print quote.extract()
    <tr style="border-bottom: 0px; ">
                <td style="padding-top: 2em;">“We accept the love we think we deserve.” Author: Stephen Chbosky</td>
                        </tr>
    >>> quote.xpath('string(.)').extract_first()
        u'\n            \u201cWe accept the love we think we deserve.\u201d Author: Stephen Chbosky\n        '
    >>> quote.xpath('normalize-space(.)').extract_first()
        u'\u201cWe accept the love we think we deserve.\u201d Author: Stephen Chbosky'

Note como não tem marcação separando o autor do conteúdo, apenas uma string
"Author:".  Então podemos usar o método `.re()` da classe seletor, que nos
permite usar uma expressão regular:

    >>> text, author = quote.xpath('normalize-space(.)').re('(.+) Author: (.+)')
    >>> text
        u'\u201cWe accept the love we think we deserve.\u201d'
    >>> author
        u'Stephen Chbosky'

O código final do spider fica:

    import scrapy


    class QuotesSpider(scrapy.Spider):
        name = 'quotes-tableful'
        start_urls = ['http://spidyquotes.herokuapp.com/tableful']
        download_delay = 1.5

        def parse(self, response):
            quotes_xpath = '//tr[./following-sibling::tr[1]/td[starts-with(., "Tags:")]]'

            for quote in response.xpath(quotes_xpath):
                texto, autor = quote.xpath('normalize-space(.)').re('(.+) Author: (.+)')
                tags = quote.xpath('./following-sibling::tr[1]//a/text()').extract()
                yield dict(texto=texto, autor=autor, tags=tags)

            link_next = response.xpath('//a[contains(., "Next")]/@href').extract_first()
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))


Note como o uso de XPath permitiu vincularmos elementos de acordo com o conteúdo
tanto no caso das tags quanto no caso do link para a próxima página.


### Lidando com dados dentro do código

Olhando o código-fonte da versão do site: <http://spidyquotes.herokuapp.com/js/>
vemos que os dados que queremos estão todos num bloco de código Javascript,
dentro de um array estático. E agora?

A dica aqui é usar a lib [js2xml](https://github.com/redapple/js2xml) para
converter o código Javascript em XML e então usar XPath ou CSS em cima do XML
resultante para extrair os dados que a gente quer.

Instale a biblioteca js2xml com:

    pip install js2xml

Exemplo no shell:

    scrapy shell http://spidyquotes.herokuapp.com/js/

    >>> import js2xml
    >>> script = response.xpath('//script[contains(., "var data =")]/text()').extract_first()
    >>> sel = scrapy.Selector(_root=js2xml.parse(script))
    >>> sel.xpath('//var[@name="data"]/array/object')
        [<Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>,
     <Selector xpath='//var[@name="data"]/array/object' data=u'<object><property name="author"><object>'>]
    >>> quote = sel.xpath('//var[@name="data"]/array/object')[0]
    >>> quote.xpath('string(./property[@name="text"])').extract_first()
        u'\u201cWe accept the love we think we deserve.\u201d'
    >>> quote.xpath('string(./property[@name="author"]//property[@name="name"])').extract_first()
        u'Stephen Chbosky'
    >>> quote.xpath('./property[@name="tags"]//string/text()').extract()
        [u'inspirational', u'love']


O código final fica:

    import scrapy
    import js2xml


    class QuotesSpider(scrapy.Spider):
        name = 'quotes-js'
        start_urls = ['http://spidyquotes.herokuapp.com/js/']
        download_delay = 1.5

        def parse(self, response):
            script = response.xpath('//script[contains(., "var data =")]/text()').extract_first()
            sel = scrapy.Selector(_root=js2xml.parse(script))
            for quote in sel.xpath('//var[@name="data"]/array/object'):
                yield {
                    'texto': quote.xpath('string(./property[@name="text"])').extract_first(),
                    'autor': quote.xpath(
                        'string(./property[@name="author"]//property[@name="name"])'
                    ).extract_first(),
                    'tags': quote.xpath('./property[@name="tags"]//string/text()').extract(),
                }

            link_next = response.css('li.next a::attr("href")').extract_first()
            if link_next:
                yield scrapy.Request(response.urljoin(link_next))

Fica um pouco obscuro pela transformação de código Javascript em XML, mas a
extração fica mais confiável do que hacks baseados em expressões regulares.

### Lidando com AJAX

Agora, vamos para a versão AJAX com scroll infinito: <http://spidyquotes.herokuapp.com/scroll/>

Se você observar o código-fonte, verá que os dados não estão lá.  No fonte só
tem um código Javascript que busca os dados via AJAX, você pode ver isso
olhando a aba *Network* das ferramentas do browser (no meu caso Chrome, mas
no Firefox é similar).

Nesse caso, precisamos replicar essas requisições com o Scrapy, e tratar
os resultados de acordo com a resposta.

Explorando no shell, vemos que o conteúdo é JSON:

    scrapy shell http://spidyquotes.herokuapp.com/api/quotes?page=1

    >>> response.headers
    {'Content-Type': 'application/json',
     'Date': 'Sun, 15 Nov 2015 22:18:29 GMT',
     'Server': 'gunicorn/19.3.0',
     'Via': '1.1 vegur'}

Portanto, podemos simplesmente usar o módulo JSON da biblioteca padrão e ser feliz:

    >>> import json
    >>> data = json.loads(response.body)
    >>> data.keys()
    [u'has_next', u'quotes', u'tag', u'page', u'top_ten_tags']
    >>> data['has_next']
    True
    >>> data['quotes'][0]
    {u'author': {u'goodreads_link': u'/author/show/12898.Stephen_Chbosky',
      u'name': u'Stephen Chbosky'},
     u'tags': [u'inspirational', u'love'],
     u'text': u'\u201cWe accept the love we think we deserve.\u201d'}
    >>> data['page']
    1

Código final do spider fica:

    import scrapy
    import json


    class QuotesSpider(scrapy.Spider):
        name = 'quotes-scroll'
        quotes_base_url = 'http://spidyquotes.herokuapp.com/api/quotes?page=%s'
        start_urls = [quotes_base_url % 1]
        download_delay = 1.5

        def parse(self, response):
            data = json.loads(response.body)
            for d in data.get('quotes', []):
                yield {
                    'texto': d['text'],
                    'autor': d['author']['name'],
                    'tags': d['tags'],
                }
            if data['has_next']:
                next_page = data['page'] + 1
                yield scrapy.Request(self.quotes_base_url % next_page)

Ao lidar com requisições desse tipo, uma ferramenta útil que pode ser o
[minreq](https://pypi.python.org/pypi/minreq), instale com: ``pip install
minreq``.

O minreq tenta encontrar a requisição mínima necessária para replicar
uma requisição do browser, e pode opcionalmente mostrar como montar
um objeto `scrapy.Request` equivalente.

Rode o minreq com:

    minreq --action print_scrapy_request

Ele fica esperando você colar uma requisição no formato cURL. Para isto,
encontre a requisição AJAX que você quer replicar na aba Network do browser, e
use o recurso "Copy as cURL":

  ![](http://i.imgur.com/hqz9b58.jpg)

Cole no prompt do minreq, e espere ele fazer a mágica. =)

> **Nota:** O minreq está em estágio pre-alpha, você provavelmente vai
> encontrar bugs -- por favor reporte no GitHub.


## Rodando no Scrapy Cloud

O [Scrapy Cloud](http://scrapinghub.com/platform/) é a plataforma PaaS para
rodar crawlers na nuvem, o que permite evitar uma série de preocupações com
infraestrutura.

Funciona como um "Heroku para crawlers", você faz deploy do seu projeto Scrapy
e configura jobs para rodar spiders periodicamente.  Você pode também
configurar scripts Python para rodar periodicamente, os quais podem gerenciar o
escalonamento dos spiders.

Comece criando uma conta free forever em: <http://try.scrapinghub.com/free>

### Criação do projeto

Até aqui nossos exemplos foram simplesmente rodando spiders com `scrapy runspider`.
Para fazer o deploy, chegou a hora de criar um projeto Scrapy propriamente dito.

Para criar um projeto, basta rodar o comando `scrapy startproject` passando o nome do projeto:

    scrapy startproject quotes_crawler

Feito isso, entre no diretório do projeto com `cd quotes_crawler` e copie os
arquivos com spiders para dentro do diretório `quotes_crawler/spiders`.
Certifique-se de usar um nome único para cada spider.

A partir desse momento, você deve ser capaz de rodar cada spider em separado usando o comando:

    scrapy crawl NOME_DO_SPIDER

> **Nota:** Dependendo do caso, é legal começar com um projeto desde o começo,
> para já fazer tudo de maneira estruturada. Pessoalmente, eu gosto de começar
> com spiders em arquivos soltos, quando estou apenas testando a viabilidade de
> um crawler. Crio um projeto apenas quando vou colaborar no código com outras
> pessoas ou fazer deploy no Cloud, nessa hora já é interessante que fique tudo
> estruturado e fácil de crescer dentro de um projeto.

### Configuração no Scrapy Cloud

Antes do deploy, você precisa criar um projeto no Scrapy Cloud. Na tela
inicial, clique no botão adicionar uma organização:

<center>
  ![](http://i.imgur.com/9fsBv4I.png)
</center>

Dê um nome para a organização e confirme:

<center>
  ![](http://i.imgur.com/GvfEXzu.png)
</center>

Em seguida, adicione um serviço do para hospedar o seu serviço, clicando no
botão "+ Service" que aparece dentro da organização criada:

<center>
  ![](http://i.imgur.com/D0VTJLc.png)
</center>

Preencha os dados do seu projeto e confirme:

<center>
  ![](http://i.imgur.com/05Hvbu3.png)
</center>

Depois disso, clique no nome do serviço na página inicial para acessar o local
onde seu projeto estará disponível:

<center>
  ![](http://i.imgur.com/OIZLxYA.png)
</center>

Note o número identificador do seu projeto: você usará esse identificador na
hora fazer o deploy.

<center>
  ![](http://i.imgur.com/ErsMJbB.png)
</center>


### Instalando e configurando shub

A maneira mais fácil de fazer deploy no Scrapy Cloud é usando a ferramenta
[shub](http://doc.scrapinghub.com/shub.html), cliente da linha de comando
para o Scrapy Cloud e demais serviços da Scrapinghub.

Instale-a com:

    pip install shub --upgrade

Faça login com o shub, usando o comando:

    shub login

Informe sua API key conforme for solicitado ([descubra aqui sua API
key](https://dash.scrapinghub.com/account/apikey)).

> **Dica:** Ao fazer login, o shub criará no arquivo `~/.netrc` uma entrada
> configurada para usar sua API key.  Esse arquivo também é usado pelo `curl`,
> o que é útil para quando você deseje fazer requisições HTTP para as APIs na
> linha de comando.


### Preparando o projeto

Antes de fazer deploy do projeto, precisamos fazer deploy das dependências no
Scrapy Cloud.
Crie um arquivo `requirements-deploy.txt` com o seguinte conteúdo:

    extruct
    js2xml
    slimit
    ply

Rode o comando:

    shub deploy-reqs PROJECT_ID requirements-deploy.txt

Substitua `PROJECT_ID` pelo id do seu projeto (neste caso, 27199).

#### Deploy das dependências

Agora faça deploy do projeto com o comando:

    shub deploy -p PROJECT_ID

Novamente, substituindo `PROJECT_ID` pelo id do seu projeto (neste caso, 27199)

Se tudo deu certo, você verá algo como

    $ shub deploy -p 27199
    Packing version 1447628479
    Deploying to Scrapy Cloud project "27199"
    {"status": "ok", "project": 27199, "version": "1447628479", "spiders": 5}
    Run your spiders at: https://dash.scrapinghub.com/p/27199/

Agora você pode ir para a URL indicada (neste caso, <https://dash.scrapinghub.com/p/27199/>)
e agendar jobs dos spiders usando o botão "Schedule".

> **Nota:** opcionalmente, você pode configurar o identificador do projeto no
> arquivo `scrapy.cfg`, para não precisar ter que lembrar a cada vez.

Para configurar um spider para rodar periodicamente, utilize a aba "Periodic
Jobs", no menu à esquerda.

# The End

Era isso, se você chegou até aqui, parabéns e obrigado pela atenção! :)

Você pode conferir o código do projeto final em: <https://github.com/eliasdorneles/quotes_crawler>

Para obter ajuda, pergunte no [Stackoverflow em Português usando a tag
scrapy](http://pt.stackoverflow.com/tags/scrapy) ou pergunte em inglês no
[Stackoverflow em inglês](http://stackoverflow.com/tags/scrapy) ou na [lista de
e-mail scrapy-users](https://groups.google.com/forum/#!forum/scrapy-users).

Obrigado Valdir pela ajuda com a montagem desse tutorial, tanto no desenvolvimento
do app `spidyquotes` quanto na escrita do material. *You rock, dude!*
