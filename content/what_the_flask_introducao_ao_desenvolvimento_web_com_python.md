Title: What the Flask? Pt-1 Introdução ao desenvolvimento web com Python
Slug: what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python
Date: 2014-05-31 17:21
Tags: flask,web,tutorial,what-the-flask
Author: Bruno Cezar Rocha
Email:  rochacbruno@gmail.com
Github: rochacbruno
Bitbucket: rochacbruno
Site: http://brunorocha.org
Twitter: rochacbruno
Linkedin: rochacbruno
Gittip: rochacbruno
Category: Flask



What The Flask - 1/6
-----------

### 6 passos para ser um Flask ninja!

Nesta série de 6 artigos/tutoriais pretendo abordar de maneira bem detalhada
o desenvolvimento web com o framework Flask.

Depois de mais de um ano desenvolvendo projetos profissionais com o Flask e
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
e baseado em 3 pilares:

- [WerkZeug](http://werkzeug.pocoo.org/) é uma biblioteca para desenvolvimento de apps [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) que é a especificação universal de como deve ser a interface entre um app Python e um web server. Ela possui a implementação básica deste padrão para interceptar requests e lidar com response, controle de cache, cookies, status HTTP, roteamento de urls e também conta com uma poderosa ferramanta de debug. Além disso o werkzeug possui um conjunto de **utils** que acabam sendo uma mão na roda mesmo em projetos que não são para a web.

- [Jinja2](http://jinja.pocoo.org/) é um template engine escrito em Python, você escreve templates utilizando marcações como ``{{ nome_da_variavel }}`` ou ``{% for nome in lista_de_nomes %} Hello {{nome}}!! {% endfor %}`` e o Jinja se encarrega de renderizar este template, ou seja, ele substitui os placeholders pelo valor de suas variáveis.
O Jinja2 já vem com a implementação da maioria das coisas necessárias na construção de templates html e além disso é muito fácil de ser customizado com template filters, macros etc.

- [Good Intentions](https://trinket.io/python/fdedd0fb94): O Flask é **Pythonico**! além do código ter alta qualidade nos quesitos de legibilidade ele também tenta seguir as premissas do [Zen do Python](https://trinket.io/python/fdedd0fb94) e dentro dessas boas intenções nós temos o fato dele ser um [**micro-framework**](http://flask.pocoo.org/docs/foreword/#what-does-micro-mean) deixando que você tenha liberdade de estruturar seu app da maneira que desejar. Tem os [padrões de projeto e extensões](http://flask.pocoo.org/docs/patterns/) que te dão a certeza de que seu app poderá crescer sem problemas. Tem os sensacionais [Blueprints](http://flask.pocoo.org/docs/blueprints/) para que você reaproveite os módulos que desenvolver. Tem o controverso uso de [Thread Locals](http://flask.pocoo.org/docs/advanced_foreword/#thread-locals-in-flask) para facilitar a vida dos desenvolvedores. E além de tudo disso, não posso deixar de mencionar a comunidade que é bastante ativa e compartilha muitos projetos de extensões open-source como o Flask Admin, Flask-Cache, Flask-Google-Maps, Flask-Mongoengine, Flask-SQLAlchemy, Flask-Login, Flask-Mail etc....


> **SUMMARY:** o Flask não fica no seu caminho deixando você fluir com o desenvolvimento de seu app, você pode começar pequeno com um app feito em um único arquivo e ir crescendo aos poucos até ter seus módulos bem estruturados de uma maneira que permita a escalabilidade e o trabalho em equipe.


### Por onde começar?

Obviamente que para seguir neste tutorial será necessário utilizar Python, não entrarei em detalhes sobre a instalação do Python neste artigo, mas com certeza aqui no [PythonClub](/) devem ter artigos explicando detalhadamente a instalação do Python e a configuração de uma virtual-env, então vamos aos requirements.

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

    (wtf_env)seuuser@suamaquina/path/to/wtf$

Instale o Flask e o Ipython

    :::bash
    pip install flask
    pip install ipython

### Level 1.1 - Hello world

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

    (wtf_env)seuuser@suamaquina/path/to/wtf$ python app.py

Abra o seu browser na url [http://localhost:5000](http://localhost:5000) e você verá:

<div style="border:1px solid black;padding:10px;">
 Hello World! <strong>I am learning Flask</strong>
</div>

> **ACHIEVEMENT UNLOCKED!** Se tudo ocorreu bem até aqui então parabéns! você passou para o level 1.2 e já pode se considerar um **programador flask nível baby** :)

Nosso próximo passo será entender detalhadamente **o que aconteceu** nas 6 linhas que escrevemos no ```app.py```


### Level 1.2 - What The F**** happened here?


#### O objeto Flask

Conforme mencionado no início deste artigo, o Flask utiliza como base o **WerkZeug** que é uma biblioteca WSGI. Para lidar com os recursos do WerkZeug precisamos de uma aplicação WSGI que é uma instância de um objeto Python que implemente o protocolo WSGI e possa ser servida pelos web servers que implementam este protocolo como o Gunicorn, Uwsgi, Apache mod_wsgi etc.

No Flask fazemos isso criando uma instancia da classe **Flask**. O que essa classe faz é basicamente abstrair em métodos simples o fluxo de trabalho do padrão WSGI e do WerkZeug. Você pode ver como isto está implementado dando uma olhada no [código fonte](https://github.com/mitsuhiko/flask/blob/master/flask/app.py#L67).


```python
    from flask import Flask

    app = Flask(__name__)
```

Nas duas linhas acima nós importamos a classe base do Flask e criamos uma instancia dela que chamamos de **app**, este **app** que é nossa aplicação WSGI que deverá ser passada para o servidor de aplicação que a estiver servindo.

> **BEST PRACTICE ADVICE:** Especifique explicitamente o nome de seu pacote na hora de criar o app Flask, ao invés de ``__name__`` informe "nome_do_pacote".

A classe Flask pode receber alguns parâmetros para instanciar o objeto **app** mas geralmente passamos apenas o **import_name** que deve ser o nome exato do pacote onde o **app** está definido. Você pode usar a variável ```__name__``` para pegar este valor dinâmicamente e você verá muitos exemplos assim, porém saiba desde já que isto [não é uma boa prática](https://github.com/mitsuhiko/flask/blob/master/flask/app.py#L98).

O Flask utiliza o **import_name** para definir o que pertence ao seu projeto e este nome é usado como base path para inferir os recursos como por exemplo a sua pasta de templates e sua pasta de arquivos estáticos.

Além disso a ferramenta de debug do Werkzeug te mostrará mensagens mais explicitas se você definir o nome do pacote de seu app.

Supondo que você criará a instancia no caminho ```yourapplication/app.py``` você tem essas 2 opções.

```python
app = Flask('yourapplication')
app = Flask(__name__.split('.')[0])
```

No ultimo caso o ```__name__``` seria **yourapplication.app** e por isso fazemos o split para se tornar ```["yourapplication", "app"]``` e então pegamos o primeiro elemento.

Eu recomendo usar o primeiro padrão pois é mais bonito :)

```python
app = Flask("wtf")
```

> **NOTE:** O único caso onde uso do ```__name__``` é recomendado é quando seu projeto se resume a um único arquivo e não está contido em um pacote.

#### Qual a vantagem de criar apps desta maneira?

Tem duas coisas interessantes nessa forma explicita de criar aplicações no Flask.

1. Umas é o fato de que você pode e é inclusive [encorajado a criar suas próprias sub-classes Flask](http://flask.pocoo.org/docs/becomingbig/#subclass) e isso te dá o poder de sobrescrever comportamentos básicos do framework como por exemplo forçar que tudo seja renderizado como JSON (Mas este é um tema que veremos com mais detalhes em outro capítulo).

2. Você pode ter mais de um app Flask em seu projeto e isto te garante reusabilidade e organização, vou dar um exemplo:

```python

# um arquivo projeto.py

web_app = Flask(__name__)

rest_api = Flask(__name__, static_folder="path/to/different/folder")

celery_app = Flask(__name__, instance_path="blablabla")


class FlaskCustomizedForSoap(Flask):
    """Um Flask customizado para sempre responder um objeto SOAP válido"""
    def make_response(self, returned_by_view):
        """faça alguma coisa para nornalizar a
        resposta das views para o padrão SOAP"""
        return soapify(returned_by_view)

soap_api = FlaskCustomizedForSoap(__name__)

```

No exemplo acima temos em um único projeto 4 apps Flask que possuem papéis diferentes e podem ter configurações personalizadas ou até mesmo serem de uma subclasse do Flask customizada para algum tipo especifico de atividade.

Neste caso para servir todas essas apps poderiamos usar o [WerkZeug Dispatcher Middleware](http://werkzeug.pocoo.org/docs/middlewares/#werkzeug.wsgi.DispatcherMiddleware) para mapear as urls de cada app para um endpoint ou um dominio diferente.

> **RELAX:** Nos próximos capítulos desta série entraremos em detalhes a respeito do Dispatcher e técnicas de organização e deploy.

#### As views e o roteamento de urls

##### Views:

Views são funções que respondem por uma determinada url, a função da view é capturar os paramêtros enviados pelo cliente via url e então efetuar o processamento necessário com o objetivo de responser com algum tipo de conteúdo ou mensagem de status que pode ser desde um texto plano, um texto com JSON, um stream de dados, um template html renderizado etc.

Por exemplo, se em um site de notícias o cliente requisitar via método [GET](http://pt.wikipedia.org/wiki/Hypertext_Transfer_Protocol#GET) a seguinte url ``http://localhost:8000/noticias/brasil?categoria=ciencia&quantidade=2`` precisamos primeiramente ter este **endpoint** ``/noticias`` mapeado para uma view no nosso sistema de rotas e dentro desta view pegaremos o argumento **brasil** e os parâmetros **categoria** e **quantidade** para utilizarmos para efetuar a busca em nosso banco de dados de notícias e então construir um retorno para exibir no navegador.

O Flask através do WerkZeug abstrai uma boa parte deste trabalho tornando isto uma tarefa bastante trivial, por baixo dos panos quando usamos o decorator **@app.route** na verdade estamos alimentando uma lista de mapeamento do Werkzeug implementada pelo [werkzeug.routing.Map](http://werkzeug.pocoo.org/docs/routing/#quickstart) e esta lista de mapeamento contém elementos do tipo **Rule** que é justamente a regra que liga uma url com uma função Python em nosso projeto.

> **QUOTE:** "Have you looked at werkzeug.routing? It's hard to find anything that's simpler, more self-contained, or purer-WSGI than Werkzeug, in general — I'm quite a fan of it!"  —  [Alex Martelli](http://en.wikipedia.org/wiki/Alex_Martelli)

O Flask oferece 2 formas para o roteamento de views:

1 Roteamento via decorator

```python
@app.route("/noticias/<pais>")
def lista_de_noticias(pais):
    cat = request.args.get("categoria")
    qtd = request.args.get("quantidade")
    noticias = BD.query(pais=pais, categoria=cat).limit(qtd)
    return render_template("lista_de_noticias.html", noticias=noticias), 200
```

A vantagem de rotear via decorator é que o Flask usará o nome de sua função automaticamente como ``endpoint``, no exemplo acima **lista_de_noticias** seria o endpoint dessa view.

> **FLASKTIONARY:** o termo **endpoint** serve para designar tanto um recurso de uma api via url, por exemplo **api.site.com/users/new**, mas no Flask ele também é utilizado para identificar o nome interno que o router usará para uma url especifica, exemplo: **lista_noticias**, isso serve para possa ser utilizada a função ``url_for`` para resolver urls dinâmicamente. **RELAX:** continuaremos falando sobre isso na parte de templates deste artigo

Você pode inclusive utiliza multiplos decorators em uma mesma função para mapear várias urls, isto é útil para abranger aquela view com ou sem parametros.

exemplo:

```python
@app.route("/noticias")
@app.route("/noticias/<pais>")
@app.route("/noticias/<pais>/<estado>")
def lista_de_noticias(pais=None, estado=None):
```

No exemplo acima a mesma view irá responder pelas urls ``/noticias``, ``/noticias/brasil`` e ``/noticias/brasil/sao-paulo``

> **WARNING:** Cuidado com o uso de multiplos decorators, a ordem em que são definidos é importante e caso esteja algum decorator customizado como por exemplo ``@seu_app.requires_login``, se este for o primeiro decorator o Flask irá usar o nome da função wrapper do decorator ao invés do nome da view para o endpoint da url. A indicação é ao criar decorators utilizar sempre o ``functools.wraps`` para resolver este problema.


2 Roteamento explicito

```python

app.add_url_rule("/noticias/<pais>",
                 endpoint="lista_noticias",
                 view_func=lista_de_noticias)
```

O caso acima é bastante útil quando você precisa automatizar ou centralizar o mapeamento de urls em um único local de seu projeto, é a maneira utilizada também com blueprints, a única desvantagem é que neste caso é sempre preciso informar explicitamente o nome do **endpoint** e a **view_func** a ser mapeada.











