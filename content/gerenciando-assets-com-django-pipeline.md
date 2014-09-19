Title: Gerenciando assets com django-pipeline
Date: 2014-09-18 19:00
Tags: Django, django-pipeline, assets, static
Category: django-apps
Slug: gerenciando-assets-com-django-pipeline
Author: Raphael Passini
Email: raphapassini@gmail.com



Gerenciando Assets Com django-pipeline
======================================

O objetivo desse post é explicar a utilização do aplicativo django-pipeline para gerenciar a compilação e compressão de arquivos CoffeScript, Less, Sass, entre outros.

Instalando
----------

Primeiro vamos instalar o pacote django-pipeline

```python
pip install django-pipeline
```

Depois vamos alterar o nosso arquivo settings.py e adicionar o pipeline ao INSTALLED_APPS

```
INSTALLED_APPS = (
    'pipeline',
)
```

Configurando os seus assets

Como funciona a configuração dos arquivos no django-pipeline, primeiro vamos criar um grupo de arquivos estáticos, por exemplo, “main”:

```python
PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'less/main.less',
            'less/extra.less',
        ),
        'output_filename': 'css/main.css',
    }
}

PIPELINE_JS = {
    'vendor': {
        'source_filenames': (
            'js/vendor/jquery.min.js',
            'js/vendor/handlebars.min.js',
        ),
        'output_filename': 'js/vendor.min.js',
    }
}
```

Os arquivos listados dentro de “source_filenames” serão compilados para o arquivo “output_filename” quando executarmos o python manage.py collectstatic Nós podemos criar quantos grupos forem necessários para nosso projeto.

Utilizando nos templates

Para incluirmos os arquivos configurados no passo anterior no nosso template é bem simples:

```python
{% load compressed %}
{% compressed_css 'main' %}
{% compressed_js 'vendor' %}
```

Colocando em produção

Para deixar o ambiente pronto para produção vamos definir um dos storages disponíveis no pipeline. Você pode ver as opções de storage disponíveis na documentação do django-pipeline. Você pode ler mais sobre os storage systems customizados aqui

```python
STATICFILES_FINDERS = (
    'pipeline.finders.PipelineFinder',
)
# PIPELINE RELATIVE CONFIG
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
```

Pronto, feito isso podemos colocar nosso projeto em produção, quando rodarmos o collectstatic os arquivos enviados para o nosso STATIC_ROOT já estarão automaticamente compilados e minificados!

Os códigos utilizados aqui podem ser obtidos no github desse tutorial: https://github.com/raphapassini/pipeline_tutorial

Achou legal? Discorda de alguma coisa? Quer acrescentar algo? Deixa seu comentário ai embaixo!