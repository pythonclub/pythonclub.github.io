Selenium - O que você deveria saber - Parte 4
#############################################

:date: 2014-07-17 11:55
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


Esse post será o mais longo, então prepare-se!


Parte 4
--------
    - `Expected conditions`_
    - `ActionsChains - Operações avançadas`_
    - `EventListener - Ouvindo seu código`_

====================
Expected conditions
====================

Em alguns casos você precisa esperar para manipular o elemento até que uma condição se satisfaça, para isso o Selenium possui um conjunto de **funções** para facilitar na maioria das situações.

Essas condições são chamadas ``expected conditions``, abaixo a lista das principais condições:

``title_is``
    Checa se o título (title) da página corresponde ao informado (comparação exata).
    Retorna True ou False.

``title_contains``
    Checa se o título contém a string informada (case-sensitive).
    Retorna True ou False.

``presence_of_element_located``
    Checa se o elemento está presente no DOM (ele não precisa estar visível).
    Retorna o elemento se ele estiver presente ou False.

``visibility_of_element_located``
    Checa se o elemento está presente no DOM e visível (ele precisa ter width e height maior que 0).
    Retorna o elemento se ele estiver visível ou False.

``text_to_be_present_in_element``
    Checa se o texto está presente no elemento.
    Retorna True ou False.

``text_to_be_present_in_element_value``
    Checa se o texto está presente no atributo "value" do elemento.
    Retorna True ou False.

``element_to_be_clickable``
    Checa se o elemento está visível e disponível para ser clicado.
    Retorna o elemento ou False.

``alert_is_present``
    Checa se existe algum alerta na página.
    Retorna o alerta ou False.

*Todas as funções estão no arquivo: selenium/webdriver/support/expected_conditions.py*

Você pode utilizar essas funções em conjunto com o que foi aprendido na `Parte 2 <http://pythonclub.com.br/selenium-parte-2.html#e-se-eu-quiser-esperar>`_

Exemplos de uso:

.. code-block:: python

  # Importar classe para inicializar o browser
  from selenium import webdriver
  # Importar a classe WebDriverWait
  from selenium.webdriver.support.ui import WebDriverWait
  # Importar a classe que contém as funções e aplicar um alias
  from selenium.webdriver.support import expected_conditions as EC
  # Importar classe para ajudar a localizar os elementos
  from selenium.webdriver.common.by import By

  firefox = webdriver.Firefox()
  # Instanciar a classe que irá esperar até 5 segundos
  wait = WebDriverWait(firefox, 5)

  # Aguardar até que a página tenha o título "PythonClub"
  wait.until(EC.title_is("PythonClub"))

  # Aguardar página contenha o título "PythonClub"
  wait.until(EC.title_contains("PythonClub"))

  # Aguardar até que o elemento "id_elemento" esteja presente no DOM
  elemento = wait.until(EC.presence_of_element_located((By.ID, 'id_elemento')))

  # Aguardar até que o elemento "id_elemento" esteja visível
  elemento = wait.until(EC.visibility_of_element_located((By.ID, 'id_elemento'))))

  # Aguardar até que o elemento "id_elemento" contenha o texto "Python"
  wait.until(EC.text_to_be_present_in_element((By.ID, 'id_elemento'), 'Python'))

  # Aguardar até que o elemento "id_elemento" contenha o valor "Python"
  wait.until(EC.text_to_be_present_in_element_value((By.ID, 'id_elemento'), 'Python')))

  # Aguardar até que o elemento "id_elemento" possa ser clicado
  elemento = wait.until(EC.element_to_be_clickable((By.ID, 'id_elemento')))

  # Aguardar até que um alerta esteja presente na página
  wait.until(EC.alert_is_present)


Após os 5 segundos, se a condição retornar ``False`` será gerado uma exception ``TimeoutException``.


Use a abuse das ``conditions``!


===================================
ActionsChains - Operações avançadas
===================================

``click_and_hold(on_element=None)``
    Clica no elemento e mantém o botão esquerdo do mouse pressionado. Se o parâmetro ``on_element`` não for informado, será realizado na posição atual do mouse.

``release(on_element=None)``
    Despressiona o botão do mouse. Se o parâmetro ``on_element`` for informado, será realizado no elemento.

``context_click(on_element=None)``
    Clica no elemento com o botão direito do mouse. Se o parâmetro ``on_element`` não for informado, será realizado na posição atual do mouse.

``double_click(on_element=None)``
    Realiza o clique duplo. Se o parâmetro ``on_element`` não for informado, será realizado na posição atual do mouse.

``key_down(value, element=None)``
    Simula uma tecla sendo pressionada e mantida assim. (Deve ser utilizada somente com as teclas de modificação **Control**, **Alt** e **Shift**). Se o parâmetro ``element`` não for informado, será realizado no elemento atual.

``key_up(value, element=None)``
    Simula uma tecla sendo despressionada. (Deve ser utilizada somente com as teclas de modificação **Control**, **Alt** e **Shift**). Se o parâmetro ``element`` não for informado, será realizado no elemento atual.

*Você pode visualizar as outras funções em: selenium/webdriver/common/action_chains.py*

As ações são armazenadas na ordem em que foram invocadas e para que sejam realizadas é preciso chamar o metódo ``perform`` da instância.


Exemplos de uso:

.. code-block:: python

  # Importar classe para inicializar o browser
  from selenium import webdriver
  # Importar a classe ActionChains responsável pelas manipulações
  from selenium.webdriver.common.action_chains import ActionChains
  # Importar a classe Keys que podem ser utilizadas no key_up e key_down
  from selenium.webdriver.common.keys import Keys

  firefox = webdriver.Firefox()
  actions = ActionChains(firefox)


  # Clicar e manter na posição atual do mouse
  actions.click_and_hold()
  # Voltar o mouse para o estado inicial
  actions.release()
  # Disparar metódo para que as ações sejam executadas
  actions.perform()


  botao = firefox.find_element_by_id("#botaoqualquer")
  # Clicar e manter em um botão
  actions.click_and_hold(on_element=botao)
  actions.perform()


  # Clicar com o botão direito na posição atual do mouse
  actions.context_click()
  actions.perform()

  # Clique duplo
  actions.double_click(on_element=botao)
  actions.perform()

  # Exemplo com key_down e key_up. Simular um CTRL + C
  actions.key_down(Keys.CONTROL) # Pressionar o CTRL
  actions.send_keys('c') # Pressionar o C
  actions.key_up(Keys.CONTROL) # Liberar o CTRL
  actions.perform()


Tem algumas outras ações bem interessantes, vale dar uma olhada no arquivo.


===================================
EventListener - Ouvindo seu código
===================================

Acredito que esse seja o último post sobre Selenium, espero que tenham gostado!
