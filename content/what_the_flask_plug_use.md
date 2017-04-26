Title: What the Flask? Pt-3 Plug & Use - extensões essenciais para iniciar seu projeto
Slug: what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto
Date: 2015-10-21 09:00
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



What The Flask - 3/5
-----------

> Finalmente!!! A terceira parte da série **What The Flask**, mas ainda não acabou, serão 5 artigos para se tornar um **Flasker**, neste capítulo falaremos sobre como instalar e configurar as principais extensões do Flask para torna-lo uma solução full-stack com bootstrap no front-end, ORM para banco de dados, admin parecido com o Django Admin, Cache, Sistema de filas (celery/huey), Controle de Acesso, Envio de email, API REST e Login Social.

<figure style="float:left;margin-right:30px;width:35%">
<img src="/images/rochacbruno/lego_snake.jpg" alt="snake" >
<figcaption>Extending Flask</figcaption>
</figure>

1. [**Hello Flask**](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python.html): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask.html): Estruturando aplicações Flask
3. [**Plug & Use**](/what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto.html): extensões essenciais para iniciar seu projeto(**<-- Você está aqui**)
4. [**Magic(app)**](/what-the-flask-pt-4-extensoes-para-o-flask.html): Criando Extensões para o Flask
5. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem

<br>

> **Micro framework?** Bom, o Flask foi criado com a premissa de ser um micro-framework, o que significa que ele não tem a intenção de entregar de bandeja para você todas as coisas que você precisa em único pacotinho e nem comandos mágicos que você roda e instantaneamente tem todo o seu projeto pronto. A idéia do Flask é ser pequeno e te dar o controle de tudo o que acontece no seu aplicativo, mas ao mesmo tempo o Flask se preocupa em ser facilmente extensivel, para isso os desenvolvedores pensaram em padrões que permitem que as extensões sejam instaladas de modo que não haja conflitos (lembra dos BluePrints do capítulo anterior?), além dos BluePrints tem também os patterns para desenvolvimento de extensions que ajuda a tornar a nossa vida mais fácil, nesta parte dessa série vamos instalar e configurar algumas das principais extensões do Flask (todas testadas por mim em projetos reais).


# CMS de notícias

Nesta série estamos desenvolvendo um mini CMS para publicação de notícias, o código está disponível no [github](http://github.com/rochacbruno/wtf) e para cada fase da evolução do projeto tem uma branch diferente. Esse aplicativo de notícias tem os seguintes requisitos:

- Front-end usando o Bootstrap
- Banco de dados MongoDB
- Controle de acesso para que apenas editores autorizados publiquem notícias
- Interface administrativa para as notícias e usuários
- Cache das notícias para minimizar o acesso ao banco de dados

> **NOTE:** Existem várias extensões para Flask, algumas são aprovadas pelos desenvolvedores e entram para a lista disponível no site oficial, algumas entram para a listagem do metaflask (projeto em desenvolvimento), e uma grande parte está apenas no github. Como existem várias extensões que fazem a mesma coisa, as vezes é dificil escolher qual delas utilizar, eu irei mostrar aqui apenas as que eu utilizo e que já tenho experiência, mas isso não quer dizer que sejam as melhores, sinta-se a vontade para tentar com outras e incluir sua sugestão nos comentários.

- [Flask Bootstrap](#bootstrap) - Para deixar as coisas bonitinhas
- [Flask MongoEngine](#mongoengine) - Para armazenar os dados em um banco que é fácil fácil!
- [Flask Security](#flask_security) - Controle de acesso
- [Flask-Admin](#flask_admin) - Um admin tão poderoso quanto o Django Admin
- [Flask Cache](#flask_cache) - Para deixar o MongoDB "de boas"
- Bônus: Utilizaremos a Flask-DebugToolbar

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

<figure style="float:left;margin-right:10px;">
<img src="/images/rochacbruno/mongo.jpg" alt="mongo" >
</figure>

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

<figure style="float:left;margin-right:10px;width:25%;">
<img src="/images/rochacbruno/security.jpg" alt="security" >
</figure>

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

Além disso o Flask-Security precisa que seja especificado qual tipo de hash usar nos passwords.

Adicione ao ``development_instance/config.cfg``

```python
SECRET_KEY = 'super-secret'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = SECRET_KEY
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
SECURITY_TRACKABLE = True  # para armazenar data, IP, ultimo login dos users.

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

<figure>
<img src="/images/rochacbruno/admin.jpg" alt="admin" >
</figure>

Todos sabemos que uma das grandes vantagens de um framework full-stack como Django ou Web2py é a presença de um Admin para o banco de dados. Mesmo sendo Micro-Framework o Flask conta com a extensão Flask-Admin que o transforma em uma solução tão completa quanto o Django-Admin.

O Flask-Admin é uma das mais importantes extensões para o Flask e é frequentemente atualizada e tem uma comunidade muito ativa! O AirBnb recentemente lançou o [AirFlow que utiliza o Flask-Admin](http://mrjoes.github.io/2015/06/17/flask-admin-120.html)

E o [QuokkaCMS](http://www.quokkaproject.org), principal CMS desenvolvido com Flask e MongoDB é baseado também no Flask-Admin.

Para começar vamos colocar os requisitos no arquivo de requirements!!

**requirements.txt**

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

O Flask-Admin é um painel administrativo para bancos de dados de seus projetos Flask e ele tem suporte a diversos ORMs e Tecnologias como MySQL, PostGres, SQLServer e ORMs SQLAlchemy, Peewee, PyMongo e MongoEngine.

O Flask Admin utiliza o Bootstrap por padrão para a camada visual do admin, mas é possivel customizar com o uso de temas.

A primeira coisa a ser feita depois de ter o Flask-Admin instalado é inicializar o admin da mesma maneira que fizemos com as outras extensões.

Vamos adicionar as seguintes linhas ao arquivo **news_app.py**

```python
from flask_admin import Admin
...

def create_app(mode):
   ...
   admin = Admin(app, name='Noticias', template_mode='bootstrap3')
   return app
```

Ficando o arquivo completo.

```python
# coding: utf-8
from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_security import Security, MongoEngineUserDatastore
from flask_admin import Admin

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
    admin = Admin(app, name='Noticias', template_mode='bootstrap3')
    return app
```

Agora basta executar ``python run.py`` e acessar [http://localhost:5000/admin/](http://localhost:5000/admin/) e você verá a tela **index** do Flask-Admin.

<figure>
<img src="/images/rochacbruno/admin_index.png" alt="admin_index" >
</figure>


Se você conseguir acessar a tela acima então o Flask-Admin está inicializado corretamente, perceba que não tem nada além de uma tela em branco e um botão "home".

Precisamos agora registrar nossas ModelViews que são as telas de administração para cada coleção ou tabela do banco de dados e também implementar a integração com o Flask-Security para garantir que somente pessoas autorizadas acessem o admin.

#### Menu de controle de acesso

Em nosso front-end incluimos na barra de menus os links de controle de acesso **login**, **alterar senha** e **logout**, precisamos agora incluir os mesmos itens na barra de menus do Flask-Admin.

Para começar crie um template novo em **templates/admin_base.html** com o seguinte conteúdo.

```html
{% extends 'admin/base.html' %}

{% block access_control %}
<div class="navbar-text btn-group pull-right">
    <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">
    <i class="glyphicon glyphicon-user"></i>
    {% if current_user.is_authenticated() %}
        {% if current_user.name -%}
            {{ current_user.name }}
        {% else -%}
            {{ current_user.email }}
        {%- endif %}
    <span class="caret"></span></a>
    <ul class="dropdown-menu" role="menu">
       <li><a href="{{url_for_security('logout')}}">Log out</a></li>
    </ul>
    {% else %}
       Access
       <span class="caret"></span></a>
       <ul class="dropdown-menu" role="menu">
           <li><a href="{{url_for_security('login')}}">Login</a></li>
        </ul>
    {% endif %}
</div>
{% endblock %}
```

Agora altere o template base do Flask-Admin incluindo o parametro ``base_template='admin_base.html'`` no **news_app.py**

```
def create_app(mode):
    ...
    admin = Admin(app, name='Noticias', template_mode='bootstrap3',
                  base_template='admin_base.html')
    return app
```

<figure>
<img src="/images/rochacbruno/admin_index_login.png" alt="admin_index_login" >
</figure>

O Flask-Admin não possui uma forma automática de integração com o Flask-Security, porém podemos facilmente sobrescrever a classe de ModelView incluindo o controle de acesso necessário.

Para que isso fique mais fácil vamos centralizar a configuração do Flask-Admin em um único arquivo.

Crie um arquivo chamado **wtf/admin.py** na raiz do projeto, iremos extender a ModelView do Flask-Admin tornando-a segura e exigindo login e também iremos registrar os models **Noticia**, **User** e **Role** em nosso painel de adminsitração.

> NOTE: Se desejar que apenas usuários que pertençam ao grupo **admin** tenham acesso descomente as linhas do método **is_acessible**

**wtf/admin.py**
```python
# coding: utf-8
from flask import abort, redirect, request, url_for
from flask_security import current_user
from flask_admin.contrib.mongoengine import ModelView
from flask_admin import Admin

from .models import Noticia
from .security_models import User, Role


admin = Admin(name='Noticias', template_mode='bootstrap3',
              base_template='admin_base.html')


# Create customized model view class
class SafeModelView(ModelView):

    def is_accessible(self):
        if not current_user.is_authenticated():
            return False
        # if not current_user.has_role('admin'):
        #     return False
        return True

    def _handle_view(self, name, **kwargs):
        """
        Redireciona o usuário para página de login ou de acesso negado
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                abort(403)  # negado, caso não pertença ao grupo admin.
            else:
                return redirect(url_for('security.login', next=request.url))


def configure_admin(app):
    admin.init_app(app)
    admin.add_view(SafeModelView(Noticia))
    admin.add_view(SafeModelView(User, category='accounts'))
    admin.add_view(SafeModelView(Role, category='accounts'))
```

Agora só precisamos substituir a maneira como inicializamos o admin pela chamada a função **configure_admin**.

No arquivo **news_app.py** troque a parte

```python
from flask_admin import Admin
...

def create_app(mode):
    ...
    admin = Admin(name='Noticias', template_mode='bootstrap3',
                  base_template='admin_base.html')
    return app
```

Pelo uso da função **configure_admin**

```python
from .admin import configure_admin
...

def create_app(mode):
    ...
    configure_admin(app)
    return app
```

Desta forma ao executar ``python run.py`` e acessar [http://localhost:5000/admin/](http://localhost:5000/admin/) estando logado você irá os menus referentes aos nossos models e poderá editar/apagar/adicionar novos usuários e notícias.

<figure>
<img src="/images/rochacbruno/admin_noticia.png" alt="admin_noticia" >
</figure>

O Flask-admin possui diversas opções de customização de template, formulários, permissões. Você pode limitar quais campos exibir, alterar o comportamento dos formulários e até mesmo incluir views e formulários que não estejam no banco de dados.

### Limitando os campos a serem exibidos.

Atualmente clicando no menu **accounts/user** a lista exibe vários campos referentes ao cadastro de usuários (incluindo a senha encriptada).

<figure>
<img src="/images/rochacbruno/admin_user_full.png" alt="admin_user_full" >
</figure>

Altere nosso arquivo **admin.py** e crie uma nova classe **UserModelView** onde limitaremos os campos que serão listados no admin.

**wtf/admin.py**

```python
...

class UserModelView(SafeModelView):
    column_list = ("name", "email", "active", "last_login_at", "login_count")

...
```

E agora no final do arquivo utilize esta classe ao adicionar a view.

```python
...
admin.add_view(UserModelView(User, category='accounts'))
...
```

> NOTE: Não iremos nos aprofundar em todas as opções de customização do Flask-admin, portanto consulte a [documentação](https://flask-admin.readthedocs.org/) para saber mais.

<figure>
<img src="/images/rochacbruno/admin_user_columns.png" alt="admin_user_columns" >
</figure>

> O diff com todas as alterações referentes ao Flask-Admin estão no commit [1359c4cf9a31a0d471a3226a1bec2a672f9ffbbb](https://github.com/rochacbruno/wtf/commit/1359c4cf9a31a0d471a3226a1bec2a672f9ffbbb)

## <a href="#flask_cache" name="flask_cache">Flask Cache - Deixando o MongoDB "de boas"</a>


A cada vez que acessamos a home do nosso site uma consulta é feita ao MongoDB, e isso está definido em **blueprints/noticias.py**

```python
@noticias_blueprint.route("/")
def index():
    todas_as_noticias = Noticia.objects.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")
```

Na linha ``todas_as_noticias = Noticia.objects.all()`` fazemos uma query ao MongoDB, se 10.000 usuários acessarem a nossa página 10.000 acessos serão feitos ao MongoDB.

O mesmo acontece na view de acesso a uma notícia ``noticia = Noticia.objects.get(id=noticia_id)`` vai até o MongoDB e faz a query procurando a notícia pelo **id** e teremos novamente problemas se por exemplo muitos usuários acessarem a mesma notícia ao mesmo tempo.

Podemos otimizar as queries no Mongo utilizando **indices** porém o mais indicado é o uso de cache.

<figure style="float:left;margin-right:10px;width:30%;">
<img src="/images/rochacbruno/deboas.jpg" alt="deboas" >
</figure>

Em ambiente de alta disponibilidade é altamente recomendado usar um servidor de cache como o **Varnish** para servir de camada intermediária ou até mesmo gerar páginas HTML estáticas de cada uma das notícias.

Mas em caso de sites menores podermos contar com um sistema de cache mais simples utilizando MemCached, Redis ou até mesmo sistema de arquivos para armazenar o cache.

Em nosso projeto usaremos o Flask-Cache que poderá ser usado com Redis ou da maneira simples utilizando o sistema de arquivos.

### Debug Toolbar

Antes de mais nada precisamos de uma ajuda para enxergarmos o problema, vamos utilizar a Flask-DebugToolbar para nos mostrar o custo de nossas idas ao banco de dados e outras coisas uteis para o desenvolvimento em Flask.

Adicione ao arquivo **requirements.txt** a **flask-debugtoolbar** e utilize o flask-mongoengine diretamente do github.

```
https://github.com/mitsuhiko/flask/tarball/master
https://github.com/MongoEngine/flask-mongoengine/tarball/master
nose
Flask-Bootstrap
Flask-Security
Flask-Login==0.2.11
Flask-Admin
flask-debugtoolbar
flask-cache
```

> NOTE: usaremos o flask-mongoengine diretamente do github **https://github.com/MongoEngine/flask-mongoengine/tarball/master** pois a versão do PyPI ainda não está compatível com a debug-toolbar

E atualize sua **env** ``pip install -r requirements.txt --upgrade``

Agora edite o arquivo **development_instance/config.cfg** adicionando as seguintes entradas.

**development_instance/config.cfg**
```python
DEBUG = True
DEBUG_TOOLBAR_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
DEBUG_TB_PANELS = (
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_mongoengine.panels.MongoDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
)
```

Inicialize a extensão no arquivo **news_app.py**


```python
...
from flask_debugtoolbar import DebugToolbarExtension
...

def create_app(mode):
   ...
    DebugToolbarExtension(app)
    return app
```

Agora execute o projeto ``python run.py`` e navegue pelo site e pelo admin e analise os painéis do Flask-DebugToolbar que aparecerão na lateral direita.

<figure>
<img src="/images/rochacbruno/debug_toolbar.png" alt="debug_toolbar" >
</figure>

Note que temos vários painéis de DEBUG incluindo o painel MongoDB exibindo o tempo consumido para o acesso ao banco de dados, clicando neste botão da toolbar você poderá visualizar as queries que foram feitas ao MongoDB.

E também é interessante analisar o botão **Profiler** que exibe e o consumo de memória e CPU em cada parte de nosso app.

<figure>
<img src="/images/rochacbruno/profiler.png" alt="profiler" >
</figure>

No nosso caso como estamos em ambiente de desenvolvimento e com apenas um usuário fazendo requests os números serão insignificantes, porém basta colocar em produção e ter um **slashdot effect** que as coisas começarão a complicar.

Portanto vamos utilizar o **Flask-Cache** para minimizar o acesso ao MongoDB.

O Flask-Cache possui integração com alguns sistemas de cache e são eles:

Built-in cache types:

- null: NullCache (default)
- simple: SimpleCache
- memcached: MemcachedCache (pylibmc or memcache required)
- gaememcached: GAEMemcachedCache
- redis: RedisCache (Werkzeug 0.7 required)
- filesystem: FileSystemCache
- saslmemcached: SASLMemcachedCache (pylibmc required)

> NOTE: O mais recomendado é o uso de **Redis** ou **memcached** mas como isso exige a instalação de libs adicionais utilizaremos o **FileSystemCache** em nosso exemplo, porém o uso de cache em file system pode ser até mais lento que o acesso direto ao banco, portanto vamos utiliza-lo somente como exemplo.

Crie um arquivo **cache.py** na raiz do projeto:

```python
from flask_cache import Cache
cache = Cache(config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/tmp'})
```

Vamos inicializar a extensão da mesma forma que fizemos com as outras e neste ponto nosso arquivo **news_app.py** deverá estar assim:

```python
# coding: utf-8
from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_security import Security, MongoEngineUserDatastore
from flask_debugtoolbar import DebugToolbarExtension

from .admin import configure_admin
from .blueprints.noticias import noticias_blueprint
from .db import db
from .security_models import User, Role
from .cache import cache


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
    configure_admin(app)
    DebugToolbarExtension(app)
    cache.init_app(app)
    return app
```

Pronto, agora podemos começar a utilizar o cache nas views e templates.

> NOTE: Escrevi um artigo explicando o Flask-Cache com mais detalhes que está disponível [em meu blog](http://brunorocha.org/python/flask/usando-o-flask-cache.html)

Vamos colocar cache nas views de acesso ao MongoDB importaremos o cache que criamos no arquivo **cache.py** e utilizaremos diretamente ou como forma de decorator.


**blueprints/noticias.py**

```python
...
from ..cache import cache
...
```

Agora vamos utilizar o cache como decorator para cachear a view **index** durante 5 minutos utilizando ``@cache.cached(timeout=300)`` para decorar a view.

```python
@noticias_blueprint.route("/")
@cache.cached(timeout=300)
def index():
    todas_as_noticias = Noticia.objects.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")

```

Agora acesse [localhost:5000](http://localhost:5000) e repare que no primeiro acesso o MongoDB será acessado mas quando der refresh (f5) agora o acesso não será mais feito durante 5 minutos.

<figure>
<img src="/images/rochacbruno/cached.png" alt="cached" >
</figure>

Uma outra maneira de cachear é chamando o cache diretamente, vamos fazer isso na view **noticia** usando **cache.get** e **cache.set**

```python
@noticias_blueprint.route("/noticia/<noticia_id>")
def noticia(noticia_id):
    noticia_cacheada = cache.get(noticia_id)
    if noticia_cacheada:
        noticia = noticia_cacheada
    else:
        noticia = Noticia.objects.get(id=noticia_id)
        cache.set(noticia_id, noticia, timeout=300)
    return render_template('noticia.html', noticia=noticia)
```

Além das dessas duas maneiras também é possível cachear blocos de template e memoizar funções que recebem argumentos.

> BEWARE: Utilizar cache e controle de acesso é algo que deve ser feito com cuidado em nosso exemplo se um usuário autenticado acessar uma notícia com acesso controlado provavelmente o cache irá armazenar esta versão e todos os outros usuários terão acesso. Portanto se este for o seu caso, utilize o nome do usuário ou grupo como chave do cache.

Se quiser saber mais detalhes sobre o Flask-Cache consulte a postagem que fiz em meu [blog](http://brunorocha.org/python/flask/usando-o-flask-cache.html) e a [documentação oficial](https://pythonhosted.org/Flask-Cache/).

> O diff com as alterações realizadas com o Flask-Cache encontra-se em [27bacd25a788ffc041de332403a2426cd199b828](https://github.com/rochacbruno/wtf/commit/27bacd25a788ffc041de332403a2426cd199b828)

Algumas outras extensões recomendadas que não foram abordadas neste artigo


- [Flasgger](https://github.com/rochacbruno/flasgger) Para criar APIs com documentaçãi via Swagger UI
- [Flask Google Maps](http://github.com/rochacbruno/Flask-GoogleMaps) Para inserir mapas facilmente em apps Flask
- [Flask Dynaconf](https://github.com/rochacbruno/dynaconf) Para configurações dinâmicas
- [Flask Email] Para avisar os autores que tem novo comentário
- [Flask Queue/Celery] Pare enviar o email assincronamente e não bloquear o request
- [Flask Classy] Um jeito fácil de criar API REST e Views
- [Flask Oauth e OauthLib] Login com o Feicibuque e tuinter

> A versão final do app está no [github](https://github.com/rochacbruno/wtf/tree/extended)

<hr>

> **END:** Sim chegamos ao fim desta terceira parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas 2 partes iremos desenvolver nossas próprias extensões e blueprints e também questṍes relacionados a deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Iniciarei um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CursoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)

<hr />

> **PUBLICIDADE 3:** Inscreva-se no meu novo [canal de tutoriais](http://www.youtube.com/channel/UCKkjiNMtdyCOFE3-w7TB8xw?sub_confirmation=1)


Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções etc na caixa de comentários abaixo.

Abraço! "Python é vida!"

