Principais dúvidas de quem quer aprender Django
###############################################

:date: 2014-05-13 23:00
:tags: python, django
:category: Django
:slug: principais-duvidas-de-quem-quer-aprender-django
:author: Regis da Silva
:email: regis.santos.100@gmail.com
:summary: Principais dúvidas de quem quer aprender Django
:github: rg3915

Vou começar este post fazendo um pequeno depoimento:

Quando eu ouvi falar de Django pela primeira vez eu me perguntei:

`O que é Django?`_

Daí eu comecei a procurar pela resposta, e surgiram outras perguntas. Eu precisei criar uma apresentação para a faculdade e consequentemente uma página com um **formulário** para inserção de dados, **gravação no banco de dados** e uma **lista** que retornasse os dados já gravados.
Procurei por vários materiais, inclusive a documentação oficial do `Django <https://www.djangoproject.com/>`_ mas encontrei muitas dificuldades para aprender do zero, só consegui entender o que era Django depois que fiz o curso `Welcome to the Django <http://welcometothedjango.com.br/>`_. Então vejamos:

- `O que é Django?`_
- `Instalando o Django`_
- `O que é MTV?`_
- `O que é Virtualenv e Requirements?`_
- `Como criar um site com formulário e lista em 30 minutos? <http://pythonclub.com.br/criar-site-com-form-lista-30-min.html>`_

===============
O que é Django?
===============

Segundo `Django Brasil <http://www.djangobrasil.org/>`_,

> *Django é um framework web de alto nível escrito em Python que estimula o desenvolvimento rápido e limpo.*

Foi criado por *Adrian Holovaty* numa agência publicitária.

Django segue o princípio **DRY** *(Dont repeat yourself)* "Não se repita".

Adota o padrão MTV, possui `mapeamento objeto-relacional <http://turing.com.br/material/acpython/mod3/django/orm1.html>`_ `ORM <http://pt.wikipedia.org/wiki/Django_(framework_web)#Mapeamento_Objeto-Relacional_.28ORM.29>`_, orientação à objeto, sistema de `administração <https://docs.djangoproject.com/en/1.6/ref/contrib/admin/>`_ automático e completo, sistema de `templates <https://docs.djangoproject.com/en/1.6/topics/templates/>`_ e é *open source*.

=======================
Instalando o Django
=======================

Na verdade não é só o Django, precisamos de:

* **Python 2.7** - Poderia ser o 3.0, mas o Python 2.7 oferece maior estabilidade, por já ser consolidada entre os usuários, e por oferecer uma gama de bibliotecas e documentação.

* **Django** - Até a data de lançamento deste post a versão é Django 1.6.4.

* **Git** - Sistema de controle de versão distribuído. 

E segundo `PyPA <https://python-packaging-user-guide.readthedocs.org/en/latest/current.html>`_ é recomendável a instalação das seguintes ferramentas:

* **Pip** - O `Pip <http://pip.readthedocs.org/en/latest/>`_ é uma ferramenta para instalar e gerenciar pacotes Python.

* **Virtualenv** - O `Virtualenv <https://python-packaging-user-guide.readthedocs.org/en/latest/projects.html#virtualenv>`_ é um ambiente virtual de desenvolvimento que isola o projeto com suas dependências específicas. Ou seja, você pode ter vários projetos com bibliotecas diferentes, versões diferentes; e um não interfere no outro, consequentemente não interfere nas configurações padrões do sistema operacional. Exemplo, você pode ter um projeto com Django 1.6 e outro com Django 1.5, cada um no seu ambiente de desenvolvimento.

Instalando o Django no Windows
------------------------------

Veja o post de `Thiago Côroa <http://pythonclub.com.br/instalacao-python-django-windows.html>`_.

Instalando o Django no Linux
------------------------------

Use o **terminal**.

* **Python 2.7** - Já vem instalado no Linux! :) Digite:

.. code-block:: bash

	$ python --V

* **Git**

.. code-block:: bash

	$ sudo apt-get install -y git

* **Curl** - Talvez precise.

.. code-block:: bash

	$ sudo apt-get install -y curl

* **Pip**

*"Curl menos letra Ó"*

.. code-block:: bash

	$ curl -O http://python-distribute.org/distribute_setup.py
	$ sudo python -y distribute_setup.py
	$ sudo easy_install pip

Fonte: `Welcome to the Django <http://welcometothedjango.com.br/>`_ Curso

* **Virtualenv**

.. code-block:: bash

	$ sudo pip install virtualenv

* **Django 1.6**

.. code-block:: bash

	$ sudo pip install django==1.6

Obs: repare que instalamos o Django direto no sistema, mas na verdade ele deverá ser instalado dentro de cada virtualenv. Leia sobre `O que é Virtualenv e Requirements?`_.

Instalando o Django no Mac
------------------------------

É semelhante ao modo do Linux usando o terminal.

==================================
O que é MTV?
==================================

MTV significa *Model*, *View* e *Template*. É o mesmo modelo de *arquitetura de software* conhecido como MVC. Mas neste caso,

* *Model* (modelo) é a camada de abstração dos dados, regras de negócios, lógica e funções. É onde acontece o ORM.

* *View* (visão), no Django, é uma função *python* que recebe uma *request* (requisição) e retorna uma *response* (resposta) web. Equivale ao *controller* de outros frameworks.

* *Templates* (prefiro não traduzir) são as páginas html, apesar de que a saída pode ser um simples texto no terminal. O legal é que templates no Django proporciona facilidade e flexibilidade, podemos criar um modelo *base* e estender sua reutilização, por exemplo.

Leia mais sobre MTV em `Entendendo como o Django trabalha <http://www.aprendendodjango.com/entendendo-como-o-django-trabalha/>`_. E veja o diagrama.
 
==================================
O que é Virtualenv e Requirements?
==================================

Como mencionado antes em `Instalando o Django`_, Virtualenv é um ambiente virtual que isola seu projeto junto com suas dependências.
Então o que é *requirements*?
É um arquivo (*requirements.txt*) que lista todas as bibliotecas que você precisa usar no seu projeto, por exemplo, eu gosto de usar:

.. code-block:: python

	Django==1.6
	Unipath==1.0
	dj-database-url==0.2.2
	dj-static==0.0.5
	gunicorn==18.0
	psycopg2==2.5.1
	django-decouple==2.1
	South==0.8.4
	mock==1.0.1
	django-extensions
	pygraphviz

Leia a continuação deste post em `Como criar um site com formulário e lista em 30 minutos? <http://pythonclub.com.br/criar-site-com-form-lista-30-min.html>`_.