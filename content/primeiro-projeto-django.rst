Seu primeiro projeto Django com Sublime Text no Linux
#####################################################

:date: 2014-04-28 10:00
:tags: python, django, vitualenv
:category: Geral
:slug: primeiro-projeto-django
:author: Fabiano Góes
:email:  fabianogoes@gmail.com
:summary: Seu primeiro projeto Django com Sublime Text no Linux


========================
O objetivo deste artigo:
========================
* Instalar/Verificar python instalado no Sistema Operacional.
* Instalar gerenciador de pacotes python: pip.
* Instalar o virtualenv.
* Criar/Ativar o virtualenv do projeto.
* Instalar o Django dentro do virtualenv.
* Criar um projeto Django.
* Criar uma app Django dentro do projeto.
* Instalar Sublime Text.
* Criar uma classe Model.
* Criar uma rota: home.
* Criar a view: home.
* Configurar o Admin.
* Rodar o Projeto.


Ambiente usado durante a escrita deste artigo
=============================================
- Sistema Operacional: Linux Ubuntu 12.04 LTS
- Python 2.7
- Django 2.6 

---------------------------------------

No Linux/Ubuntu não precisamos instalar Python, isso porque já é nativo em sistemas operacionais baseados em Unix, 
mas pra ter certeza basta executar o comando no terminal::

	$ python –version

o resultado deve ser::

	Python 2.7.4

vamos começar instalando os pacotes necessários no Sistema Operacional::

    $ sudo apt-get update
    $ sudo apt-get install python-dev python-setuptools
    $ sudo easy_install pip
    $ sudo pip install virtualenv
	
pra testar se o virtualenv está instalado corretamente execute no terminal::

	$ virtualenv –version	
	
resultado::

	1.9.1

O pacote **python-setuptools** foi necessário apenas para instalar o **easy_install** que usamos para instalar o **pip**
A partir de agora dentro do ambiente virtual sempre usaremos o pip para instalar os pacotes necessários.	

muito bem, com o **virtualenv** instalado o próximo passo será criar um **virtualenv** e assim instalarmos o **Django**.

vamos criar nosso virtualenv chamado **pythonclub**::
	
	$ virtualenv pythonclub –no-site-packages 
	
**–no-site-packages** = esse parametro do virtualenv indica que meu ambiente virtual será totalmente isolado 
do meu sistema operacional, e só enxergara os pacotes instalados dentro do virtualenv.

agora vamos entrar dentro do ambiente virtual que criamos, e vamos ativar o virtualenv::
	
	$ cd pythonclub/
	$ source bin/activate
	
Neste momento temos nosso ambiente virtual criado e ativado, pronto para instalar o django, e é isso que vamos fazer::

	$ pip install django
	
Quando executamos o **pip install django** e não especificamos a versão, será instalado ultima versão disponivel, 
se quizermos instalar uma versão especifica podemos executar assim: **$ pip install django==1.5.4**

Então podemos finalmente criar nosso projeto django executando o comando::

	$ django-admin.py startproject first_django_project
	
Com nosso projeto criado podemos criar uma app para este projeto, e vamos criar uma app com o nome: **core**::

	$ cd first_django_project
	$ python manage.py startapp core
	
até aqui a estrutura de diretórios deve estar assim::

	pythonclub/
	bin/
	first_django_project/
	├── core
	│   ├── __init__.py
	│   ├── admin.py
	│   ├── models.py
	│   ├── tests.py
	│   └── views.py
	├── first_django_project
	│   ├── __init__.py
	│   ├── __init__.pyc
	│   ├── settings.py
	│   ├── settings.pyc
	│   ├── urls.py
	│   └── wsgi.py
	└── manage.py
	include/
	lib/
	
	
OBS: Os diretórios bin/, include/ e lib/ são diretórios do virtualenv, o restante são diretórios do projeto.

TODO: Instalar Sublime Text.

TODO: Criar uma classe Model.

TODO: Criar uma rota: home.

TODO: Criar a view: home.

TODO: Configurar o Admin.

TODO: Rodar o Projeto.	


