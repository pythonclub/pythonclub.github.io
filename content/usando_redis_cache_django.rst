Usando Redis para cache e sessão do Django
#############################################

:date: 2014-06-06 15:50
:tags: python, django, redis
:category: Python, Django
:slug: usando-redis-cache-django
:author: Lucas Magnum
:email:  contato@lucasmagnum.com.br
:github: lucasmagnum
:linkedin: lucasmagnum


Nesse post irei explicar como substituir o sistema de cache e sessão do Django para funcionar com o Redis.
Vou explicar como `instalar <#instalacao>`_ e alguns `comandos <#comandos-basicos>`_ do Redis.
Depois como Django trabalha como o `cache`_ e `sessão <#sessao>`_ e logo em seguida vamos aprender a alterar o Django para utilizar o Redis como forma de armazenamento.


Django
------

Utilizarei nesse exemplo versão "1.6.4" do Django.

.. code-block :: bash

  pip install Django==1.6.4


Para instalar e configurar um ambiente para o Django basta seguir um dos tutoriais abaixo:

  - `Regis da Silva - Quem quer aprender Django <http://pythonclub.com.br/principais-duvidas-de-quem-quer-aprender-django.html>`_
  - `Thiago Corôa - Instalação Python e Django <http://pythonclub.com.br/instalacao-python-django-windows.html>`_


Inicie um novo projeto e faça as configurações abaixo.


=======
Cache
=======

O Django vem com um framework de cache que segue a seguinte filosofia:
  - Deve ser o mais rápido possível
  - Deve provê uma interface consistente entre diferentes ``backends``
  - Deve ser extensível o suficiente para atender as necessidades do desenvolvedor


Toda a configuração de cache fica armazenado na variável ``CACHES`` no nosso ``settings.py``.

Utilizarei a biblioteca `django-redis <https://github.com/niwibe/django-redis>`_ como nosso ``backend`` de cache e session.

Vamos instalar o ``django-redis``:

.. code-block :: bash

  pip install django-redis


Agora abra seu arquivo ``settings.py`` e adicione a variável ``CACHES`` com os seguintes valores:

.. code-block :: python

  CACHES = {
      'default': {
          'BACKEND': '',
          'LOCATION': '',
          'OPTIONS': {
              'CLIENT_CLASS': '',
          }
      }
  }

O que significa esses valores??

**BACKEND** : Caminho para a classe que será responsável por realizar adicionar, remover, alterar os dados do cache.

**LOCATION**: Localização do cache para ser utilizado, no nosso caso é o ``IP``:``porta``:``Número do banco de dados``

**CLIENT_CLASS**: Própria do ``django-redis``, serve para determinar qual classe será utilizada como cliente.


Iremos utilizar as classes padrão do ``django-redis`` e sua configuração final ficará assim:

.. code-block :: python

  CACHES = {
      'default': {
          'BACKEND': 'redis_cache.cache.RedisCache',
          'LOCATION': '127.0.0.1:6379:1',
          'OPTIONS': {
              'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
          }
      }
  }


Links úteis:
  - `Django cache framework <https://docs.djangoproject.com/en/dev/topics/cache/>`_
  - `Django cache framework phisolophy <https://docs.djangoproject.com/en/dev/misc/design-philosophies/#cache-design-philosophy>`_
  - `Classes client disponíveis para django-redis <http://niwibe.github.io/django-redis/#_default_client>`_

=======
Sessões
=======

Para ativar a funcionalidade de sessão, é preciso editar a variável ``MIDDLEWARE_CLASSES`` no arquivo ``settings.py``.
Basta adicionar ``django.contrib.sessions.middleware.SessionMiddleware`` dentro da listagem.

`settings.py`

.. code-block :: python

  MIDDLEWARE_CLASSES = [
    # [...] outros middlewares
    'django.contrib.sessions.middleware.SessionMiddleware'
  ]


Por padrão a sessão já vem ativada.


Vamos utilizar uma sessão baseada no cache, como já foi instalado o ``django-redis`` só é adicionar as seguintes linhas no arquivo `settings.py`

.. code-block :: python

  SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
  SESSION_CACHE_ALIAS = 'default'


**SESSION_CACHE_ALIAS** se refere a chave que configuramos no cache, se configurássemos mais que um cache, poderíamos informar outro valor.


Links úteis:
  - `How to use sessions <https://docs.djangoproject.com/en/dev/topics/http/sessions/>`_

Redis
------

Redis é um armazenador de dados no formato "key-value" ou "chave-valor".
O acrônimo Redis significa "REmote DIctionary Server".
Os dados são armazenados por padrão são em memória.

=================
Instalação
=================

Acesse o `tutorial oficial <http://redis.io/download>`_ de instalação do Redis, baixe a versão mais nova e siga os passos descritos para finalizar a instalação.

=================
Comandos básicos
=================

Quando o Redis é instalado, ele cria um atalho para seu cliente chamado ``redis-cli`` e com ele podemos executar os comandos abaixo:

Primeiro abra o cliente:

.. code-block :: bash

    >> redis-cli

Com o cliente aberto podemos escolher qual ``database`` queremos trabalhar, utilizando o comando ``select``.
Basta informar qual o índice da base que queremos utilizar.

.. code-block:: bash

  127.0.0.1:6379 > select 1

Nesse caso selecionamos a base de índice 1 para realizar as consultas.

Se quisermos consultar todas as ``keys`` que estão armazenadas, basta utilizarmos o comando ``keys`` com um parâmetro "*".

.. code-block:: bash

  127.0.0.1:6379[1] > keys *

Se nossas ``keys`` fossem nomeadas com o prefixo "cache" ou "session", poderíamos consultá-las assim:

.. code-block :: bash

  127.0.0.1:6379[1] > keys cache:*
  127.0.0.1:6379[1] > keys session:*


Existe também a `lista completa de comandos <http://redis.io/commands>`_.


Como testar
-----------

Vá até a pasta do nosso projeto e execute o `syncdb` para sincronizar a base de dados.

.. code-block :: bash

  python manage.py syncdb


Inicie também o servidor de desenvolvimento do Django.

.. code-block :: bash

  python manage.py runserver

Abra seu navegador e entre na página de administração do Django `localhost:8000/admin <http://localhost:8000/admin>`_.

Faça seu login para que seja gravado um registro de sessão na base.

Para visualizar se o registro foi gravado com sucesso, execute os seguintes comandos:

.. code-block :: bash

  >> redis-cli

  127.0.0.1:6379> select 1
  127.0.0.1:6379[1]> keys *

  1) ":1:django.contrib.sessions.cachemnpnqzfl03iwugb99q9ls4w0k2r74gs2"


Se tudo ocorreu como planejado, nesse momento temos as sessões e o cache sendo armazenados no Redis.


Espero que tenha gostado, até o próximo!