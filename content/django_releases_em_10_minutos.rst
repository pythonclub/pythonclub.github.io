Django - 3 anos em 10 minutos
#############################################

:date: 2015-04-06 11:55
:tags: python, django
:category: Python
:slug: django-overview-10-minutos
:author: Lucas Magnum
:email:  lucasmagnumlopes@gmail.com
:github: lucasmagnum
:linkedin: lucasmagnum


Em março de 2012 foi lançada a versão 1.4 e por aqui que nossa jornada começa, o objetivo não é entrar em detalhes em todas as features que foram implementadas e sim um `overview` sobre as que considero mais importantes para nosso dia a dia.


Versão `1.4 <https://docs.djangoproject.com/en/1.4/releases/1.4/>`_ (Há 3 anos)
--------------------------------------------------------------------------------

Lançada em Março de 2012, suporta Python 2.5 >= 2.7.

Foi a primeira versão LTS (long-term support), ou seja, ela recebeu correções e atualizações de segurança por pelo menos 3 anos após à data de lançamento.

É a primeira versão a permitir o uso de `custom project template <https://docs.djangoproject.com/en/1.4/ref/django-admin/#django-admin-startproject>`_ e tornar o arquivo `manage.py` *o* que conhecemos hoje.

Foi a primeira versão a suportar o `testes <https://docs.djangoproject.com/en/1.4/topics/testing/#django.test.LiveServerTestCase>`_ feitos com frameworks que utilizam o browser como o `Selenium <http://pythonclub.com.br/selenium-parte-1.html>`_.


Algumas outras coisas legais foram:

    * `bulk_create <https://docs.djangoproject.com/en/1.4/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create>`_ para criar vários objetos de uma só vez.
    * `prefetch_related <https://docs.djangoproject.com/en/1.4/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related>`_ para realizar `joins` em tabelas que possuem relações `many-to-many`.
    * `reverse_lazy <https://docs.djangoproject.com/en/1.4/topics/http/urls/#reverse-lazy>`_ que permite fazer `reverse` antes das configurações de URL serem carregadas.


Versão `1.5 <https://docs.djangoproject.com/en/1.5/releases/1.5/>`_ (Há 2 anos)
--------------------------------------------------------------------------------

Lançada em Fevereiro de 2013, suporta Python 2.6.5 >= 2.7 (Python 3 - Experimental).

A versão 1.5 ficou bem conhecida pela reformulação na aplicação de autenticação, é possível `customizar um usuário <https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#auth-custom-user>`_ conforme nossas necessidades.

É possivel também passar os campos que você `gostaria de atualizar <https://docs.djangoproject.com/en/1.5/ref/models/instances/#specifying-which-fields-to-save>`_ quando for salvar um objeto.

Algumas outras coisas legais foram:

    * `verbatim <https://docs.djangoproject.com/en/1.5/ref/templates/builtins/#std:templatetag-verbatim>`_ template tag para casos onde você deseja ignorar a sintaxe do template.
    * `novos tutoriais <https://docs.djangoproject.com/en/1.5/releases/1.5/#new-tutorials>`_ foram inseridos para ajudar iniciantes e existe também uma seção `Tutoriais Avançados`


Versão `1.6 <https://docs.djangoproject.com/en/1.6/releases/1.6/>`_ (Há 1 ano e meio)
--------------------------------------------------------------------------------------

Lançada em Novembro de 2013, suporta Python 2.6.5 >= 3.3. (Python 3!!!!)


A versão 1.6 alterou um pouco do `layout` padrão dos projetos que estávamos acostumados, para nossa alegria o `admin.py` é adicionado por padrão na aplicação :)

Transações possuem `autocommit` habilitado por padrão!

Os testes são localizados em qualquer arquivo que possua o nome começando com **test_** (Antigamente os testes só eram encontrados nos arquivos models.py e tests.py)

Algumas outras coisas legais foram:

    * `check <https://docs.djangoproject.com/en/1.6/ref/django-admin/#django-admin-check>`_ comando para validar se suas configurações estão compatíveis com a versão do django.


Versão `1.7 <https://docs.djangoproject.com/en/1.7/releases/1.7/>`_ (Há 8 meses)
---------------------------------------------------------------------------------

Lançada em Setembro de 2014, suporta Python 2.7 >= 3.4.

Um novo conceito de `migrações <https://docs.djangoproject.com/en/1.7/topics/migrations/>`_ foi implementado, até o momento a maioria utilizava o `South <https://south.readthedocs.org/en/latest/>`_, nessa versão tudo é `built-in`.

Para criar uma aplicação não é necessário mais conter o arquivo `models.py`.

O `conceito de aplicação <https://docs.djangoproject.com/en/1.7/ref/applications/>`_ foi atualizado e existem vários novas maneiras de se customizar seus dados :)

O comando `check` foi evoluído e agora realiza uma varredura quase completa no seu código para identificar possíveis problemas.


Versão `1.8 <https://docs.djangoproject.com/en/1.8/releases/1.8/>`_
--------------------------------------------------------------------

Lançada em Abril de 2015, a versão 1.8 introduz várias features legais!

É a segunda versão LTS (long-term support), ou seja, vai receber correções e atualizações de segurança por pelo menos 3 anos após à data de lançamento.

Agora há a possibilidade de utilizar `várias linguagens(engines) <https://docs.djangoproject.com/en/1.8/topics/templates/>`_ de templates, ou seja, você pode usar simuntaneamente (não no mesmo arquivo) a `Django Template Language <https://docs.djangoproject.com/en/1.8/ref/templates/language/>`_ ou `Jinja2 <http://jinja.pocoo.org/>`_. Há uma API padronizada para quem quiser adicionar suporte para outras linguagens de template no futuro. Há um `guia de migração <https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/>`_ .

Novos campos foram introduzidos como `UUIDField <https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.UUIDField>`_ e `DurationField <https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.DurationField>`_ e  ainda tem mais!

O `Model._meta API <https://docs.djangoproject.com/en/1.8/releases/1.8/#model-meta-api>`_ foi totalmente refatorado e padronizado. O `Model._meta` API foi incluida no Django 0.96 e serve para obter informações sobre campos do Model, contudo, essa api era considerada de uso privado, e não tinha qualquer documentação ou comentários. Agora com tudo padronizado, abre uma gama de novas opções para criar apps plugaveis que fazem coisas com Models arbitrarios.

Algumas outras coisas legais foram:

    * O comando de gerenciamento `inspectdb <https://docs.djangoproject.com/en/1.8/howto/legacy-databases/#integrating-django-with-a-legacy-database>`_ agora suporta fazer engenharia reversa tambem de Database Views (nas versões anteriores, o inspectdb inspecionava somente tabelas, mas não conseguia "ver" as views).
    * Adição/Melhoria de `Query Expressions, Conditional Expressions, and Database Functions <https://docs.djangoproject.com/en/1.8/releases/1.8/#query-expressions-conditional-expressions-and-database-functions>`_ . Isso adiciona muito mais flexibilidade para fazer pesquisas mais complexas no banco de dados.



Há várias outras ótimas melhorias que omiti, veja o `release note <https://docs.djangoproject.com/en/1.8/releases/>`_ completo.

O Futuro
----------

Versão 1.9 (Com lançamento previsto para Outubro de 2016)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

O Django 1.8 mal foi lançado, e já há algumas novidades que talvez venham no Django 1.9.

Muito provavelmete, o Django 1.9 vai adicionar os tão esperados `Campos Compostos <https://github.com/django/deps/pull/12>`_ . Isso vai permitir fazer coisas mais complexas, como ter um campo Dinheiro, que "sabe" como fazer conversões de moeda (ex. Real para Dolar).

Tambem existe uma expectativa que o tema `django-flat-admin <https://pypi.python.org/pypi/django-flat-theme>`_ para o `Admin <https://docs.djangoproject.com/en/1.8/ref/contrib/admin/>`_ seja integrado no Django 1.9, virando o tema padrão. O `django-flat-admin <https://pypi.python.org/pypi/django-flat-theme>`_ somente modifica o CSS, nenhuma tag HTML é alterada em relação ao HTML original do Admin, então ele é relativemente compativel (desde que você não tenha incluido customizações no CSS do Admin). Os core developers do Django estão tratando desse assunto `neste tópico <https://groups.google.com/forum/#!msg/django-developers/HJAikaEBqJ4/pxj1SuwbJm0J>`_


Veja o `Roadmap <https://code.djangoproject.com/wiki/Version1.9Roadmap>`_ do que vem por ai no Django 1.9

