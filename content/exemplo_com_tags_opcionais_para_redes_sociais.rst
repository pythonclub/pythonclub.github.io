Exemplo de Publicação 2 (em RST) com tags opcionais para redes sociais
##############################

:date: 2014-04-01 17:21
:tags: exemplo
:category: Geral
:slug: exemplo-de-publicacao-em-rst-com-tags-opcionais-para-redes-sociais
:author: Fábio Caritas Barrionuevo da Luz
:email:  bnafta@gmail.com
:github: seu_usuario_do_github
:bitbucket: seu_usuario_do_bitbucket
:site: endereço_completo_de_seu_site_ou_blog
:twitter: seu_usuario_do_twitter
:facebook: seu_usuario_do_facebook
:linkedin: seu_usuario_do_linkedin
:gittip: seu_usuario_do_gittip



===================
MODIFICADO O TITULO
===================

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
