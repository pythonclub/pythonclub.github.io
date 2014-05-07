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
1. Instalar/Verificar python instalado no Sistema Operacional.
2. Instalar gerenciador de pacotes python: pip.
3. Instalar o virtualenv.
4. Criar/Ativar o virtualenv do projeto.
5. Instalar o Django dentro do virtualenv.
6. Criar um projeto Django.
7. Criar uma app Django dentro do projeto.
8. Instalar Sublime Text.
9. Criar uma classe Model.
10. Criar uma rota: home.
11. Criar a view: home.
12. Configurar o Admin.
13. Rodar o Projeto.


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
