Selenium - O que você deveria saber - Parte 2
#############################################

:date: 2014-05-10 14:49
:tags: selenium, python, selenium-serie
:category: Python
:slug: selenium-parte-2
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br

Esse é o segundo post da série sobre Selenium, hoje vamos manipular formulários, frames e múltiplas janelas.
Vamos também descobrir que é possível esperar para tentar descobrir um elemento na página.

Se você não leu a primeira parte, clique `aqui <http://pythonclub.com.br/selenium-parte-1.html>`_.

Parte 2
---------
    - `Brincando com formulários`_
    - `Trabalhando com múltiplas janelas`_
    - `Trabalhando com frames`_
    - `E se eu quiser esperar?!`_

==========================
Brincando com formulários
==========================

Quem nunca precisou preencher um formulário na web?

Hoje vamos aprender como fazer isso, vamos visualizar o exemplo abaixo que procura por um termo no google.

.. code-block:: python

  from selenium import webdriver
  from selenium.webdriver.common.keys import Keys

  firefox = webdriver.Firefox()
  firefox.get('http://google.com.br/')

  # pegar o campo de busca onde podemos digitar algum termo
  campo_busca = firefox.find_element_by_name('q')

  # Digitar "Python Club" no campo de busca
  campo_busca.send_keys('Python Club')

  # Simular que o enter seja precisonado
  campo_busca.send_keys(Keys.ENTER)


Foi bem simples, encontramos o ``campo_busca`` e invocamos o metódo ``send_keys`` com o texto
que desejamos digitar e depois simulamos o pressionamento do botão "Enter".

**Nota**: Sempre que houver a necessidade de utilizar uma tecla especial podemos encontrá-la na classe ``Keys``.


E se for um campo ``select``, como eu faço?

## TODO: Encontrar site com exemplo de Select, selecionar 2 campos

select_by_visible_text
select_by_index
select_by_value

## TODO: Exemplo de radio input

==================================
Trabalhando com múltiplas janelas
==================================

## TODO: Encontrar um site que abra seus links em uma nova janela
Alternar entre janelas e realizar alguns cliques.

=======================
Trabalhando com frames
=======================

## TODO: Encontrar um site que tem vários iframes

=========================
E se eu quiser esperar?!
=========================

## TODO: Encontrar um site com animações, onde o objeto html aparece dinamicamente.