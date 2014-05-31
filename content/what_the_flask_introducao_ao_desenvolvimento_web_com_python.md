Title: What the Flask? Pt-1 Introdução ao desenvolvimento web com Python
Slug: what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python
Date: 2014-05-31 02:22
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

> **TL;DR:** A versão final do aplicativo explicado neste artigo está no [github](https://github.com/rochacbruno/wtf)

A série **W**hat **T**he **F**lask será dividida nos seguintes capítulos.

1. [**Hello Flask**](/what_the_flask_introducao_ao_desenvolvimento_web_com_python.html): Introdução ao desenvolvimento web com Flask  - **<-- Você está aqui**
2. **Flask patterns**: boas práticas na estrutura de aplicações Flask
3. **Plug & Use**: extensões essenciais para iniciar seu projeto
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask e para o Jinja2
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.

# Hello Flask
### Parte 1 - Introdução ao desenvolvimento web com Flask

#### Conhecendo o Flask

- [O que é Flask](#o_que_e_flask)
- [Por onde começar](#por_onde_comecar)
- [Hello World](#hello_world)
- [O objeto Flask](#o_objeto_flask)
- [Views e roteamento de urls](#views_e_roteamento_de_urls)
- [O contexto da aplicação](#o_contexto_da_aplicacao)
- [O objeto "request" + acessando dados via GET e POST](#o_objeto_request_acessando_dados_via_get_e_post)
- [Sessões e biscoitos](#sessoes_e_biscoitos)

#### Quick and Dirty Tutorial: Desenvolvendo um aplicativo de notícias

- [Acessando banco de dados (pequeno exemplo com dataset)](#acessando_bando_de_dados_pequeno_exemplo_com_dataset)
- [Servindo arquivos estáticos e upload de MEDIA](#servindo_arquivos_estaticos)
- [Templates com Jinja2](#template_com_jinja_2)


> **ATENÇÃO:** Este artigo é bem longo, então já coloca ai nos favoritos pois pode ser que não dê tempo de você terminar hoje :)


### <a name="o_que_e_flask" href="#o_que_e_flask">O que é Flask?</a>

![Flask logo](http://flask.pocoo.org/static/logo.png)

Flask é um micro-framework (um framework minimalista) desenvolvido em Python
e baseado em 3 pilares:

- [WerkZeug](http://werkzeug.pocoo.org/) é uma biblioteca para desenvolvimento de apps [WSGI](http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) que é a especificação universal de como deve ser a interface entre um app Python e um web server. Ela possui a implementação básica deste padrão para interceptar requests e lidar com response, controle de cache, cookies, status HTTP, roteamento de urls e também conta com uma poderosa ferramenta de debug. Além disso o werkzeug possui um conjunto de **utils** que acabam sendo uma mão na roda mesmo em projetos que não são para a web.

- [Jinja2](http://jinja.pocoo.org/) é um template engine escrito em Python, você escreve templates utilizando marcações como ``{{ nome_da_variavel }}`` ou ``{% for nome in lista_de_nomes %} Hello {{nome}}!! {% endfor %}`` e o Jinja se encarrega de renderizar este template, ou seja, ele substitui os placeholders pelo valor de suas variáveis.
O Jinja2 já vem com a implementação da maioria das coisas necessárias na construção de templates html e além disso é muito fácil de ser customizado com template filters, macros etc.

- [Good Intentions](https://trinket.io/python/fdedd0fb94): O Flask é **Pythonico**! além do código ter alta qualidade nos quesitos de legibilidade ele também tenta seguir as premissas do [Zen do Python](https://trinket.io/python/fdedd0fb94) e dentro dessas boas intenções nós temos o fato dele ser um [**micro-framework**](http://flask.pocoo.org/docs/foreword/#what-does-micro-mean) deixando que você tenha liberdade de estruturar seu app da maneira que desejar. Tem os [padrões de projeto e extensões](http://flask.pocoo.org/docs/patterns/) que te dão a certeza de que seu app poderá crescer sem problemas. Tem os sensacionais [Blueprints](http://flask.pocoo.org/docs/blueprints/) para que você reaproveite os módulos que desenvolver. Tem o controverso uso de [Thread Locals](http://flask.pocoo.org/docs/advanced_foreword/#thread-locals-in-flask) para facilitar a vida dos desenvolvedores. E além de tudo disso, não posso deixar de mencionar a comunidade que é bastante ativa e compartilha muitos projetos de extensões open-source como o Flask Admin, Flask-Cache, Flask-Google-Maps, Flask-Mongoengine, Flask-SQLAlchemy, Flask-Login, Flask-Mail etc....


> **SUMMARY:** o Flask não fica no seu caminho deixando você fluir com o desenvolvimento de seu app, você pode começar pequeno com um app feito em um único arquivo e ir crescendo aos poucos até ter seus módulos bem estruturados de uma maneira que permita a escalabilidade e o trabalho em equipe.


### <a name=por_onde_comecar href=#por_onde_comecar>Por onde começar?</a>

Obviamente que para seguir neste tutorial será necessário utilizar Python, não entrarei em detalhes sobre a instalação do Python neste artigo, mas com certeza aqui no [PythonClub](/) devem ter artigos explicando detalhadamente a instalação do Python e a configuração de uma virtual-env, então vamos aos requirements.

#### Você vai precisar de:

- **Python 2.7** (não usaremos Python 3 pois ainda tem extensões que não migraram)
- **Ipython** - Um terminal interativo (REPL) com poderes da super vaca ("Have you mooed today?")
- **virtualenv** ou **virtualenv wrapper** - para criação de ambientes isolados
- Um **editor** de código ou IDE de sua preferência - (Gedit, Notepad++, sublime, Emacs, VIM etc..)
- Um **browser** de verdade - espero que você não esteja usando o I.E :P
- **Dataset** - Biblioteca para acesso a bancos de dados
- **Flask** - Geralmente usado para armazenar vodka ou scotch (wtf?)

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

No Flask criamos a aplicação WSGI instanciando a classe **Flask**. O que essa classe faz é basicamente abstrair em métodos simples o fluxo de trabalho do padrão WSGI e do WerkZeug. Você pode ver como isto está implementado dando uma olhada no [código fonte](https://github.com/mitsuhiko/flask/blob/master/flask/app.py#L67).


```python
    from flask import Flask

    app = Flask(__name__)
```

Nas duas linhas acima nós importamos a classe base do Flask e criamos uma instancia dela que chamamos de **app**, este **app** que é nossa aplicação WSGI que deverá ser passada para o servidor de aplicação que a estiver servindo.

> **BEST PRACTICE ADVICE:** Especifique explicitamente o nome de seu pacote na hora de criar o app Flask, ao invés de ``__name__`` informe "nome_do_pacote".

A classe Flask pode receber alguns parâmetros para instanciar o objeto **app** mas geralmente passamos apenas o **import_name** que deve ser o nome exato do pacote onde o **app** está definido. Você pode usar a variável ```__name__``` para pegar este valor dinâmicamente e você verá muitos exemplos assim, porém saiba desde já que isto [não é uma boa prática](https://github.com/mitsuhiko/flask/blob/master/flask/app.py#L98).

O Flask utiliza o **import_name** para definir o que pertence ao seu projeto e este nome é usado como base path para inferir os recursos como por exemplo descobrir onde fica a sua pasta de templates e sua pasta de arquivos estáticos.

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

No exemplo acima temos em um único projeto 4 apps Flask que possuem papéis diferentes e podem ter configurações personalizadas ou até mesmo serem de uma subclasse do Flask customizada para algum tipo especifico de atividade como retornar dados no padrão <strike>SOAP</strike> (fique longe disso :P, use REST).

Neste caso para servir todas essas apps poderiamos usar o [WerkZeug Dispatcher Middleware](http://werkzeug.pocoo.org/docs/middlewares/#werkzeug.wsgi.DispatcherMiddleware) para mapear as urls de cada app para um endpoint ou um dominio diferente.

> **RELAX:** Nos próximos capítulos desta série entraremos em detalhes a respeito do Dispatcher e técnicas de organização e deploy.

Como você pode perceber, ao instanciar o objeto Flask podemos passar vários argumentos na inicialização, não vou abordar com detalhes cada um desses argumentos, mas você pode conferir diretamente na [documentação](http://flask.pocoo.org/docs/api/#application-object).

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

> **TIP:** Enquanto estiver desenvolvendo use ``debug=True`` para ativar o Werkzeug debugger e ``use_reloader=True`` para que o Flask dê um restart no servidor de desenvolvimento sempre que detectar alterar no código fonte.
(quando fizer deploy mude esses valores para False)

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

Views precisam retornar um objeto do tipo **Response** ou uma tupla formada por até 3 elementos, um **body** que pode ser um objeto serializável como por exemplo um texto, um inteiro representando o código de **status HTTP** e um dicionário de **headers**, sendo que os dois ultimos elementos são opcionais.

Exemplo:

```python
@app.route("/<name>")
def index(name):
    if name.lower() == "bruno":
        return "Olá {}".format(name), 200
    else:
        return "Not Found", 404
```

Na view acima caso seja requisitada a url ``localhost:5000/Bruno`` o código de status será o "200" que representa "OK". Porém se requisitar informando um nome diferente o código de status será "404" com a mensagem "Not Found". Cada cliente pode implementar um comportamento diferente para o tratamento desses códigos de status, isto é muito importante principalmente quando trabalhamos com APIs.

> **RELAX:** Se você não informar o código de status o Flask irá tentar resolver para você. Por padrão qualquer retorno no formato string é convertido para um objeto Response com código de status 200 e no header vai o Content-Type "text/html" automaticamente. Flask is full of magic :)

```python
@app.route("/<name>")
def index(name):
    return "Olá {}".format(name)
```

O exemplo acima também é válido, e neste caso o Flask irá informar automaticamente o código 200 ao menos que uma excessão HTTP seja levantada explicitamente ou por motivo de algum erro em seu código.

> **NOTE:** Ao desenvolver uma API REST ou formulários que serão consumidos via Ajax é recomendado informar explicitamente os códigos HTTP e tratar adequadamente as excessões HTTP, pois do lado do cliente o comportamento pode depender desses códigos de status.

Além disso o Flask oferece alguns **helpers** para facilitar o tratamento de excessões http, por exemplo o **404** ou **503** podem ser definidos através do helper **abort** e o **301/302** com o uso do helper **redirect**.

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

> **RELAX:** Logo mais falaremos a respeito dos templates

JSON

Ao invés de retornar uma página HTML você poderá precisar retornar JSON, JSONP ou algum outro formato como <strike>XML</strike> arghhhhh.

Você pode simplesmente retornar uma string jsonificada porém também é preciso dizer ao cliente que o **content_type** ou **mimetype** em questão é **application/json**, <strike>m$/application:xml</strike> ou qualquer outro formato.

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

As linhas acima "ocorrem" geralmente no estado de configuração e portanto assumimos que **não** existe um **request** em andamento. Um detalhe importante é o fato de que este estado é válido apenas para o **top level** module, ou seja, dentro do escopo de funções, views, classes etc o estado será outro.

#### 2 Estado de request

É quando seu app já foi iniciado e está **registrado** no servidor WSGI e então acontece uma requisição (algum cliente acessa uma url), neste momento o Flask irá popular o objeto request com os dados desta requisição e você poderá acessar o objeto request.


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

No exemplo acima acessamos os valores do objeto request, tanto os passados via GET(querystring) tanto quanto os passados via POST (formulário). Além disso acessamos a **current_app** para pegar as configs da app em execução. O **current_app** existe pois no Flask é possível ter mais de um objeto Flask em um único projeto e portanto precisamos de uma forma dinâmica de acessar o app em execução.

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

O objeto **request** é um **proxy** global que internamente garante você acesse a requisição atual ou *thread-local atual. Ele carrega dados referentes a cada requisição HTTP, nele podemos acessar as variáveis enviadas atráves da url ou de um formulário, podemos também verificar o método HTTP entre outros dados importantes que podem ser conferidos na [doc](http://flask.pocoo.org/docs/api/#incoming-request-data).

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

- request.**method**: Informa qual método HTTP foi usado na requisiçao
- request.**headers**: headers HTTP da requisição, útil para checar o mimetype e dados de basic auth.
- request.**environ**: Variáveis de ambiente do WSGI, navegador, ip do cliente etc
- request.**path**, request.url: O path ou a url completa da requisição
- request.**is_xhr**: Informa se é ou não uma requisição Ajax
- request.**blueprint**: Nome do blueprint que interceptou o request, Blue o que? -- Calma, veremos o que é isso mais adiante


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
curl --data "categoria=esportes&limit=10" http://localhost:5000/noticias
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
curl -X POST -d {"categoria": "esporte"} http://localhost:5000/noticias --header "Content-Type:application/json"
```

O restante é igual, basta usar o ``request.is_json`` para checar se a requisição é com JSON payload e então acessar os dados.

#### request.files / file uploads

Caso seu formulário ou API permitam o envio de arquivos esses dados serão colocados no ``request.files``. Isto ocorre pois internamente o Flask transforma os dados recebidos em um objeto **FileStorage** para permitir que você manipule os com mais facilidade.

Requisição: (equivale a um formulário com file upload)

```bash
curl --form "photo=@picture.jpg&item_id=12345" http://localhost:5000/change_photo
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

Antes de falar de "Session" precisamos falar de "Cookies", pois um não vive sem o outro! <3

Cookie é um "storage" de dados que é armazenado pelo cliente (browser, etc), os cookies trafegam via HTTP header e você pode ler e escrever cookies.

Existe uma série de [especificações](http://en.wikipedia.org/wiki/HTTP_cookie) a respeito, mas não entrarei nos detalhes, vamos apenas ver como manipula-los no Flask.

#### Escrevendo em um biscoito! (estranho isso né?)

Para escrever dados em um cookie usamos o objeto **Response**, portanto sempre que precisar escrever um cookie será necessário criar explicitamente um objeto **Response** para este fim.

```python
from flask import abort, make_response

@app.route('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if valid_login(username, password):
        response = make_response("Hello! Welcome back!")
        response.set_cookie('username', username)
        response.set_cookie('user_hash', get_hash(username))
        ...
        return response
    else:
        abort(403)
```

No exemplo acima validamos o username e o password e caso o usuário seja válido gravamos algumas informações no cookie.

> **DUMMY CODE ALERT:** O código acima é apenas um exemplo tosco, para controlar acesso recomendo o uso de Flask-Login ou Flask-Security

#### Lendo o biscoito (da sorte?)

Bom, assumindo que temos as informações **username** e **user_hash** gravadas no browser do cliente, e que este enviará este cookie no HEADER a cada requisição que fizer, podemos facilmente ler os dados contidos no cookie através do objeto **request**.

```python
from flask import request, redirect, url_for

@app.route('/')
def index():
    username = request.cookies.get('username')
    user_hash = request.cookies.get('user_hash')
    # request.cookies é um dict, portanto use o .get para evitar KeyError
    if is_logged(username, user_hash):
        return "Welcome!"
    else:
        redirect(url_for('login'))
```

Neste outro **DUMMY CODE** pegamos os dados que recebemos do cookie e usamos para veriricar se o usuário está logado ou algo do tipo.

#### Sessions

No Flask existe o objeto **session** que é também uma forma de armazenar informação que será persistida entre requests, na **session** você pode armazenar informações de controle de acesso e até mesmo preferencias do usuário.

As sessions dependem dos cookies, pois são indexadas atráves de um **SESSION_ID** que por padrão é sempre gravado em um cookie. Além disso o Flask por padrão guarda tembém os dados da **session** nos cookies, ou seja, os dados ficam lá do lado cliente, porém ele utiliza criptografia nesses dados, é possível visualizar o conteúdo deste cookie mas para alterar é sempre preciso assina-lo com a chave de criptografia correta e é para isso que serve a configuração **SECRET_KEY** lá nos config de seu app Flask.

```python
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

@app.route('/')
def index():
    if 'username' in session:
        return 'OLá, você está logado como %s' % escape(session['username'])
    return redirect(url_for('login'))

# O escape() precisa ser usado apenas se você não estiver usando um template.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None) # Apaga os dados de login lá da session
    return redirect(url_for('index'))


```

> **TIP:** Você pode armazenar as sessions em outro local diferente dos cookies se desejar, isto é útil quando você precisa manipular as sessions do lado servidor ou quando quer por exemplo saber quantos usuários estão com sessões abertas. Pode ser no memcached, banco SQL, redis ou MongoDB por exemplo. Uma ótima extensão para fazer isso é o [Flask-KVsession](https://github.com/mbr/flask-kvsession) baseado no simplekv.


### <a name="acessando_bando_de_dados_pequeno_exemplo_com_dataset" href="#acessando_bando_de_dados_pequeno_exemplo_com_dataset"> Acessando banco de dados (pequeno exemplo com dataset)</a>

Uma das vantagens do Flask é o fato dele não estar limitado a um ORM especifico para lidar com banco de dados, você poderá escolher entre SQlAlchemy, Peewee, Pony, MongoEngine etc. Você pode também fazer tudo na **unha** usando mysql-python ou Pymongo se preferir, enfim, a escolha é sua!

Em outro capítulo desta série mostrarei exemplos com o MongoEngine, mas nesta parte introdutória vamos usar o módulo [dataset](https://github.com/pudo/dataset) que é uma camada de abstração para ler e escrever dados nos bancos SQLite, MySQL ou Postgres.

A vantagem do dataset é que ele é incrivelmente simples, não exige especificação de **schema** e é puro Python.

Para começar instale o **dataset** na sua virtualenv.

```bash
(wtf_env)seuuser@suamaquina/path/to/wtf$ pip install dataset
```

> **NOTE:** O dataset vai instalar várias dependencias, entre elas estão o **alembic** para efetuar migrations automáticas e o **SQLAlchemy** para conexão e mapeamento.

### Escrevendo no banco de dados

agora na raiz do projeto vamos criar um arquivo novo chamado ``db.py``.

```python
# coding: utf-8

import dataset

db = dataset.connect('sqlite:///noticias.db')
noticias = db['noticias']
```

Agora crie um arquivo ``news_app.py`` e vamos inicialmente criar uma view contendo um formulário para **cadastro de novas notícias**.

> **NOTE:** Inicialmente não vamos nos preocupar com segurança, csrf ou login, mas nos próximos capítulos desta sério iremos evoluir este pequeno app.

```python
# coding: utf-8

from flask import Flask, request, url_for

from db import noticias


app = Flask("wtf")

# por enquanto vamos usar um template html hardcoded
# mas calma! em breve falaremos  sobre os templates com Jinja2
base_html = u"""
  <html>
  <head>
      <title>{title}</title>
  </head>
  <body>
     {body}
  </body>
  </html>
"""


@app.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        dados_do_formulario = request.form.to_dict()
        nova_noticia = noticias.insert(dados_do_formulario)
        return u"""
            <h1>Noticia id %s inserida com sucesso!</h1>
            <a href="%s"> Inserir nova notícia </a>
        """ % (nova_noticia, url_for('cadastro'))
    else:  # GET
        formulario = u"""
           <form method="post" action="/noticias/cadastro">
               <label>Titulo:<br />
                    <input type="text" name="titulo" id="titulo" />
               </label>
               <br />
               <label>Texto:<br />
                    <textarea name="texto" id="texto"></textarea>
               </label>
               <input type="submit" value="Postar" />
           </form>
        """
        return base_html.format(title=u"Inserir nova noticia", body=formulario)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
```

Salve e execute seu aplicativo ``python news_app.py`` e acesse [http://localhost:5000/noticias/cadastro](http://localhost:5000/noticias/cadastro)

Você verá um formulário com os campos **titulo** e **texto**, insira uma notícia nova e repita o processo algumas vezes. Note que na raiz de seu projeto agora terá um banco de dados SQLite **noticias.db**.

### Lendo do banco de dados

Abra o arquivo ``news_app.py`` e após a linha 39 vamos incluir uma view para listar todas as notícias na home do site.

```python
@app.route("/")
def index():

    noticia_template = u"""
        <a href="/noticia/{noticia[id]}">{noticia[titulo]}</a>
    """

    # it's a kind of magic :)
    todas_as_noticias = [
        noticia_template.format(noticia=noticia)
        for noticia in noticias.all()
    ]

    return base_html.format(
        title=u"Todas as notícias",
        body=u"<br />".join(todas_as_noticias)
    )
```

Agora ao acessar [localhost:5000](http://localhost:5000) Você verá uma lista de links com os títulos das notícias que cadastrou!

Só falta agora uma última view que será a utilizada para exibir a notícia quando você clicar no link.

```python
@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    noticia = noticias.find_one(id=noticia_id)  # query no banco de dados
    noticia_html = u"""
        <h1>{titulo}</h1>
        <p>{texto}</p>
    """.format(**noticia)  # remember, Python is full of magic!

    return base_html.format(title=noticia['titulo'], body=noticia_html)
```


Seu app de cadastro e leitura de notícias está pronto!

A versão completa pode ser encontrada [neste link](https://gist.github.com/rochacbruno/5ed42779bbb8d7738d71), salve o arquivo e execute ``python news_app.py`` acesse [localhost:5000](http://localhost:5000) e agora você terá a lista de notícias e poderá clicar em cada uma delas para ler seu conteúdo.

> **CALMA:** Falta muita coisa ainda, ainda precisa de login, segurança contra csrf, sanitizar o html da notícia, permitir que a notícia seja alterada e etc..


### <a name="servindo_arquivos_estaticos" href="#servindo_arquivos_estaticos"> Servindo arquivos estáticos</a>

Arquivos estáticos são todos os arquivos que você deseja entregar ao cliente sem a necessidade de processar, ou seja, sem a necessidade de efetuar nenhum tipo de computação dentro do Flask.

Geralmente arquivos JavaScript, CSS, imagens, videos, documentos etc são incluidos nesta categoria. Para evitar o **overhead** de processamento ao servir estes arquivos o **ideal** é sempre delegar esta tarefa ao servidor web que estiver sendo usado, isto é fácil de ser feito no Nginx e também no Apache, para isso esses servidores mapeiam um padrão de url, por exemplo todas as urls contendo:  ``/static/*.[jpg|png|gif|css...]`` e servem estes arquivos diretamente sem passar pelo servidor de palicação (o WSGI).

Porém durante o desenvolvimento você vai precisar servir estes arquivos enquanto testa, para isso o Flask implementa um endpoint especifico que pode ser configurado ao iniciar a aplicação e também oferece um template tag que ajuda a resolver esse caminho dinamicamente nos templates.

> **TIP:** É possivel definir um endpoint dinâmico para os arquivos estáticos e desta forma hospedar em um CDN ou em serviços externos como Amazon S3, Akamai ou Dropbox.

#### Definindo a pasta e o endpoint dos arquivos estáticos

No arquivo ``wtf/news_app.py`` da nossa app de notícias criarmos uma instância a app com ``Flask('wtf')`` sem passar nenhum parâmetro adicional, neste caso o Flask irá assumir o comportamento default que é ter uma pasta de estáticos localizada em ``wtf/static`` e o endpoint de estáticos mapeado para ``/static/`` e na maioria dos casos esta convenção irá atender perfeitamente.

Caso você precise especificar um caminho diferente para os arquivos físicos ou um mapeamento de url diferente poderá informar ao Flask através dos seguintes parâmetros:

```python
app = Flask("wtf", static_folder='assets', static_url_path="assets_v1")
```

No exemplo acima agora os arquivos estáticos deverão ficar em uma pasta ``wtf/assets`` e a url para acessa-los será ``localhost:8000/assets_v1/arquivo.ext`` ao invés de ``/static/arquivo.ext``.


#### Mão na massa

Crie uma nova pasta ``wtf/static`` e salve o seguinte arquivo dentro dela

Clique com o botão direito do mouse e escolha "salvar imagem..."

![https://jobs.github.com/images/modules/company/generic_logo.gif](https://jobs.github.com/images/modules/company/generic_logo.gif)

Agora modifique o ``news_app.py`` e vamos exibir este logotipo na página inicial, para isso primeiro altere o ``base_html`` incluindo o placeholder ``{{logo_url}}``.


```python
base_html = u"""
  <html>
  <head>
      <title>{title}</title>
  </head>
  <body>
     <img src="{logo_url}" />
     <hr />
     {body}
  </body>
  </html>
"""
```

Agora altere o retorno das views incluindo a variavel **logo_url**, por exemplo na view ``cadastro`` altere para:

```python
        return base_html.format(
            title=u"Inserir nova noticia",
            body=formulario,
            logo_url=url_for('static', filename='generic_logo.gif')
        )
```

Repita o procedimento para as outras 2 views incluindo o trecho ``logo_url=url_for('static', filename='generic_logo.gif')`` no .format.

O helper ``url_for`` criou dinâmicamente uma url completa apontando par ao nosso arquivo estático, e se por acaso mudarmos os valores de static_folder e static_path não teremos que nos preocupar com a mudança das urls em nossos templates html pois o uso do endpoint especial **static** no url_for garante isso.

> **TIP:** Os preguiçosos podem baixar o [arquivo](https://gist.github.com/rochacbruno/71e874ac18177b22a31a).

#### Gravando e servindo arquivos de MEDIA

Geralmente chamamos de arquivos de MEDIA aqueles arquivos que não fazem parte da estrutura do nosso site, enquanto os css e js e também imagens do layout e logotipos são fixos de nossa estrutura. Uma foto de um usuário ou um documento .doc ou .pdf anexado a uma notícia são contéudo dinâmico que precisaremos servir do mesmo modo que servimos os arquivos estáticos.

Resolver isso no Flask é uma tarefa relativamente fácil, vamos começar com os uploads de arquivos.

#### Upload de arquivos

Agora para cada notícia o usuário também poderá incluir uma imagem, vamos implementar o upload desta imagem.

Inicialmente crie uma nova pasta ``wtf/media_files`` e edite as primeiras linhas do ``news_app.py`` incluindo a configuração do local onde os arquivos de media serão armazenados.


```python
# coding: utf-8

import os

from flask import Flask, request, url_for

from db import noticias

app = Flask("wtf")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')

```

A config "MEDIA_ROOT" irá guardar o caminho absoluto para a pasta ``../wtf/media_files``

Agora edite a view de cadastro de notícias:

1. inclua ``enctype="multipart/form-data"`` no html do formulário para permitir uploads.
2. Insira um campo para upload de arquivo
3. importe o ``current_app`` para poder acessar os configs da app em execução e o `secure_filename`` para garantir um nome válido para o upload
4. implemente o upload da imagem utilizando o ``request.files`` e salve o caminho da imagem junto com a notícia


```python
...

from werkzeug import secure_filename

from flask import Flask, request, url_for, current_app

...

@app.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        dados_do_formulario = request.form.to_dict()
        imagem = request.files.get('imagem')
        if imagem:
            filename = secure_filename(imagem.filename)
            path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
            imagem.save(path)
            dados_do_formulario['imagem'] = filename
        nova_noticia = noticias.insert(dados_do_formulario)
        return u"""
            <h1>Noticia id %s inserida com sucesso!</h1>
            <a href="%s"> Inserir nova notícia </a>
        """ % (nova_noticia, url_for('cadastro'))
    else:  # GET
        formulario = u"""
           <form method="post" action="/noticias/cadastro"
             enctype="multipart/form-data">
               <label>Titulo:<br />
                    <input type="text" name="titulo" id="titulo" />
               </label>
               <br />
               <label>Texto:<br />
                    <textarea name="texto" id="texto"></textarea>
               </label>
               <br />
               <label> Imagem:<br />
                  <input type="file" name="imagem" id="imagem" />
               </label>
               <input type="submit" value="Postar" />
           </form>
        """
        return base_html.format(
            title=u"Inserir nova noticia",
            body=formulario,
            logo_url=url_for('static', filename='generic_logo.gif')
        )

```

Com isso pode acessar [localhost:5000/noticias/cadastro](http://localhost:5000/noticias/cadastro) e inserir uma notícia com imagem!

Se preferir faça [download](https://gist.github.com/rochacbruno/00adfb0145797fb95c76) da versão completa do ``news_app.py``


#### Servindo os arquivos de media

Agora vamos fazer com que a imagem inserida na notícia seja mostrada na página dela junto com o seu texto. Nós já vimos que o Flask tem um endpoint **static** para servir os arquivos estáticos da pasta padrão, porém no nosso caso os arquivos estão localizados em outra pasta, a **media_files**, teremos que criar uma view para servir estes arquivos.

Comece importando a fuinção ``send_from_directory`` lá no inicio do ``news_app.py``

```python
from flask import Flask, request, url_for, current_app, send_from_directory
```

Agora vamos incluir uma nova view após a linha 104:

```python
@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)
```

Esta view será responsável por pegar o arquivo do diretório e fazer stream para o cliente. O próximo passo e construir a url usando o endpoint **media** que é o nome da view.

Altere a view **noticia** incluindo a imagem no html e resolvendo a url para a imagem correspondente com o url_for, caso a notícia não possua imagem usaremos uma imagem padrão.


```python
@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    noticia = noticias.find_one(id=noticia_id)  # query no banco de dados
    if noticia.get('imagem'):
        imagem_url = url_for('media', filename=noticia.get('imagem'))
    else:
        imagem_url = "http://placehold.it/100x100"

    noticia_html = u"""
        <h1>{titulo}</h1>
        <img src="{imagem_url}">
        <hr />
        <p>{texto}</p>
    """.format(
        imagem_url=imagem_url,
        **noticia
    )  # remember, Python is full of magic!

    return base_html.format(
        title=noticia['titulo'],
        body=noticia_html,
        logo_url=url_for('static', filename='generic_logo.gif')
    )

```

Faça o [download](https://gist.github.com/rochacbruno/27fc63e46966aeca89a0) da versão com exibição de imagens.

Agora acesse as noticias que cadastrou com imagem para visualizar a imagem junto com a notícia. :)


### <a name="template_com_jinja_2" href="#template_com_jinja_2"> Templates com Jinja2</a>

Até agora escrevemos HTML diretamente em strings no ``news_app.py``, porém conforme o app vai crescendo começa a ficar impossível dar manutenção nesses templates hardcoded, sem contar que é mais interessante ter isso em uma camada separada possibilitando a substituição a qualquer momento.

No Flask você até pode escolher utilizar um outro engine de templates como o Mako, Genshi, TAL etc, porém o padrão implementado no **render_template** do Flask é o Jinja2.

O Jinja2 foi inspirado na sintaxe do sistema de templates do Django e é muito fácil de utilizar. Para este nosso app de notícias você precisará saber apenas alguns conceitos do Jinja2, mas no decorrer desta série exploraremos outros assuntos mais avançados como criação de macros, template loaders e extensões.

#### Base template

Todo site tem um layout comum que se repete em todas as páginas, geralmente onde fica a barra superior, os menus, o logotipo e o rodapé. Para não precisar ficar repetindo essa parte do código no template de todas as páginas é comum criarmos um base template e depois ir estendendo ele nos outros templates.

Exemplo:

base.html
```html
<html>
<body>
    {% block topo %}
    <img src="logo.png"><br />
    <menu><ul><li>HOME</li><li>CADASTRO</li></ul></menu>
    {% endblock %}
    <hr />
    {% block content%}<!-- page content -->{% endblock%}
</body>
</html>
```

Repare que no exemplo acima usamos a tag ``{% block <block_name> %}`` para definir uma area no template que poderá ser sobrescrita pelos templates que estenderem o template base.

#### Estendendo o template base

Agora imagine que vamos criar o template que vai exibir a lista de notícias.

```html
{% extends "base.html" %}
{% block content %}
    <ul>
       {% for noticia in noticias %}
           <li>{{noticia['titulo']}}</li>
       {% endfor %}
    </ul>
{% endblock %}
```

Repare desta vez que não foi necessário reescrever o html básico e nem o bloco do menu, apenas sobrescrevemos o bloco **content** e dentro dele montamos a lista de notícias.

O Jinja2 aceita um subset limitado da linguagem Python, ou seja, você pode usar Python nos templates, mas não pode fazer qualquer coisa. O mais indicado é que você limite-se a usar o básico que são os loops e as expressões condicionais, além é claro dos statements da própria linguagem de templates.

No Jinja os statements do template engine, as tags customizadas e código Python devem ficar entre "{%" e "%}". Já a "impressão" de valores no html é feita entre "{{" e "}}", sendo que esta sintaxe pode até ser customizada para qualquer outra combinação que você preferir.

Uma outra caracteristica interessante é que nos templates chaves de dicionários podem ser acessadas via **.** ou via **[ ]** os dois casos funcionam. exemplo: ``{{ noticia['titulo'] }}`` ou ``{{ noticia.titulo }}``


#### definindo a pasta de templates

Assim como no caso dos estáticos o Flask já tem um padrão que é sempre procurar os templates em uma pasta chamada ``templates`` mas você pode alterar este caminho se preferir.

```python
app = Flask('wtf', templates_folder='outra_pasta_de_templates')
```

No nosso caso vamos utilizar o padrão e criar uma nova pasta ``wtf/templates`` e dentro desta pasta crie um novo arquivo chamado ``wtf/templates/base.html`` e vamos usa-lo para substituir a variavel ``base_html`` no ``news_app.py``.

Crie orquivo ``templates/base.html`` e apague a variavel ``base_html`` do ``news_app.py``

```html
<html>
<head>
    <title>{% block title %} {{title or "Notícias"}} {% endblock %}</title>
</head>
<body>
   <img src="{{url_for('static', filename='generic_logo.gif')}}">
   <nav>
       <a href="{{url_for('index')}}">HOME</a> | <a href="{{url_for('cadastro')}}">CADASTRO</a>
   </nav>
   <hr />
   {% block content %} {% endblock %}
</body>
</html>

```

Desta maneira podemos utilizar o helper **url_for** direto no template para acessar os arquivos estáticos. Repare também que fizemos uma impressão condicional em ``{{ title or "Notícias"}}`` isso é possível pois no Jinja2 qualquer variável não existente é avaliada como **None**, este mesmo trecho poderia ser escrito da seguinte maneira ``{{ title|default("Notícias") }}``

Agora vamos criar um template para a home do site, onde a lista de notícias é exibida.

Crie o arquivo ``templates/index.html``

```html
{% extends "base.html" %}
{% block content %}
<ul>
    {% for noticia in noticias %}
    <li>
        <a href="{{url_for('noticia', noticia_id=noticia.id)}}">
         {{noticia.titulo}}
        </a>
    </li>
    {% endfor %}
</ul>
{% endblock %}
```

Neste exemplo utilizamos um loop ``for`` para iterar sobre a lista de noticias que será passada pela view, também usamos o url_for para criar a url que levará para a página de leitura da notícia.

Agora crie agora o template da página da notícia em ``templates/noticia.html``

```html
{% extends "base.html" %}
{% block title%}
    {{noticia.titulo}}
{% endblock%}

{% block content %}
    <h1>{{noticia.titulo}}</h1>
    {% if noticia.imagem %}
        <img src="{{ url_for('media', filename=noticia.imagem) }}" width="300" />
    {% endif %}
    <hr />
    <p>
        {{noticia.texto}}
    </p>
{% endblock %}

```

Agora falta apenas o template para o formulário de cadastro de nova notícia e basta copiar e colar o html da variavel formulário para um template chamado ``templates/cadstro.html`` e fazer pequenas alterações.


```html
{% extends "base.html" %}
{% block content %}
<form method="post" action="{{ url_for('cadastro') }}" enctype="multipart/form-data">
   <label>Titulo:<br />
        <input type="text" name="titulo" id="titulo" />
   </label>
   <br />
   <label>Texto:<br />
        <textarea name="texto" id="texto"></textarea>
   </label>
   <br />
   <label> Imagem:<br />
      <input type="file" name="imagem" id="imagem" />
   </label>
   <input type="submit" value="Postar" />
</form>
{% endblock %}
```

Vamos criar também um template para exibir uma mensagem de sucesso ao inserir nova notícia em ``templates/cadastro_sucesso.html``

```html
{% extends "base.html" %}
{% block title %}
    Notícia {{id_nova_noticia}} inserida com sucesso
{% endblock %}

{% block content %}
    <h1>Notícia {{id_nova_noticia}} inserida com sucesso!</h1>
    <a href="{{url_for('noticia', noticia_id=id_nova_noticia)}}"> Ler Notícia </a><br />
    <a href="{{url_for('cadastro')}}"> Cadastrar nova notícia </a>
{% endblock %}
```

Após salvar os 5 arquivos de template base.html, index.html, noticia.html, cadastro.html e cadastro_sucesso.html dentro da pasta templates, altere o ``news_app.py`` para usar a função **render_template** que recebe como parâmetros o nome do template e as variaveis que estarão disponíveis no escopo do template.

```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Flask, request, current_app, send_from_directory, render_template
)

from db import noticias

app = Flask("wtf")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
app.config['MEDIA_ROOT'] = os.path.join(PROJECT_ROOT, 'media_files')


@app.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":

        dados_do_formulario = request.form.to_dict()
        imagem = request.files.get('imagem')

        if imagem:
            filename = secure_filename(imagem.filename)
            path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
            imagem.save(path)
            dados_do_formulario['imagem'] = filename

        id_nova_noticia = noticias.insert(dados_do_formulario)
        return render_template('cadastro_sucesso.html',
                                id_nova_noticia=id_nova_noticia)

    return render_template('cadastro.html', title=u"Inserir nova noticia")


@app.route("/")
def index():
    todas_as_noticias = noticias.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")


@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    noticia = noticias.find_one(id=noticia_id)
    return render_template('noticia.html', noticia=noticia)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
```

Após salvar os templates e o news_app.py modificado reinicie o serviço flask no terminal usando CTRL+C e executando novamente ``python news_app.py``. Isso é necessário pois o Flask cria o cache de templates no momento da inicialização do aplicativo.

Acesse o app via [localhost:5000](http://localhost:5000) e veja que agora a barra de menu se mantém em todas as páginas.


O aplicativo completo pode ser obtido no [repositorio do github](https://github.com/rochacbruno/wtf).

> **END:** Sim chegamos ao fim desta primeira parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas 5 partes iremos nos aprofundar em boas práticas, uso e desenvolvimento de extensões e blueprints e também questṍes relacionados a deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Estou iniciando um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CurdoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)


Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções ou bitcoins (LOL) na caixa de comentários abaixo.

Abraço! "Python é vida!"




























