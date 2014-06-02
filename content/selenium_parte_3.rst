Selenium - O que você deveria saber - Parte 3
#############################################

:date: 2014-05-30 10:49
:tags: selenium, python, selenium-serie
:category: Python
:slug: selenium-parte-3
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br
:github: lucasmagnum
:linkedin: lucasmagnum


Esse é o terceiro post da série sobre Selenium, hoje vamos aprender a executar código javascript e usar diferentes navegadores.

Se você não leu a segunda parte, clique `aqui <http://pythonclub.com.br/selenium-parte-2.html>`_.

Parte 3
---------
    - `Executando código javascript`_
    - `Como utilizar diferentes navegadores`_

==============================
Executando código javascript
==============================

Algumas vezes é necessário executar algum código ``javascript``, seja para adiantar a execução de uma função
ou até mesmo para manipular um elemento.

Vamos ao nosso exemplo:

.. code-block:: python

  from selenium import webdriver

  firefox = webdriver.Firefox()
  firefox.get('http://google.com.br/')

  firefox.execute_script('alert("código javascript sendo executado")')

  firefox.execute_async_script('alert("código javascript sendo executado")')


O Selenium permite que você faça isso através de uma instância do navegador, chamando os metódos ``execute_script`` e ``execute_async_script``.

A diferença entre os dois é que o primeiro (``execute_script``) irá esperar até ter a resposta do navegador e o outro não.

Você pode executar qualquer código javascript e isso pode ser muito útil!


=====================================
Como utilizar diferentes navegadores
=====================================

Para utilizar navegadores diferentes é bem simples, vamos ver como configurar 2 navegadores diferentes.


Firefox
-------

O *Firefox* é o mais simples de ser configurado, você não precisa passar nenhum parâmetro adicional.

.. code-block:: python

  from selenium import webdriver

  firefox = webdriver.Firefox()


Se a instalação do firefox tiver sido alterada e feito em alguma pasta diferente da padrão, você pode informar o caminho para o executável.

.. code-block:: python

  from selenium import webdriver

  firefox = webdriver.Firefox(firefox_binary='/bin/firefox')

  # se estiver usando o windows, basta informar o caminho completo
  firefox = webdriver.Firefox(firefox_binary='C:/firefox/firefox.exe')


Chrome
------

Para utilizar *Chrome* você precisa ter instalado o chrome no seu computador, você pode fazer isso pelo terminal:

.. code-block:: bash

  apt-get install chromium-browser


Após instalar o navegador você precisa realizar o download do ``chromedriver`` que é um intermediário entre o Selenium o e Chrome.

Por default o Selenium procura pelo ``chromedriver`` na mesma pasta de onde está sendo executado.

Faça o download da ultima versão do `chromedriver <http://chromedriver.storage.googleapis.com/index.html>`_, coloque em um local de sua preferência e passe o caminho completo na hora de iniciar o navegador.

.. code-block:: python

  from selenium import webdriver

  chrome = webdriver.Chrome(executable_path='<caminho para chromedriver>')

  # exemplo
  chrome = webdriver.Chrome(executable_path='/home/lucasmagnum/downloads/chromedriver')


Você pode visualizar todos os navegadores `suportados <http://docs.seleniumhq.org/about/platforms.jsp>`_ pelo Selenium


Por hoje é só!
Nos vemos na próxima, espero que tenha aprendido algo hoje :)

