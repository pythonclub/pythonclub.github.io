Exemplo de Publicação (em RST)
##############################

:date: 2014-04-24 17:21
:tags: exemplo
:category: Geral
:slug: exemplo-de-publicacao-em-rst
:author: André Luiz
:email:  contato@xdvl.info

===========
Lorem Ipsum
===========

Sub-titulo
----------

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lista
-----

* Lorem ipsum
* dolor sit amet
* consectetur adipisicing elit
* sed do eiusmod

Imagem
------

.. image:: images/python-logo-master-v3-TM.png
   :alt: python logo

Syntax Highlight
----------------

.. code-block:: python

    from django.views.generic import TemplateView

    from braces.views import LoginRequiredMixin


    class IndexView(LoginRequiredMixin, TemplateView):
        template_name = 'core/index.html'
