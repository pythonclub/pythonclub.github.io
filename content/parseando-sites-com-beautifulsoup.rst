Exemplo de como "Parsear" Sites com BeautifulSoup
#################################################

:date: 2014-05-13 22:00
:tags: beautifulsoup
:category: Python
:slug: parseando-sites-com-beautifulsoup
:author: Gilmar Soares
:email:  linux.soares@gmail.com
:github: github.com/linuxsoares


=================================
Parseando Sites com BeautifulSoup
=================================


Como "pegar" informações de Sites com BeautifulSoup?
----------------------------------------------------

Vamos falar nesse artigo do Beautifulsoup, biblioteca Python necessária para fazer “parse” de sites. 

Para iniciarmos o exemplo será necessário instalar a biblioteca Python Beautifulsoup no seu ambiente, e assumo que o leitor tenha PIP instalado, então segue comando para instalação:

.. code-block:: bash

	$ pip install beautifulsoup4

A partir desse momento vamos começar a trabalhar com o Beautifulsoup.

Imaginamos que você tenha que fazer parse de um simples site, e que este tenha apenas esse arquivo html:

.. code-block:: bash

	$ 	arquivo_html = ”””<html>
	$ 	  <head>
	$ 	   <title>
	$ 		Exemplo de Beautifulsoup
	$ 	   </title>
	$ 	  </head>
	$ 	  <body>
	$ 	   <p class="title">
	$ 		<b>
	$ 	 	Exemplo de Beautifulsoup
	$ 		</b>
	$ 	   </p>
	$ 	   <p class="story">
	$ 		Vamos fazer "parses" desse simples exemplo de html com Beautifulsoup.
	$ 		<a class="sister" href="http://examplo.com/link1" id="link1">
	$ 	 	Link1
	$ 		</a>
	$ 		,
	$ 		<a class="sister" href="http://examplo.com/link2" id="link2">
	$ 	 	Link2
	$ 		</a>
	$ 		and
	$ 		<a class="sister" href="http://examplo.com/link2_teste" id="link2">
	$ 	 	Link3 Test
	$ 		</a>
	$ 		; Vamos lá!!!!!!!!!!!!!!!!!!!!!
	$ 	   </p>
	$ 	   <p class="story">
	$ 		...
	$ 	   </p>
	$ 	  </body>
	$ 	 </html>”””

Vamos fazer nossa biblioteca ler nossa variavel html, dessa forma:

.. code-block:: bash
	
	$ soup = BeautifulSoup(arquivo_html )

Pronto! Assim como tudo em Python… é simples :)

Agora podemos trabalhar com todo o conteúdo HTML a partir dos métodos da biblioteca.

Para o título:

.. code-block:: bash

	$ soup.title: este comando irá trazer o seguinte: => <title>Exemplo de Beautifulsoup</title>

Para as informações desse título:

.. code-block:: bash

	$ soup.title.string: este comando irá trazer o seguinte => Exemplo de Beautifulsoup

Para os “P” de HTML:
.. code-block:: bash

	$ soup.p: este comando irá trazer o seguinte => <p class="title"><b>Exemplo de Beautifulsoup</b></p>

Para pegar o nome da classe usada no “P”:
.. code-block:: bash

	$ soup.p['class']: este comando irá trazer o seguinte => u'title'

Vamos agora demonstrar como fazer uma busca no documento HTML, digamos que tenhamos a necessidade de pegar todos os <a></a> do nosso arquivo HTML, então usaremos o Beautifulsoup da seguinte maneira:

.. code-block:: bash

	$ soup.find_all('a'): este comando irá trazer o seguinte => 
	$ [
	$ <a class="sister"href="http://examplo.com/link1" id="link1">Link1</a>
	$ <a class="sister" href="http://examplo.com/link2" id="link2">Link2</a>
	$ <a class="sister" href="http://examplo.com/link2_teste" id="link2">Link3 Test</a>
	$ ]

Vamos deixar essa busca mais elaborada, vamos buscar um ID especifico do nosso arquivo HTML dessa forma:

.. code-block:: bash

	$ soup.find(id="link1"): este comando irá trazer o seguinte => 
	$ <a class="sister"href="http://examplo.com/link1" id="link1">Link1</a>

Bom, esta é uma pequena explicação de como funciona o Beautifulsoup. Caso tenham interesse em algo mais especifico, eu utilizei em produção para fazer captura de uns dados, o Script esta no GITHUB no seguinte endereço:
https://github.com/linuxsoares/scripts/blob/master/getVerbos.py
nesse Script implementei bastante coisa do Beautifulsoup e algumas outras coisas também.

Qualquer dúvida pode entrar em contato:
	* Email: linux.soares@gmail.com
	* Twitter: `@gilmar_soares <https://twitter.com/gilmar_soares>`_
	* Facebook: `facebook.com/linux.soares <https://www.facebook.com/linux.soares>`_
	




