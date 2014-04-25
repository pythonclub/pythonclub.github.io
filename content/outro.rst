Mais um exemplo de Publicação
#############################

:date: 2014-04-25 12:21
:tags: exemplo
:category: Geral
:slug: exemplo-de-publicacao
:author: Fábio C. Barrionuevo da Luz
:summary: Exemplo de Publicação

===========
Lorem Ipsum
===========

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse




.. code-block:: python

    from django.views.generic import TemplateView

    from braces.views import LoginRequiredMixin


    class IndexView(LoginRequiredMixin, TemplateView):
        template_name = 'core/index.html'
