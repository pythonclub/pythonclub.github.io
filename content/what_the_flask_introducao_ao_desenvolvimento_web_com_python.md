Title: What the Flask? Pt-1 Introdução ao desenvolvimento web com Python
Date: 2014-05-31 17:21
Tags: flask, web
Category: web, flask
Slug: what_the_flask_introducao_ao_desenvolvimento_web_com_python
Author: Bruno Cezar Rocha
Email:  rochacbruno@gmail.com
Github: rochacbruno
Bitbucket: rochacbruno
Site: http://brunorocha.org
Twitter: rochacbruno
Linkedin: rochacbruno
Gittip: rochacbruno



What The Flask - 1/6
-----------

### 6 passos para ser um Flask ninja!

Nesta série de 6 artigos/tutoriais pretendo abordar de maneira bem detalhada
o desenvolvimento web com o framework Flask.

Depois de + de um ano desenvolvendo projetos profissionais com o Flask e
adquirindo experiência também no desenvolvimento do projeto open source
[Quokka CMS](http://quokkaproject.org) resolvi compartilhar algumas dicas
para facilitar a vida de quem pretende começar a desenvolver para web com Python.

A série **W**hat **T**he **F**lask será dividida nos seguintes capítulos.

1. [**Hello Flask**](/what_the_flask_introducao_ao_desenvolvimento_web_com_python.html): Introdução ao desenvolvimento web com Flask  - **<-- Você está aqui**
2. **Flask patterns**: boas práticas na estrutura de aplicações Flask
3. **Plug & Use**: extensões essenciais para iniciar seu projeto
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.


### O que é Flask?

![Flask logo](http://flask.pocoo.org/static/logo.png)

Flask é um micro-framework (um framework minimalista) desenvolvido em Python
e baseado em 3 coisas:

- [WerkZeug](http://werkzeug.pocoo.org/) é uma biblioteca para desenvolvimento de apps [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) que é a especificação universal de como deve ser a interface entre um app Python e um web server. Ela possui a implementação básica deste padrão para interceptar requests e lidar com response, controle de cache, cookies, status HTTP, roteamento de urls e também conta com uma poderosa ferramanta de debug. Além disso o werkzeug possui um conjunto de **utils** que acabam sendo uma mão na roda mesmo em projetos que não são para a web.

- [Jinja2](http://jinja.pocoo.org/) é um template engine escrito em Python, você escreve templates utilizando marcações como ``{{ nome_da_variavel }}`` ou ``{% for item in lista %} Hello!! {% endfor %}`` e o Jinja se encarrega de renderizar este template, ou seja, ele substitui os placeholders pelo valor de suas variáveis.
O Jinja2 já vem com a implementação da maioria das coisas necessárias na construção de templates html e além disso é muito fácil de ser customizado com template filters, macros etc.

- [Good Intentions](https://trinket.io/python/fdedd0fb94): O Flask é **Pythonico**! além do código ter alta qualidade nos quesitos de legibilidade ele também tenta seguir as premissas do [Zen do Python](https://trinket.io/python/fdedd0fb94) e dentro dessas boas intenções nós temos o fato dele ser um [**micro-framework**](http://flask.pocoo.org/docs/foreword/#what-does-micro-mean) deixando que você tenha liberdade de estruturar seu app da maneira que desejar. Tem os [padrões de projeto e extensões](http://flask.pocoo.org/docs/patterns/) que te dão a certeza de que seu app poderá crescer sem problemas. Tem os sensacionais [Blueprints](http://flask.pocoo.org/docs/blueprints/) para que você reaproveite os módulos que desenvolver. Tem o controverso uso de [Thread Locals](http://flask.pocoo.org/docs/advanced_foreword/#thread-locals-in-flask) para facilitar a vida dos desenvolvedores.


> Em resumo: o Flask não fica no seu caminho deixando você seguir o seu caminho no desenvolvimento de seu app, você pode começar pequeno com um site feito em um único arquivo e ir crescendo aos poucos até ter seus módulos estruturados de uma maneira que permita a escalabilidade e o trabalho em equipe.

Além disso, não posso deixar de mencionar a comunidade que é bastante ativa e compartilha muitos projetos de extensões open-source como o Flask Admin, Flask-Cache, Flask-Google-Maps, Flask-Mongoengine, Flask-SQLAlchemy, Flask-Login, Flask-Mail etc....

### Por onde começar?

Obviamente que para seguir neste tutorial será necessário utilizar Python, não entrarei em detalhes sobre a instalação do Python neste artigo, mas com certeza aqui no PythonClub devem ter artigos explicando detalhadamente a instalação do Python e configuração de uma virtual-env, então vamos aos requirements.

#### Você vai precisar de:

- Python 2.7 (não usaremos Python3 ainda, pois ainda tem extensões que não migraram)
- Ipython - Um terminal interativo (REPL) com superpoderes
- virtualenv e virtualenv wrapper - para criação de ambientes isolados
- Um editor de código ou IDE de sua preferência - (Gedit, Notepad++, sublime, Emacs, VIM etc..)
- Um browser de verdade - espero que você não esteja usando o I.E :P


#### Ambiente

Inicie criando uma pasta para o projeto no local de sua preferencia

(se preferir pode fazer via File Browser ou IDE)

    :::bash

    mkdir wtf
    touch wtf/__init__.py
    touch wtf/app.py
    cd wtf


Agora crie uma [virtualenv](http://virtualenv.readthedocs.org/en/latest/) para o projeto

Usando virtualenvwrapper **recommended**


    :::bash
    sudo apt-get install virtualenvwrapper
    mkvirtualenv wtf

Ou usando apenas virtualenv


    :::bash
    sudo apt-get install python-virtualenv
    virtualenv wtf_env
    source wtf_env/bin/activate

Com uma das opções acima o seu console agora deverá exibir algo como:

    :::bash

    (wtf)seuuser@suamaquina/path/to/wtf$

Instale o Flask e o Ipython

    :::bash
    pip install flask
    pip install ipython

### Hello world

Agora que o ambiente está pronto abra o arquivo ```app.py``` em seu editor favorito e vamos fazer o **Hello World** para começarmos bem o tutorial.

    :::python

    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello World! <strong>I am learning Flask</strong>", 200

    app.run()

Agora salve o arquivo e vá para o terminal e execute:

    :::bash

    (wtf)seuuser@suamaquina/path/to/wtf$ python app.py

Abra o seu browser de verdade na url [http://localhost:5000](http://localhost:5000) e você verá:

> Hello World! **I am learning Flask**


## Congratulations for your fantastic achievement!

> Se tudo ocorreu bem até aqui então parabéns! você passou para o level 1.2 e já pode se considerar um **programador flask nível baby** :)

Antes de continuar para o level 1.2 vamos entender detalhadamente o que aconteceu nas 6 linhas de código que escrevemos no ```app.py```:


