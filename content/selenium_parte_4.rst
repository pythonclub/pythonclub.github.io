Selenium - O que você deveria saber - Parte 4
#############################################

:date: 2014-06-24 11:55
:tags: selenium, python, selenium-serie
:category: Python
:slug: selenium-parte-4
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br
:github: lucasmagnum
:linkedin: lucasmagnum


Esse é o quarto post da série sobre Selenium, hoje você irá aprender a fazer algumas coisas mais interessantes!

    - Veja a `primeira parte <http://pythonclub.com.br/selenium-parte-1.html>`_.
    - Veja a `segunda parte <http://pythonclub.com.br/selenium-parte-2.html>`_.
    - Veja a `terceira parte <http://pythonclub.com.br/selenium-parte-3.html>`_.


Esse post será o mais logno, então prepare-se!


Parte 4
--------
    - `Expected conditions`_
    - `ActionsChains - Operações avançadas com o mouse`_
    - `EventListener - Ouvindo seu código`_

====================
Expected conditions
====================

Em alguns casos você precisa esperar para manipular o elemento até que uma condição se satisfaça, para isso o Selenium possui um conjunto de **funções** para facilitar na maioria das situações.

Essas condições pré-determinadas são chamadas ``expected conditions``, abaixo a lista das principais condições:

**title_is**
    Checa se o título (title) da página corresponde ao informado (comparação exata).
    Retorna True ou False.

**title_contains**
    Checa se o título contém a string informada (case-sensitive).
    Retorna True ou False.

**presence_of_element_located**
    Checa se o elemento está presente no DOM (ele não precisa estar visível).
    Retorna o elemento se ele estiver presente ou False.

**visibility_of_element_located**
    Checa se o elemento está presente no DOM e visível (ele precisa ter width e height maior que 0).
    Retorna o elemento se ele estiver visível ou False.

**text_to_be_present_in_element**
    Checa se o texto está presente no elemento.
    Retorna True ou False.

**text_to_be_present_in_element_value**
    Checa se o texto está presente no atributo "value" do elemento.
    Retorna True ou False.

**element_to_be_clickable**
    Checa se o elemento está visível e disponível para ser clicado.
    Retorna o elemento ou False.

**alert_is_present**
    Checa se existe algum alerta na página.
    Retorna o alerta ou False.

*Todas as funções estão no arquivo: selenium/webdriver/support/expected_conditions.py*


===============================================
ActionsChains - Operações avançadas com o mouse
===============================================

===================================
EventListener - Ouvindo seu código
===================================

Acredito que esse seja o último post sobre Selenium, espero que tenham gostado!
