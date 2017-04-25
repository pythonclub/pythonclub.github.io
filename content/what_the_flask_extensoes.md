Title: What the Flask? pt 4 e 5 Criando Extensões para o Flask
Slug: what-the-flask-pt-4-e-5-como-criar-extensoes-para-o-flask
Date: 2017-04-24 09:00
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



What The Flask - 4-5/6
----------------------

> Finalmente!!! Depois de uma longa espera o **What The Flask** está de volta!
> A idéia era publicar primeiro a parte 4 (sobre Blueprints) e só depois a 5
> sobre como criar extensões. Mas esses 2 temas estão muito interligados
> então neste artigo os 2 assuntos serão abordados.


<figure style="float:left;margin-right:30px;width:35%">
<img src="/images/rochacbruno/code.png" alt="code" >
</figure>


1. [**Hello Flask**](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask): Estruturando aplicações Flask
3. [**Plug & Use**](/what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto): extensões essenciais para iniciar seu projeto.
4. [**e 5 Criando Extensões para o Flask**](what-the-flask-pt-4-5-como-criar-extensoes-e-plugins-para-flask)(**<-- Você está aqui**)
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.


Não sei se você ainda se lembra? mas estavámos desenvolvendo um [CMS de notícias](http://github.com/rochacbruno/wtf),
utilizamos MongoDB, Flask-Security, Flask-Admin e Bootstrap, neste artigo
iremos adicionar mais uma extensão em nosso CMS, mas iremos criar a extensão
ao invés de usar uma das extensões disponiveis.

> **Extensão ou Plugin?** Por [definição](https://pt.wikipedia.org/wiki/Plug-in)
**plugin** é a palavra usada para descrever um aplicativo totalmente externo e
desacoplado da lógica do framework. Enquanto **extensão** é o termo usado para
descrever um módulo que utiliza as mesmas estruturas do framework e que pode opcionalmente ser ativado.
No Flask sempre será mais comum usarmos apenas a palavra **Extension** pois
conforme já mencionado aqui nesta série, o **flask** encoraja a sobrecarga de
seus métodos internos fazendo com que a maioria das extensões injetem
funcionalidades diretamente ou até mesmo alterem o **core** do framework
e por isso o termo extensão é mais utilizado pela comunidade.
Podemos usar a palavra **plugin** para descrever módulos que sejam escritos para adicionar funcionalidades não ao flask mas sim a camadas de mais alto nível da aplicação e que não seja de uso geral. **Extension** é um módulo que pode ser
reaproveitado por qualquer aplicativo escrito em **flask** enquanto **plugin** é
um módulo escrito especificamente para a sua aplicação.

# Quando criar uma extensão?

Faz sentido criar uma extensão quando você identifica uma functionalidade
que pode ser reaproveitada por outras aplicações Flask, assim você mesmo se
beneficia do fato de não precisar reescrever (copy-paste) aquela funcionalidade
em outros apps e também pode publicar sua extensão como open-source beneficiando
toda a comunidade e incorporando as melhorias, ou seja, todo mundo ganha!

Imagine que você está publicando seu site mas gostaria de prover um `sitemap`. (URL que lista todas as páginas existentes no seu site usada pelo Google para melhorar a sua classificação nas buscas).

Como veremos no exemplo abaixo publicar um sitemap é uma tarefa bastante
simples, mas é uma coisa que você precisará fazer em todos os sites que
desenvolver e que pode se tornar uma funcionalidade mais complexa na medida
que necessitar controlar datas de publicação e extração de URLs automáticamente.

Vamos começar com este pequeno e bastante simples exemplo.

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

> NOTES: O app acima é apenas um simples exemplo de como gerar um sitemap e a
intenção dele aqui é apenas a de servir de exemplo para extensão que criaremos
nos próximos passos, existem outras boas práticas a serem seguidas na
publicação de [sitemap](https://www.sitemaps.org/pt_BR/protocol.html) mas não é
o foco deste tutorial.

Vamos então transformar o exemplo acima em uma `Extensão` e utilizar uma abordagem
mais dinâmica para coletar as URLs, mas antes vamos entender como funcionam as
extensões.

# Como funciona uma Extensão do Flask?

Lembra que na [parte 2](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask.html#app_factory) desta série falamos sobre os `patterns` do Flask e sobre
o `application factory` e `blueprints`? então as extensões irão seguir estes
mesmos padrões em sua arquitetura.

O grande segredo para se trabalhar com `Flask` é entender que sempre iremos
interagir com uma instância geralmente chamada de `app` e que pode ser acessada
também através do proxy `current_app` e que sempre aplicaremos um padrão que
é quase `funcional` em cima deste objeto sendo que a grande direfença aqui é
que neste paradigma do Flask as funções (chamadas de `factories`) introduzem `side effects`, ou seja, elas alteram ou injetam funcionalidades no `app`. (enquanto em um paradigma funcional as funções não podem ter side effects)

Também é importante entender os estados `configuração`, `request` e `interativo` do
Flask, asunto que abordamos na [parte 1](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python.html#o_contexto_da_aplicacao) desta série.

Em resumo, iremos criar uma `factory` que recebe uma instância da `app` (ou acessa através do proxy `current_app`) e então altera ou injeta funcionalidades nesse objeto.

Dominar o Flask depende exclusivamente de entender esse padrão de factories e os 3 estados citados acima, se você não está seguro quanto a estes conceitos aconselho reler
as [partes 1 e 2](/tag/what-the-flask.html) desta série (e é claro sinta se livre para deixar comentários
com as suas dúvidas).

Só para exemplificar veja o seguinte exemplo:

```python
app = Flask(__name__)  # criamos a instancia de app
admin = Admin()  # instancia do Flask-Admin ainda não inicializada

do_something(app)  # injeta ou altera funcionalidades do app
do_another_thing(app, admin)  # injeta ou altera funcionalidades do app ou do admin
Security(app)  # adiciona funcionalidades de login e controle de acesso
Cache(app)  # adiciona cache para views e templates
Sitemap(app)  # A extensão que iremos criar! adiciona o /sitemap.xml no app

admin.init_app(app)  # agora sim inicializamos o flask-admin no modo lazy
```

Olhando o código acima pode parecer bastante simples, você pode achar que basta
receber a intância de `app` e sair alterando sem seguir nenhum padrão.

```python
def do_something(app):
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
problemas com o `factory` acima e alguns deles são:

1. Nunca devemos definir rotas dessa maneira com `app.route` em uma extensão o correto é usar blueprints.
2. Lembre-se dos 3 estados do Flask, devemos levar em consideração que no momento
que a aplicação for iniciada a extensão pode ainda não estar pronta para ser carregada,
por exemplo, a sua extensão pode depender de um banco de dados que ainda não
foi inicializado, portanto as extensões precisam sempre ter um modo lazy.
3. Usar funções pode se ruma boa idéia na maioria dos casos, mas lembre-se que
precisamos manter estado em algumas situações então pode ser melhor usar
classes ao invés de funções pois as classes permitem uma construção mais dinâmica.
4. Nossa extensão precisa ser reutilizavel em qualquer app flask, portanto usar
classes faz mais sentido pois podemos receber configurações de inicialização especificas.

> NOTE: Eu não estou dizendo que você não deve usar funções para extender seu app
Flask, eu mesmo faço isso em muitos casos. Apenas tenha em mente esses detalhes
citados  na hora de decidir qual abordagem usar.

# Patterns of a Flask extension

Preferencilmente uma `Extensão` do `flask` deve seguir esses padrões:


- Ser inicializada através de uma `Classe`
- Estar em um módulo nomeado com o prefixo `flask_` como por exemplo `flask_admin`
e `flask_login` (mas eu mesmo já quebrei essa regra no [flasgger](http://github.com/rochacbruno/flasgger)) e neste artigo criaremos o `flask_simple_sitemap`.
- Fornecer um método de inicialização `lazy` nomeado `init_app`.
- Ler todas as suas configurações a partir do `app.config`
- Ter suas configurações prefixadas com o nome da extensão, exemplo: `SIMPLE_SITEMAP_URLS` ao invés de apenas `SITEMAP_URLS` pois isto evita conflitos
com configurações de outras extensões.
- Caso a extensão adicione views e URL rules, isto deve ser feito com `Blueprint`
- Caso a extensão adicione arquivos estáticos ou de template isto também deve ser
feito com `Blueprint`
- ao registrar urls e endpoints permitir que sejam dinâmicos através de config e
sempre prefixar com o nome da extensão. Exemplo: `url_for('simple_sitemap.sitemap')` é
melhor do que `url_for('sitemap')` para evitar conflitos caso outra estensão tbm crie um
endpoint chamado `sitemap` (lembra do Zen do Python? Namespaces são uma ótima idéia)
mas não se preocupe pois usando Blueprint isso já é resolvido automaticamente.

# Criando a extensão Simple Sitemap

Ok, agora que você já sabe a teoria vamos para a prática, vamos reescrever o
nosso app do **Exemplo 1** usando uma extensão chamada `flask_simple_sitemap` e para isso vamos começar criando a extensão:

A extensão será um novo módulo Python que vai ser instalado usando `setup` ou `pip` portanto crie um projeto separado.


Em seu terminal `*nix` execute:

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
echo 'include flask_simple_sitemap/templates/sitemap.xml' > MANIFEST.in

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
├── setup.py
└── tests.py

2 directories, 8 files
```

O primeiro passo é escrever o `setup.py` já que a extensão precisa ser instalada e disponibilizada no **PyPI** para instalação via `pip`:


```python
from setuptools import setup

setup(
    name='flask_simple_sitemap',
    version='0.0.1',
    packages=['flask_simple_sitemap']
)
```

Eu tenho o costumo de praticar o que eu chamo de **RDD** (**R**eadme **D**riven **D**development), ou seja,
ao criar projetos como este eu costumo escreve primeiro o **README.md** explicando como deve funcionar e só
depois de ter isto pronto que eu começo a programar.

Edite o `README.md`

```markdown

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

```python
# Test Setup
# O ideal é fazer isso em forma de fixture no conftest.py
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

# Testes

def test_custom_url_is_set():
    response = client.get('/test_sitemap.xml')
    assert response.status_code == 200

def test_generated_sitemap():
    response = client.get('/test_sitemap.xml')
    xml = response.data.decode('utf-8')
    result = xmltodict.parse(xml)
    assert 'urlset' in result
    # rules are Ordered
    assert result['urlset']['url'][0]['loc'] == '/test_sitemap.xml'
    assert result['urlset']['url'][1]['loc'] == '/hello'
    assert result['urlset']['url'][2]['loc'] == '/this_is_a_test'

# permite testar manualmente o app
# python tests.py
# acesse localhost:5000/test_sitemap.xml
if __name__ == '__main__':
    app.run(debug=True)

```

Para que os testes acima sejam executados precisamos instalar algumas dependencias portanto o `requirements-test.txt` precisa deste conteúdo:

```
flask
pytest
xmltodict
--editable .
```

Vamos então começar a desenvolver editando primeiro o
`flask_simple_sitemap/templates/sitemap.xml` este template espera um dict `paths`
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

E então escrevemos a classe base da extensão no arquivo `flask_simple_sitemap/base.py`

Lembrando de algumas boas práticas:

- Prover um método de inicialização lazy com a assinatura `init_app(self, app)`
- Impedir registro em duplicidade e inserir um registro no `app.extensions`
- Ao adicionar rotas sempre usar Blueprints e namespaces
- Configs devem sempre ter um prefixo (já aprendemos a usar o config namespace do Flask na parte 1)
- Ao instanciar a extensão o `__init__` deve receber `app` como um parametro opcional

> NOTE: Leia atentamente os comentários e docstrings do código abaixo.

```python
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

        # OBS: Não tenha medo de repetir os dados! tem horas que o DRY não se
        aplica! lembre-se do Zen do Python: `praticidade vence a pureza` :)
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

> **NOTE**: Neste exemplo usamos um método de desenvolvimento muito legal chamado **ITF** (**Important Things First**).
> Arquitetura, documentação, testes e front end são muito mais importantes do que a implementação em si.
> assumimos que mesmo que a nossa implementação seja alterada os conceitos anteriores se mantém integros com a proposta do produto.
> **1)** definimos a arquitetura **2)** escrevemos documentação **3)** escrevemos testes **4)** implementamos o código do front end **5)** back end é o menos importante do ponto de vista do produto e por isso ficou para o final! :)

O código da extensão etá disponível em [http://github.com/rochacbruno/flask_simple_sitemap](http://github.com/rochacbruno/flask_simple_sitemap)

# Usando a extensão em nosso CMS de notícias

Agora vem a melhor parte, usar a extensão recém criada em nosso projeto existente.




> O diff com as alterações realizadas com o Flask-Cache encontra-se em [27bacd25a788ffc041de332403a2426cd199b828](https://github.com/rochacbruno/wtf/commit/27bacd25a788ffc041de332403a2426cd199b828)

Algumas outras extensões recomendadas que não foram abordadas neste artigo

- [Flask Email] Para avisar os autores que tem novo comentário
- [Flask Queue/Celery] Pare enviar o email assincronamente e não bloquear o request
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

