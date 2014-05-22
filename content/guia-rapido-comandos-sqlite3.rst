Guia rápido de comandos SQLite3
###############################

:date: 2014-05-16 01:00
:tags: sqlite
:category: Banco de dados
:slug: guia-rapido-comandos-sqlite3
:author: Regis da Silva
:email: regis.santos.100@gmail.com
:summary: Guia rápido de comandos SQLite3
:github: rg3915

É sempre bom ter tudo que você precisa de forma rápida e simples.

Escrevi este post para um mini tutorial de SQLite3. Através do **terminal**:

1. Criando um banco de dados.

.. code-block:: bash

	$ sqlite3 Clientes.db

2. A Ajuda.

.. code-block:: bash

	sqlite> .help

3. Criando a tabela *clientes*.

.. code-block:: sql

	sqlite> CREATE TABLE clientes(
	   ...> id INTEGER NOT NULL PRIMARY KEY,
	   ...> Nome VARCHAR(100) NOT NULL,
	   ...> CPF VARCHAR(11) NOT NULL,
	   ...> Email VARCHAR(20) NOT NULL,
	   ...> Fone VARCHAR(20),
	   ...> UF VARCHAR(2) NOT NULL
	   ...> );

4. Visualizando o código SQL que criou a tabela.

.. code-block:: bash

	sqlite> .schema clientes

5. Visualizando todas as tabelas existentes.

.. code-block:: bash

	sqlite> .table

6. Saindo do SQLite3.

.. code-block:: bash

	sqlite> .exit

Abra um editor de texto e salve um arquivo com o nome *inserirdados.sql*.

.. code-block:: bash

	$ gedit inserirdados.sql

E digite a inserção de alguns dados.

.. code-block:: sql

	INSERT INTO clientes VALUES(1, 'Regis', '00000000000', 'rg@email.com', '1100000000', 'SP');
	INSERT INTO clientes VALUES(2, 'Abigail', '11111111111', 'abigail@email.com', '1112345678', 'RJ');
	INSERT INTO clientes VALUES(3, 'Benedito', '22222222222', 'benedito@email.com', '1187654321', 'SP');
	INSERT INTO clientes VALUES(4, 'Zacarias', '33333333333', 'zacarias@email.com', '1199999999', 'RJ');

7. Importe estes comandos no sqlite.

.. code-block:: bash

	$ sqlite3 Clientes.db < inserirdados.sql

8. Abra o SQLite3 novamente, e visualize os dados.

.. code-block:: sql

	$ sqlite3 Clientes.db
	sqlite> SELECT * FROM clientes;

9. Você pode exibir o nome das colunas digitando

.. code-block:: bash

	sqlite> .header on

10. Para escrever o resultado num arquivo externo digite

.. code-block:: sql

	sqlite> .output resultado.txt
	sqlite> SELECT * FROM clientes;
	sqlite> .exit
	$ cat resultado.txt

11. Adicionando uma nova coluna na tabela clientes.

.. code-block:: sql

	sqlite> ALTER TABLE clientes ADD COLUMN bloqueado BOOLEAN;

No SQLite3 os valores para boolean são 0 (falso) e 1 (verdadeiro).

12. Visualizando as colunas da tabela clientes.

.. code-block:: bash

	sqlite> PRAGMA table_info(clientes);

13. Alterando os valores do campo bloqueado.

.. code-block:: sql

	sqlite> UPDATE clientes SET bloqueado=0; -- comentario: Atualiza todos os registros para Falso.
	sqlite> UPDATE clientes SET bloqueado=1 WHERE id=1; -- Atualiza apenas o registro com id=1 para Verdadeiro.
	sqlite> UPDATE clientes SET bloqueado=1 WHERE UF='RJ'; -- Atualiza para Verdadeiro todos os registros com UF='RJ'.

Faça um SELECT novamente para ver o resultado.

Mais informações em `SQLite.org <http://www.sqlite.org/cli.html>`_.

Futuramente pretendo postar algo sobre SQLite3 e Python...