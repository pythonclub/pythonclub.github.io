5 Django Apps que não vivo sem
##############################

:date: 2014-05-05 18:00
:tags: django, django-apps, south, test, nose, coverage
:category: Geral
:slug: 5-django-apps-que-nao-vivo-se
:author: Igor Santos
:email:  igr.exe@gmail.com
:summary: 5 Django Apps que não vivo sem


=====================
1. South (Migrations)
=====================

O `South <http://south.readthedocs.org/en/latest/>`_, faz com que o Django suporte migrações de banco de dados de forma simples, estável e totalmente independente do backend de banco de dados utilizado, a partir da alteração dos models, você roda um comando e plin a "mágica" acontece, o base de dados está novamente igual aos seus modelos.

Essa app se tornou tão popular que na versão `Django 1.7 <https://docs.djangoproject.com/en/dev/topics/migrations/>`_ passou a ser nativo do Django.

Para versão Django anterior 1.7, também é muito simples utilizar o South basta instala-lo, e adicionar no *INSTALLED_APPS*.

.. code-block:: bash

    pip install south

Comandos utilizados:

.. code-block:: bash

    ./manage.py schemamigration app_name --initial  [cria a estrutura de migracao inicial]
    ./manage.py migration app_name          [realiza migracao na app especificada]
    ./manage.py migration --all         [realiza migracao em todas as apps instaladas]
    ./manage.py schemamigration app_name --auto [realiza migracao no modelo alterado]


================================
2. django-nose + coverage (Test)
================================

O `django-nose <https://github.com/django-nose/django-nose>`_ é uma django app que utiliza o `nose <https://nose.readthedocs.org/en/latest/>`_ como TestRunner do Django, isso possibilita você adicionar qualquer plugin compatível com o Nose, além de outras muitas vantagens, que na verdade não conheço a fundo.

Um plugin do Nose que achei muito bacana é o `coverage <http://django-testing-docs.readthedocs.org/en/latest/coverage.html>`_, ele informa a cobertura de testes em seu código, basicamente ele realiza uma analise linha a linha, e verifica se seus testes unitários passaram por essas linhas, e no final ele apresenta um relatório com a quantidade de código testado.

Testei ele até a versão Django 1.6 e funcionou muito bem, é muito simples de instalar e configurar.

.. code-block:: bash
    
    pip install django-nose
    pip install coverage

Configurando o settings do projeto.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'django_nose',
    )

    # diz ao Django que o TestRunner sera o Nose
    TEST_RUNNER = 'django_nose.NoseTestSuitRunner'

    # alguns parametros que serao passados default ao nose
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=foo,bar', # informa os pacotes que ele que verifica a cobertura de tests
    ]

**Dica:** O recomendado é que essa configuração fique em um settings especifico para test, eu costumo separar meu settings em 4 arquivos diferentes, [common, prod, dev, test].

O coverage mostra a seguinte tabela:

.. code-block:: bash

    Name               Stmts   Miss  Cover   Missing
    ------------------------------------------------
    foo.models            30      5    85%   10-12, 16, 19
    bar.models            10      1    90%   4
    ------------------------------------------------
    TOTAL                 40      6    87%

- Stmts: Linhas que precisam ser testadas.
- Miss: Linhas que não foram testadas.
- Cover: Quantidade de código coberto por testes em porcentagem.
- Missing: Linhas que não foram testadas.


=====================
3. model_mommy (Mock)
=====================

`model_mommy <https://github.com/vandersonmota/model_mommy>`_ oferece um jeito fácil e inteligente de criar fixtures para Django, é muito simples, e tem o objetivo de facilitar a escrita de testes, fazendo com que você consiga criar um objeto com apenas uma linha de código.

Esse é um simples exemplo, com coisas mais comuns no seu dia,

.. code-block:: python

    from model_mommy import mommy

    class MyCaseTest(TestCase):
        def setUp(self):
            # criar e persiste o User na database
            self.user = mommy.make('auth.User')
            # cria o User sem persistir
            self.user = mommy.prepare('auth.User')
            # cria o User, atribui um username e persiste
            self.user = mommy.make('auth.User', username=u'user.test')
            # cria e persiste uma lista de User
            self.list_users = mommy.make('auth.User', _quantity=3)

**Note:** não foi preciso importar o model User, pois o model_mommy faz isso pra você, mas tome cuidado, o model_mommy é case sensitive.

**Dica:** seguindo a mesma dica do django-nose, adicione o model_mock ao INSTALLED_APPS de uma settings especifica para testes, ou para desenvolvimento.

Essa é uma django app muito poderosa e possui diversas outras funcionalidades, vale a pena fazer uma visitinha no `seu repositório <https://github.com/vandersonmota/model_mommy>`_.


=================================
4. Django Extensions (Extensions)
=================================

O `django extensions <http://django-extensions.readthedocs.org/en/latest/index.html>`_ possui uma `lista considerável <http://django-extensions.readthedocs.org/en/latest/command_extensions.html>`_ de funcionalidades, a ideia é juntar diversas funcionalidades que agilizam o desenvolvimento, e adicioná-los a lista de comandos do **manage.py**.

Mas quero falar de uma funcionalidade especifica que uso muito, é o `shell_plus <http://django-extensions.readthedocs.org/en/latest/shell_plus.html>`_, que carrega automaticamente models das apps instaladas no meu projeto, no shell interativo do python, além disso você possui diversas configurações bacanas, como escolher tipos diferentes de shell python, como por exemplo `ipython <https://github.com/ipython/ipython>`_.

.. code-block:: shell

    ./manage.py shell_plus --use-ipython