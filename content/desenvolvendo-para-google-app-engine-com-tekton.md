Title: Criação de aplicações no Google App Engine com o Tekton
Slug: desenvolvendo-para-google-app-engine-com-tekton
Date: 24-05-2015
Tags: tekton, python, google app engine, tutorial
Author: Guido Luz Percú
Email:  guidopercu@gmail.com
Github: GuidoBR
Site: http://www.guidopercu.com.br/
Twitter: oumguido
Category: google app engine

## Google App Engine (GAE)
É a plataforma de Cloud Computing do Google, com ela você pode desenvolver e hospedar aplicações usando Python (2.7) que escalam facilmente, [pagando muito pouco por isso].

As desvantagens (em relação a outras plataformas de nuvem, como o Heroku por exemplo) são:
- Você terá que desenvolver pensando na plataforma (banco de dados NoSQL, por isso o [Django não é recomendável].).
- Versão do Python é antiga e não há planos para mudar isso no momento.

## Tekton
É um framework para desenvolvimento Web especialmente pensado para uso no Google App Engine. Nele podemos aproveitar o melhor do Django (scaffold, código HTML e validação de formulários a partir de modelos, apps isoladas) sem perder as vantagens que o GAE nos oferece.  

 ## Como iniciar
 O primeiro passo é baixar  o [SDK do Google App Engine], com isso pronto podemos começar a conhecer o Tekton:

```
$ wget https://github.com/renzon/tekton/archive/master.zip
$ unzip master
$ mv master projeto_appengine && cd projeto_appengine     
```
Nesse ponto podemos explorar e conhecer a estrutura de diretórios.
```
└── backend
 ├── appengine
 ├── apps
 ├── build_scripts
 ├── test
 └── venv
```

```
$ cd backend/venv/ && ./venv.sh
$ source ./bin/activate         
```
Com o ambiente virtual pronto, tudo deve estar funcionando. Para testar, 
vamos utilizar o próprio servidor que vem com o pacote antes de subir parao GAE.

``` 
cd ../appengine && dev_appserver.py . 
```

Tudo certo! Você deve estar vendo o projeto template no seu localhost:8080

Para realizar o deploy no App Engine:

```         
appcfg.py update . --oauth2
```                 
Você pode conhecer mais sobre o projeto no [Github], no [grupo de discussões] ou nas vídeo aulas gratuitas no [Youtube].
[SDK do Google App Engine]:https://cloud.google.com/appengine/downloads 
[pagando muito pouco por isso]:https://cloud.google.com/appengine/pricing
[Django não é recomendável]:http://imasters.com.br/desenvolvimento/app-engine-e-django-hell/
[Youtube]:https://www.youtube.com/playlist?list=PLA05yVJtRWYRGIeBxag8uT-3ftcMVT5oF
[Github]:https://github.com/renzon/tekton
[grupo de discussões]:https://groups.google.com/forum/#!forum/tekton-web
