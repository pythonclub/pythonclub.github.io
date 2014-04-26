5 Django Apps que não vivo sem
##############################

:date: 2014-05-05 18:00
:tags: django, django-apps, south
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

	./manage.py schemamigration app_name --initial	[cria a estrutura de migracao inicial]
	./manage.py migration app_name			[realiza migracao na app especificada]
	./manage.py migration --all			[realiza migracao em todas as apps instaladas]
	./manage.py schemamigration app_name --auto	[realiza migracao no modelo alterado]