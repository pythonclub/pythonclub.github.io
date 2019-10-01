Title: Peewee - Um ORM Python minimalista
Slug: peewee-um-orm-python-minimalista
Date: 2017-07-20 23:45:24
Category: Python
Tags: Python, Peewee, ORM, banco de dados
Author: Michell Stuttgart
Email: michellstut@gmail.com
Github: mstuttgart
Linkedin: michell.stuttgart
Site: https://mstuttgart.github.io/
Summary: Conheça o Peewee, um prático e minimalista ORM Python

[Peewee](http://peewee.readthedocs.io/en/latest/index.html) é um ORM destinado a criar e gerenciar tabelas de banco de dados relacionais através de objetos Python. Segundo a [wikipedia](https://pt.wikipedia.org/wiki/Mapeamento_objeto-relacional), um ORM é:
>>> Mapeamento objeto-relacional (ou ORM, do inglês: Object-relational mapping) é uma técnica de desenvolvimento utilizada para reduzir a impedância da programação orientada aos objetos utilizando bancos de dados relacionais. As tabelas do banco de dados são representadas através de classes e os registros de cada tabela são representados como instâncias das classes correspondentes.

O que o ORM faz é, basicamente, transformar classes Python em tabelas no banco de dados, além de permitir construir *querys* usando diretamente objetos Python ao invés de SQL.

O Peewee é destinado a projetos de pequeno/médio porte, se destacando pela simplicidade quando comparado a outros ORM mais conhecidos, como o SQLAlchemy. Uma analogia utilizada pelo autor da API e que acho muito interessante é que Peewee está para o SQLAlchemy assim como SQLite está para o PostgreSQL.

Em relação aos recursos por ele oferecidos, podemos citar que ele possui suporte nativo a SQLite, PostgreSQL e MySQL, embora seja necessário a instalação de *drivers* para utilizá-lo com PostgreSQL e MySQL e suporta tanto Python 2.6+ quanto Python 3.4+. 

Neste tutorial, utilizaremos o SQLite, por sua simplicidade de uso e por não precisar de nenhuma configuração.

### Instalação

O Peewee pode ser facilmente instalado com o gerenciador de pacotes *pip*:

```bash
pip install peewee
```

### Criando o banco de dados

Para criar as tabelas é bem simples. Inicialmente passamos o nome do nosso banco de dados (a extensão `*.db` indica um arquivo do SQLite).

```python
import peewee

db = peewee.SqliteDatabase('codigo_avulso.db')

```

Diferente de outros bancos de dados que funcionam através um servidor, o SQLite cria um arquivo de extensão `*.db`, onde todos os nossos dados são armazenados.

**DICA**: caso deseje ver as tabelas existentes no arquivo `codigo_avulso.db`, instale o aplicativo `SQLiteBrowser`. Com ele fica fácil monitorar as tabelas criadas e acompanhar o tutorial.

```bash
 sudo apt-get install sqlitebrowser
```

A título de exemplo, vamos criar um banco destinado a armazenar nomes de livros e de seus respectivos autores. Comecemos primeiro com a classe que representa os autores.

```python
import peewee

db = peewee.SqliteDatabase('codigo_avulso.db')

class Author(peewee.Model):
    """
    Classe que representa a tabela Author
    """

    # A tabela possui apenas o campo 'name', que
    # receberá o nome do autor
    name = peewee.CharField()

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente.
        database = db

```
Em seguida, criamos a classe que representa os livros. Ela possui uma relação de "muitos para um" com a tabela de autores, ou seja, cada livro possui apenas um autor, mas um autor pode possuir vários livros.

```python
import peewee

db = peewee.SqliteDatabase('codigo_avulso.db')

class Book(peewee.Model):
    """
    Classe que representa a tabela Book
    """

    # A tabela possui apenas o campo 'title', que
    # receberá o nome do livro
    title = peewee.CharField()

    # Chave estrangeira para a tabela Author
    author = peewee.ForeignKeyField(Author)

    class Meta:
        # Indica em qual banco de dados a tabela
        # 'author' sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente.
        database = db
```

Agora, vamos reunir tudo em um único arquivo `model.py`. Como exemplo, eu criei um arquivo *main.py* para utilizarmos as classes que acabamos de criar.

```python

import peewee
from model import Author, Book


if __name__ == '__main__':
    try:
        Author.create_table()
    except peewee.OperationalError:
        print 'Tabela Author ja existe!'

    try:
        Book.create_table()
    except peewee.OperationalError:
        print 'Tabela Book ja existe!'

```

Após executarmos o código, será criado um arquivo de nome `codigo_avulso.db` no mesmo diretório do nosso arquivo `main.py`, contendo as tabelas `Author` e `Book`. A estrutura do diretório ficou assim:

```bash
.
├── codigo_avulso.db
├── main.py
├── model.py
```

### Inserindo dados no banco

Agora, vamos popular nosso banco com alguns autores e seus respectivos livros. Isso pode ser feito de dois modos. Através do método `create`, quando desejamos inserir um registro apenas; ou pelo método `insert_many`, quando desejamos inserir vários registros de uma vez em uma mesma tabela.

```python

# Inserimos um autor de nome "H. G. Wells" na tabela 'Author'
author_1 = Author.create(name='H. G. Wells')

book_1 = {
    'title': 'A Máquina do Tempo',
    'author': author_1,
}

book_2 = {
    'title': 'Guerra dos Mundos',
    'author': author_1,
}

# Inserimos um autor de nome "Julio Verne" na tabela 'Author'
author_2 = Author.create(name='Julio Verne')

book_3 = {
    'title': 'Volta ao Mundo em 80 Dias',
    'author': author_2,
}

book_4 = {
    'title': 'Vinte Mil Leguas Submarinas',
    'author_id': author_1,
}

books = [book_1, book_2, book_3, book_4]

# Inserimos os quatro livros na tabela 'Book'
Book.insert_many(books).execute()

```

### Consultando dados no banco

O Peewee possui comandos destinados a realizar consultas no banco. De maneira semelhante ao conhecido `SELECT`. Podemos fazer essa consulta de duas maneiras. Se desejamos o primeiro registro que corresponda a nossa pesquisa, podemos utilizar o método `get()`.

```python
book = Book.get(Book.title == "Volta ao Mundo em 80 Dias").get()
book.title
```
Porém, se desejamos mais de um registro, utilizamos o método `select`. Por exemplo, para consultar todos os livros escritos pelo autor "H. G. Wells".

```python
books = Book.select().join(Author).where(Author.name=='H. G. Wells')

# Exibe a quantidade de registros que corresponde a nossa pesquisa
print books.count()

for book in books:
	book.title

# Resultado:
# * A Máquina do Tempo
# * Guerra dos Mundos
# * Vinte Mil Leguas Submarinas

```

Também podemos utilizar outras comandos do SQL como `limit` e `group` (para mais detalhes, ver a documentação [aqui](http://peewee.readthedocs.io/en/latest/index.html)).

### Alterando dados no banco

Alterar dados também é bem simples. No exemplo anterior, se observarmos o resultado da consulta dos livros do autor "H. G. Wells", iremos nos deparar com o livro de título "Vinte Mil Léguas Submarinas". Se você, caro leitor, gosta de contos de ficção-científica, sabe que esta obra foi escrito por "Julio Verne", coincidentemente um dos autores que também estão cadastrados em nosso banco. Sendo assim, vamos corrigir o autor do respectivo livro.

Primeiro vamos buscar o registro do autor e do livro:

```python
new_author = Author.get(Author.name == 'Julio Verne')
book = Book.get(Book.title=="Vinte Mil Leguas Submarinas")
```
Agora vamos alterar o autor e gravar essa alteração no banco.

```python
# Alteramos o autor do livro
book.author = new_author

# Salvamos a alteração no banco
book.save()
```

### Deletando dados do banco

Assim como as operações anteriores, também podemos deletar registros do banco de maneira bem prática. Como exemplo, vamos deletar o livro "Guerra dos Mundos" do nosso banco de dados.

```python
# Buscamos o livro que desejamos excluir do banco
book = Book.get(Book.title=="Guerra dos Mundos")

# Excluimos o livro do banco
book.delete_instance()
```
Simples não?

### Conclusão

É isso pessoal. Este tutorial foi uma introdução bem enxuta sobre o Peewee. Ainda existem muitos tópicos que não abordei aqui, como a criação de *primary_key*, de campos *many2many* entre outros recursos, pois foge do escopo deste tutorial. Se você gostou do ORM, aconselho a dar uma olhada também na sua documentação, para conseguir extrair todo o potencial da ferramenta. A utilização de um ORM evita que o desenvolvedor perca tempo escrevendo *query* SQL e foque totalmente no desenolvimento de código. 

O Peewee também possui suporte ao flamework *flask*, então dependendo do tamanho do projeto, pode ser uma alternativa interessante no lugar de ORM mais complexos como o SQLAlchemy.

É isso pessoal. Obrigado pela leitura e até o próximo tutorial!

### Referências

* [Documentação do Peewee (em inglês)](http://peewee.readthedocs.io/en/latest/index.html)
* [An Intro to peewee – Another Python ORM](https://www.blog.pythonlibrary.org/2014/07/17/an-intro-to-peewee-another-python-orm/)
* [Introduction to peewee](http://jonathansoma.com/tutorials/webapps/intro-to-peewee/)
* [Introdução à Linguagem SQL](https://www.novatec.com.br/livros/introducao-sql/)

