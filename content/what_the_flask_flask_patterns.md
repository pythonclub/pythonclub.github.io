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
- [Logando e debugando](#log)
- [Testing](#testing)

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

> Esta versão com blueprint está disponível no [github](https://github.com/rochacbruno/wtf/tree/blueprint) e o diff entre as versões está nessa [url](https://github.com/rochacbruno/wtf/commit/315c7af699bb215b53299c43af017becb7c1a8c2). <3 Github.

O ideal mesmo em termos de organização é que o Blueprint tenha sua própria pasta de templates e arquivos estáticos.

Também existem abordagens onde os blueprints são registrando dinâmicamente de acordo com módulos de uma pasta especifica ou uma lista no settings.py.

Uma outra coisa ideal de se fazer é ao invés de criar o blueprint em um único arquivo separa-lo em módulos para **models**, **views** etc.

> **RELAX:** Veremos essas abordagens mais avançadas de uso dos blueprints em um próximo capítulo desta série.