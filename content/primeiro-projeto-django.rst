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
    $ sudo apt-get install python-virtualenv
    $ sudo easy_install pip
	
pra testar se o virtualenv está instalado corretamente execute no terminal::

	$ virtualenv –version	
	
resultado::

	1.9.1

O pacote **python-setuptools** foi necessário pra instalar o **easy_install** que usamos apenas para instalar o **pip**
A partir de agora dentro do ambiente virtual sempre usaremos o pip para instalar os pacotes necessários.	

muito bem, com o **virtualenv** instalado o próximo passo será criar um ambiente virtual e assim instalarmos o **Django**.

vamos criar nosso virtualenv chamado **pythonclub**::
	
	$ virtualenv pythonclub –system-site-packages 
