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

# Hello Flask
### Parte 1 - Introdução ao desenvolvimento web com Flask

- [O que é Flask](#o_que_e_flask)
- [Por onde começar](#por_onde_comecar)
- [Hello World](#hello_world)
- [O objeto Flask](#o_objeto_flask)
- [Views e roteamento de urls](#views_e_roteamento_de_urls)
- [O contexto da aplicação](#o_contexto_da_aplicacao)
- [O objeto "request" + acessando dados via GET e POST](#o_objeto_request_acessando_dados_via_get_e_post)
- [Sessões e biscoitos](#sessoes_e_biscoitos)
- [Acessando banco de dados (pequeno exemplo com dataset)](#acessando_bando_de_dados_pequeno_exemplo_com_dataset)
- [Servindo arquivos estáticos](#servindo_arquivos_estaticos)
- [Templates com Jinja2](#template_com_jinja_2)
- [Customizando o Jinja com macros, filters e template globals](#customizando_o_jinja_com_macros_filters_e_template_globals)

> **DISCLAIMER:** Este tutorial será bem longo, então já coloca ai nos favoritos pois não vai dar tempo de você terminar hoje :)


### <a name="o_que_e_flask" href="#o_que_e_flask">O que é Flask?</a>

![Flask logo](http://flask.pocoo.org/static/logo.png)

Flask é um micro-framework (um framework minimalista) desenvolvido em Python
e baseado em 3 pilares:

- [WerkZeug](http://werkzeug.pocoo.org/) é uma biblioteca para desenvolvimento de apps [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) que é a especificação universal de como deve ser a interface entre um app Python e um web server. Ela possui a implementação básica deste padrão para interceptar requests e lidar com response, controle de cache, cookies, status HTTP, roteamento de urls e também conta com uma poderosa ferramanta de debug. Além disso o werkzeug possui um conjunto de **utils** que acabam sendo uma mão na roda mesmo em projetos que não são para a web.

- [Jinja2](http://jinja.pocoo.org/) é um template engine escrito em Python, você escreve templates utilizando marcações como ``{{ nome_da_variavel }}`` ou ``{% for nome in lista_de_nomes %} Hello {{nome}}!! {% endfor %}`` e o Jinja se encarrega de renderizar este template, ou seja, ele substitui os placeholders pelo valor de suas variáveis.
O Jinja2 já vem com a implementação da maioria das coisas necessárias na construção de templates html e além disso é muito fácil de ser customizado com template filters, macros etc.

- [Good Intentions](https://trinket.io/python/fdedd0fb94): O Flask é **Pythonico**! além do código ter alta qualidade nos quesitos de legibilidade ele também tenta seguir as premissas do [Zen do Python](https://trinket.io/python/fdedd0fb94) e dentro dessas boas intenções nós temos o fato dele ser um [**micro-framework**](http://flask.pocoo.org/docs/foreword/#what-does-micro-mean) deixando que você tenha liberdade de estruturar seu app da maneira que desejar. Tem os [padrões de projeto e extensões](http://flask.pocoo.org/docs/patterns/) que te dão a certeza de que seu app poderá crescer sem problemas. Tem os sensacionais [Blueprints](http://flask.pocoo.org/docs/blueprints/) para que você reaproveite os módulos que desenvolver. Tem o controverso uso de [Thread Locals](http://flask.pocoo.org/docs/advanced_foreword/#thread-locals-in-flask) para facilitar a vida dos desenvolvedores. E além de tudo disso, não posso deixar de mencionar a comunidade que é bastante ativa e compartilha muitos projetos de extensões open-source como o Flask Admin, Flask-Cache, Flask-Google-Maps, Flask-Mongoengine, Flask-SQLAlchemy, Flask-Login, Flask-Mail etc....


> **SUMMARY:** o Flask não fica no seu caminho deixando você fluir com o desenvolvimento de seu app, você pode começar pequeno com um app feito em um único arquivo e ir crescendo aos poucos até ter seus módulos bem estruturados de uma maneira que permita a escalabilidade e o trabalho em equipe.


### <a name=por_onde_comecar href=#por_onde_comecar>Por onde começar?</a>

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

Usando virtualenvwrapper **(recommended)**


    :::bash
    sudo apt-get install virtualenvwrapper
    mkvirtualenv wtf_env

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

### <a name="hello_world" href="#hello_world">Level 1.1 - Hello world</a>

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


### <a name="o_objeto_flask" href="#o_objeto_flask">O objeto Flask</a>

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

1. Uma é o fato de que você pode e é inclusive [encorajado](http://flask.pocoo.org/docs/becomingbig/#subclass) a criar suas próprias sub-classes Flask e isso te dá o poder de sobrescrever comportamentos básicos do framework como por exemplo forçar que tudo seja renderizado como JSON (Mas este é um tema que veremos com mais detalhes em outro capítulo).

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

Como você pode perceber, ao criar o objeto Flask podemos passar vários argumentos na inicialização, você pode conferir cada um desses argumentos diretamente na [documentação](http://flask.pocoo.org/docs/api/#application-object).

### <a name="views_e_roteamento_de_urls" href="#views_e_roteamento_de_urls">As views e o roteamento de urls</a>

##### Views:

Views são funções (ou classes) que respondem por uma determinada url, a função da view é capturar os paramêtros enviados pelo cliente via url e então efetuar o processamento necessário com o objetivo de responser com algum tipo de conteúdo ou mensagem de status que pode ser desde um texto plano, um texto com JSON, um stream de dados, um template html renderizado etc.

Por exemplo, se em um site de notícias o cliente requisitar via método [GET](http://pt.wikipedia.org/wiki/Hypertext_Transfer_Protocol#GET) a seguinte url ``http://localhost:8000/noticias/brasil?categoria=ciencia&quantidade=2`` precisamos primeiramente ter este **endpoint** ``/noticias`` mapeado para uma view no nosso sistema de rotas e dentro desta view pegaremos o argumento **brasil** e os parâmetros **categoria** e **quantidade** para utilizarmos para efetuar a busca em nosso banco de dados de notícias e então construir um retorno para exibir no navegador.

O Flask através do WerkZeug abstrai uma boa parte deste trabalho tornando isto uma tarefa bastante trivial, por baixo dos panos quando usamos o decorator **@app.route** na verdade estamos alimentando uma lista de mapeamento do Werkzeug implementada pelo [werkzeug.routing.Map](http://werkzeug.pocoo.org/docs/routing/#quickstart) e esta lista de mapeamento contém elementos do tipo **Rule** que é justamente a regra que liga uma url com uma função Python em nosso projeto.

> **QUOTE:** "Have you looked at werkzeug.routing? It's hard to find anything that's simpler, more self-contained, or purer-WSGI than Werkzeug, in general — I'm quite a fan of it!"  —  [Alex Martelli](http://en.wikipedia.org/wiki/Alex_Martelli)

O Flask oferece 2 formas para o roteamento de views:

1 Roteamento via decorator

```python
from flask import Flask, request, render_template

app = Flask("wtf")

@app.route("/noticias/<pais>")
def lista_de_noticias(pais):
    cat = request.args.get("categoria")
    qtd = request.args.get("quantidade")
    noticias = BD.query(pais=pais, categoria=cat).limit(qtd)
    return render_template("lista_de_noticias.html", noticias=noticias), 200

app.run(debug=True, use_reloader=True)
```

A vantagem de rotear via decorator é que o Flask usará o nome de sua função automaticamente como ``endpoint``, no exemplo acima **lista_de_noticias** seria o endpoint dessa view.

> **FLASKTIONARY:** o termo **endpoint** serve para designar tanto um recurso de uma api via url, por exemplo **api.site.com/users/new**, mas no Flask ele também é utilizado para identificar o nome interno que o router usará para uma url especifica, exemplo: **lista_noticias**, isso serve para possa ser utilizada a função ``url_for`` para resolver urls dinâmicamente. **RELAX:** continuaremos falando sobre isso na parte de templates deste artigo

Você pode inclusive utilizar multiplos decorators em uma mesma função para mapear várias urls, isto é útil para abranger uma mesma view com ou sem parametros.

exemplo:

```python
@app.route("/noticias")
@app.route("/noticias/<pais>")
@app.route("/noticias/<pais>/<estado>")
def lista_de_noticias(pais=None, estado=None):
```

No exemplo acima a mesma view irá responder pelas urls ``/noticias``, ``/noticias/brasil`` e ``/noticias/brasil/sao-paulo``

> **WARNING:** Cuidado com o uso de multiplos decorators, a ordem em que são definidos é importante e caso esteja usando algum decorator customizado como por exemplo ``@seu_app.requires_login``, se este for o primeiro decorator o Flask irá usar o nome da função wrapper do decorator ao invés do nome da view para o endpoint da url. A indicação é ao criar decorators utilizar sempre o ``functools.wraps`` para resolver este problema.


2 Roteamento explicito

```python

app.add_url_rule("/noticias/<pais>",
                 endpoint="lista_noticias",
                 view_func=lista_de_noticias)
```

O caso acima é bastante útil quando você precisa automatizar ou centralizar o mapeamento de urls em um único local de seu projeto, é a maneira utilizada também com blueprints, a única desvantagem é que neste caso é sempre preciso informar explicitamente o nome do **endpoint** e a **view_func** a ser mapeada.


> **TIP:** Enquanto estiver desenvolvendo use ``debug=True`` para ativar o Werkzeug debugger e ``use_reloader=True`` para que o Flask dê um restart no servidor de desenvolvimento sempre que detectar alterar no código fonte.
(quando fizer deploy mude esses valores para False)

#### Regras de URL

As urls são recebidas no formato texto, por exemplo: ``/noticias/1``, porém em alguns casos queremos que o valor passado como argumento seja convertido para um tipo de dados especifico, ou seja, queremos receber o ``1`` como um inteiro.

Você já sabe que o Flask utiliza o router do WerkZeug que internamente já implementa alguns [conversores](http://werkzeug.pocoo.org/docs/routing/#builtin-converters) para as regras de url.

Os "conversores" padrão são:

- ``/noticias/<categoria>``, recebe o parâmetro "categoria" no formato unicode, exemplo "entretenimento".
- ``/noticias/<int:noticia_id>``, recebe o parâmetro "noticia_id" no formato inteiro, exemplo: "1"
- ``/cotacao/<float:dolar>/``, recebe o parâmetro "dolar" como float, exemplo: "3.2"
- ``/imagem/<path>``, recebe o parâmetro "path" como um caminho, exemplo: "animais/marssupiais/quokka.png"

Também é possivel utilizar **regex**, passar parâmetros para validação ou até mesmo criar seus próprios conversores de url, mas este assunto não veremos neste tutorial :(

#### A barra no final da url

Isto sempre causa certa confusão, portanto é sempre bom pensar um pouco antes de tomar esta decisão, sua url vai obrigar o uso da **trailing backslash** ou não?

No Flask existe uma convenção bastante útil: caso você declare sua url sem a barra no final ``/noticias/<categoria>`` então esta url será acessível apenas sem a barra no final. Agora se você deseja que a url ``/noticias/entretenimento/`` seja válida declare sua regra como ``/noticias/<categoria>/`` desta forma mesmo que o usuário esqueça de colocar a barra na hora de requisitar a url, o Flask irá automaticamente redirecionar o usuário para a url correta com a "/" no final.

> **TIP:** Eu costumo utilizar uma lógica simples para decidir sobre o uso da "/", se a url define um recurso final da minha árvore de recursos, por exemplo, se a url é para uma imagem ``/imagens/foto.jpg`` ou se é para uma postagem de um site ``/noticias/apenda-python.html`` ou até mesmo ``/noticias/aprenda-python``, então eu declaro a url sem a "/" no final. Porém se a url representa uma categoria, uma tag ou uma pasta então coloco a "/" no final pois desta forma segue o conceito de árvore, igual a árvore de arquivos e diretórios. Ex: ``/noticias/entretenimento/`` ou ``/tags/python/``.

#### O retorno <strike style="color: red">de Jedi</strike> da view


> **TIP:** Pode ir escrevendo os códigos deste tutorial ai no ``app.py`` para ir testando enquanto lê este artigo.

Views precisam retornar uma tupla formada por 2 elementos, um **body** que pode ser um objeto serializável como por exemplo um texto, e também devem retornar um inteiro representando o código de status HTTP.

Exemplo:

```python
@app.route("/<name>")
def index(name):
    if name.lower() == "bruno":
        return "Olá {}".format(name), 200
    else:
        return "Not Found", 404
```

Na view acima caso seja requisitada a url ``site.com/Bruno`` o código de status será o "200" que representa "OK". Porém se requisitar informando um nome diferente o código de status será "404" com a mensagem "Not Found". Cada cliente pode implementar um comportamento diferente para o tratamento desses códigos de status, isto é muito importante principalmente quando trabalhamos com APIs.

> **RELAX:** Se você não informar o código de status o Flask irá tentar resolver para você. Por padrão qualquer retorno no formato string é convertido para um Response com código 200 e o mimetype "text/html"

```python
@app.route("/<name>")
def index(name):
    return "Olá {}".format(name)
```

O exemplo acima também é válido, e neste caso o Flask irá informar automaticamente o código 200 ao menos que uma excessão HTTP seja levantada explicitamente ou por motivo de algum erro em seu código.

> **NOTE:** Ao desenvolver uma API REST ou formulários que serão consumidos via Ajax é recomendado informar explicitamente os códigos HTTP e tratar adequadamente as excessões HTTP, pois do lado do cliente o comportamento pode depender desses códigos de status.

Além disso o Flask oferece alguns **helpers** para facilitar o tratamento de excessões http, por exemplo o **404** ou **503** pode ser feito através do helper **abort** e o **301/302** pode ser feito com o uso do helper **redirect**.

```python
from flask import redirect, abort

@app.route("/shortener/<tiny_url>")
def url_shortener(tiny_url):
    try:
        url = banco_de_dados.select(shortened=tiny_url).url
    except AttributeError:
        # objeto NoneType não tem o atributo url, ou seja, não existe
        abort(404)
    except ConnectionError:
        # não conseguiu conectar no MySQL # TODO: Use o PostGres :)
        abort(503)  # ServiceUnavailable
    else:
        redirect(url)
```

O caso acima é a implementação de um encurtador de urls que procura uma url no banco de dados através de seu código ex: ``/shortener/x56ty`` e então utiliza 3 helpers para definir o status HTTP adequado, no melhor dos casos o usuário será redirecionado para a url **desencurtada**.


#### HTML, JSON, XML etc


HTML

Obviamente que você pode retornar conteúdo formatado e não apenas texto puro, isso poderá ser <strike style="color:red">feito direto na view</strike> ou em um <span style="color:green">template</span>.

```python
@app.route("/html_page/<nome>")
def html_page(nome):
    return u"""
    <html>
       <head><title>Ainda não sei usar o Jinja2 :)</title></head>
       <body>
          <h1>Olá %s Coisas que você não deve fazer.</h1>
          <ul>
            <li> Escrever html direto na view </li>
            <li> Tentar automatizar a escrita de html via Python</li>
            <li> deixar de usar o Jinja2 </li>
          </ul>
       </body>
    </html>
    """ % nome
```

O exemplo acima apesar de em alguns raros casos ser útil, não é recomendado, o ideal é usar templates para deixar a camada de apresentação desacoplada da lógica do nosso app.

assumindo que o trecho html acima está em um arquivo ``templates/html_page.html`` podemos fazer o seguinte.

```python
from flask import render_template

@app.route("/html_page/<nome>")
def html_page(nome):
    return render_template("html_page.html", nome=nome)
```

e dentro do arquivo html basta utilizar ``{{nome}}`` no lugar de ``%s``

> **RELAX:** Logo mais falaremos mais a respeito dos templates

JSON

Ao invés de retornar uma página HTML você poderá precisar retornar JSON, JSONP ou algum outro formato como <strike>XML</strike> arghhhhh.

Você pode simplesmente retornar uma string jsonificada porém tbm é preciso dizer ao cliente que o **content_type** ou **mimetype** em questão é **application/json**, <strike>m$/application:xml</strike> ou qualquer outro formato.

Existem 3 possibilidades:

Criar um objeto Response explicitamente

```python
import json
from flask import make_response

def json_api():
    pessoas = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               {"nome": "Anneke van Giersbergen"},
               {"nome": "Steven Wilson"}]
    response = make_response(json.dumps(pessoas))
    response.content_type = "application/json"
    # ou
    # response.headers['Content-Type'] = "application/json"
    return response
```

Retornar uma tupla de 3 elementos, no formato ``(string, status_code, headers_dict)``

```python
def json_api():
    pessoas = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               {"nome": "Anneke van Giersbergen"},
               {"nome": "Steven Wilson"}]
    return json.dumps(pessoas), 200, {"Content-Type": "application/json"}
```


Os exemplos acima são válidos e poderão ser seguidos para outros tipos de dados, porém como JSON é um tipo de retorno muito comum o Flask já vem com um helper para ajuda-lo a economizar umas linhas de código.

```python
from flask import jsonify

def json_api():
    pessoas = [{"nome": "Bruno Rocha"},
               {"nome": "Arjen Lucassen"},
               {"nome": "Anneke van Giersbergen"},
               {"nome": "Steven Wilson"}]
    return jsonify(pessoas=pessoas, total=len(pessoas))
```

Com o uso de **jsonify** o Flask já se encarrega do header adequado e ainda valida a segurança no formato do JSON, além disso fica muito mais bonito o código.


### <a name="o_contexto_da_aplicacao" href="#o_contexto_da_aplicacao">The application context</a>

> **NOTE:** Esta é uma questão um pouco complexa, eu não vou tentar explicar em detalhes e vou apenas abordar os pontos importantes de forma bem resumida e simplificada, caso tenha interesse em entender mais a fundo pode dar uma lida nos [docs](http://flask.pocoo.org/docs/appcontext/) a respeito.


Existem 3 estados em que uma app Flask pode estar:

#### 1 Estado de configuração.

É quando a app é instanciada, e nenhum request ocorreu ainda, é o momento em que você pode seguramente modificar as configurações e carregar módulos, extensões etc.

Este estado ocorre antes do **dispatch**, ou seja, no nosso caso é antes do **app.run()** ser executado, mas no caso de servir seu app com outro app server como gunicorn ou uwsgi este estado é antes do servidor WSGI registrar o objeto **application**.

Exemplo:

```python

app = Flask("wtf")

app.config["SECRET_KEY"] = "schblaums"
app.config["DEBUG"] = True

from flask.ext.magic import MakeMagic
MakeMagic(app)

```

As linhas acima "ocorrem" geralmente no estado de configuração e portanto não assumimos que existe um **request** em andamento. Um detalhe importante é o fato de que este estado é válido apenas para o **top level** module, ou seja, dentro do escopo de funções, views, classes etc o estado será outro.

#### 2 Estado de request

É quando seu app já foi iniciado e está **registrado** no servidor WSGI e então acontece uma requisição, neste momento o Flask irá popular o objeto request com os dados desta requisição e você poderá acessar o objeto request.


```python
from flask import request, current_app, jsonify

app = Flask(__name__)

@app.route("/show_config")
def show_config():
    querystring_args = request.args.to_dict()
    post_args = request.form.to_dict()
    return jsonify(
        debug=current_app.config.get('DEBUG'),
        args=querystring_args,
        vars=post_args
    )
```

No exemplo acima acessamos os valores do objeto request, tanto os passados via GET(querystring) tanto quanto os passados via POST (formulário). Além disso acessamos a **current_app** para pegar as configs da app em execução. Isto existe pois no Flask é possível ter mais de um objeto Flask em um único projeto.

Mais de um app em um único projeto:

> **It's weird**

```python
app = Flask(__name__)
outra_app = Flask(__name__)

@app.route("/url_na_app")
@outra_app.route("/url_na_outra_app")
def view():
    ....

if X:
    app.run()
elif Y:
    outra_app.run()

```

O exemplo acima é meio non-sense mas é possível, além disso para fazer este tipo de coisa é recomendado usar o dispatcher middleware.


#### 3 Estado interativo ou estado de testes

As vezes para efetuar pequenos testes ou até mesmo escrever testes unitários é necessário acessar o objeto **request** ou o **current_app** em um script standalone ou em um terminal interativo.

```python
>>> from flask import Flask, current_app, request
>>> app = Flask(__name__)
>>> print request.form
...Traceback (most recent call last)
RuntimeError: working outside of request context
```

Nesta hora você pensa **WTF** terei que fazer um request cada vez que precisar testar esse código? não, calma, o Flask oferece uma solução.


```python
>>> from flask import Flask, current_app, request
>>> app = Flask(__name__)
>>> with app.test_request_context("/teste", "x.com", "aaa=1&bb=2"):
...     print request.args.to_dict()
...     print request.path

{'aaa': u'1', 'bb': u'2'}
u"/teste"
```

Enfim, usamos o gerenciador de contexto ``app.test_request_context`` para fazer um **mock** de um request real que será usado apenas para fins de testes.

## <a name="o_objeto_request_acessando_dados_via_get_e_post" href="#o_objeto_request_acessando_dados_via_get_e_post">O objeto "request" + acessando dados via GET e POST</a>

O objeto **request** é um **proxy** que internamente garante você acesse a requisição atual ou thread atual. Ele carrega dados referentes a cada requisição HTTP, nele podemos acessar as variáveis enviadas atráves da url ou de um formulário, podemos também verificar o método HTTP entre outros dados importantes que podem ser conferidos na [doc](http://flask.pocoo.org/docs/api/#incoming-request-data).

Os itens mais importantes são: (method, args, form, path, is_json)


É muito útil checar qual o método HTTP que foi requisitado, isto é o que possibilita a criação de uma API REST, o exemplo a seguir é auto explicativo:

```python
from flask import request, jsonify

@app.route("/noticia")
@app.route("/noticia/<int:noticia_id>")
def noticia_api(noticia_id=None):
    if request.method == "GET":
        if noticia_id:
            # retorna uma noticia especifica
            return jsonify(noticia=noticias.filter(id=noticia_id))
        else:
            # retorna todas as noticias
            return jsonify(noticias=noticias.all())
    elif request.method == "POST":
        if request.is_json:
            # se o request veio com o mimetype "json" usa os dados para
            # inserir novas noticias
            noticias.bulk_insert(request.json)
            return "Noticias inseridas com sucesso", 201
        else:
            # assumimos que os dados vieram via Ajax/POST/Formulário
            noticias.create(request.form)
            return "Noticia criada com sucesso", 201
    elif request.method == "DELETE" and noticia_id:
        # apaga uma noticia especifica
        noticias.delete(id=noticia_id)
        return "Noticia apagada com sucesso!", 204
    ...
```

> **WAIT:** O exemplo acima é apenas uma das formas de se fazer isso, e não é a forma mais recomendada. É preferivel o uso de geradores de API como o Python-EVE ou o Flask-API. Além disso também é possível utilizar class based Method views para melhorar o código, mas veremos isso em um próximo capítulo.

### Valores mais importantes do objeto **request**

- request.method: Informa qual método HTTP foi usado na requisiçao
- request.headers: headers HTTP da requisição, útil para checar o mimetype e dados de basic auth.
- request.environ: Variáveis de ambiente do WSGI, navegador, ip do cliente etc
- request.path, request.url: O path ou a url completa da requisição
- request.is_xhr: Informa se é ou não uma requisição Ajax
- request.blueprint: Nome do blueprint que interceptou o request (veremos isso mais adiante)


### Acessando dados do request

#### request.args

Um dicionário com os valores passados via GET (na url após o ?).

url requisitada: ``/noticias?categoria=esportes&limit=10``

```python
>>> request.args
ImmutableMultiDict([('categoria', u'esportes'), ('limit', u'10')])
>>> request.args.to_dict()
{u"categoria": u"esportes", u"limit": u"10"}
>>> request.args.get("categoria")
u"esportes"
```

Não é muito comum mas em alguns casos as chaves podem se repetir, neste caso devemos usar o ``getlist``.

url requisitada: ``/noticias?categoria=esportes&categoria=musica``
```python
>>> request.args
ImmutableMultiDict([('categoria', u'esportes'), ('categoria', u'musica')])
>>> request.args.to_dict()  # mantém só os primeiros
{u"categoria": u"esportes"}
>>> request.args.getlist("categoria")
[u"esportes", u"musica"]
```

#### request.form

O request.form funciona da mesma forma que o .args porém ele intercepta apenas os argumentos passados via POST, PUT ou PATCH, ou seja, via formulário ou payload.

exemplo de requisição POST via console

```bash
curl --data "categoria=esportes&limit=10" http://site.com/noticias
```

A requisição acima corresponde ao submit de um formulário contento os campos "categoria" e "limit".

```python
>>> request.form
ImmutableMultiDict([('categoria', u'esportes'), ('limit', u'10')])
>>> request.form.to_dict()
{u"categoria": u"esportes", u"limit": u"10"}
>>> request.form.get("categoria")
u"esportes"
```

repare que é exatamente o mesmo funcionamento do .args

#### request.json

É exatamente a mesma coisa do .args e do .form, porém ele será populado quando o request trouxer o mimetype "application/json", então os dados do JSON no payload serão colocados neste atributo.

Requisição

```bash
curl -X POST -d {"categoria": "esporte"} http://site.com/noticias --header "Content-Type:application/json"
```

O restante é igual, basta usar o ``request.is_json`` para checar se a requisição é com JSON payload e então acessar os dados.

#### File uploads

Caso seu formulário ou API permitam o envio de arquivos esses dados serão colocados no ``request.files``. Isto ocorre pois internamente o Flask transforma os dados recebidos em um objeto **FileStorage** para permitir que você manipule os com mais facilidade.

Requisição: (equivale a um formulário com file upload)

```bash
curl --form "photo=@picture.jpg&item_id=12345" http://site.com/change_photo
```

para salvar a imagem:

```python
import os
from flask import current_app
from werkzeug import secure_filename

@app.route("/change_photo")
def perfil():
    item_id = request.form.get('item_id')
    photo = request.files.get('photo')
    if item_id and photo:
        filename = secure_filename(photo.filename)
        file_path =os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        photo.save(file_path)
        banco_de_dados.get(item_id=item_id).update(photo_path=file_path)
    return "Imagem atualizada", 201
```

> **TIP:** Sempre utilize o helper **secure_filename** do Werkzeug pois ele sanitiza a url removendo caracteres indesejados e evitando dor de cabeça com file system.

### <a name="sessoes_e_biscoitos" href="#sessoes_e_biscoitos"> Sessions and Cookies</a>

Sessions


























