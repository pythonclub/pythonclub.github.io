PostgreSql e Python3
====================

:status: draft
:date: 2015-02-17 13:00
:tags: python, postresql, banco de dados
:category: Python, Banco de dados
:slug: postgresql-e-python3
:author: Regis da Silva
:email: regis.santos.100@gmail.com
:github: rg3915
:summary: Esta é a parte 2 (de 3) da série de posts sobre PostgreSql...

Se você já leu o *Tutorial Postgresql* este post é uma continuação. Aqui nós veremos como manipular um banco de dados PostgreSql no Python3.

Além da instalação mostrada no primeiro post precisaremos de

.. code-block:: bash

    $ sudo apt-get install python-psycopg2 # para python2
    # ou
    $ sudo apt-get install python3-psycopg2 # para python3

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

Abra o python3.

.. code-block:: bash

    $ python3
    Python 3.4.0 (default, Apr 11 2014, 13:05:18) 
    [GCC 4.8.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

Importe o psycopg2

.. code-block:: python

    >>> import psycopg2

Conectando a um banco de dados existente

.. code-block:: python

    >>> conn = psycopg2.connect("dbname=mydb user=myuser")

Abrindo um cursor para manipular o banco

.. code-block:: python

    >>> cur = conn.cursor()

Criando uma nova tabela

.. code-block:: python

    >>> cur.execute("CREATE TABLE person (id serial PRIMARY KEY, name text, age integer);")

Inserindo dados.O Psycopg faz a conversão correta. Não mais injeção SQL.

.. code-block:: python

    >>> cur.execute("INSERT INTO person (name, age) VALUES (%s, %s)",("O'Relly", 60))
    >>> cur.execute("INSERT INTO person (name, age) VALUES (%s, %s)",('Regis', 35))

Grava as alterações no banco

.. code-block:: python

    >>> conn.commit()

# Select

.. code-block:: python

    >>> cur.execute("SELECT * FROM person;")
    >>> cur.fetchall()

Fecha a comunicação com o banco

.. code-block:: python

    >>> cur.close()
    >>> conn.close()
    >>> exit()

Leia também

*Tutorial PostgreSql*

*PostgreSql e Django*

http://initd.org/psycopg/docs/

http://initd.org/psycopg/docs/usage.html
