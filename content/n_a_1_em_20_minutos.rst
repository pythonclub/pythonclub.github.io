Como otimizar suas consultas no Django - De N a 1 em 20 minutos
###############################################################

:date: 2015-05-10 13:55
:tags: python, django
:category: Python
:slug: django-introducao-queries
:author: Lucas Magnum
:email:  lucasmagnumlopes@gmail.com
:github: lucasmagnum
:linkedin: lucasmagnum


Essa semana fiz uma palestra em um BEV no `Luizalabs <http://luizalabs.com/>`_.
Resolvi falar sobre Django, pois é um framework que utilizamos na empresa para diversos projetos.

O objetivo é ensinar algumas técnicas simples e que auxiliam a diminuir o número de consultas que realizamos
no banco de dados.de

Os slides podem acessados `aqui <https://docs.google.com/presentation/d/1SV27J8rFfORxE_JrU5NPahfqDJk6y87MuQUeKVTA0Gw/edit?usp=sharing>`_.

Então, vamos lá!


Overview
--------

Geralmente nossa aplicação Django tem um arquivo ``models.py``, que contém nossa representação das tabelas no banco de dados.

Para os próximos exemplos considere esse arquivo:

.. code-block:: python

    from django.contrib.auth.models import User
    from django.db import models

    class Cadastro(models.Model):
        # chave estrangeira para o usuário
        user = models.OneToOneField(User)

        # Outros campos
        # [...]


Veja o exemplo abaixo, é muito comum ver algo parecido em algum tutorial sobre Django.

.. code-block:: python

    >> Cadastro.objects.all()

Mas o que realmente acontece quando fazemos isso?

Para que a consulta aconteça, 5 elementos principais precisam interagir entre si.
Os elementos são:

.. code-block:: python

    Model
    Manager
    QuerySet
    Query
    SQLCompiler

É importante entender o papel de cada um, para que sejamos capazes de atuar com assertividade.

**Model**
    * É uma representação da nossa tabela de dados, contém os campos e os comportamentos dos dados que estamos armazenando.

**Manager**
    * Está sempre acoplado a um model e é responsável por expor os métodos do QuerySet.
      Quando não declaramos nenhum manager, o Django cria por padrão o ``objects``.

**QuerySet**
    * QuerySet é um conjunto de ações que serão realizadas no banco de dados (select, insert, update ou delete).
      Responsável por interagir diretamente com a Query.

**Query**
    * Cria uma estrutura de dados complexa com todos os elementos presentes em uma consulta.
      Gera uma representação SQL de um QuerySet.

**SQLCompiler**
    * Recebe as instruções SQL e realiza as operações no banco de dados.


Agora que conhecemos os 5 elementos principais, vamos falar sobre **QuerySet**, é com ele
que vamos conseguir construir queries mais eficientes.

QuerySets são Lazy
------------------
Algo que é importante notar sobre o comportamento das QuerySets, são que elas são Lazy.

Mas o que é isso?

Imaginem as seguintes consultas:

.. code-block:: python

    >> cadastros = Cadastro.objects.all()
    >> ativos = cadastros.filter(ativo=True)
    >> inativos = cadastros.filter(inativo=True)

Sabe quantas consultas foram realizadas no banco de dados, por essas 3 linhas de código? NENHUMA.
QuerySets podem ser:

    * Construídas
    * Filtradas
    * Limitadas
    * Ordenadas
    * Passadas comoo parâmetro

E nenhuma consulta será realizada no banco de dados.

Quando dizemos que as QuerySets são lazy, queremos dizer que as consultas só serão realizadas no banco de dados, quando pedimos!

Então, como pedimos?

.. code-block:: python

    # Quando solicitamos somente um resultado
    >> Cadastro.objects.all()[0]

    # Quando fazemos um slicing passando o parâmetro `step`
    >> Cadastro.objects.all()[::2]

    # Quando fazemos uma iteração
    >> [cadastro for cadastro in Cadastro.objects.all()]

    # Quando chamamos o método len()
    >> len(Cadastro.objects.all())

    # Quando chamamos o método list()
    >> list(Cadastro.objects.all())

     # Quando chamamos o método bool()
    >> bool(Cadastro.objects.all())

    # Quando chamamos o método repr()
    >> repr(Cadastro.objects.all())


Uma vez que entendemos como as consultas são realizadas no banco de dados, vamos aprender como resolver os problemas mais comuns quando se trata de consultas: relacionamentos.


Relacionamento OneToOne e ForeignKey
------------------------------------

OneToOne e ForeignKey são os tipos de relacionamentos mais comuns no Django, estamos utilizando-os quase intuitivamente.

Imaginem o seguinte cenário:

Temos um loop e a cada iteração invocamos um atributo do models que é uma chave estrangeira para outra tabela.

.. code-block:: python

    >> cadastros = Cadastros.objects.all()
    >> cadastros.count()
    500 # Temos 500 cadastros no nosso banco de dados

    # Fazemos uma iteração em todos os cadastros
    >> for cadastro in cadastros:
        # realizamos um print com o nome do usuário para tal cadastro.
        # note que essa poderia ser qualquer outra operação, onde o atributo `user` fosse acessado
        print cadastro.user

Esse é um código simples e que geralmente não vemos problemas nenhum, mas iremos nos supreender
com quantas queries são realizadas no banco de dados.

.. code-block:: python

    # https://docs.djangoproject.com/en/1.8/faq/models/#how-can-i-see-the-raw-sql-queries-django-is-running
    >> from django.db import connection

    >> cadastros = Cadastros.objects.all()

    >> for cadastro in cadastros:
        print cadastro.user

    >> print len(connection.queries)
    501

Foram realizadas **501** consultas para iterar sobre 500 cadastros (1 consulta para retornar todos os cadastros e 1 consulta para cada vez que acessamos o atributo ``user``).
Isso ocorre, porque estamos acessando um atributo que é um relacionamento para outra tabela,
cada vez que o Django acessa esse atributo uma nova consulta precisa ser realizada no banco de dados.

Isso é válido tanto para OneToOne e ForeignKey.

Como podemos resolver isso? Utilizando o método do QuerySet chamado ``select_related``.

select_related
--------------

Veja o mesmo código sendo executado com `select_related <https://docs.djangoproject.com/en/1.8/ref/models/querysets/#select-related>`_.

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastros.objects.select_related('user').all()

    >> for cadastro in cadastros:
        print cadastro.user

    >> print len(connection.queries)
    1

O objetivo do ``select_related`` é realizar uma única query que une todos os ``models`` relacionados.
Ele faz isso através de um ``JOIN`` na instrução ``SQL``, então realiza o cache do atributo para que possa acessá-lo sem realizar uma nova consulta.

O único problema do ``select_related`` é que não funciona para campos **ManyToMany** e **Relacionamentos Reversos**, mas para esses casos temos o ``prefetch_related``.

Primeiro, vamos entender o que é um relacionamento reverso.

Relacionamento reverso
----------------------

Por padrão o Django adiciona um relacionamento reverso quando sua tabela é referenciada por uma chave estrangeira.

Se não passar o parâmetro related_name, irá seguir o padrão <nome_tabela>_set

.. code-block:: python

    from django.contrib.auth.models import User
    from django.db import models

    class Cadastro(models.Model):
        user = models.OneToOneField(User)

        # Outros campos
        # [...]

    class Endereco(models.Model):
        cadastro = models.ForeignKey(Cadastro)

        # Outros campos
        # [...]

Dessa forma, criamos um relacionamento reverso no model ``Cadastro``, quando referenciamos ele numa chave estrangeira no model ``Endereco``.


.. code-block:: python

    >> cadastros = Cadastro.objects.all()

    >> for cadastro in cadastros:

        # Uma vez que o relacionamento foi criado, podemos acessá-lo
        print cadastro.endereco_set.all()


Se houvesse o parâmetro `related_name`, acessariamos pelo nome que criamos.

.. code-block:: python

    class Endereco(models.Model):
        cadastro = models.ForeignKey(Cadastro, related_name='enderecos')

        # Outros campos
        # [...]


    >> cadastros = Cadastro.objects.all()
    >> for cadastro in cadastros:
        # Acessando através do related_name
        print cadastro.enderecos.all()


Relacionamentos reversos não são possíveis com o ``select_related``, por isso criou-se a partir da versão 1.4 o método ``prefetch_reĺated``.


prefetch_related
----------------

Ao acessar um **relacionamento reverso** ou atributo **ManyToMany**, assim como vimos para **OneToOne** e **ForeignKey**, uma nova consulta será realizada.

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastros.objects.all()

    >> for cadastro in cadastros:
        print cadastro.enderecos.all()

    >> print len(connection.queries)
    501

Para esses casos, utilizamos o `prefetch_related <https://docs.djangoproject.com/en/1.8/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related>`_, ela tem o comportamento similar ao ``select_related`` como diferença principal que o ``JOIN`` é realizado no ``Python``.

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastros.objects.prefetch_related('enderecos').all()

    >> for cadastro in cadastros:
        print cadastro.enderecos.all()

    >> print len(connection.queries)
    1

Legal, aprendemos a como diminuir o número de consultas que realizamos quando desejamos retirar alguma informação do banco de dados, mas e quando desejamos inserir, atualizar e deletar?

Inserir dados
-------------

Um problema para inserir dados é quando precisamos iterar sobre um conjunto grande de informações e criar um registro para cada linha, usos comum para importações e logs.

.. code-block:: python

    >> from django.db import connection
    >> nomes = [
        'Lucas', 'Teste 01', 'Teste 02', 'Nome 3', # 1000 nomes no total
    ]

    # Inserimos um cadastro para cada nome que existe na nossa variável `nomes`
    >> for nome in nomes:
        Cadastro.objects.create(nome=nome)

    >> print len(connection.queries)
    1000

E acessamos 1000 vezes o banco de dados para criar todos os cadastros.
Existe um método chamado ``bulk_create``, que resolve nosso problema.

.. code-block:: python

    >> from django.db import connection
    >> nomes = [
        'Lucas', 'Teste 01', 'Teste 02', 'Nome 3', # 1000 nomes no total
    ]

    >> cadastros = []
    >> for nome in nomes:
       cadastro = Cadastro(nome=nome)
       cadastros.append(cadastro)

    # Insere todos os cadastros de uma só vez
    >> Cadastro.objects.bulk_create(cadastros)
    >> print len(connection.queries)
    1

O **bulk_create** recebe uma lista de cadastros e cria realizando somente uma query.
É bom notar que cada item dentro da variável ``cadastros`` é uma representação do modelo de Cadastro.

    Não funciona para relacionamentos **ManyToMany** e que os ``signals`` do Django ``pre_save`` e ``post_save`` não serão chamados,
    pois o método ``save`` não é utilizado nesse caso.


Atualizar dados
---------------

Muitas vezes precisamos atualizar um conjunto de dados e fazemos isso através de uma iteração sobre cada objeto e alterando o campo que desejamos.

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastro.objects.all()

    >> for cadastro in cadastros:
        cadastro.notificado = True
        cadastro.save()

    >> print len(connection.queries)
    501 # 1 consulta para retornar os cadastros e 1 para cada item no loop


E cada vez que chamamos o método ``save`` uma nova consulta é realizada.

Para esses casos podemos utilizar o método ``update``.

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastro.objects.all()

    >> cadastros.update(notificado=True)
    500 # Retorna a quantidade de itens que foram atualizados

    >> print len(connection.queries)
    1


O **update** realiza um **SQL Update** no banco de dados e retorna a quantidade de linhas que foram atualizados.

  Os ``signals`` do Django ``pre_save`` e ``post_save`` não serão chamados,
  pois o método ``save`` não é utilizado nesse caso.


Deletar dados
---------------

O mesmo comportamento existe quando estamos removendo alguns dados.
Se fosse preciso apagar todos os dados, seria comum se alguém escrevesse assim:

.. code-block:: python

    >> from django.db import connection

    >> cadastros = Cadastro.objects.all()

    >> for cadastro in cadastros:
        cadastro.delete()

    >> print len(connection.queries)
    501 # 1 consulta para retornar os cadastros e 1 para cada item no loop

Porém, pode-se fazer dessa maneira:

.. code-block:: python

    >> from django.db import connection

    >> Cadastro.objects.all().delete()

    >> print len(connection.queries)
    1

QuerySet possui um método chamado **delete** que apaga todos os dados retornados.

.. code-block:: python

    # Apagar somente inativos
    >> Cadastro.objects.filter(inativo=True).delete()

    # Apagar somente ativos
    >> Cadastro.objects.filter(ativo=True).delete()

Deve-se lembrar, que assim como o **update** e o **bulk_create** os signals do Django não serão chamados, no caso do **delete** os signals são ``pre_delete`` e ``pos_delete``.


Espero que tenha ajudado, até a próxima!
