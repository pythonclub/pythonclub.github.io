Title: What the Flask? Pt-3 Plug & Use - extensões essenciais para iniciar seu projeto
Slug: what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto
Date: 2015-10-23 00:00
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



What The Flask - 3/6
-----------

> Finalmente!!! A terceira parte da série **What The Flask**, mas ainda não acabou, serão 6 artigos para se tornar um **Flasker**, neste capítulo falaremos sobre como instalar e configurar as principais extensões do Flask para torna-lo uma solução full-stack com bootstrap no front-end, ORM para banco de dados, admin parecido com o Django Admin, Cache, Sistema de filas (celery/huey), Controle de Acesso, Envio de email, API REST e Login Social.

<figure style="float:left;margin-right:30px;width:35%">
<img src="/images/rochacbruno/lego_snake.jpg" alt="snake" >
<figcaption>Extending Flask</figcaption>
</figure>

1. [**Hello Flask**](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask): Estruturando aplicações Flask
3. [**Plug & Use**](/what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto): extensões essenciais para iniciar seu projeto. **<-- Você está aqui**
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask e para o Jinja2
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.

<br>

> **Micro framework?** Bom, o Flask foi criado com a premissa de ser um micro-framework, o que significa que ele não tem a intenção de entregar de bandeja para você todas as coisas que você precisa em único pacotinho e nem comandos mágicos que você roda e instantaneamente tem todo o seu projeto pronto. A idéia do Flask é ser pequeno e te dar o controle de tudo o que acontece no seu aplicativo, mas ao mesmo tempo o Flask se preocupa em ser facilmente extensivel, para isso os desenvolvedores pensaram em padrões que permitem que as extensões sejam instaladas de modo que não haja conflitos (lembra dos BluePrints do capítulo anterior?), além dos BluePrints tem também os patterns para desenvolvimento de extensions que ajuda a tornar a nossa vida mais fácil, nesta parte dessa série vamos instalar e configurar algumas das principais extensões do Flask (todas testadas por mim em projetos reais).


# CMS de notícias

Nesta série estamos desenvolvendo um mini CMS para publicação de notícias, o código está disponível no [github](http://github.com/rochacbruno/wtf) e para cada fase da evolução do projeto tem uma branch diferente. Esse aplicativo de notícias tem os seguintes requisitos:

- Banco de dados MongoDB
- Controle de acesso para que apenas editores autorizados publiquem notícias
- Interface administrativa para notícias, categorias, tags, media e usuários
- Front end usando o Bootstrap
- Cache das notícias para minimizar o acesso ao banco de dados
- Banco de dados MongoDB

> **NOTE:** Existem várias extensões para Flask, algumas são aprovadas pelos desenvolvedores e entram para a lista disponível no site oficial, algumas entram para a listagem do metaflask (projeto em desenvolvimento), e uma grande parte está apenas no github. Como existem várias extensões que fazem a mesma coisa, as vezes é dificil escolher qual delas utilizar, eu irei mostrar aqui apenas as que eu utilizo e que já tenho experiência, mas isso não quer dizer que sejam as melhores, sinta-se a vontade para tentar com outras e incluir sua sugestão nos comentários.

- [Flask Bootstrap](#bootstrap) - Para deixar as coisas bonitinhas
- [Flask MongoEngine](#mongoengine) - Para armazenar os dados em um banco que é fácil fácil!
- [Flask Security](#flask_security) - Controle de acesso
- [Flask-Admin](#flask_admin) - Um admin tão poderoso quanto o Django Admin
- [Flask Cache](#flask_cache) - Para não estressar o Mongo

> **TL;DR:** A versão final do app deste artigo esta no [github](https://github.com/rochacbruno/wtf/tree/extended), os apressados podem querer executar o app e explorar o seu código antes de ler o artigo completo.

## <a href="#bootstrap" name="bootstrap">Deixando as coisas bonitinhas com o Bootstrap!</a>

Atualmente a versão do nosso CMS está funcional porém bem feinha, não trabalhamos no design das páginas pois obviamente este não é o nosso objetivo, mas mesmo assim podemos deixar as coisas mais bonitinhas.

<figure style="border:1px solid black;">
<img src="/images/rochacbruno/wtf_index.png" alt="wtf_index" >
<figcaption>Atual Layout do nosso CMS</figcaption>
</figure>

Com a ajuda do Bootstrap e apenas uns ajustes básicos no front end podemos transformar o layout em algo muito mais apresentável.

Usaremos a extensão Flask-Bootstrap que traz alguns templates de base e utilidades para uso do Bootstrap no Flask.

Comece editando o arquivo de requirements adicionando **Flask-Bootstrap**

Arquivo **requirements.txt**
```
https://github.com/mitsuhiko/flask/tarball/master
dataset
nose
Flask-Bootstrap
```


Agora instale as dependencias em sua virtualenv.

```bash
pip install -r requirements.txt --upgrade
```


Agora com o Flask-Bootstrap instalado basta iniciarmos a extensão durante a criação de nosso app.

Editando o arquivo **news_app.py** incluiremos:

```python
...
from flask_bootstrap import Bootstrap

def create_app(mode):
    ...
    ...
    Bootstrap(app)
    return app
```

Sendo que o arquivo completo ficaria:

```python
# coding: utf-8
from os import path
from flask import Flask
from .blueprints.noticias import noticias_blueprint
from flask_bootstrap import Bootstrap


def create_app(mode):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "%s_instance" % mode
    )

    app = Flask("wtf",
                instance_path=instance_path,
                instance_relative_config=True)

    app.config.from_object('wtf.default_settings')
    app.config.from_pyfile('config.cfg')

    app.config['MEDIA_ROOT'] = path.join(
        app.config.get('PROJECT_ROOT'),
        app.instance_path,
        app.config.get('MEDIA_FOLDER')
    )

    app.register_blueprint(noticias_blueprint)

    Bootstrap(app)
    return app
```


As extensões Flask seguem dois padrões de inicialização: Imediato e Lazy, é recomendado que toda extensão siga este protocolo.

Inicialização imediata:

```python
from flask_nome_da_extensao import Extensao
app = Flask(__name__)
Extensao(app)
```

Da forma acima sempre importamos uma classe com o nome da extensao e então passamos o nosso **app** como parametro na inicialiação da extensão. Assim durante o init da extensão ela poderá injetar templates, modificar rotas e adicionar configs no app que foi passado como parametro.

Inicialização Lazy:

```python
from flask_nome_da_extensao import Extensao
app = Flask(__name__)
extensao = Extensao()  # note que não é passado nada como parametro!


# em qualquer momento no seu código
Extensao.init_app(app)
```

Geralmente o primeiro modo **inicio imediato** é o mais utilizado, o carregamento Lazy é útil em situações mais complexas como por exemplo se o seu sistema estiver esperando a conexão com um banco de dados.

> NOTE: Toda extensão do Flask deve começar com o nome **flask_** para ser considerada uma extensão dentro dos padrões.

No nosso caso utilizamos **Bootstrap(app)** e agora o bootstrap já está disponível para ser utilizado em nossos templates!

### Customizando os templates com o BootStrap.

Precisaremos efetuar algumas mudanças nos templates para que eles utilizem os estilos do Bootstrap 3.x

> Não entrarei em detalhes a respeito da estensão Flask-Bootstrap pois temos mais uma série de extensões para instalar, mas você pode consultar a [documentação oficial](https://pythonhosted.org/Flask-Bootstrap/basic-usage.html) para saber mais a respeito dos blocos de template e utilidades disponíveis.

### Comece alterando o template **base.html** para:

```html
{%- extends "bootstrap/base.html" %}
{% import "bootstrap/utils.html" as utils %}
{% block title %} {{title or "Notícias"}} {% endblock %}
{% block navbar -%}
    <nav class="navbar navbar-default">
       <a class="navbar-brand" href="#"><img src="{{url_for('static', filename='generic_logo.gif')}}" style="height:30px;"></a>
       <ul class="nav navbar-nav">
         <li><a href="{{url_for('noticias.index')}}">HOME</a> </li>
         <li><a href="{{url_for('noticias.cadastro')}}">CADASTRO</a></li>
       </ul>
    </nav>
{%- endblock navbar %}

{% block content %}
 <div class="container">
    <div class="jumbotron">
      {% block news %}
      {% endblock %}
    </div>
{%- endblock content%}
```

Algumas coisas continuaram iguais ao template antigo, porém agora estamos utilizando blocos **navbar** e **content** definidos pelo Flask-Bootstrap e criamos um novo bloco **news** que usaremos para mostras as nossas notícias.

### Altere o template index.html

```html
{% extends "base.html" %}
{% block news %}
<h1>Todas as notícias</h1>
<ul>
    {% for noticia in noticias %}
    <li>
        <a href="{{url_for('noticias.noticia', noticia_id=noticia.id)}}">
         {{noticia.titulo}}
        </a>
    </li>
    {% endfor %}
</ul>
{% endblock %}

```

apenas mudamos o nome do bloco utilizado de **content** para **news** e adicionamos um título.

### Altere o template noticia.html

```html
{% extends "base.html" %}
{% block title%}
    {{noticia.titulo}}
{% endblock%}

{% block news %}
    <h1>{{noticia.titulo}}</h1>
    {% if noticia.imagem %}
        <img src="{{ url_for('noticias.media', filename=noticia.imagem) }}" width="300" />
    {% endif %}
    <hr />
    <p>
        {{noticia.texto|safe}}
    </p>
{% endblock %}
```

Novamente mudamos o bloco principal de **content** para **news**

### Altere os templates cadastro.html e cadastro_sucesso.html

Altere o bloco utilizado de **content** para **news** e o restante deixe como está por enquanto.

```html
{% extends "base.html" %}
{% block news %}
<form method="post" action="{{ url_for('noticias.cadastro') }}" enctype="multipart/form-data">
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

### Resultado Final!

Antes do bootstrap

<figure style="border:1px solid black;">
<img src="/images/rochacbruno/wtf_index.png" alt="wtf_index" >
</figure>

e depois:

<figure>
<img src="/images/rochacbruno/bootstrap.png" alt="wtf_index_bootstrap" >
</figure>



> O diff com as mudanças que foram feitas pode ser acessado neste [link](https://github.com/rochacbruno/wtf/commit/5645de0fb208fc9ee34e502d901c057c9a3f2445)


Agora que o app já está com uma cara mais bonita, vamos passar para o próximo requisito: Banco de Dados.

Até agora usamos o **dataset** que é uma mão na roda! integrando facilmente o nosso projeto com bancos como MySQL, Postgres ou SQLite.

Porém nosso site de notícias precisa utilizar **MongoDB** e para isso vamos recorrer ao **Flask-MongoEngine**

## <a href="#mongoengine" name="mongoengine"> Utilizando MongoDB com Flask</a>

Vamos migrar do Dataset + SQlite para MongoDB e obviamente você irá precisar do MongoDb Server rodando, você pode preferir instalar o Mongo localmente se estiver em uma máquina Linux/Debian: ``sudo apt-get install mongodb`` ou siga instruções no site oficial do Mongo de acordo com seu sistema operacional.

Uma opção melhor é utilizar o **docker** para executar o MongoDB, desta forma você não precisa instalar o servidor de banco de dados em seu computador, precisa apenas do Docker e da imagem oficial do Mongo.

Vou mostrar os preocedimentos para instalação e execução no Linux/Debian, mas você pode tranquilamente utilizar outro S.O bastando seguir as instruções encontradas no site do docker.

#### Instalando o docker

No linux a maneira mais fácil de instalar o Docker é rodando o seguinte comando

```
wget -qO- https://get.docker.com/ | sh
```

Se você precisar de ajuda ou estiver usando um sistema operacional alternativo pode seguir as [instruções do site oficial](http://docs.docker.com/linux/started/)


#### Executando um container MongoDB

No DockerHub está disponível a imagem oficial do Mongo, basta executar o comando abaixo para ter o Mongo rodando em um container.

```
docker run -d -v $PWD/mongodata:/data/db -p 27017:27017 mongo
```

A parte do ``$PWD/mongodata:`` pode ser substituida pelo caminho de sua preferencia, este é o local onde o Mongo irá salvar os dados.

> Se preferir executar no modo efemero (perdendo todos os dados ao reiniciar o container) execute apenas ``docker run -d -p 27017:27017 mongo``


#### Instalando o MongoDB localmente (não recomendado, use o docker!)

Você pode preferir não usar o Docker e instalar o Mongo localmente, [baixe o mongo](https://www.mongodb.org/downloads) descompacte, abra um console separado e execute: ``./bin/mongod --dbpath /tmp/`` lembrando de trocar o ``/tmp`` por um diretório onde queira salvar seus dados.

Se preferir utilize os pacotes oficiais do seu sistema operacional para instalar o Mongo.

> IMPORTANTE: Para continuar você precisa ter uma instância do MongoDB rodando localmente, no Docker ou até mesmo em um servidor remoto se preferir.

## Flask-Mongoengine

Adicione a extensão Flask-Mongoengine ao seu arquivo requirements.txt

```
https://github.com/mitsuhiko/flask/tarball/master
flask-mongoengine
nose
Flask-Bootstrap
```

Agora execute ``pip install -r requirements.txt --upgrade`` estando na virtualenv de seu projeto.

### Substituindo o Dataset pelo MongoEngine

Agora vamos substituir o **dataset** pelo **MongoEngine**, por padrão o MongoEngine tentará conectar no **localhost** na porta **27017** e utilizar o banco de dados **test**. Mas no nosso caso é essencial informarmos exatamente as configurações desejadas.

No arquivo de configuração em ``development_instance/config.cfg`` adicione as seguintes linhas:

```python
MONGODB_DB = "noticias"
MONGODB_HOST = "localhost"  # substitua se utilizar um server remoto
MONGODB_PORT = 27017
```

Agora vamos ao arquivo ``db.py`` vamos definir a conexão com o banco de dados Mongo, apague todo o conteúdo do arquivo e substitua por:

**db.py**

```python
# coding: utf-8
from flask_mongoengine import MongoEngine
db = MongoEngine()
```

Crie um novo arquivo chamado **models.py**, é nesse arquivo que definiremos o esquema de dados nas nossas notícias. Note que o Mongo é um banco schemaless, poderiamos apenas criar um objeto **Noticia(db.DynamicDocument)** usando herança do DynamicDocument e isso tiraria a necessidade da definição do schema, porém, na maioria dos casos definir um schema básico ajuda a construir formulários e validar os dados.


**models.py**

```python
# coding: utf-8
from .db import db


class Noticia(db.Document):
    titulo = db.StringField()
    texto = db.StringField()
    imagem = db.StringField()

```

Nosso próximo passo é alterar as views para que o armazenamento seja feito no MongoDB ao invés do SQLite.

No MongoEngine algumas operações serão um pouco diferente, alguns exemplos:

**Criar um novo registro de Noticia**

```python
Noticia.objects.create(titulo='Hello', texto='World', imagem='caminho/imagem.png')
```

**Buscar todas as Noticias**

```python
Noticia.objects.all()
```

**Buscar uma noticia pelo id**
```python
Noticia.objects.get(id='xyz')
```


Altere ``blueprints/noticias.py`` para:

```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, request, current_app, send_from_directory, render_template
)
from ..models import Noticia

noticias_blueprint = Blueprint('noticias', __name__)


@noticias_blueprint.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        dados_do_formulario = request.form.to_dict()
        imagem = request.files.get('imagem')
        if imagem:
            filename = secure_filename(imagem.filename)
            path = os.path.join(current_app.config['MEDIA_ROOT'], filename)
            imagem.save(path)
            dados_do_formulario['imagem'] = filename
        nova_noticia = Noticia.objects.create(**dados_do_formulario)
        return render_template('cadastro_sucesso.html',
                               id_nova_noticia=nova_noticia.id)
    return render_template('cadastro.html', title=u"Inserir nova noticia")


@noticias_blueprint.route("/")
def index():
    todas_as_noticias = Noticia.objects.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")


@noticias_blueprint.route("/noticia/<noticia_id>")
def noticia(noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    return render_template('noticia.html', noticia=noticia)


@noticias_blueprint.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)
```

Lembre-se que nós ainda não conectamos ao Mongo Server apenas definimos como será a conexão, então precisaremos agora usar o método lazy de inicialização de extensões chamando o ``init_app()`` do MongoEngine.

No arquivo ``news_app.py`` adicione as seguintes linhas.

```python
...
from db import db

def create_app(mode):
    ...
    db.init_app(app)
    return app
```

Sendo que o arquivo final será:

```python
# coding: utf-8
from os import path
from flask import Flask
from .blueprints.noticias import noticias_blueprint
from flask_bootstrap import Bootstrap
from db import db


def create_app(mode):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "%s_instance" % mode
    )

    app = Flask("wtf",
                instance_path=instance_path,
                instance_relative_config=True)

    app.config.from_object('wtf.default_settings')
    app.config.from_pyfile('config.cfg')

    app.config['MEDIA_ROOT'] = path.join(
        app.config.get('PROJECT_ROOT'),
        app.instance_path,
        app.config.get('MEDIA_FOLDER')
    )

    app.register_blueprint(noticias_blueprint)

    Bootstrap(app)
    db.init_app(app)
    return app
```

Execute o programa

```python
python run.py
```

E veja se consegue inserir algumas noticias acessando [http://localhost:5000](http://localhost:5000)

Para explorar os dados do MongoDB visualmente você pode utilizar o RoboMongo.

<figure>
<img src="/images/rochacbruno/robomongo.png" alt="wtf_robomongo" >
</figure>

> O Diff das alterações que fizemos relativas ao Flask-MongoEngine podem ser comparadas nos seguintes commits [88effa01b5ffd11f3fd7d5530f90591e421dd109](https://github.com/rochacbruno/wtf/commit/88effa01b5ffd11f3fd7d5530f90591e421dd109) e [189f4d4d2c8af845ccc0b181e4f6a1831578fbfa](https://github.com/rochacbruno/wtf/commit/189f4d4d2c8af845ccc0b181e4f6a1831578fbfa)

## <a href="#flask_security" name="flask_security">Controle de acesso com o Flask Security</a>

Nosso CMS de notícias está inseguro, ou seja, qualquer um que acessar a url [http://localhost:5000/noticias/cadastro](http://localhost:5000/noticias/cadastro) vai conseguir adicionar uma nova notícia sem precisar efetuar login.

Para resolver este tipo de problema existe a extensão Flask-Login que oferece métodos auxiliares para autenticar usuários e também a Flask-Security é um pacote feito em cima do Flask-Login (controle de autenticação), Flask-Principal (Controle de Permissões) e Flask-Mail (envio de email).

A vantagem de usar o Flask-Security é que ele já se integra com o MongoEngine e oferece templates prontos para login, alterar senha, envio de email de confirmação etc...

Começaremos adicionando a dependencia ao arquivo de requirements.

**requirements.txt**

```
https://github.com/mitsuhiko/flask/tarball/master
flask-mongoengine
nose
Flask-Bootstrap
Flask-Security
```

E então instalamos com ``pip install -r requirements.txt --upgrade``

### Secret Key

Para encriptar os passwords dos usuários o Flask-Login irá utilizar a chave secret key do settings de seu projeto. É muito importante que esta chave seja segura e gerada de maneira randomica (utilize uuid4 ou outro método de geração de chaves).

Para testes e desenvolvimento você pode utilizar texto puro. **mas em produção escolha uma chave segura!**

Adicione ao ``development_instance/config.cfg``

```python
SECRET_KEY = 'super-secret'
```

> Importante se esta chave for perdida todas as senhas armazenadas serão invalidadas.

### Definindo o schema dos usuários e grupos

O Flask-Security permite o controle de acesso utilizando RBAC (Role Based Access Control), ou seja, usuários pertencem a grupos e os acessos são concedidos aos grupos.

Para isso precisamos armazenar (no nosso caso no MongoDB) os usuários e seus grupos.

Crie um novo arquivo **security_models.py** e criaremos duas classes **User** e **Role**

```python
# coding: utf-8
from .db import db
from flask_security import UserMixin, RoleMixin
from flask_security.utils import encrypt_password


class Role(db.Document, RoleMixin):

    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

    @classmethod
    def createrole(cls, name, description=None):
        return cls.objects.create(
            name=name,
            description=description
        )


class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.EmailField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(
        db.ReferenceField(Role, reverse_delete_rule=db.DENY), default=[]
    )
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=255)
    current_login_ip = db.StringField(max_length=255)
    login_count = db.IntField()
    username = db.StringField(max_length=50, required=False, unique=True)
    remember_token = db.StringField(max_length=255)
    authentication_token = db.StringField(max_length=255)

    @classmethod
    def createuser(cls, name, email, password,
                   active=True, roles=None, username=None,
                   *args, **kwargs):
        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles,
            username=username,
            *args,
            **kwargs
        )
```

O arquivo acima define os models com todas as propriedades necessárias para que o Flask-Security funcione com o MongoEngine, não entrerei em detalhes de cada campo pois usaremos somente o básico neste tutorial, acesse a documentação do Flask-Security se desejar saber mais a respeitod e cada atributo.

### Inicializando o Flask Security em seu projeto

Da mesma forma que fizemos com as outras extensões iremos fazer como security, alterando o arquivo **news_app.py** e inicializando a extensão utilizando o método default.

Importaremos o **Security** e o **MongoEngineUserDatastore** e inicializaremos a extensão passando nossos models de User e Role.

```python
...
from flask_security import Security, MongoEngineUserDatastore
from .db import db
from .security_models import User, Role

def create_app(mode):
   ...
   Security(app=app, datastore=MongoEngineUserDatastore(db, User, Role))
   return app
```

**news_app.py**

```python
# coding: utf-8
from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_security import Security, MongoEngineUserDatastore

from .blueprints.noticias import noticias_blueprint
from .db import db
from .security_models import User, Role


def create_app(mode):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "%s_instance" % mode
    )

    app = Flask("wtf",
                instance_path=instance_path,
                instance_relative_config=True)

    app.config.from_object('wtf.default_settings')
    app.config.from_pyfile('config.cfg')

    app.config['MEDIA_ROOT'] = path.join(
        app.config.get('PROJECT_ROOT'),
        app.instance_path,
        app.config.get('MEDIA_FOLDER')
    )

    app.register_blueprint(noticias_blueprint)

    Bootstrap(app)
    db.init_app(app)
    Security(app=app, datastore=MongoEngineUserDatastore(db, User, Role))
    return app
```

Pronto, agora temos nossa base de usuários e grupos definida e o Security irá iniciar em nosso app todo o restante necessário para o controle de login (session, cookies, formulários etc..)

#### Exigindo login para cadastro de notícia

Altere a view de cadastro em ``blueprints/noticias.py`` e utilize o decorator ``login_required`` que é disponibilizado pelo Flask-Security, sendo que o inicio do arquivo ficará assim:

```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, request, current_app, send_from_directory, render_template
)
from ..models import Noticia
from flask_security import login_required  # decorator

noticias_blueprint = Blueprint('noticias', __name__)


@noticias_blueprint.route("/noticias/cadastro", methods=["GET", "POST"])
@login_required  # aqui o login será verificado
def cadastro():
    ...
```

Execute ``python run.py`` acesse [http://localhost:5000/noticias/cadastro](http://localhost:5000/noticias/cadastro) e verifique que o login será exigido para continuar.

> NOTE: Se por acaso ocorrer um erro **TypeError: 'bool' object is not callable** execute o seguinte comando ``pip install Flask-Login==0.2.11`` e adicione  ``Flask-Login==0.2.11`` no arquivo requirements.txt. Este erro ocorre por causa de um recente bug na nova versão do Flask-Login.

Se tudo ocorrer como esperado agora você será encaminhado para a página de login.

<figure>
<img src="/images/rochacbruno/login.png" alt="login" >
</figure>

O único problema é que você ainda não possui um usuário para efetuar o login. Em nosso model de User definimos um método **create_user** que pode ser utilizado diretamente em um terminal iPython. Porém o Flask-Security facilita bastante fornecendo também um formulário de registro de usuários.

Adicione as seguintes configurações no arquivo ``development_instance/config.cfg`` para habilitar o formulário de registro de usuários.

```python
SECURITY_REGISTERABLE = True

# as opções abaixo devem ser removidas em ambiente de produção
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
SECURITY_CHANGEABLE = True
```

Agora acesse [http://localhost:5000/register](http://localhost:5000/register) e você poderá registar um novo usuário e depois efetuar login.

<figure>
<img src="/images/rochacbruno/register.png" alt="register" >
</figure>

> NOTE: É recomendado que a opção de registro de usuário seja desabilidata em ambiente de produção, que seja utilizado outros meios como o Flask-Admin que veremos adiante para registrar novos usuários ou que seja habilitado o Captcha para os formulários de registro e login e também o envio de email de confirmação de cadastro.

Todas as opções de configuração do Flsk-Security estão disponíveis em [https://pythonhosted.org/Flask-Security/configuration.html](https://pythonhosted.org/Flask-Security/configuration.html)

Agora será interessante mostrar opções de Login, Logout, Alterar senha na barra de navegação. Para isso altere o template ``base.html`` adicionando o bloco de access control.

```html
{%- extends "bootstrap/base.html" %}
{% import "bootstrap/utils.html" as utils %}
{% block title %} {{title or "Notícias"}} {% endblock %}
{% block navbar -%}
    <nav class="navbar navbar-default">
       <a class="navbar-brand" href="#"><img src="{{url_for('static', filename='generic_logo.gif')}}" style="height:30px;"></a>
       <ul class="nav navbar-nav">
         <li><a href="{{url_for('noticias.index')}}">HOME</a> </li>
         <li><a href="{{url_for('noticias.cadastro')}}">CADASTRO</a></li>
         {% block access_control %}
            <li class="divider-vertical"></li>
            {% if current_user.is_authenticated() %}
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                 {{current_user.email}}  <b class="caret"></b>
              </a>
              <ul class="dropdown-menu">
                  <li><a href="{{url_for_security('change_password')}}"><i class="icon-user"></i> Change password</a></li>
                  <li><a href="{{url_for_security('logout')}}"><i class="icon-off"></i> Logout</a></li>
              </ul>
            </li>
            {% else %}
              <li><a href="{{url_for_security('login')}}"><i class="icon-off"></i> Login</a></li>
            {% endif %}
        {% endblock %}
       </ul>
    </nav>
{%- endblock navbar %}
{% block content %}
 <div class="container">
  {%- with messages = get_flashed_messages(with_categories=True) %}
  {%- if messages %}
    <div class="row">
      <div class="col-md-12">
        {{utils.flashed_messages(messages)}}
      </div>
    </div>
  {%- endif %}
  {%- endwith %}
    <div class="jumbotron">
      {% block news %}
      {% endblock %}
    </div>
{%- endblock content%}
```

O resultado final será:

<figure>
<img src="/images/rochacbruno/access.png" alt="access" >
</figure>

As opções de customização e instruções de como alterar os formulários e templates do Flask-Security encontram-se na [documentação oficial](https://pythonhosted.org/Flask-Security/).

> O diff com todas as alterações feitas com o Flask-Security pode ser consultado neste [link](https://github.com/rochacbruno/wtf/commit/3766bfabb6d9c359731ff3a143101209af0d207f)

## <a href="#flask_admin" name="flask_admin">Flask Admin - Um admin tão poderoso quanto o Django Admin!</a>

Todos sabemos que uma das grandes vantagens de um framework full-stack como Django ou Web2py é a presença de um Admin para o banco de dados. Mesmo sendo Micro-Framework o Flask conta com a extensão Flask-Admin que o transforma em uma solução tão completa quanto o Django-Admin.

Para começar vamos colocar os requisitos no arquivo de requirements!!

**requirements.txt
```
https://github.com/mitsuhiko/flask/tarball/master
flask-mongoengine
nose
Flask-Bootstrap
Flask-Security
Flask-Login==0.2.11
Flask-Admin
```

Instalar com ``pip install -r requirements.txt --upgrade``

### Admin para o seu banco de dados MongoDB!!!




Extensões recomendadas que não foram abordadas neste artigo

- [Flask Email] Para avisar os autores que tem novo comentário
- [Flask Queue] Pare enviar o email assincronamente e não bloquear o request
- [Flask Classy] Um jeito fácil de criar API REST e Views
- [Flask Oauth e OauthLib] Login com o Feicibuque e tuinter

> A versão final do app está no [github](https://github.com/rochacbruno/wtf/tree/extended)

<hr>

> **END:** Sim chegamos ao fim desta terceira parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas 3 partes iremos desenvolver nossas próprias extensões e blueprints e também questṍes relacionados a deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Estou iniciando um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CursoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)


Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções etc na caixa de comentários abaixo.

Abraço! "Python é vida!"
