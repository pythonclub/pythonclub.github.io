Selenium - O que você deveria saber - Parte 2
#############################################

:date: 2014-05-23 14:49
:tags: selenium, python, selenium-serie
:category: Python
:slug: selenium-parte-2
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br
:github: lucasmagnum
:linkedin: lucasmagnum


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

Digamos que exista o seguinte código:

.. code-block:: html

  <select name="estados">
    <option value="mg">MG</option>
    <option value="rj">RJ</option>
    <option value="sp">SP</option>
  </select>


Existe uma classe só para facilitar o trabalho com ``selects``, ela possui metódos para selecionar uma opção pelo seu texto ou valor, entre outras.

.. code-block:: python

  # Importar a classe Select
  >> from selenium.webdriver.support.ui import Select

  # É preciso passar o elemento para a classe
  >> estados = Select(firefox.find_element_by_name('estados'))

  # Selecionar a opção MG
  >> estados.select_by_visible_text('MG')

  # Selecionar a opção SP
  >> estados.select_by_value('sp')

Agora você já sabe o básico para manipular um formulário, você pode digitar nos campos, selecionar valores, clicar em botões.

==================================
Trabalhando com múltiplas janelas
==================================

E quando se abre uma nova janela? ou um alerta? O que fazemos?

.. code-block:: python

  >> firefox.window_handles
  [u'{7fd12d82-4fb3-48a4-a8b9-e1e460c00236}']

A instância ``firefox`` possui um atributo chamado ``window_handles``, que é uma lista
contendo um ID para cada janela aberta.

**Nota**: O ID é criado para nova janela aberta e não para uma ABA ou um alerta javascript.

Quando você abrir uma nova janela, poderá perceber que é criado automaticamente um novo ID.

.. code-block:: python

  >> firefox.window_handles
  [u'{7fd12d82-4fb3-48a4-a8b9-e1e460c00236}', u'{2ce4de19-0902-48e3-a1cc-50f6378afd79}']

Para alternar entre janelas, basta chamar o metódo ``switch_to_window`` passando o ID da janela como parâmetro.

Imagine que temos uma janela aberta na página do Google e a outra na página da Python Club.

.. code-block:: python

  >> firefox.window_handles
  [u'{7fd12d82-4fb3-48a4-a8b9-e1e460c00236}', u'{2ce4de19-0902-48e3-a1cc-50f6378afd79}']

  # Título da janela atual
  >> firefox.title
  u'Google'

  # Trocar para a última janela da lista
  >> firefox.switch_to_window_handles(firefox.window_handles[-1])
  >> firefox.title
  u'PythonClub //'

  # Fechar a janela atual
  >> firefox.close()

  # Voltar para a janela do Google
  >> firefox.switch_to_window_handles(firefox.window_handles[-1])
  >> firefox.title
  u'Google'

E como saber o ID da janela atual? Simples!

.. code-block:: python

  >> firefox.current_window_handle
  u'{7fd12d82-4fb3-48a4-a8b9-e1e460c00236}'

Fácil não?!

E se abrir um alerta ``javascript``, como fazemos???

Existe uma função para tratar alertas ``javascript``, a função ``switch_to_alert`` irá permitir que manipule eles sem problemas.

.. code-block:: python

  >> alerta = firefox.switch_to_alert()
  >> alerta.  # Tab para autocomplete
  alerta.accept     alerta.dismiss    alerta.driver     alerta.send_keys  alerta.text

  # Se for um `confirm`, você pode aceitar ou cancelar.
  >> alerta.accept()  # Aceitar, ou clicar em "OK"
  >> alerta.dismiss() # Cancelar, ou clicar em "Cancel"/"Cancelar"

  # Se for uma caixa de texto e você quiser digitar algo
  >> alerta.send_keys('Digitar esse texto')

  # Se você quiser visualizar o texto que está presente no alerta
  >> alerta.text
  u'Texto do alerta'


=======================
Trabalhando com frames
=======================

Não existe muita diferença entre manipulação de frames e janelas, o princípio é o mesmo.

  - Encontrar o elemento (metódo ``find_element``)
  - Mudar para ele (metódo ``switch_to_frame``)
  - Realizar as ações

--------------
Conceitos
--------------

  Por padrão o frame principal ou aquele que está disponível quando você abre uma página é denominado ``default_content``.

  Se algum elemento estiver dentro de um frame você não irá localizá-lo sem "entrar" neste frame.

  Se você estiver dentro de um frame e o elemento estiver no ``default_content`` você não conseguirá localizá-lo sem voltar para o frame principal.


*Exemplo*:

  Precisamos clicar em um botão que está dentro de um frame.

  **Premissas**: O iframe onde estão os botões que precisamos manipular possui o ID ``buttons``

.. code-block:: python

  # Vamos tentar localizar o botão que está dentro do frame e será gerado uma Exception
  >> firefox.find_element_by_id('<botao_id>')
  NoSuchElementException: Message: u'Unable to locate element: {"method":"id","selector":"<botao_id>"}'

  # Precisamos antes encontrar o frame
  >> frame = firefox.find_element_by_id('buttons')

  # Vamos alterar para ele
  >> firefox.switch_to_frame(frame)

  # Agora podemos encontrar o elemento
  >> botao = firefox.find_element_by_id('<botao_id>')

  # E podemos manipulá-lo :)
  >> botao.click()


=========================
E se eu quiser esperar?!
=========================

Quando você tenta localizar um elemento, o Selenium irá consultar a página e se não encontrar será gerado uma ``exception`` de imediato.

Mas e se o elemento demorar um pouco para aparecer, pode ser que ele faça parte de uma animação, um consulta ``ajax`` ou qualquer coisa do tipo.

Então precisamos dizer ao Selenium para **esperar**.

Existe uma classe chamada ``WebDriverWait`` que pode ser utilizada para para esperar por determinadas ações.

Hoje será apresentado o básico sobre ela e voltaremos a falar sobre na Parte 4 deste tutorial.

Veja o exemplo abaixo:

.. code-block:: python

  >> elemento = firefox.find_element_by_id('<elemento_id>')

Nesse caso se o elemento não existe, será gerado uma ``exception``.

Mas e se soubermos que ele pode demorar um tempo para aparecer?

.. code-block:: python

  # Importar a classe WebDriverWait
  >> from selenium.webdriver.support.ui import WebDriverWait

  def esperar_pelo_elemento(firefox):
    return firefox.find_element_by_id('<elemento_id>')

  >> elemento = WebDriverWait(firefox, 5).until(esperar_pelo_elemento)

O que fizemos? Nós pedimos para o ``firefox`` esperar por ``5`` segundos até que o resultado da função ``esperar_pelo_elemento`` seja ``True``. Caso passe esse tempo e ele não encontre o elemento, então será gerada uma ``exception``.

Essa foi nossa introdução ao ``WebDriverWait``, basicamente você precisa passar uma função que aceite como parâmetro a instância do navegador e lá executar o código para encontrar o elemento.


Por hoje é só!
Nos vemos na próxima, espero que tenha aprendido algo hoje :)

