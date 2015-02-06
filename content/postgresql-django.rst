PostgreSql + Django
===================

:date: 2015-02-05 18:00
:tags: python, postresql, banco de dados
:category: Python, Banco de dados
:slug: postgresql-django
:author: Regis da Silva
:email: regis.santos.100@gmail.com
:github: rg3915
:summary: Esta é a parte 3 (de 3) da série de posts sobre PostgreSql...

Se você já leu o *Tutorial Postgresql* e *Postgresql + Python3*, este post é uma continuação. Aqui nós veremos usar PostgreSql no `Django <http://pythonclub.com.br/tutorial-django-17.html>`_.

Para quem já leu `Two Scoops of Django <http://twoscoopspress.com/products/two-scoops-of-django-1-6>`_ sabe que o `PyDanny <http://www.pydanny.com/>`_ recomenda fortemente o uso do `PostgreSQL <http://www.postgresql.org/>`_ em seus projetos.

Então vejamos aqui como configurar o Postgresql para ser usado no `Django <http://pythonclub.com.br/tutorial-django-17.html>`_.

Precisamos criar o banco manualmente
------------------------------------

Começando...

.. code-block:: bash

    $ sudo su - postgres

Veja o prompt:

.. code-block:: bash

    postgres@myuser:~$

Criando o banco

.. code-block:: bash

    $ createdb mydb

Se existir o banco faça

.. code-block:: bash

    $ dropdb mydb

e crie novamente. Para sair digite

.. code-block:: bash

    $ exit

Django
------

Vamos criar um virtualenv e instalar o `psycopg2 <http://initd.org/psycopg/docs/install.html#use-a-python-package-manager>`_, além do django.

.. code-block:: bash

    virtualenv -p /usr/bin/python3 teste
    cd teste
    source bin/activate
    pip install psycopg2 django
    pip freeze
    pip freeze > requirements.txt

**Dica**: Para diminuir o caminho do prompt digite

.. code-block:: bash

    $ PS1="(`basename \"$VIRTUAL_ENV\"`):/\W$ "

**Dica**: 

.. code-block:: bash
    
    vim ~/.bashrc +
    alias manage='python $VIRTUAL_ENV/manage.py'

Com isto nós podemos usar apenas ``manage`` ao invés de ``python manage.py``.

Criando o projeto
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    django-admin.py startproject myproject .
    cd myproject
    python ../manage.py startapp core

**Edite o settings.py**

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.path.join(BASE_DIR, 'mydb'),
            'USER': 'myuser',
            'PASSWORD': 'mypassword',
            'HOST': '127.0.0.1',
            'PORT': '', # 8000 is default
        }
    }

**Rode a aplicação**

.. code-block:: bash

    python manage.py migrate
    python manage.py runserver

http://127.0.0.1:8000/ ou http://localhost:8000/

**Edite o models.py**

.. code-block:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    
    
    class Person(models.Model):
        name = models.CharField(_('Nome'), max_length=50)
        email = models.EmailField(_('e-mail'), max_length=30, unique=True)
        age = models.IntegerField(_('Idade'))
        active = models.BooleanField(_('Ativo'), default=True)
        created_at = models.DateTimeField(
            _('Criado em'), auto_now_add=True, auto_now=False)
    
        class Meta:
            ordering = ['name']
            verbose_name = "pessoa"
            verbose_name_plural = "pessoas"
    
        def __str__(self):
            return self.name

Leia mais em

`Tutorial Django 1.7 <http://pythonclub.com.br/tutorial-django-17.html>`_ 

`Como criar um site com formulário e lista em 30 minutos? <http://pythonclub.com.br/criar-site-com-form-lista-30-min.html>`_ 

**Edite o settings.py** novamente

Em *INSTALLED_APPS* insira a app *core*.

.. code-block:: python

    INSTALLED_APPS = (
    	...
        'myproject.core',
    )

**Faça um migrate**

.. code-block:: bash

    python manage.py makemigrations core
    python manage.py migrate

Um pouco de shell
^^^^^^^^^^^^^^^^^

.. code-block:: bash

    python manage.py shell
    Python 3.4.0 (default, Apr 11 2014, 13:05:18) 
    [GCC 4.8.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> 



Serve para manipular a app pelo **terminal**.

.. code-block:: python

    >>> from myproject.core.models import Person
    >>> p = Person.objects.create(name='Regis',email='regis@example.com',age=35)
    >>> p.id
    >>> p.name
    >>> p.email
    >>> p.age
    >>> p.active
    >>> p.created_at
    >>> p = Person.objects.create(name='Xavier',email='xavier@example.com',age=66,active=False)
    >>> persons = Person.objects.all().values()
    >>> for person in persons: print(person)
    >>> exit()

Leia mais em

*Tutorial PostgreSql*

*PostgreSql + Python3*

`Tutorial Django 1.7 <http://pythonclub.com.br/tutorial-django-17.html>`_ 

`Como criar um site com formulário e lista em 30 minutos? <http://pythonclub.com.br/criar-site-com-form-lista-30-min.html>`_ 

`How To Install and Configure Django with Postgres, Nginx, and Gunicorn <https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn>`_ 

http://www.postgresql.org/docs/9.4/static/tutorial-createdb.html

http://www.postgresql.org/docs/9.4/static/index.html

http://www.postgresql.org/docs/9.4/static/tutorial-sql.html