Title: What the Flask? pt 4 - Extensões para o Flask
Slug: what-the-flask-pt-4-extensoes-para-o-flask
Date: 2017-04-26 09:00
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


What The Flask - 4/5
--------------------

> Finalmente!!! Depois de uma longa espera o **What The Flask** está de volta!
> A idéia era publicar primeiro a parte 4 (sobre Blueprints) e só depois a 5
> sobre como criar extensões. Mas esses 2 temas estão muito interligados
> então neste artigo os 2 assuntos serão abordados. E a parte 5 será a final falando sobre deploy!


<figure style="float:left;margin-right:30px;width:35%">
<img src="/images/rochacbruno/code.png" alt="code" >
</figure>


1. [**Hello Flask**](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python.html): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask.html): Estruturando aplicações Flask
3. [**Plug & Use**](/what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto.html): extensões essenciais para iniciar seu projeto
4. [**Magic(app)**](/what-the-flask-pt-4-extensoes-para-o-flask.html): Criando Extensões para o Flask(**<-- Você está aqui**)
5. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem


Não sei se você ainda se lembra? mas estavámos desenvolvendo um [CMS de notícias](http://github.com/rochacbruno/wtf),
utilizamos as extensões `Flask-MongoEngine`, `Flask-Security`, `Flask-Admin` e `Flask-Bootstrap`.

E neste artigo iremos adicionar mais uma extensão em nosso CMS, mas **iremos criar uma extensão**
ao invés de usar uma das extensões disponíveis.

> **Extensão ou Plugin?** Por [definição](https://pt.wikipedia.org/wiki/Plug-in)
**plugins** diferem de **extensões**.
Plugins geralmente são externos e utilizam algum tipo de API pública para se integrar com o aplicativo.
Extensões, por outro lado, geralmente são integradas com a lógica da aplicação, isto é, as interfaces do próprio framework.
Ambos, plugins e extensões, aumentam a utilidade da aplicação original, mas **plugin** é algo relacionado apenas a camadas de mais
alto nível da aplicação, enquanto extensões estão acopladas ao framework. Em outras palavras, **plugin** é algo que você escreve
pensando apenas na **sua aplicação** e está altamente acoplado a ela enquanto **extensão** é algo que pode ser usado **por qualquer aplicação** escrita no mesmo framework pois está acoplado a lógica do framework e não das aplicações escritas com ele.

# Quando criar uma extensão?

Faz sentido criar uma extensão quando você identifica uma functionalidade
que pode ser **reaproveitada** por outras aplicações Flask, assim você mesmo se
beneficia do fato de não precisar reescrever (copy-paste) aquela funcionalidade
em outros apps e também pode publicar sua extensão como **open-source** beneficiando
toda a **comunidade** e incorporando as **melhorias**, ou seja, **todo mundo ganha!**

## Exemplo prático

Imagine que você está publicando seu site mas gostaria de prover um `sitemap`. (URL que lista todas as páginas existentes no seu site usada pelo Google para melhorar a sua classificação nas buscas).

Como veremos no exemplo abaixo publicar um **sitemap** é uma tarefa bastante
simples, mas é uma coisa que você precisará fazer em todos os sites que
desenvolver e que pode se tornar uma funcionalidade mais complexa na medida
que necessitar controlar datas de publicação e extração de URLs automáticamente.

## Exemplo 1 - Publicando o sitemap sem o uso de extensões

```python
from flask import Flask, make_response

app = Flask(__name__)

@app.route('/artigos')
def artigos():
    "este endpoint retorna a lista de artigos"

@app.route('/paginas')
def paginas():
    "este endpoint retorna a lista de paginas"

@app.route('/contato')
def contato():
    "este endpoint retorna o form de contato"

######################################
# Esta parte poderia ser uma extensão
######################################
@app.route('/sitemap.xml')
def sitemap():
    items = [
        '<url><loc>{0}</loc></url>'.format(page)
        for page in ['/artigos', '/paginas', '/contato']
    ]
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{0}</urlset>'
    ).format(''.join(items)).strip()
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response
#######################################
# / Esta parte poderia ser uma extensão
#######################################


app.run(debug=True)
```

Executando e acessando http://localhost:5000/sitemap.xml o resultado será:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>/artigos</loc></url>
    <url><loc>/paginas</loc></url>
    <url><loc>/contato</loc></url>
</urlset>
```

> **NOTE**: O app acima é apenas um simples exemplo de como gerar um sitemap e a
intenção dele aqui é apenas a de servir de exemplo para extensão que criaremos
nos próximos passos, existem outras boas práticas a serem seguidas na
publicação de [sitemap](https://www.sitemaps.org/pt_BR/protocol.html) mas não é
o foco deste tutorial.

Vamos então transformar o exemplo acima em uma **Extensão** e utilizar uma abordagem
mais dinâmica para coletar as URLs, mas antes vamos entender como funcionam as
extensões no Flask.

# Como funciona uma Extensão do Flask?

Lembra que na [parte 2](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask.html#app_factory) desta série falamos sobre os **patterns** do Flask e sobre
o **application factory** e **blueprints**? As extensões irão seguir estes
mesmos padrões em sua arquitetura.

O grande **"segredo"** para se trabalhar com **Flask** é entender que sempre iremos
interagir com uma instância geralmente chamada de **app** e que pode ser acessada
também através do proxy **current_app** e que sempre aplicaremos um padrão que
é quase **funcional** neste deste objeto sendo que a grande diferença aqui é
que neste paradigma do Flask as funções (chamadas de **factories**) introduzem **side effects**, ou seja, elas alteram ou injetam funcionalidades no **app** que é manipulado até que chega ao seu **estado de execução**. (enquanto em um paradigma funcional as funções não podem ter side effects)

Também é importante entender os estados **configuração**, **request** e **interativo/execução** do
Flask, asunto que abordamos na [parte 1](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python.html#o_contexto_da_aplicacao) desta série.

Em resumo, iremos criar uma **factory** que recebe uma instância da classe **Flask**, o objeto **app** (ou o acessa através do proxy **current_app**) e então altera ou injeta funcionalidades neste objeto.

Dominar o Flask depende muito do entendimento desse **padrão de factories** e os **3 estados da app** citados acima, se você não está seguro quanto a estes conceitos aconselho reler
as [partes 1 e 2](/tag/what-the-flask.html) desta série (e é claro sinta se livre para deixar comentários
com as suas dúvidas).

Só para relembrar veja o seguinte exemplo:

```python
app = Flask(__name__)  # criamos a instancia de app
admin = Admin()  # instancia do Flask-Admin ainda não inicializada

do_something(app)  # injeta ou altera funcionalidades do app
do_another_thing(app, admin)  # injeta ou altera funcionalidades do apo ou do admin
Security(app)  # adiciona funcionalidades de login e controle de acesso
Cache(app)  # adiciona cache para views e templates
SimpleSitemap(app)  # A extensão que iremos criar! Ela adiciona o /sitemap.xml no app

admin.init_app(app)  # agora sim inicializamos o flask-admin no modo lazy
```

Olhando o código acima pode parecer bastante simples, você pode achar que basta
receber a intância de `app` e sair alterando sem seguir nenhum padrão.

```python
def bad_example_of_flask_extension(app):
    "Mal exemplo de factory que injeta ou altera funcionalidades do app"
    # adiciona rotas
    @app.route('/qualquercoisa)
    def qualquercoisa():
        ...
    # substitui objetos usando composição
    app.config_class = MyCustomConfigclass
    # altera config
    app.config['QUALQUERCOISA'] = 'QUALQUERVALOR'
    # sobrescreve métodos e atributos do app
    app.make_responde = another_function
    # Qualquer coisa que o Python (e a sua consciência) permita!
```

Isso pode provavelmente funcionar mas não é uma boa prática, existem muitos
problemas com o **factory** acima e alguns deles são:

1. Nunca devemos definir rotas dessa maneira com `app.route` em uma extensão **o correto é usar blueprints**.
2. Lembre-se dos **3 estados do Flask**, devemos levar em consideração que no momento
que a aplicação for iniciada a extensão pode ainda não estar pronta para ser carregada,
por exemplo, a sua extensão pode depender de um banco de dados que ainda não
foi inicializado, portanto as extensões precisam sempre ter um **modo lazy**.
3. Usar funções pode se ruma boa idéia na maioria dos casos, mas lembre-se que
precisamos manter estado em algumas situações então pode ser **melhor usar
classes** ao invés de funções pois as classes permitem uma construção mais dinâmica.
4. Nossa extensão precisa ser reutilizavel em qualquer app flask, portanto
devemos usar namespaces ao ler configurações e definir rotas.

> **NOTE**: Eu **NÃO** estou dizendo que você não deve usar funções para extender seu app
Flask, eu mesmo faço isso em muitos casos. Apenas tenha em mente esses detalhes
citados na hora de decidir qual abordagem usar.

# Patterns of a Flask extension

Preferencialmente uma **Extensão** do **Flask** deve seguir esses **padrões**:

- Estar em um módulo nomeado com o prefixo **flask_** como por exemplo **flask_admin**
e **flask_login** e neste artigo criaremos o **flask_simple_sitemap**. (**NOTE:** Antigamente as extensões usavam o padrão **flask.ext.nome_extensao** mas este tipo de plublicação de módulo com namespace do **flask.ext** foi descontinuado e não é mais recomendado.)
- Fornecer um **método** de inicialização **lazy** nomeado **init_app**.
- Ler todas as suas configurações a partir do **app.config**
- Ter suas configurações prefixadas com o nome da extensão, exemplo: **SIMPLE_SITEMAP_URLS** ao invés de apenas **SITEMAP_URLS** pois isto evita conflitos com configurações de outras extensões.
- Caso a extensão adicione views e URL rules, isto deve ser feito com **Blueprint**
- Caso a extensão adicione arquivos estáticos ou de template isto também deve ser
feito com **Blueprint**
- ao registrar **urls** e **endpoints** permitir que sejam dinâmicos através de config e
sempre prefixar com o nome da extensão. Exemplo: `url_for('simple_sitemap.sitemap')` é
melhor do que `url_for('sitemap')` para evitar conflitos com outras extensões.

> **NOTE:** Tenha em mente que regras foram feitas para serem **quebradas**,
> O **Guido** escreveu na [PEP8](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds) "A Foolish Consistency is the Hobgoblin of Little Minds", ou seja, tenha os padrões como guia mas nunca deixe que eles atrapalhem
> o seu objetivo.
> Eu mesmo já quebrei essa regra 1 no [flasgger](http://github.com/rochacbruno/flasgger),
> eu poderia ter chamado de `flask_openapi` ou `flask_swaggerui` mas achei `Flasgger` um nome mais divertido :)

De todos os padrões acima o mais importante é o de evitar o conflito com outras extensões!

> Zen do Python: **Namespaces são uma ótima idéia! vamos usar mais deles!**

# Criando a extensão Simple Sitemap

Ok, agora que você já sabe a **teoria** vamos colocar em **prática**,
abre ai o **vim**, **emacs**, **pycharm** ou seu **vscode** e vamos reescrever o
nosso app do **Exemplo 1** usando uma extensão chamada **flask_simple_sitemap** e para isso vamos começar criando a extensão:

A extensão será um **novo módulo Python** que vai ser instalado usando `setup` ou `pip` portanto crie um projeto separado.


Em seu terminal `*nix` execute os comandos:

```bash
➤ $
# Entre na pasta onde vc armazena seus projetos
cd Projects

# crie o diretório root do projeto
mkdir simple_sitemap
cd simple_sitemap

# torna a extensão instalável (vamos escrever esse arquivo depois)
touch setup.py

# é sempre bom incluir uma documentação básica
echo '# Prometo documentar essa extensão!' > README.md

# se não tiver testes não serve para nada! :)
touch tests.py

# crie o diretório que será o nosso package
mkdir flask_simple_sitemap

# __init__.py para transformar o diretório em Python package
echo 'from .base import SimpleSitemap' > flask_simple_sitemap/__init__.py

# A implementação da extensão será escrita neste arquivo
# (evite usar main.py pois este nome é reservado para .zipped packages)
touch flask_simple_sitemap/base.py

# Crie a pasta de templates
mkdir flask_simple_sitemap/templates

# usaremos Jinja para gerar o XML
touch flask_simple_sitemap/templates/sitemap.xml

# incluindo templates no build manifest do setuptools
echo 'recursive-include flask_simple_sitemap/templates *' > MANIFEST.in

# precisaremos de um arquivo de requirements para os testes
touch requirements-test.txt

```

Agora voce terá a seguinte estrutura:

```bash
➤ tree
simple_sitemap/
├── flask_simple_sitemap/
│   ├── base.py
│   ├── __init__.py
│   └── templates/
│       └── sitemap.xml
├── MANIFEST.in
├── README.md
├── requirements-test.txt
├── setup.py
└── tests.py

2 directories, 8 files
```

O primeiro passo é escrever o `setup.py` já que a extensão precisa ser instalavél:


```python
from setuptools import setup, find_packages

setup(
    name='flask_simple_sitemap',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
```

Eu tenho o costumo de praticar o que eu chamo de **RDD** (**R**eadme **D**riven **D**development), ou seja,
ao criar projetos como este eu costumo escreve primeiro o **README.md** explicando como deve funcionar e só
depois de ter isto pronto que eu começo a programar.

Edite o `README.md`

```text

# Flask Simple Sitemap

Esta extensão adiciona a funcionalidade de geração de sitemap ao seu app flask.

## Como instalar?

Para instalar basta clonar o repositório e executar:

    $ python setup.py install

Ou via `pip install flask_simple_sitemap`

## Como usar?

Basta importar e inicializar:

    from flask import Flask
    from flask_simple_sitemap import SimpleSitemap

    app = Flask(__name__)
    SimpleSitemap(app)

    @app.route('/)
    def index():
        return 'Hello World'

Como em toda extensão Flask também é possível inicializar no modo Lazy chamando
o método `init_app`

## Opções de configuração:

esta extensão utiliza o namespace de configuração `SIMPLE_SITEMAP_`

- **SIMPLE_SITEMAP_BLUEPRINT** define o nome do blueprint e do url prefix (default: `'simple_sitemap'`)
- **SIMPLE_SITEMAP_URL** define a url que irá renderizar o sitemap (default: `'/sitemap.xml'`)
- **SIMPLE_SITEMAP_PATHS** dicionário de URLs a serem adicionadas ao sitemap (exemplo: URLs criadas a partir de posts em bancos de dados)

```

Agora que já sabemos pelo **README** o que queremos entregar de funcionalidade
já é possível escrever o **tests.py** e aplicar também um pouco de **TDD**

O Flask tem uma integração bem interesante com o **py.test** e podemos editar o **tests.py**
da seguinte maneira:

> **NOTE:** O ideal é fazer o **test setup** no arquivo **conftest.py** e usar fixtures do py.test, mas aqui vamos
> escrever tudo junto no **tests.py** para ficar mais prático.  
<br />
> **Zen do Python:** `praticidade vence a pureza` :)


```python
####################################################################
# Início do Test Setup
#

import xmltodict
from flask import Flask
from flask_simple_sitemap import SimpleSitemap

app = Flask(__name__)
extension = SimpleSitemap()

app.config['SIMPLE_SITEMAP_BLUEPRINT'] = 'test_sitemap'
app.config['SIMPLE_SITEMAP_URL'] = '/test_sitemap.xml'
app.config['SIMPLE_SITEMAP_PATHS'] = {
    '/this_is_a_test': {'lastmod': '2017-04-24'}
}

@app.route('/hello')
def hello():
    return 'Hello'

# assert lazy initialization
extension.init_app(app)

client = app.test_client()

#
# Final Test Setup
####################################################################

####################################################################
# Cláusula que Permite testar manualmente o app com `python tests.py`
#
if __name__ == '__main__':
    app.run(debug=True)
#
# acesse localhost:5000/test_sitemap.xml
####################################################################

####################################################################
# Agora sim os testes que serão executados com `py.test tests.py -v`
#

def test_sitemap_uses_custom_url():
    response = client.get('/test_sitemap.xml')
    assert response.status_code == 200

def test_generated_sitemap_xml_is_valid():
    response = client.get('/test_sitemap.xml')
    xml = response.data.decode('utf-8')
    result = xmltodict.parse(xml)
    assert 'urlset' in result
    # rules are Ordered
    assert result['urlset']['url'][0]['loc'] == '/test_sitemap.xml'
    assert result['urlset']['url'][1]['loc'] == '/hello'
    assert result['urlset']['url'][2]['loc'] == '/this_is_a_test'

#
# Ao terminar o tutorial reescreva esses testes usando fixtures :)
# E é claro poderá adicionar mais testes!
###################################################################
```

Para que os testes acima sejam executados precisamos instalar algumas dependencias portanto o **requirements-test.txt** precisa deste conteúdo:

```
flask
pytest
xmltodict
--editable .
```

> **NOTE:** ao usar `--editable .` no arquivo de requirements você faz com que a extensão seja auto instalada em modo de edição
> desta forma executamos apenas `pip install -r requirements-test.txt` e o pip se encarrega de rodar o `python setup.py develop`.

Vamos então começar a desenvolver editando o **front-end** da extensão 
que será escrito no template: **flask_simple_sitemap/templates/sitemap.xml** este template espera um dict `paths`
chaveado pela `location` e contento `sitemap tag names` em seu valor.
exemplo `paths = {'/artigos': {'lastmod': '2017-04-24'}, ...}`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for loc, data in paths.items() %}
    <url>
        <loc>{{loc|safe}}</loc>
        {% for tag_name, value in data.items() %}
            <{{tag_name}}>{{value}}</{{tag_name}}>
        {% endfor %}
    </url>
    {% endfor %}
</urlset>
```

E então finalmente escreveremos a classe base da extensão no arquivo **flask_simple_sitemap/base.py**

Lembrando de algumas boas práticas:

- Prover um método de inicialização **lazy** com a assinatura `init_app(self, app)`
- Impedir registro em **duplicidade** e inserir um registro no `app.extensions`
- Ao adicionar rotas sempre usar **Blueprints** e **namespaces** (o Blueprint já se encarrega do namespace nas urls)
- Configs devem sempre ter um prefixo, faremos isso com o `get_namespace` que aprendemos na parte 1

> **NOTE:** Leia atentamente os **comentários** e **docstrings** do código abaixo.

```python
# coding: utf-8
from flask import Blueprint, render_template, make_response


class SimpleSitemap(object):
    "Extensão Flask para publicação de sitemap"

    def __init__(self, app=None):
        """Define valores padrão para a extensão
        e caso o `app` seja informado efetua a inicialização imeditatamente
        caso o `app` não seja passado então
        a inicialização deverá ser feita depois (`lazy`)
        """
        self.config = {
            'blueprint': 'simple_sitemap',
            'url': '/sitemap.xml',
            'paths': {}
        }
        self.app = None  # indica uma extensão não inicializada

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Método que Inicializa a extensão e
        pode ser chamado de forma `lazy`.

        É interessante que este método seja apenas o `entry point` da extensão
        e que todas as operações de inicialização sejam feitas em métodos
        auxiliares privados para melhor organização e manutenção do código.
        """
        self._register(app)
        self._load_config()
        self._register_view()

    def _register(self, app):
        """De acordo com as boas práticas para extensões devemos checar se
        a extensão já foi inicializada e então falhar explicitamente caso
        seja verdadeiro.
        Se tudo estiver ok, então registramos o app.extensions e o self.app
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'simple_sitemap' in app.extensions:
            raise RuntimeError("Flask extension already initialized")

        # se tudo está ok! então registramos a extensão no app.extensions!
        app.extensions['simple_sitemap'] = self

        # Marcamos esta extensão como inicializada
        self.app = app

    def _load_config(self):
        """Carrega todas as variaveis de config que tenham o prefixo `SIMPLE_SITEMAP_`
        Por exemplo, se no config estiver especificado:

            SIMPLE_SITEMAP_URL = '/sitemap.xml'

        Podemos acessar dentro da extensão da seguinte maneira:

           self.config['url']

        e isto é possível por causa do `get_namespace` do Flask utilizado abaixo.
        """
        self.config.update(
            self.app.config.get_namespace(
                namespace='SIMPLE_SITEMAP_',
                lowercase=True,
                trim_namespace=True
            )
        )

    def _register_view(self):
        """aqui registramos o blueprint contendo a rota `/sitemap.xml`"""
        self.blueprint = Blueprint(
            # O nome do blueprint deve ser unico
            # usaremos o valor informado em `SIMPLE_SITEMAP_BLUEPRINT`
            self.config['blueprint'],

            # Agora passamos o nome do módulo Python que o Blueprint
            # está localizado, o Flask usa isso para carregar os templates
            __name__,

            # informamos que a pasta de templates será a `templates`
            # já é a pasta default do Flask mas como a nossa extensão está
            # adicionando um arquivo na árvore de templates será necessário
            # informar
            template_folder='templates'
        )

        # inserimos a rota atráves do método `add_url_rule` pois fica
        # esteticamente mais bonito do que usar @self.blueprint.route()
        self.blueprint.add_url_rule(
            self.config['url'],  # /sitemap.xml é o default
            endpoint='sitemap',
            view_func=self.sitemap_view,  # usamos outro método como view
            methods=['GET']
        )

        # agora só falta registar o blueprint na app
        self.app.register_blueprint(self.blueprint)

    @property
    def paths(self):
        """Cria a lista de URLs que será adicionada ao sitemap.

        Esta property será executada apenas quando a URL `/sitemap.xml` for requisitada

        É interessante ter este método seja público pois permite que seja sobrescrito
        e é neste método que vamos misturar as URLs especificadas no config com
        as urls extraidas do roteamento do Flask (Werkzeug URL Rules).

        Para carregar URLs dinâmicamente (de bancos de dados) o usuário da extensão
        poderá sobrescrever este método ou contribur com o `SIMPLE_SITEMAP_PATHS`

        Como não queremos que exista duplicação de URLs usamos um dict onde
        a chave é a url e o valor é um dicionário completando os dados ex:

        app.config['SIMPLE_SITEMAP_PATHS'] = {
            '/artigos': {
                'lastmod': '2017-01-01'
            },
            ...
        }
        """

        paths = {}

        # 1) Primeiro extraimos todas as URLs registradas na app
        for rule in self.app.url_map.iter_rules():
            # Adicionamos apenas GET que não receba argumentos
            if 'GET' in rule.methods and len(rule.arguments) == 0:
                # para urls que não contém `lastmod` inicializamos com
                # um dicionário vazio
                paths[rule.rule] = {}

        # caso existam URLs que recebam argumentos então deverão ser carregadas
        # de forma dinâmica pelo usuário da extensão
        # faremos isso na hora de usar essa extensão no CMS de notícias.

        # 2) Agora carregamos URLs informadas na config
        # isso é fácil pois já temos o config carregado no _load_config
        paths.update(self.config['paths'])

        # 3) Precisamos sempre retornar o `paths` neste método pois isso permite
        # que ele seja sobrescrito com o uso de super(....)
        return paths

    def sitemap_view(self):
        "Esta é a view exposta pela url `/sitemap.xml`"
        # geramos o XML através da renderização do template `sitemap.xml`
        sitemap_xml = render_template('sitemap.xml', paths=self.paths)
        response = make_response(sitemap_xml)
        response.headers['Content-Type'] = 'application/xml'
        return response
```

> **NOTE**: Neste exemplo usamos um método de desenvolvimento muito legal que eu chamo de:
> <br> **ITF** (**Important Things First**) onde **Arquitetura, Documentação, Testes e Front End (e protótipos)** são muito mais importantes do que a implementação de back end em si.
> <br> Assumimos que caso a nossa implementação seja alterada os conceitos anteriores se mantém integros com a proposta do produto.
> <br> Ordem de prioridade no projeto: **1)** Definimos a arquitetura **2)** Escrevemos documentação **3)** Escrevemos testes **4)** Implementamos front end (e protótipo) **5)** **back end é o menos importante** do ponto de vista do produto e por isso ficou para o final! :)

O código da extensão etá disponível em [http://github.com/rochacbruno/flask_simple_sitemap](http://github.com/rochacbruno/flask_simple_sitemap)

# Usando a extensão em nosso CMS de notícias

Agora vem a melhor parte, usar a extensão recém criada em nosso projeto existente.

O repositório do CMS está no [github](https://github.com/rochacbruno/wtf/tree/extended) 
Precisamos do **MongoDB** em execução e a forma mais fácil é através do **docker**

```bash
➤ docker run -d -p 27017:27017 mongo
```

Se preferir utilize uma instância do MongoDB instalada localmente ou um Mongo As a Service.

> **NOTE:** O modo de execução acima é efemero e não persiste os dados, para persistir use `-v $PWD/etc/mongodata:/data/db`.

Agora que o Mongo está rodando execute o nosso CMS.

Obtendo, instalando e executando:

```bash
➤
git clone -b extended --single-branch https://github.com/rochacbruno/wtf.git extended
cd wtf

# adicione nossa extensao nos requirements do CMS 
# sim eu publiquei no PyPI, mas se preferir instale a partir do fonte que vc escreveu
echo 'flask_simple_sitemap' >> requirements.txt

# activate a virtualenv
pip install -r requirements.txt

# execute
python run.py 
```

Agora com o CMS executando acesse [http://localhost:5000](http://localhost:5000) e verá a seguinte tela:

<figure>
<img src="/images/rochacbruno/cms_index.png" alt="cms" >
</figure>

Os detalhes dessa aplicação você deve ser lembrar pois estão nas partes [1, 2 e 3](http://pythonclub.com.br/tag/what-the-flask.html) deste tutorial. 

Agora você pode
se registrar novas notícias usando o link [cadastro](http://localhost:5000/noticias/cadastro) e precisará efetuar **login** e para isso
deve se [registrar](http://localhost:5000/admin/register/) como usuário do aplicativo.

### Temos as seguintes **urls** publicads no CMS

- `'/'` lista todas as noticias na home page
- `'/noticias/cadastro'` exibe um formulário para incluir noticias
- `'/noticia/<id>` acessa uma noticia especifica
- `'/admin'` instancia do **Flask Admin** para adminstrar usuários e o banco de dados

Agora vamos incluir a extensão **flask_simple_sitemap** que criamos e adicionar as URLs das noticias dinâmicamente.

Edite o arquico **wtf/news_app.py** incluindo a extensão **flask_simple_sitemap** e também adicionando as URLs de todas as noticias
que existirem no banco de dados.

```python
# coding: utf-8
from os import path
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_security import Security, MongoEngineUserDatastore
from flask_debugtoolbar import DebugToolbarExtension

###############################################
# 1) importe a nossa nova extensão
from flask_simple_sitemap import SimpleSitemap

from .admin import configure_admin
from .blueprints.noticias import noticias_blueprint
from .db import db
from .security_models import User, Role
from .cache import cache

##############################################
# 2) importe o model de Noticia
from .models import Noticia


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

    ############################################
    # 3) Adicionane as noticias ao sitemap
    app.config['SIMPLE_SITEMAP_PATHS'] = {
        '/noticia/{0}'.format(noticia.id): {} # dict vazio mesmo por enquanto!
        for noticia in Noticia.objects.all()
    }

    ############################################
    # 4) Inicialize a extensão SimpleSitemap
    sitemap = SimpleSitemap(app)

    return app
```

Agora execute o `python run.py` e acesse [http://localhost:5000/sitemap.xml](http://localhost:5000/sitemap.xml) 

Você verá o **sitemap** gerado incluindo as URLs das notícias cadastradas!

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
  <loc>/noticia/58ffe998e138231eef84f9a7</loc>
</url>
<url>
  <loc>/noticias/cadastro</loc>
</url>
<url>
  <loc>/</loc>
</url>
...
# + um monte de URL do /admin aqui
</urlset>
```

> **NOTE:** Funcionou! legal! porém ainda não está bom. Existem algumas 
> melhorias a serem feitas e vou deixar essas melhorias para você fazer!

# Desafio What The Flask!

## 1) Melhore a geração de URLs do CMS

Você reparou que a URL das notícias está bem feia? 
**/noticia/58ffe998e138231eef84f9a7** não é uma boa URL
Para ficar mais simples no começo optamos por usar o **id** da notícia como URL 
mas isso não é uma boa prática e o pior é que isso introduz até mesmo **problemas de
segurança**.

Você conseguer arrumar isso? transformando em: **/noticia/titulo-da-noticia-aqui** ?

Vou dar umas dicas:

**Altere o Model:**

- Altere o model Noticia em: [https://github.com/rochacbruno/wtf/blob/extended/wtf/models.py#L5](https://github.com/rochacbruno/wtf/blob/extended/wtf/models.py#L5).
- Insira um novo campo para armazenar o **slug** da notícia, o valor será o título transformado para **lowercase**, **espaços substituidos por -**. Ex: para o **título**: 'Isto é uma notícia' será salvo o **slug**: 'isto-e-uma-noticia'.
- Utilize o método **save** do MongoEngine ou se preferir use **signals** para gerar o **slug** da notícia.
- Utilize o módulo **awesome-slugify** disponível no `PyPI` para criar o **slug** a partir do título.

**Altere a view:**

- Altere a view que está em: [https://github.com/rochacbruno/wtf/blob/extended/wtf/blueprints/noticias.py#L45](https://github.com/rochacbruno/wtf/blob/extended/wtf/blueprints/noticias.py#L45).
- Ao invés de `<noticia_id>` utilize `<noticia_slug>`.
- Efetue a busca através do campo **slug**.

Altere as urls passadas ao **SIMPLE_SITEMAP_PATHS** usando o **slug** ao invés do **id**.

## 2) Adicione data de publicação nas notícias

Reparou que o sitemap está sem a data da notícia? adicione o campo **modified**
ao model **Noticia** e faça com que ele salve a data de **criação** e/ou **alteração** da notícia.

**Queremos algo como:**

```python
    app.config['SIMPLE_SITEMAP_PATHS'] = {
        '/noticia/{0}'.format(noticia.slug): {
            'lastmod': noticia.modified.strftime('%Y-%m-%d')
        }
        for noticia in Noticia.objects.all()
    }
```

**Para gerar no sitemap:**

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
  <loc>/noticia/titulo-da-noticia</loc>
  <lastmod>2017-04-25</lastmod>
</url>
...
```

## 3) Crie uma opção de filtros na extensão `simple_sitemap`

Uma coisa chata também é o fato do `sitemap.xml` ter sido gerado com esse 
monte de URL indesejada. As URLs iniciadas com `/admin` por exemplo não precisam
ir para o `sitemap.xml`.

Implemente esta funcionalidade a extensão:

> **DICA**: Use **regex** `import re`

```python
app.config['SIMPLE_SITEMAP_EXCLUDE'] = [
    # urls que derem match com estes filtros não serão adicionadas ao sitemap
    '^/admin/.*'
]
```

> **DESAFIO:** Após implementar as melhorias inclua nos comentários um link para a sua solução, pode ser um **fork** dos repositórios
> ou até mesmo um link para **gist** ou **pastebin** (enviarei uns adesivos de Flask para quem completar o desafio!)

<hr />

> O diff com as alterações realizadas no CMS encontra-se no [github.com/rochacbruno/wtf](https://github.com/rochacbruno/wtf/compare/extended...sitemap?expand=1) <br>
> A versão final da extensão `SimpleSitemap` está no [github.com/rochacbruno/flask_simple_sitemap](https://github.com/rochacbruno/flask_simple_sitemap) <br>
> A versão final do CMS app está no [github.com/rochacbruno/wtf](https://github.com/rochacbruno/wtf/tree/sitemap)

Se você está a procura de uma extensão para `sitemap` para uso em produção aconselho a [flask_sitemap](https://github.com/inveniosoftware/flask-sitemap) 

<hr>

> **END:** Sim chegamos ao fim desta quarta parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas partes iremos efetuar o deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Iniciarei um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CursoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)

<hr />

> **PUBLICIDADE 3:** Inscreva-se no meu novo [canal de tutoriais](http://www.youtube.com/channel/UCKkjiNMtdyCOFE3-w7TB8xw?sub_confirmation=1)

Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções etc na caixa de comentários abaixo.

Abraço! "Python é vida!"

