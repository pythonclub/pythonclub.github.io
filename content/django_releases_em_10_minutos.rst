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


Versão 1.4 (Há 3 anos)
----------------------

Lançada em Março de 2012, suporta Python 2.5 >= 2.7.

É a primeira versão a permitir o uso de `custom project template <https://docs.djangoproject.com/en/1.4/ref/django-admin/#django-admin-startproject>`_ e tornar o arquivo `manage.py` *o* que conhecemos hoje.

Foi a primeira versão a suportar o `testes <https://docs.djangoproject.com/en/1.4/topics/testing/#django.test.LiveServerTestCase>`_ feitos com frameworks que utilizam o browser como o `Selenium <http://pythonclub.com.br/selenium-parte-1.html>`_.


Algumas outras coisas legais foram:

    * `bulk_create <https://docs.djangoproject.com/en/1.4/ref/models/querysets/#django.db.models.query.QuerySet.bulk_create>`_ para criar vários objetos de uma só vez.
    * `prefetch_related <https://docs.djangoproject.com/en/1.4/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related>`_ para realizar `joins` em tabelas que possuem relações `many-to-many`.
    * `reverse_lazy <https://docs.djangoproject.com/en/1.4/topics/http/urls/#reverse-lazy>`_ que permite fazer `reverse` antes das configurações de URL serem carregadas.


Versão 1.5 (Há 2 anos)
----------------------

Lançada em Fevereiro de 2013, suporta Python 2.6.5 >= 2.7 (Python 3 - Experimental).

A versão 1.5 ficou bem conhecida pela reformulação na aplicação de autenticação, é possível `customizar um usuário <https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#auth-custom-user>`_ conforme nossas necessidades.

É possivel também passar os campos que você `gostaria de atualizar <https://docs.djangoproject.com/en/1.5/ref/models/instances/#specifying-which-fields-to-save>`_ quando for salvar um objeto.

Algumas outras coisas legais foram:

    * `verbatim <https://docs.djangoproject.com/en/1.5/ref/templates/builtins/#std:templatetag-verbatim>`_ template tag para casos onde você deseja ignorar a sintaxe do template.
    * `novos tutoriais <https://docs.djangoproject.com/en/1.5/releases/1.5/#new-tutorials>`_ foram inseridos para ajudar iniciantes e existe também uma seção `Tutoriais Avançados`


Versão 1.6 (Há 1 ano e meio)
----------------------------

Lançada em Novembro de 2013, suporta Python 2.6.5 >= 3.3. (Python 3!!!!)


A versão 1.6 alterou um pouco do `layout` padrão dos projetos que estávamos acostumados, para nossa alegria o `admin.py` é adicionado por padrão na aplicação :)

Transações possuem `autocommit` habilitado por padrão!

Os testes são localizados em qualquer arquivo que possua o nome começando com **test_** (Antigamente os testes só eram encontrados nos arquivos models.py e tests.py)

Algumas outras coisas legais foram:

    * `check <https://docs.djangoproject.com/en/1.6/ref/django-admin/#django-admin-check>`_ comando para validar se suas configurações estão compatíveis com a versão do django.


Versão 1.7 (Há 8 meses)
-----------------------

Lançada em Setembro de 2014, suporta Python 2.7 >= 3.4.

Um novo conceito de `migrações <https://docs.djangoproject.com/en/1.7/topics/migrations/>`_ foi implementado, até o momento a maioria utilizava o `South <https://south.readthedocs.org/en/latest/>`_, nessa versão tudo é `built-in`.

Para criar uma aplicação não é necessário mais conter o arquivo `models.py`.

O `conceito de aplicação <https://docs.djangoproject.com/en/1.7/ref/applications/>` foi atualizado e existem vários novas maneiras de se customizar seus dados :)

O comando `check` foi evoluído e agora realiza uma varredura quase completa no seu código para identificar possíveis problemas.


Versão 1.8
----------

Lançada em Abril de 2015, a versão 1.8 introduz várias features legais!

Possibilidade de utilizar `várias engines <https://docs.djangoproject.com/en/1.8/topics/templates/>`_ de templates.

Novos campos foram introduzidos como `UUIDField <https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.UUIDField>`_ e `DurationField <https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.DurationField>`_ e  ainda tem mais!


Acompanhe as `releases <https://docs.djangoproject.com/en/1.8/releases/>`_.
