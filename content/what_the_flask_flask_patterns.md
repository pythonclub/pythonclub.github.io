Title: What the Flask? Pt-2 Flask Patterns - boas práticas na estrutura de aplicações Flask
Slug: what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask
Date: 2014-06-20 02:22
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



What The Flask - 2/6
-----------

> **CONTEXT PLEASE:** Esta é a segunda parte da série **What The Flask**, 6 artigos para se tornar um **Flasker** (não, não é um cowboy que carrega sua garrafinha de whisky para todo lado). A primeira parte está aqui no [PythonClub](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python) e o app está no [github](https://github.com/rochacbruno/wtf/tree/pt-1).

<figure style="float:left;margin-right:30px;">
<img src="/images/rochacbruno/cowboy_flask.jpg" alt="a flasker" style="width:90%">
<figcaption>Professional Flask Developer</figcaption>
</figure>

1. [**Hello Flask**](/what_the_flask_introducao_ao_desenvolvimento_web_com_python.html): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask): Estruturando aplicações Flask - **<-- Você está aqui**
3. **Plug & Use**: extensões essenciais para iniciar seu projeto
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask e para o Jinja2
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.

<br>
> **Você sabia?** Flask quer dizer "Frasco/Frasqueira", ou seja, aquela garrafinha ali da foto acima que geralmente os cowboys, os Irlandeses, o John Wayne, os bebados profissionais e os hipsters gostam de utilizar para tomar desde vodka, whisky, vinho e até suco de caju (no caso dos [hipsters](http://www.cafepress.com/+hipster+flasks)). Bom você pode estar se perguntando: Por que colocar esse nome em um framework? Antes do Flask já existia o Bottle "garrafa" que surgiu com a idéia revolucionária de ser um framework de um [arquivo só](https://github.com/defnull/bottle/blob/master/bottle.py). Como o criador do Flask é meio contrário a esta idéia de colocar um monte de código Python em um único arquivo ele decidiu ironizar e fazer uma piada de 1 de abril e então criou um framework chamado [Denied](http://denied.immersedcode.org/) que era uma piada ironizando o Bottle e outros micro frameworks, mas as pessoas levaram a sério e gostaram do [estilo do denied!](http://denied.immersedcode.org/screencast.mp4) A partir disso ele decidiu pegar as boas idéias tanto do Bottle como do Denied e criar algo sério e então surgiu o Flask. O nome vem da idéia de que **Bottle**/Garrafa é para tomar de goladas, mas **Flask**/Frasco você toma **uma gota por vez**, desta forma você aprecia melhor a bebida e até hoje o slogan do Flask é " Development one drop at time".

# Flask Patterns
### Parte 2 - Boas práticas na estrutura de aplicações Flask

> **NOTE:** As dicas deste artigo são baseadas nesta parte da [documentação oficial do flask](http://flask.pocoo.org/docs/patterns/) com algumas adaptações levando em consideração a experiência que já tive na organização de apps Flask. Isso não quer dizer que esse é o único jeito de desenvolver em Flask, nem que é o melhor, lembre-se, o Flask é micro e te dá a liberdade para organizar as coisas como você bem entender, mas como eu já quebrei a cabeça resolvendo um monte de pequenos problemas vou compartilhar a receita que tem dado certo para mim.

- [One file to rule them all?](#one_file_is_bad_if_you_are_big)
- [O problema do Ovo e da Galinha](#circular_imports)
- [Azul da cor do mar ♫](#blueprints)
- [A fantástica fábrica de web apps](#app_factory)
- [Você pode ter mais de um app](#multiple_apps)
- [Configurações para todo lado](#config)
- [A app Flask quase perfeita](#flask_app_quase_perfeita)

> **TL;DR:** A versão final do app deste artigo esta no [github](https://github.com/rochacbruno/wtf), os apressados podem querer executar o app e explorar o seu código antes de ler o artigo completo.

## <a href="#one_file_is_bad_if_you_are_big" name="one_file_is_bad_if_you_are_big">One file to rule them all?</a>

O exemplo mais básico de um projeto Flask é um one-file application, e normalmente você pode começar dessa maneira mas se eu projeto começar a crescer ele vai se tornar de difícil manutenção, imagine que uma equipe de 10 programadores irá trabalhar no mesmo projeto, é comum que ao usar um sistema de controle de versão como o git você acompanhe o histórico de evolução de cada um dos arquivos e constantemente faça "merges" entre os desenvolvedores, estando tudo em único arquivo este processo pode resultar em um número muito grande de conflitos para resolver. Além disso no [Zen do Python](http://legacy.python.org/dev/peps/pep-0020/) tem a famosa frase **"Sparse is better than dense."**.

Você pode até ter motivos para querer um projeto de um arquivo só, pelo fato de ser **cool**, pelo fato de se exibir para os amigos dizendo que em Python isso é possível :), ou para economizar em espaço em disco, mas a verdade é que sempre será uma boa idéia separar a estrutura de seu projeto em vários pacotes, módulos e scripts, separados e com responsabilidades bem específicas.

### HANDS ON

Vamos começar a explorar o nosso app de exemplo que está no github, O app principal (com excessão do db) está em um único [arquivo](https://github.com/rochacbruno/wtf/blob/master/news_app.py)

``Algumas linhas foram suprimidas para melhorar a legibilidade``

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
    ...
    return render_template('cadastro.html', title=u"Inserir nova noticia")


@app.route("/")
def index():
    ...
    return render_template('index.html', ...)


@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    ...
    return render_template('noticia.html', noticia=noticia)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

```

O ideal neste caso será separar em alguns arquivos com responsabilidades específicas, **configurações** vão para um arquivo de settings, a **criação e setup do app** ficaria em um arquivo e as **views** ficariam em um outro, no nosso caso o db já está separado. Um outro detalhe é que agora precisaremos de um arquivo **run.py** que será o responsável por iniciar o servidor do Flask.

#### a estrutura seria essa:

```bash
/wtf
    /news_app.py
    /views.py
    /db.py
    /run.py
    /settings.py
    /templates/*
    /static/*
    /media_files/*
```

Ainda não é o ideal e já discutiremos o motivo, mas já é uma evolução a separação em mais de um arquivo.


## <a href="#circular_imports" name="circular_imports">O problema do Ovo e da Galinha</a>

> Quem nasceu primeiro a **app** ou as **views**?

##### settings.py
```python
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media_files')
```

#####  news_app.py
```python
from flask import Flask

app = Flask("wtf")
app.config.from_object('settings')

import views
```

#####  views.py
```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import request, current_app, send_from_directory, render_template

from db import noticias
from news_app import app


@app.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    ...
    return render_template('cadastro.html', title=u"Inserir nova noticia")


@app.route("/")
def index():
    ...
    return render_template('index.html', ...)


@app.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    ...
    return render_template('noticia.html', noticia=noticia)


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)

```

##### run.py
```python
from news_app import app
app.run(debug=True, use_reloader=True)
```

LINDO! agora temos nossa estrutura toda separada, porém acabamos de inserir o **Problema do Ovo e da Galinha** formalmente conhecido como **circular imports** ou **cyclic reference**.

```bash
news_app.py                           views.py

+--------------------------+          +--------------------------+
|                          |          |                          |
| app = Flask(...)         |  <-----+ | from news_app import app |
|                          |          |                          |
|                          |          | @app.route("/")          |
|                          |          | def view():              |
| import wtf.views         | +----->  |     ...                  |
|                          |          |                          |
+--------------------------+          +--------------------------+

```


<figure style="float:left;margin-right:10px;">
<img src="/images/rochacbruno/ovo-ou-galinha.jpg" alt="ovo-galinha" width="200">
</figure>

Como você pode reparar no diagrama acima o **news_app** importa **views** e ao mesmo tempo **views** importa do **news_app** e este é um problema muito chato de se resolver, neste caso específico não teremos problemas para rodar este projeto pois colocamos o **import wtf.views** no final do arquivo **news_app.py** e estamos importanto o módulo completo apenas para que as rotas sejam configuradas. E além disso incluímos o **run.py** que é o responsável por rodar o servidor Flask evitando que o circular import atrapalhe na execução do projeto, mas se por acaso tentarmos importar ou referenciar alguma função especifica do arquivo de views teremos sérios problemas.

> Esta versão está no [github](https://github.com/rochacbruno/wtf/tree/circular_imports)

E outro detalhe é que fica meio feio e fora das regras de estilo [Pythonica](http://legacy.python.org/dev/peps/pep-0008/#imports), experimente alterar o **news_app.py** colocando os imports na ordem correta e fazendo import explicito:

```python
from flask import Flask
from wtf.views import cadastro, index, noticia, media

app = Flask("wtf")
app.config.from_object('wtf.settings')

```

Agora ficou mais bonito! porém não funciona. No console você verá um **ImportError** não muito explicito e nessa hora você provalmente vai pensar:

> PO**A Flask! mas que droga hein? vou usar outro framework mais estável :(

**CALMA!!!** tudo foi muito bem pensado, vamos agora ver a melhor forma de resolver este tipo de problema no Flask.

## <a href="#blueprints" name="blueprints">Azul da cor do mar ♫</a>

O Flask tem um conceito para criação de módulos que é sensacional, talvez a idéia mais **Pythonica** já implementada por um framework, quem dera que tudo na vida fosse como os Blueprints!

<figure style="float:left;margin-right:10px;">
<img src="/images/rochacbruno/blueprint.jpg" alt="blueprint" width="400">
</figure>

Blueprints são **projetos** assim como essas folhas azuis usadas por arquitetos e projetistas e eles servem para criar plantas. Na engenharia o blueprint tem uma caracteristica interessante que é o fato de poder ser utilizado em camadas, imagine um projeto de um prédio onde cada andar é uma folha azul com os detalhes de projeto daquele andar especifico. A vantagem disso é que se o projetista precisar substituir o projeto de um andar ele precisará mexer em apenas uma das folhas, deixando todo o restante do projeto intacto!

No Flask os Blueprints fazem exatamente esse mesmo papel, cada pedaço do seu projeto fica em um **blueprint** separado, ou seja, é como se você tivesse vários projetos em um só. Isto traz grandes beneficios:

- Reaproveitamento de código (DRY) pois você pode usar o mesmo blueprint em vários projetos
- Desacoplamento
- Dinamização (os blueprints podem ser registrados dinâmicamente)
- A galinha nasce primeiro! - resolvemos o **circular import**
- O código fica LINDO!

### Blueprints

Um blueprint é como um **app** que criamos com ``app = Flask()``, so que não é um **app!**. Bom, não quero confundir sua cabeça com este conceito mas você sabe o que é **duck typing?**.

> **Duck Typing**: É um termo cunhado pelo alex Martelli em uma mensagem enviada para a lista comp.lang.python onde em uma tradução bem livre dizia o seguinte: "Se um objeto anda como um pato e faz quack como um pato então ele é um pato".

Voltando ao blueprint podemos dizer que, "Se o objeto faz roteamento como um app, acessa recursos como um app e se comporta como um app, então ele é um app!". O Blueprint é mais ou menos isso, ele é um **projeto** de um app que tem praticamente as mesmas caracteristicas de um app, só que ele não pode ser usado diretamente como um **app**,  para isso ele precisa ser registrado e construído.

É como desenhar o projeto de um aplicativo com suas views, rotas, templates etc e ai entregar este projeto para o **Flask** e dizer, "Vai lá Flask constrói isso aqui para mim, mas constrói só na hora em que eu precisar, ahh e guarda esse projeto com você pois eu posso querer construir mais desses depois."

### Bullshit, SHOW ME THE CODE!

Blueprints são ao mesmo tempo simples e poderosos então vamos ver como funciona na prática.

> **ZEN DO BLUEPRINT:** Every single **contact-us** page should be in a separate Blueprint. If the implementation is hard to explain, it's a bad idea. If the implementation is easy to explain, it may be a good idea. Blueprints are one honking great idea -- let's do more of those!

Vamos agora resolver o nosso antigo problema de singular imports utilizando blueprint, termos que alterar um pouco a estrutura de nosso app que agora será.

```bash
/wtf
    /news_app.py
    /db.py
    /run.py
    /settings.py
    /blueprints/
        /__init__.py
        /noticias.py
    /templates/*
    /static/*
    /media_files/*
```

Estamos removendo o arquivo de **views** e inserindo um novo módulo **blueprints** que irá conter nossos blueprints cada um em seu módulo separado, por enquanto teremos apenas o **noticias.py**

> **NOTE:** No Python 2.x o arquivo é necessário sempre ter o arquivo ``__init__.py`` para indicar que um diretório deve ser tratado como um pacote Python, desta forma é possível importar módulos de dentro deste pacote. No Python 3.x isso não é mais necessário.

O restante da nossa app continuará praticamente igual, apagaremos apenas o **views.py** e incluiremos o seguinte arquivo com o nosso blueprint.

##### /wtf/blueprints/noticias.py

```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, request, current_app, send_from_directory, render_template
)
from db import noticias

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

        id_nova_noticia = noticias.insert(dados_do_formulario)
        return render_template('cadastro_sucesso.html',
                               id_nova_noticia=id_nova_noticia)

    return render_template('cadastro.html', title=u"Inserir nova noticia")


@noticias_blueprint.route("/")
def index():
    todas_as_noticias = noticias.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")


@noticias_blueprint.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    noticia = noticias.find_one(id=noticia_id)
    return render_template('noticia.html', noticia=noticia)


@noticias_blueprint.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)

```

Repare que agora a única diferença é que ao invés de **app.route** usaremos **nome_do_blueprint.route** e você pode inclusive se preferir colocar este blueprint em qualquer outro diretório desde que esteja no Python PATH.

Como já falei antes o Blueprint acima é apenas um projeto de como esta parte da app deve funcionar, portanto agora precisamos entregar este projeto ao Flask e pedir que ele contrua. Para isso basta alterar o **news_app.py** removendo o circular import e registrando o blueprint.

##### news_app.py

```python
# coding: utf-8
from flask import Flask

from blueprints.noticias import noticias_blueprint
app = Flask("wtf")
app.config.from_object('settings')
app.register_blueprint(noticias_blueprint)
```

Caso você crie mais blueprints será necessário apenas registra-los repetindo a linha ```app.register_blueprint(objeto_do_blueprint)```.

Como existe a possibilidade de termos vários Blueprints uma coisa que pode acontecer é termos views com o mesmo nome, por exemplo, é bem comum ter uma view chamada **index** em todos os Blueprints, isso levaria a conflitos na hora de resolver o endpoint da url e para evitar isso o Flask exige que sejamos explicitos na hora de criar as urls com o **url_for** portanto será necessário alterar todos os templates incluindo o nome do blueprint, exemplo:

##### templates/index.html
Alterar de:

```html
...
<a href="{{url_for('noticia', noticia_id=noticia.id)}}">
...
```

para:


```html
...
<a href="{{url_for('noticias.noticia', noticia_id=noticia.id)}}">
...
```

Agora precisamos usar **noticias.noticia**, onde **noticias** é o nome do blueprint e **noticia** o endpoint da view.

Blueprints também podem ser **montados** em uma url base diferente:

```python
app.register_blueprint(objeto_do_blueprint, url_prefix='/portal')
```

Dessa forma todas as rotas criadas dentro do Blueprint serão automaticamente mapeadas para a base **/portal**, ou seja, ao invés de **/noticias/cadastro** ficaria **/portal/noticias/portal**.

> Esta versão com blueprint está disponível no [github](https://github.com/rochacbruno/wtf/tree/blueprint) e o diff entre as versões está nessa [url](https://github.com/rochacbruno/wtf/commit/315c7af699bb215b53299c43af017becb7c1a8c2). <3 Github.

O ideal mesmo em termos de organização é que o Blueprint tenha sua própria pasta de templates e arquivos estáticos.

Também existem abordagens onde os blueprints são registrando dinâmicamente de acordo com módulos de uma pasta especifica ou uma lista no settings.py.

Uma outra coisa ideal de se fazer é ao invés de criar o blueprint em um único arquivo separa-lo em módulos para **models**, **views** etc.

Para que servem mesmo os Blueprints?

- Construir grandes projetos baseados em uma coleção de diferentes Blueprints
- Registrar um blueprint em uma url base diferente ou em um subdominio diferente
- Registrar um mesmo blueprint multiplas vezes no projeto usando urls e configurações diferentes
- Prover templates, arquivos estáticos, template filters, macros, template globals e outros recursos (um blueprint não é obrigado a implementar views)
- Servir de base para a criação de extensões para o Jinja e Flask

> **RELAX:** Veremos essas abordagens mais avançadas de uso dos blueprints em um próximo capítulo desta série.

## <a href="#app_factory" name="app_factory">A fantástica fábrica de web apps</a>

<figure style="float:left;margin-right:10px;">
<img src="/images/rochacbruno/fabrica.jpg" alt="fabrica" width="230">
</figure>

Arquivos separados cada um com sua responsabilidade, Blueprints para criar módulos reutilizaveis e configurações organizadas. Mas ainda não está perfeito.

Nós já vimos como é possível modularizar o projeto com o uso dos Blueprints e eu citei que podemos registrar os Blueprints em urls ou subdominios diferentes.

Mas existem dois casos em que Blueprints sozinhos não resolvem todos os problemas. Um deles é nos **testes**, ao escrever testes unitários precisaremos de um objeto **app** com configurações especificas para testes, você querer por exemplo que no momento dos testes o app conecte-se em um banco de dados de testes.

Além disso em projetos grandes é comum juntar mais de uma app em um único projeto, imagine que na sua empresa tem 2 times, um que trabalha com desenvolvimento de **api** e outro que trabalha no desenvolvimento do **site**. E ainda pode ter outro time trabalhando no desenvolvimento de um **blog**. Mas no final todos esses apps deve ser servidor debaixo de um mesmo webserver e de um mesmo dominio.

Outro caso comum é o uso de soluções prontas, uma boa opção é usar o Flask-API para montar a **/api** de seu projeto ou o QuokkaCMS para o **/blog** e ai você já teria no mínimo 2 apps diferentes em um mesmo projeto.

### Chega de teoria!

No Flask é recomendado o uso de **Application Factories** que é simplesmente o uso de funções para criar instancia da **app** Flask ao invés de cria-la diretamente no **top level** do seu arquivo de app. Com isso é possível reutilizar essa função com diferentes parâmetros. vamos ver um exemplo.

No arquivo ``news_app.py`` ao invés disso:

```python
# coding: utf-8
from flask import Flask

from blueprints.noticias import noticias_blueprint
app = Flask("wtf")
app.config.from_object('settings')
app.register_blueprint(noticias_blueprint)
```

teremos isso:

```python

# coding: utf-8
from flask import Flask
from blueprints.noticias import noticias_blueprint

def create_app(config_filename=None):
    app = Flask("wtf")
    if config_filename:
        app.config.from_pyfile(config_filename)

    app.register_blueprint(noticias_blueprint)

    return app
```

e no ``run.py`` mudaremos de:

```python
from news_app import app
app.run(debug=True, use_reloader=True)
```

para:

```python
from news_app import create_app
app = create_app(config_filename='/server/wtf/settings.py')
app.run(debug=True, use_reloader=True)
```

> Para melhorar ainda mais podemos criar uma função manipuladora para registrar os blueprints ``register_blueprints(app)`` que pode carregar os blueprints diretamente de uma pasta ou de uma variavel no settings, mas como eu já disse isso vai ficar para um próximo capitulo.

Ok, ao invés de criarmos o ``app`` direto no top level criamos ele dentro de uma função, qual a vantagem?

### 1. Testes

Você poderá criar uma suite de testes facilmente e manipular as configurações desta instancia.

##### /wtf/tests/test_app.py
```python

import unittest
from news_app import create_app
from flask import request


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_filename="/path/to/test_settings.py")

    def test_request_args(self):
        with self.app.test_request_context('/?name=BrunoRocha'):
             self.assertEqual(request.args.get('name'), 'BrunoRocha')
```

### <a href="#multiple_apps" name="multiple_apps">2. Instanciar multiplos apps em um mesmo projeto </a>

##### /wtf/multiple_run.py

```python
from werkzeug.wsgi import DispatcherMiddleware

from news_app import create_app as create_news_app
from quokka.core import create_app as create_quokka_app
from flask.ext.api import create_app as create_api

app = create_news_app(config_filename='/server/wtf/settings.py')
blog_app = create_quokka_app(config='quokka.mysettings')
api_v1 = create_api(serializers=['xml', 'json'], settings='api_settings_v1')

app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app,  # servido em /
    {
        '/blog': blog_app,
        '/api/v1': api_v1
    }
)

app.run(debug=True, use_reloader=True)

```

> Esta versão com application factory está no [github](https://github.com/rochacbruno/wtf/tree/application_factory)

Além desses dois exemplos também existe a possibilidade de utilizar o **shell** do Flask para criar instancias da **app** interativamente.

> Mostrarei como utilizar o **shell** e criar comandos de console usando o Click e o Flask-Script em um outro capítulo :)


## <a href="#config" name="config">Configurações para todo lado</a>

#### Regra N.1: Configurações não pertencem a sua base de código!

Ao desenvolver projetos para web, principalmente grandes projetos é muito comum termos diferentes **ambientes** e isto nos obriga a ter diferentes conjuntos de configurações, como no exemplo do tópico anterior, podemos ter o ambiente de **desenvolvimento**, o ambiente de **testes**, o ambiente de **homologação** e o ambiente de **produção**.

Gerenciar estes múltiplos ambientes requer acima de tudo muita disciplina, a Regra N.1 deverá ser seguida a risca, ou seja, **NUNCA** faça configurações no modo **HARD CODED**, sempre utilize variáveis de settings para coisas que se alteram entre diferentes ambientes e sempre tenha um valor **default** para todos os casos.

No Flask isso é fácil pois já existe uma convenção de que configurações ficam em **app.config** ou **current_app.config** dependendo do estado da app. A única coisa que precisamos nos preocupar é em escrever corretamente os arquivos de configuração de forma que sejam de fácil manutenção e que sejam carregados de forma dinâmica de acordo com o ambiente em que a app está sendo executada.

Por padrão o Flask já oferece todas as ferramentas necessárias para gerenciar questões de configurações, tudo o que **no outro framework** :) acabamos precisando de módulos de terceiros para fazer as coisas de maneira **decoupled**, no Flask já esta built-in. Então vamos conhecer as abordagens de configuração.

#### O objeto "config"

Independente da abordagem de configuração que você escolher, no final as variáveis vão para no mesmo atributo que é o **app.config**, este atributo é uma subclasse de **dict** e se comporta exatamente como um dicionário, sendo assim podemos alterar seus valores livremente. (mas lembre-se que isso deve ocorrer quando a app estiver em estado de configuração).

```python
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DATABASE'] = "mysql://user:password@localhost/database"

>>> print(app.config)
{"DEBUG": True, "DATABASE": "mysql://user:password@localhost/database", ...}
```

Por padrão no momento em que o objeto **app** for instanciado o Flask já irá colocar uma série de valores default no **app.config**, este valores podem ser conferidos no seguinte [link](http://flask.pocoo.org/docs/config/#builtin-configuration-values).

Existem alguns valores de configuração que podem ser setados de diferentes formas, o "DEBUG" é um deles, e pode ser feito de uma dessas 3 formas.

```python
app.config['DEBUG'] = True
app.debug = True
app.run(debug=True)
```

Como o objeto **config** é um dicionário a maneira mais fácil e prática de atualiza-lo é usando o método update presente nos dicionários Python.


```python
my_app_config = {
    "DEBUG": True,
    "DATABASE": "mysql://user:password@localhost/database",
    ...
}

app = Flask(__name__)

app.config.update(**my_app_config)

```

Usar o método **update** em conjunto com a funcionalidade de descompactação de dicionários ``**`` do Python é a maneira mais fácil de atualizar as configurações e isto pode ser feito de forma condicional tendo o seu dicionário de config em um arquivo separado ou até mesmo em um arquivo JSON de fácil manutenção.

#### Configurando "like a boss", ou melhor "like a Flasker" :)

Como já falei no ínicio deste tópico, é muito comum você precisar que as configurações variem de acordo com o ambiente ou servidor em que está rodando, para isso o Flask fornece mais 3 abordagems de configurações bastante úteis.


#### Usando um arquivo de configurações *.cfg

Esta é a maneira mais comum, você coloca suas variáveis em um arquivos referentes a cada ambiente, por exemplo na raiz de seu projeto você pode ter os seguintes arquivos **development.cfg**, **test.cfg** e **production.cfg**.

> O tipo de arquivo **cfg** é um arquivo Python normal e aceita a sintaxe normal do Python, porém utiliza a extensão **cfg** para que possa ser diferenciado do estante do seu código e isto é muito útil pois certamente você não vai querer mandar esses arquivos sensiveis para o github por exemplo, basta colocar ```*.cfg``` no .gitignore e esses arquivos ficarão fora do controle de versões.

###### production.cfg
```python
DEBUG = False
DATABASE = "mysql://user:password@mysqlserver.company.com/database"
```

###### development.cfg
```python
DEBUG = True
DATABASE = "mysql://user:password@localhost/development_database"
```

E agora no app

```python
from flask import Flask

def create_app(mode):
    app = Flask(__name__)
    app.config.from_pyfile("%s.cfg" % mode)
    return app
```

E então em seu **run.py**

```python
import sys
from app import create_app
mode = sys.argv[1] if len(sys.argv) > 1 else 'development'
app = create_app(mode=mode)
app.run()
```

No exemplo acima usamos o **sys.argv** para capturar os argumentos passados para o **run.py** mas em outro capítulo veremos como usar o **click** ou o **Flask-Script** para fazer isso de maneira mais elegante.

Bom, agora para executar o seu app em ambiente de desenvolvimento você usará:

```bash
python run.py development
```

e em produção você irá utilizar

```bash
python run.py production
```

> **NOTE:** Em produção geralmente não usaremos o **run.py**, ao invés disso teremos uma arquivo **WSGI** para ser inicializado com **Gunicorn** ou **Uwsgi**, veremos isso na última parte desta série.


#### Usando variável de ambiente (recommended)

Seguinte a idéia do tópico anterior: configurar a partir de um arquivo **cfg**, vamos agora melhorar essa abordagem fazendo com que o arquivo seja decidido com o uso de uma variável de ambiente. Esta é a maneira mais recomendada para gerir as configurações.

Vamos alterar apenas o arquivo **app.py** e o **run.py**

app.py

```python
from flask import Flask

def create_app(config_env_var='FLASK_CONFIG'):
    app = Flask(__name__)
    app.config.from_envvar(config_env_var, silent=False)
    return app
```

run.py

```python
import sys
from app import create_app
config_env_var = sys.argv[1] if len(sys.argv) > 1 else 'FLASK_CONFIG'
app = create_app(config_env_var)
app.run()
```

Está bem parecido com a versão anterior, porém agora quem decide qual configuração será carregada será uma variável de embiente, usamos o **silent=False** para que ocorra um erro nos informando caso a variável **FLASK_CONFIG** não exista no ambiente, por isso no nosso processo de **deploy** teremos que garantir a existencia dessa variável, assim como teremos que garantir que ela exista em nosso ambiente de desenvolvimento.

A vantagem dessa abordagem é que você pode setar esse valor no arquivo "~/.bashrc" tanto na máquina servidor quanto na de desenvolvimento e então não se preocupar mais em ficar mudando o **modo** de configuração. Além disso lenbre-se que o arquivo pode estar localizado em qualquer diretório.

Na máquina de desenvolvimento
```bash
export FLASK_CONFIG=/path/to/development.cfg
export FLASK_CONFIG_TEST=/path/to/test.cfg
```

Na máquina de produção
```bash
export FLASK_CONFIG=/server/configurations/production.cfg
```

Agora é só executar o **run.py** e caso precise alterar, para teste por exemplo use ``python run.py FLASK_CONFIG_TEST``

> **NOTE:** Se você é usuário <strike>Windows</strike> deverá usar **set** no lugar de **export**.  Exemplo:   ```set FLASK_CONFIG=/path/to/development.cfg``` ou se preferir acessar este [link](http://www.ubuntu.com/download/desktop) e resolver este problema de uma maneira mais elegante :)


#### Usando um arquivo de configurações *.json

Da mesma forma como usamos o **cfg** também é possivel utilizar **json**, exemplo:

##### production.json

```json
{
  "DEBUG": true,
  "DATABASE": "mysql://user:password@localhost/database",
    ...
}
```


##### app.py
```python

app = Flask(__name__)
app.config.from_json('production.json')
```

> **NOTE:** A sintaxe no JSON é um pouco diferente de um dict Python, use **true** e **false** ao invés de **True** e **False**

#### Usando objetos para configurações default

Como já citado no ínicio deste capítulo, **SEMPRE TENHA VALORES DEFAULT**, a maneira recomendada para isso é usar objetos, porém  o uso e objetos devem ser apenas para valores DEFAULT. valores que variam de acordo com o ambiente devem usar as outras abordagens **from_pyfile**, **from_envvar** ou **from_json**. Isto por que geramente **objetos** devem fazer parte de seu codebase e serem distribuidos em sistemas de controle de versão, já os arquivos **json** ou **cfg** podem estar no .gitignore.

> **NOTE:** usando **from_object** o Flask itá utilizar apenas as constantes, ou seja, identificadores definidos em maiusculo.

##### usando um arquivo Python

default_settings.py
```python
SECRET_KEY = "mskcjdnfksdbflsjhgnaslkgnsfkjg"
...
```

app.py

```python
from flask import Flask

DEBUG = False
USE_CACHE = False


def create_app(config_env_var='FLASK_CONFIG', extra_config=None):
    app = Flask(__name__)
    app.config.from_object(__name__)  # pega as constantes do próprio arquivo
    app.config.from_object('default_settings')  # pega o módulo, pode usar o caminho completo
    app.config.from_envvar(config_env_var, silent=False)  # pega o caminho do arquivo de uma env-var
    if extra_config:
        app.config.update(**extra_config)   # usa um dict Python
    return app
```

Repare que podemos mesclar todas as abordagens de configuração, sendo que de acordo com a ordem que forem carregadas os valores serão sobrescritos.


##### Agora com um pouco de classe

Uma forma bem interessante de fazer a mesma coisa é utilizar classes Python ao invés de apenas arquivos, pois dessa forma podemos ter herança e polimorfismo. veja este exemplo:

default_settings.py
```python

class BaseConfig(object):
    DEBUG = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = "djfnsdjkfnsjdf"
    MEDIA_ROOT = "/path/to/media_files/in/server"


class DevelopmentConfig(ProductionConfig):
    MEDIA_ROOT = "/home/me/projects/wtf/media_files"

```

Agora na hora de configurar podemos variar entre Development e Production

```python

def create_app(mode='Production'):
    app = Flask(__name__)
    app.config.from_object("default_settings.%sConfig" % mode)
    ...
    return app
```

O método de configuração **from_object** aceita como parametro um arquivo Python ou diretamente o nome de uma classe ou objeto dentro deste arquivo.

> **LEMBRE-SE:** Você deve usar o **from_object** apenas para carregar valores default, valores especificos como senhas, strings de conexão etc devem ser colocados em arquivos fora de seu controle de versṍes.

#### Instance folders

Uma outra abordagem interessante é o uso de "diretórios de instancia" é bastante útil para gerenciar não apenas configurações mas também serve para termos outros recursos como arquivos de bancos de dados, arquivos de media/upload, caches etc em pastas separadas de acordo com o ambiente em que a app está sendo executada.

Por padrão a pasta de instancia é chamada **instance** e fica na raiz do projeto, mas você pode alterar este caminho utilizando o parâmetro **intance_path**. O ideal é que esta pasta fique fora de seu controle de versões, ou que seja gerenciada em um repositório privado separado de seu codebase principal.

Imagine a seguinte estrutura

```bash
/seuprojeto
    /app.py
    /run.py
    /...
    /production_instance
        /config.cfg
        /database.sqlite
        /nginx.conf
    /development_instance
        /config.cfg
        /database.sqlite
        /nginx.conf
```

Agora na hora de criar o app iremos alternar entre essas duas pastas de instancia

```python
from os import path

def create_app(mode='production'):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "%s_instance" % mode
    )
    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)
    app.config.from_pyfile('config.cfg')
    ...
    return app
```

Dessa forma o **instance_path** será alternado de acordo com o **mode** e o parâmetro **instance_relative_config** fará com que o **config.cfg** seja procurado dentro da pasta da isntancia.

> **NOTE:** o **instance_path** pode ser qualquer outro caminho, não precisa estar na raiz do seu projeto você pode usar **/server/configs/qualquer_pasta**. O instance_path tem que ser um caminho absoluto.

As pastas de instancia não servem apenas para configuração, mas em outro capítulo veremos como usa-las para arquivos de media e bancos de dados, confgurações de webservers etc.


#### Config namespaces

Uma outra utilizade que o objeto **config** possui é o **get_namespace** e ele serve para agrupar variáveis de configuração que pertencem a um dominio especifico, por exemplo bancos de dados.

config.cfg
```python
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "myapp_db"
MONGO_PASSWORD = "schbalums123"

REDIS_HOST = "sdjfksdf.redis.aws.com"
REDIS_PASSWORD = "foo_bar_123"

```

Agora imagine que queremos pegar todas as configurações referents ao MONGO e ao REDIS em dicionários separados:

```python
app = Flask(__name__)
app.config.from_pyfile('config.cfg')

>>> print(app.config.get_namespace('MONGO_')
{
    "host": "localhost",
    "port": 27017,
    "db": "myapp_db"
}

>>> print(app.config.get_namespace('REDIS_', lowercase=False))
{
    "HOST": "sdjfksdf.redis.aws.com",
    "PASSWORD": "foo_bar_123"
}
```

O **get_namespace** irá pegar todas as váriaveis definidas no namespace especificado, por padrão retorna as chaves em minusculo, mas caso queira manter em maiusculo basta usar **lowercase=False**

Esta ferramenta é útil para efetuar conexões a banco de dados, exemplo:

```python

from pymongo import MongoClient

db = MongoClient.connect(**app.config.get_namespace('MONGO_'))
db.foo.find(...)
```

> **ATENÇÃO:** O método **get_namespace** está disponível somente a partir da versão 1.0 do Flask, por enquanto você deverá usar o seguinte comando para instalar esta versão:

```bash
pip install https://github.com/mitsuhiko/flask/tarball/master
```

Pois a versão que está no PyPI ainda é a 0.10.1

## <a href="#flask_app_quase_perfeita" name="flask_app_quase_perfeita">A app Flask quase perfeita</a>

Ainda temos muito a discutir aqui na série What The Flask, mas só com o que vimos até aqui já é possível estruturar a app quase perfeita, **quase**, pois ainda falta falar mais sobre blueprints, instance folders, testing, debugging, extensões, e deploy com fabric, gunicorn e nginx.

Vamos juntar tudo o que vimos até agora em nossa app de notícias.

### O pacote Python e os imports relativos

Preferencialmente, e para permitir o uso de import relativo é ideal que nossa app esteja contida em um pacote Python, isso significa que todos os nossos arquivos, exceto os arquivos de execução "run.py" e arquivos de deploy "requirements.txt", "setup.py" e os tests devem ficar contidos em uma pasta que tenha um ``__init__.py``. No nosso caso para fazer isso e simples, basta incluir um nível a mais de diretório, vamos aproveitar e implementar a ideia de **instance folder** para conter o banco de dados e as configurações alterando nossa estrutura atual para:

```bash
wtf/
├── multiple_run.py
├── requirements.txt
├── run.py
├── tests/
│   └── test_basic.py
└── wtf/
    ├── __init__.py
    ├── db.py
    ├── another_app.py
    ├── news_app.py
    ├── default_settings.py
    ├── blueprints/
    │   ├── __init__.py
    │   └── noticias.py
    ├── development_instance/
    │   ├── config.cfg
    │   ├── media_files/
    │   └── noticias.db
    ├── production_instance/
    │   ├── media_files/
    │   └── noticias.db
    │   └── config.cfg
    ├── static
    │   └── generic_logo.gif
    └── templates
        ├── base.html
        ├── cadastro.html
        ├── cadastro_sucesso.html
        ├── index.html
        └── noticia.html
```

Algumas mudanças serão necessárias, primeiro teremos que alterar todos os imports para usar relative imports, dessa forma fora do módulo **wtf** ao invés de ``from news_app import create_app`` usaremos o caminho completo ``from wtf.news_app import create_app`` e dentro do módulo **wtf** podemos fazer imports relativos, ao invés de ``from blueprints import noticias`` usaremos ``from .blueprints.noticias import noticias_blueprint``, repare no uso do **.**, dentro do blueprint ao invés de ``from db import noticias`` usaremos ``from ..db import noticias`` repare que dessa vez usamos **..**, indicando que o objeto está a dois niveis acima relativo ao módulo atual.

##### run.py
```python
import sys
from wtf.news_app import create_app
mode = sys.argv[1] if len(sys.argv) > 1 else 'development'
app = create_app(mode=mode)
app.run(**app.config.get_namespace('RUN_'))
```

##### wtf/development_instance/config.cfg
```python
RUN_DEBUG = True
RUN_USE_RELOADER = True
RUN_HOST='localhost'
RUN_PORT=5000
DATABASE_NAME = 'noticias.db'
MEDIA_FOLDER = 'media_files'
```

##### wtf/news_app.py

```python
from os import path
from flask import Flask
from .blueprints.noticias import noticias_blueprint


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

    return app
```

##### wtf/db.py

```python
from os import path
from flask import current_app
import dataset

def get_table(tablename):
    database_name = current_app.config['DATABASE_NAME']
    database_path = path.join(current_app.instance_path, database_name)
    db = dataset.connect('sqlite:///{0}'.format(database_path))
    return db[tablename]
```

Agora nossa versão do **db** é uma função que retorna a tabela de acordo com o banco especifico dentro da nossa **instance_path**

##### wtf/blueprints/noticias.py
```python
# coding: utf-8
import os
from werkzeug import secure_filename
from flask import (
    Blueprint, request, current_app, send_from_directory, render_template
)
from ..db import get_table

noticias_blueprint = Blueprint('noticias', __name__)


@noticias_blueprint.route("/noticias/cadastro", methods=["GET", "POST"])
def cadastro():
    noticias = get_table('noticias')
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


@noticias_blueprint.route("/")
def index():
    noticias = get_table('noticias')
    todas_as_noticias = noticias.all()
    return render_template('index.html',
                           noticias=todas_as_noticias,
                           title=u"Todas as notícias")


@noticias_blueprint.route("/noticia/<int:noticia_id>")
def noticia(noticia_id):
    noticias = get_table('noticias')
    noticia = noticias.find_one(id=noticia_id)
    return render_template('noticia.html', noticia=noticia)


@noticias_blueprint.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(current_app.config.get('MEDIA_ROOT'), filename)
```

> **NOTE:** Não se esqueça de executar ``pip install -r requirements.txt --upgrade`` para atualizar o Flask

Para melhorar ainda mais esta versão, o caminho do instance_path poderia estar em uma variável de ambiente. Mas do jeito que está está quase perfeito. Agora e possivel executar com ``python run.py`` ou ``python run.py production`` para alternar entre os ambientes. As pastas ``development_instance`` e ``production_instance`` podem ficar de fora do seu controle versão, bastando adiciona-las no .gitignore.

> A versão final do app está no [github](https://github.com/rochacbruno/wtf/tree/almost_perfect)

Nesta versão é possivel executar os tests com ``nosetests tests/`` na raiz do projeto! **escreva mais testes!**

Também temos o **multiple_run** que utiliza o DispatcherMiddleware para juntar dois apps, experimente executar ``python multiple_run.py`` e você verá que o app de noticias será servido no "/" mas se acessar "/another" estará acessando a outra app contida no arquivo "wtf/another_app.py".

Nos próximos capítulos iremos evoluir este app para o uso de algumas extensões essenciais, uncluiremos controle de login, cache, interface de administração, suporte a html e markdown nas noticias e outras coisas.

> **END:** Sim chegamos ao fim desta segunda parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas 4 partes iremos nos aprofundar no uso e desenvolvimento de extensões e blueprints e também questṍes relacionados a deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Estou iniciando um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CursoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)


Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções etc na caixa de comentários abaixo.

Abraço! "Python é vida!"

