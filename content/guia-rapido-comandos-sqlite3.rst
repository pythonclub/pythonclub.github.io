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

`Criando uma tabela`_

`CRUD`_

`Backup`_

`Relacionando tabelas`_

Escrevi este post para um mini tutorial de SQLite3. Através do **terminal**:

Criando uma tabela
------------------

1. Criando um banco de dados.

.. code-block:: bash

	$ sqlite3 Clientes.db

2. A Ajuda.

.. code-block:: bash

	sqlite> .help

3. Criando a tabela *clientes*.

.. code-block:: sql

	sqlite> CREATE TABLE clientes(
	   ...> id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	   ...> Nome VARCHAR(100) NOT NULL,
	   ...> CPF VARCHAR(11) NOT NULL,
	   ...> Email VARCHAR(20) NOT NULL,
	   ...> Fone VARCHAR(20),
	   ...> UF VARCHAR(2) NOT NULL
	   ...> );

**Nota**: Se usamos ``AUTOINCREMENT`` não precisamos do ``NOT NULL``.

.. code-block:: sql

	sqlite> CREATE TABLE clientes(
	   ...> id INTEGER PRIMARY KEY AUTOINCREMENT,
	   ...> ...

4. Visualizando o código SQL que criou a tabela.

.. code-block:: bash

	sqlite> .schema clientes

5. Visualizando todas as tabelas existentes.

.. code-block:: bash

	sqlite> .table

6. Saindo do SQLite3.

.. code-block:: bash

	sqlite> .exit

CRUD
----

Abra um editor de texto e salve um arquivo com o nome *inserirdados.sql*.

.. code-block:: bash

	$ gedit inserirdados.sql

E digite a inserção de alguns dados.

.. code-block:: sql

	INSERT INTO clientes VALUES(1, 'Regis', '00000000000', 'rg@email.com', '1100000000', 'SP');
	INSERT INTO clientes VALUES(2, 'Abigail', '11111111111', 'abigail@email.com', '1112345678', 'RJ');
	INSERT INTO clientes VALUES(3, 'Benedito', '22222222222', 'benedito@email.com', '1187654321', 'SP');
	INSERT INTO clientes VALUES(4, 'Zacarias', '33333333333', 'zacarias@email.com', '1199999999', 'RJ');


**Nota**: No caso do ``INSERT INTO`` não precisamos numerar, basta trocar o número do ``id`` por ``NULL``, exemplo:

.. code-block:: sql

	INSERT INTO clientes VALUES(NULL, 'Carlos', '99999999999', 'carlos@email.com', '118888-8888', 'SP');

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

14. Deletando registros.
   
.. code-block:: sql

	sqlite> DELETE FROM clientes WHERE id=4;

**Cuidado**: se você não usar o ``WHERE`` e escolher um ``id`` você pode deletar todos os registros da tabela.

15. Você pode exibir os dados na forma de coluna.

.. code-block:: bash

	sqlite> .mode column

Backup
------

.. code-block:: bash

	$ sqlite3 Clientes.db .dump > clientes.sql
	$ cat clientes.sql 
	PRAGMA foreign_keys=OFF;
	BEGIN TRANSACTION;
	CREATE TABLE clientes(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	Nome VARCHAR(100) NOT NULL,
	CPF VARCHAR(11) NOT NULL,
	Email VARCHAR(20) NOT NULL,
	Fone VARCHAR(20),
	UF VARCHAR(2) NOT NULL
	);
	INSERT INTO "clientes" VALUES(1,'Regis','00000000000','rg@email.com','1100000000','SP');
	INSERT INTO "clientes" VALUES(2,'Abigail','11111111111','abigail@email.com','1112345678','RJ');
	INSERT INTO "clientes" VALUES(3,'Benedito','22222222222','benedito@email.com','1187654321','SP');
	INSERT INTO "clientes" VALUES(4,'Zacarias','33333333333','zacarias@email.com','1199999999','RJ');
	COMMIT;

Pronto, se corromper o seu banco de dados, você pode recuperá-lo:

.. code-block:: bash

	$ mv Clientes.db Clientes.db.old
	$ sqlite3 Clientes_recuperado.db < clientes.sql 
	$ sqlite3 Clientes_recuperado.db 'SELECT * FROM clientes;'

Faça um SELECT novamente para ver o resultado do novo banco de dados.

Relacionando tabelas
--------------------

Todos devem saber que num banco de dados relacional a **chave estrangeira** ou ``FOREIGN KEY`` tem um papel importante no relacionamento entre duas tabelas. Veremos aqui como relacionar duas tabelas.

Primeiros façamos um backup do nosso bd.

.. code-block:: bash

	$ sqlite3 Clientes.db .dump > clientes.sql

Apenas para relembrar, vamos ver qual é a nossa tabela...

.. code-block:: bash

	$ sqlite3 Clientes.db
	sqlite> .tables
	clientes
	sqlite> .header on
	sqlite> .mode column

E quais são seus registros.

.. code-block:: sql

	sqlite> SELECT * FROM clientes;

.. code-block:: bash

	id          Nome        CPF          Email         Fone        UF          bloqueado 
	----------  ----------  -----------  ------------  ----------  ----------  ----------
	1           Regis       00000000000  rg@email.com  1100000000  SP          1         
	2           Abigail     11111111111  abigail@emai  1112345678  RJ          1         
	3           Benedito    22222222222  benedito@ema  1187654321  SP          0         

Então vamos criar duas novas tabelas: *cidades* e *clientes_novo*.

.. code-block:: sql

	sqlite> CREATE TABLE cidades(
	   ...> id INTEGER PRIMARY KEY AUTOINCREMENT,
	   ...> cidade TEXT,
	   ...> uf VARCHAR(2)
	   ...> );
	   ...> CREATE TABLE clientes_novo(
	   ...> id INTEGER PRIMARY KEY AUTOINCREMENT,
	   ...> Nome VARCHAR(100) NOT NULL,
	   ...> CPF VARCHAR(11) NOT NULL,
	   ...> Email VARCHAR(20) NOT NULL,
	   ...> Fone VARCHAR(20),
	   ...> bloqueado BOOLEAN,
	   ...> cidade_id INTEGER,
	   ...> FOREIGN KEY (cidade_id) REFERENCES cidades(id)
	   ...> );

Segundo `Sqlite Drop Column <http://grasswiki.osgeo.org/wiki/Sqlite_Drop_Column>`_, não tem como "*deletar*" uma coluna, então precisamos criar uma nova tabela *clientes_novo* com os campos que precisamos e copiar os dados da primeira tabela para esta.

.. code-block:: sql
	
	sqlite> INSERT INTO clientes_novo (id, Nome, CPF, Email, Fone, bloqueado)
	   ...> SELECT id, Nome, CPF, Email, Fone, bloqueado FROM clientes;

Veja que selecionamos os campos da tabela *clientes* e a inserimos em *clientes_novo*. Note que não copiamos o campo *UF* porque agora ele é da tabela *cidades*.

Agora podemos *deletar* a tabela "antiga".

.. code-block:: sql

	sqlite> DROP TABLE clientes;

E **renomear** a nova tabela.

.. code-block:: sql

	sqlite> ALTER TABLE clientes_novo RENAME TO clientes;

Veja o resultado da nova tabela.

.. code-block:: sql

	sqlite> SELECT * FROM clientes;

.. code-block:: bash

	id          Nome        CPF          Email         Fone        bloqueado   cidade_id 
	----------  ----------  -----------  ------------  ----------  ----------  ----------
	1           Regis       00000000000  rg@email.com  1100000000  1                     
	2           Abigail     11111111111  abigail@emai  1112345678  1                     
	3           Benedito    22222222222  benedito@ema  1187654321  0               

Agora você terá que popular as cidades e definir a ``cidade_id`` em cada cliente. Lembrando que a chave é ``AUTOINCREMENT``, então use ``NULL``.

.. code-block:: sql

	sqlite> INSERT INTO cidades VALUES (NULL,'Campinas','SP');
	sqlite> INSERT INTO cidades VALUES (NULL,'Sao Paulo','SP');
	sqlite> INSERT INTO cidades VALUES (NULL,'Rio de Janeiro','RJ');

Veja os registros da tabela *cidades*.

.. code-block:: sql

	sqlite> SELECT * FROM cidades;

.. code-block:: bash

	id          cidade      uf        
	----------  ----------  ----------
	1           Campinas    SP        
	2           Sao Paulo   SP        
	3           Rio de Jan 	RJ 

Agora precisamos atualizar a ``cidade_id`` de cada cliente.

.. code-block:: sql

	sqlite> UPDATE clientes SET cidade_id = 3 WHERE id = 1;
	sqlite> UPDATE clientes SET cidade_id = 1 WHERE id = 2;
	sqlite> UPDATE clientes SET cidade_id = 2 WHERE id = 3;

Resultado.

.. code-block:: sql

	sqlite> SELECT * FROM clientes;

.. code-block:: bash

	id          Nome        CPF          Email         Fone        bloqueado   cidade_id 
	----------  ----------  -----------  ------------  ----------  ----------  ----------
	1           Regis       00000000000  rg@email.com  1100000000  1           3         
	2           Abigail     11111111111  abigail@emai  1112345678  1           1         
	3           Benedito    22222222222  benedito@ema  1187654321  0           2

Façamos um ``INNER JOIN`` para visualizar todos os dados, inclusive a *cidade* e o *uf*.

.. code-block:: sql

	sqlite> SELECT * FROM clientes INNER JOIN cidades ON clientes.cidade_id = cidades.id;

.. code-block:: bash

	id          Nome        CPF          Email         Fone        bloqueado   cidade_id   cidade          uf        
	----------  ----------  -----------  ------------  ----------  ----------  ----------  --------------  --
	1           Regis       00000000000  rg@email.com  1100000000  1           3           Rio de Janeiro  RJ        
	2           Abigail     11111111111  abigail@emai  1112345678  1           1           Campinas        SP        
	3           Benedito    22222222222  benedito@ema  1187654321  0           2           Sao Paulo       SP

Referências
-----------

`SQLite.org <http://www.sqlite.org/cli.html>`_

`Introduction to Foreign Key Constraints <http://www.sqlite.org/foreignkeys.html>`_

`Making Other Kinds Of Table Schema Changes <http://www.sqlite.org/lang_altertable.html>`_

`Sqlite Drop Column <http://grasswiki.osgeo.org/wiki/Sqlite_Drop_Column>`_

Leia também sobre `SQLite3 e Python <http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html>`_.