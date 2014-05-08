Selenium - O que você deveria saber - Parte 1
#############################################

:date: 2014-05-08 12:09
:tags: selenium, python, selenium-serie
:category: Python
:slug: selenium-parte-1
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br

Esse é o primeiro post da série sobre o Selenium, pretendo cobrir desde o básico até algumas coisas mais legais :)

================
Introdução
================
`Selenium <http://docs.seleniumhq.org/>`_ é um ótimo framework para realizar diversos tipos de tarefas com o browser.

Nesta série, vou tentar compartilhar com vocês o que acredito ser necessário para o bom uso da ferramenta.

Veja como está organizada a série:

Parte I
---------
    - `Instalação`_
    - `Abrindo uma página`_
    - `Manipulando elementos`_

Parte 2
---------
    - Brincando com formulários
    - Trabalhando com múltiplas janelas
    - Trabalhando com frames
    - E se eu quiser esperar?!

Parte 3
--------
    - Executando código javascript
    - Como utilizar diferentes navegadores

Parte 4
--------
    - Expected conditions
    - ActionsChains - Operações avançadas com o mouse
    - EventListener - Ouvindo seu código


================
Instalação
================

Para instalar o Selenium não existe nenhum segredo, basta executar:

.. code-block:: bash

  pip install selenium

==================
Abrindo uma página
==================

.. code-block:: python

  from selenium import webdriver

  firefox = webdriver.Firefox()
  firefox.get('http://google.com.br')

Vamos entender o que está acontecendo aqui.

Primeiro eu importo o ``webdriver`` que é o módulo que provê implementações para diferentes browsers.

.. code-block:: python

  from selenium import webdriver

Nesse caso utilizaremos o "Mozila Firefox", pois não precisa de nenhuma configuração adicional, basta que ele esteja instalado.

Então criamos uma instância chamada ``firefox`` e depois invocamos o metódo ``get`` passando como parâmetro a URL da página que desejamos abrir.

.. code-block:: python

  firefox = webdriver.Firefox()
  firefox.get('http://google.com.br/')


Outros exemplos:

.. code-block:: python

  # Abrir o site da Python Brasil
  firefox.get('http://python.org.br/')

  # Abrir o site da Python MG
  firefox.get('http://pythonmg.com.br/')


=====================
Manipulando elementos
=====================

Sempre existe a necessidade de manipularmos algum elemento da página,
para isso você precisa saber como encontrá-lo.

*Conhecimento em HTML é necessário para facilitar a manipulação da página*

Se precisarmos encontrar um elemento pelo id, invocamos o metódo ``find_element_by_id``:

.. code-block:: python

  # Se o elemento não for encontrado uma exception é gerada
  find_element_by_id('<id>')

Se precisarmos encontrar todos os elementos que possuem uma classe específica, invocamos o metódo ``find_elements_by_class_name``.

.. code-block:: python

  # Retornam vários elementos ou uma lista vazia
  find_elements_by_class_name('<class_name>')


Existem diversos metódos disponíveis, abaixo estão os que mais utilizo:

.. code-block:: python

  # Encontrar elemento pelo ID
  find_element_by_id('<id>')

  # Encontrar elemento pelo atributo name
  find_element_by_name('<name>')

  # Encontrar elemento pelo texto do link
  find_element_by_link_text('<text>')

  # Encontrar elemento pelo seu seletor css
  find_element_by_css_selector('<css_selector>')

  # Encontrar elementos pelo nome da tag
  find_elements_by_tag_name('<tag_name>')

  # Encontrar elementos pela classe
  find_elements_by_class_name('<class_name>')


Para visualizar todos os metódos, veja a `documentação <http://selenium-python.readthedocs.org/locating-elements.html#locating-elements>`_.


Exemplo para estudo
-------------------

*Let's code*

..

  **Premissas**

  No `Python Club <http://pythonclub.com.br/>`_ os ``posts`` estão localizados dentro de uma ``div``.

  .. code-block:: html

    <div class="posts">
      <section class="post">[...]</section>
      <section class="post">[...]</section>
      <section class="post">[...]</section>
    </div>

  E cada ``post`` está dentro de uma ``section`` que possue a ``class="post"`` .

  .. code-block:: html

    <section class="post">
      <header class="post-header">
        [...]
        <h3>
          <a class="post-title" href="<post_url>"><post_title></a>
        </h3>
        [...]
      </header>
    </section>

  **Objetivo**

  Queremos que seja mostrado o título de cada ``post`` e seu ``link``.


Execute o código abaixo e veja o resultado.

.. code-block:: python

  from selenium import webdriver

  # Criar instância do navegador
  firefox = webdriver.Firefox()

  # Abrir a página do Python Club
  firefox.get('http://pythonclub.com.br/')

  # Seleciono todos os elementos que possuem a class post
  posts = firefox.find_elements_by_class_name('post')

  # Para cada post printar as informações
  for post in posts:

      # O elemento `a` com a class `post-title`
      # contém todas as informações que queremos mostrar
      post_title = post.find_element_by_class_name('post-title')

      # `get_attribute` serve para extrair qualquer atributo do elemento
      post_link = post_title.get_attribute('href')

      # printar informações
      print u"Títutlo: {titulo}, \nLink: {link}".format(
        titulo=post_title.text,
        link=post_link
    )

  # Fechar navegador
  firefox.quit()


Código-fonte do exemplo: `pythonclub.py <https://github.com/LucasMagnum/selenium-serie/blob/master/pythonclub.py>`_.


Desafios
---------

  **Desafio 1**

  Modificar o exemplo para mostrar o nome do autor do ``post``.

  **Desafio 2**

  Modificar o exemplo 01 para salvar os dados(titulo, link, autor) em um arquivo ``json``.


Por hoje é só!

Qualquer dúvida pode enviar um e-mail `contato@lucasmagnum.com.br <contato@lucasmagnum.com.br>`_ ficarei feliz em ajudar =)

