Title: TDD com Python e Flask
Date: 2016-03-14 11:59
Tags: tdd, test driven development, flask
Category: TDD
Slug: tdd-com-python-e-flask
Author: Eduardo Cuducos
About_author: Sociólogo, geek, cozinheiro e fã de esportes.
Email:  cuducos@gmail.com
Github: cuducos
Site: http://cuducos.me
Twitter: cuducos
Linkedin: cuducos

# TDD com Python e Flask

> Baseado na palestra que ofereci no [encontro](http://www.meetup.com/Grupy-SP/events/228437612/) do [Grupy-SP](https://groups.google.com/forum/#!forum/grupy-sp), em 12 de março de 2016. O código dessa atividade está disponível no [meu GitHub](https://github.com/cuducos/grupy-python-tdd-flask).

A ideia desse exercício é introduzir a ideia de _test driven development_ (TDD) usando [Python](http://http://python.org) e [Flask](http://flask.pocoo.org/) — digo isso pois a aplicação final desse “tutorial” não é nada avançada, tampouco funcional. E isso se explica por dois motivos: primeiro, o foco é sentir o que é o _driven_ do TDD, ou seja, como uma estrutura de _tests first_ (sempre começar escrevendo os testes, e não a aplicação) pode guiar o processo de desenvolvimento; e, segundo, ser uma atividade rápida, de mais ou menos 1h.

Em outras palavras, não espere aprender muito de Python ou Flask. Aqui se concentre em sentir a diferença de utilizar uma método de programar. Todo o resto é secundário.

## 1. Preparando o ambiente

### Requisitos

Para esse exercício usaremos o Python versão 3.5.1 com o framework Flask versão 0.10.1. É recomendado, mas não necessário, usar um [virtualenv](http://virtualenv.readthedocs.org).

> Como o código é bem simples, não acho que você vá ter muitos problemas se utilizar uma versão mais antiga do Python (ou mesmo do Flask). Em todo caso, em um detalhe ou outro você pode se deparar com mensagens distintas se utilizar o Python 2.

Você pode verificar a versão do seu Python com esse comando:

```console
$ python --version                                                                                    
```

Dependendo da sua instalação, pode ser que você tenha que usar `python3` ao invés de `python` — ou seja, o comando todo deve ser `python3 --version`. O resultado deve ser esse:

```
Python 3.5.1
```

E instalar o Flask assim:

```
$ pip install Flask
```

O `pip` é um gerenciador de pacotes do Python. Ele vem instalado por padrão nas versões mais novas do Python. Dependendo da sua instalação, pode ser que você tenha que usar `pip3` ao invés de `pip` — ou seja, o comando todo deve ser `pip3 install Flask`. Com esse comando ele vai instalar o Flask e qualquer dependência que o Flask tenha:

```console
Collecting Flask
Collecting Jinja2>=2.4 (from Flask)
  Using cached Jinja2-2.8-py2.py3-none-any.whl
Collecting itsdangerous>=0.21 (from Flask)
Collecting Werkzeug>=0.7 (from Flask)
  Using cached Werkzeug-0.11.4-py2.py3-none-any.whl
Collecting MarkupSafe (from Jinja2>=2.4->Flask)
Installing collected packages: MarkupSafe, Jinja2, itsdangerous, Werkzeug, Flask
Successfully installed Flask-0.10.1 Jinja2-2.8 MarkupSafe-0.23 Werkzeug-0.11.4 itsdangerous-0.24
```
### Arquivos 

Vamos usar, nesse exercício, basicamente 2 arquivos:

* `app.py`: onde criamos nossa aplicação web;;
* `tests.py`: onde escrevemos os testes que guiarão o desenvolvimento da aplicação, e que, também, garantirão que ela funcione.


## 2. Criando a base dos testes

No arquivo `tests.py` vamos usar o módulo [unittest](https://docs.python.org/3.5/library/unittest.html), que já vem instalado por padrão no Python.

Criaremos uma estrutura básica para que, toda vez que esse arquivo seja executado, o `unittest` se encarregue de encontrar todos os nossos testes e rodá-los.

Vamos começar escrevendo com uma exemplo fictício: testes para um método que ainda não criamos, um método que calcule números fatoriais. A ideia é só entender como escreveremos testes em um arquivo (`tests.py`) para testar o que escreveremos no outro arquivo (`app.py`).

A estrutura básica a seguir cria um caso de teste da `unittest` e, quado executada, teste nosso método `fatorial(numero)` para todos os números de 0 até 6:

```python
import unittest


class TestFatorial(unittest.TestCase):

    def test_fatorial(self):
        self.assertEqual(fatorial(0), 1)
        self.assertEqual(fatorial(1), 1)
        self.assertEqual(fatorial(2), 2)
        self.assertEqual(fatorial(3), 6)
        self.assertEqual(fatorial(4), 24)
        self.assertEqual(fatorial(5), 120)
        self.assertEqual(fatorial(6), 720)

if __name__ == '__main__':
    unittest.main()
```

Se você conhece um pouco de inglês, pode ler o código em voz alta, ele é quase auto explicativo: importamos o módulo _unittest_ (linha 1), criamos um objeto que é um caso de teste do método fatorial (linha 4), escrevemos um método de teste (linha 6) e esse método se assegura de que o retorno de `fatorial(numero)` é o resultado que esperamos (linhas 5 a 11).

Agora podemos rodar os testes assim:

```console
$ python testes.py
```

Veremos uma mensagem de erro, `NameError`, pois não definimos nossa função `fatorial(numero)`:

```
E
======================================================================
ERROR: test_fatorial (__main__.TestSimples)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 7, in test_fatorial
    self.assertEqual(fatorial(0), 1)
NameError: name 'fatorial' is not defined

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
```

Tudo bem, a ideia não é brincar com matemática agora. Mas vamos criar essa função lá no `app.py` só para ver como a gente pode “integrar” esses dois arquivos — ou seja, fazer o `tests.py` testar o que está em `app.py`.

Vamos adicionar essas linhas ao `app.py`:

```python
def fatorial(numero):
    if numero in (0, 1):
        return 1
    return numero * fatorial(numero - 1)
```

E adicionar essa linha no topo do `tests.py`:

```python
from app import fatorial
```

Agora, rodando os testes vemos que a integração entre `app.py` e `tests.py` está funcionando:

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Ótimo. Chega de matemática, vamos ao TDD com Flask, um caso muito mais tangível do que encontramos no nosso dia-a-dia.

## 3. Primeiros passos para a aplicação web

### Criando um servidor web

Como nosso foco é começar uma aplicação web, podemos descartar os testes e o método fatorial que criamos no passo anterior. Ao invés disso, vamos escrever um teste simples, para ver se conseguimos fazer o Flask criar um servidor web.

Descarte tudo do `tests.py` substituindo o conteúdo do arquivo por essas linhas:

```python
import unittest
from app import meu_web_app


class TestHome(unittest.TestCase):

    def test_get(self):
        app = meu_web_app.test_client()
        response = app.get('/')
        self.assertEqual(200, response.status_code)
        
if __name__ == '__main__':
    unittest.main()
```

Esse arquivo agora faz quatro coisas referentes a nossa aplicação web:

1. Importa o objeto `meu_web_app` (que ainda não criamos) do nosso arquivo `app.py`;
1. Cria uma instância da nossa aplicação web específica para nossos testes (é o método `meu_web_app.test_client()`, cujo retorno batizamos de `app`);
1. Tenta acessar a “raíz” da nossa aplicação — ou seja, se essa aplicação web estivesse no servidor `pythonclub.com.br` estaríamos acessando [http://pythonclub.com.br/](http://pythonclub.com.br/).
1. Verifica se, ao acessar esse endereço, ou seja, se ao fazer a requisição HTTP para essa URL, temos como resposta o código 200, que representa sucesso.

Os códigos de status de requisição HTTP mais comuns são o `200` (sucesso), `404` (página não encontrada) e `302` (redirecionamento) — mas a [lista de completa](https://pt.wikipedia.org/wiki/Lista_de_códigos_de_status_HTTP) é muito maior que isso. 

De qualquer forma não conseguiremos rodar esses testes. O interpretador do Python vai nos retornar um erro:

```
ImportError: cannot import name 'meu_web_app'
```

Então vamos criar o objeto `meu_web_app` lá no `app.py`. Descartamos tudo que tínhamos lá substituindo o contéudo do arquivo por essas linhas:

```python
from flask import Flask

meu_web_app = Flask()
```

Apenas estamos importando a classe principal do Flask, e criando uma instância dela. Em outras palavras, estamos começando a utilizar o framework.

E agora o erro muda:

```
Traceback (most recent call last):
  File "tests.py", line 2, in <module>
    from app import meu_web_app
  File "/Users/cuducos/Desktop/flask/app.py", line 3, in <module>
    meu_web_app = Flask()
TypeError: __init__() missing 1 required positional argument: 'import_name'
```

Importamos nosso `meu_web_app`, mas quando instanciamos o Flask temos um problema. Qual problema? O erro nos diz: quando tentamos chamar `Flask()` na linha 3 do `app.py` está faltando um argumento posicional obrigatório (_missing 1 required positional argument_). Estamos chamando `Flask()` sem nenhum argumento. O erro ainda nos diz que o que falta é um nome (_import_name_). Vamos batizar nossa instância com um nome:

```python
meu_web_app = Flask(`meu_web_app`)
```

E agora temos uma nova mensagem de erro, ou seja, progresso!

> Eu amo testes que falham! A melhor coisa é uma notificação em vermelho me dizendo que os testes estão falhando. Isso significa que eu tenho testes e que eles estão funcionando!
> 
> — [Bruno Rocha](https://twitter.com/rochacbruno)

```
F
======================================================================
FAIL: test_get (__main__.TestHome)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 10, in test_get
    self.assertEqual(200, response.status_code)
AssertionError: 200 != 404

----------------------------------------------------------------------
Ran 1 test in 0.015s

FAILED (failures=1)
```

Temos uma aplicação web rodando, mas quando tentamos acessar a raíz dela, ela nos diz que a página não está definida, não foi encontrada (é o que nos diz o código `404`).

### Criando nossa primeira página

O Flask facilita muito a criação de aplicações web. De forma simplificada a qualquer método Python pode ser atribuída uma URL. Isso é feito com um decorador:

```
@app.route('/')
def pagina_inicial():
    return ''
```

Adicionando essas linhas no `app.py`, os testes passam:

```
.
----------------------------------------------------------------------
Ran 1 test in 0.013s

OK
```

Se a curiosidade for grande, esse artigo (em inglês) explica direitinho como o `Flask.route(rule, **options)` funciona: [Things which aren't magic - Flask and @app.route](http://ains.co/blog/things-which-arent-magic-flask-part-1.html).

Para garantir que tudo está certinho mesmo, podemos adicionar mais um teste. Queremos que a resposta do servidor seja um HTML:

```python
def test_content_type(self):
    app = meu_web_app.test_client()
    response = app.get('/')
    self.assertIn('text/html', response.content_type)
```

Rodando os testes, veremos que agora temos dois testes. E ambos passam!

### Eliminando repetições

Repararam que duas linhas se repetem nos métodos `test_get()` e `test_content_type()`?

```python
app = meu_web_app.test_client()
response = app.get('/')
```

Podemos usar um método especial da classe `unittest.TestCase` para reaporiveitar essas linhas. O método `TestCase.setUp()` é executado ao iniciar cada teste, e através do `self` podemos acessar objetos de um método a partir de outro método:

```python
class TestHome(unittest.TestCase):

    def setUp(self):
        app = meu_web_app.test_client()
        self.response = app.get('/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn('text/html', self.response.content_type)
```

Não vamos precisar nesse exemplo, mas o método `TestCase.tearDown()` é executado ao fim de cada teste (e não no início, como a `setUp()`). Ou seja, se precisar repetir algum comando sempre após cada teste, a `unittest` também faz isso para você.

## 4. Preenchendo a página

### Conteúdo como resposta

Temos um servidor web funcionando, mas não vemos nada na nossa aplicação web. Podemos verificar isso em três passos rápidos:

Primeiro adicionamos essas linhas ao `app.py` para que, quando executarmos o `app.py` (mas não quando ele for importado no `tests.py`), a aplicação web seja iniciada:

```python
if __name__ == "__main__":
    meu_web_app.run()
```

Depois executamos o arquivo:

```console
$ python app.py
```

Assim vemos no terminal essa mensagem:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Se acessarmos essa URL no nosso navegador, podemos ver a aplicação rodando: [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

E veremos que realmente não há nada, é uma página em branco.

Vamos mudar isso! Vamos construir o que seria uma página individual, mostrando quem a gente é. Na minha vou querer que esteja escrito (ao menos), meu nome. Então vamos escrever um teste para isso:

```python
def test_content(self):
    self.assertIn('Eduardo Cuducos', self.response.data)
```

Feito isso, teremos uma nova mensagem de erro nos testes:

```
TypeError: a bytes-like object is required, not 'str'
```

Essa mensagem nos diz que estamos comparando uma _string_ com um objeto que é de outro tipo, que é representado por _bytes_. Não é isso que queremos. Como explicitamente passamos para o teste uma _string_ com nosso nome, podemos assumir que é o `self.response.data` que vem codificado em _bytes_. Vamos decodificá-lo para _string_.

> _Bytes precisam ser decodificados para string (método `decode`). Strings precisam ser codificados para bytes para então mandarmos o conteúdo para o disco, para a rede (método `encode`)._
>
> — [Henrique Bastos](http://henriquebastos.net)

```python
def test_content(self):
    self.assertIn('Eduardo Cuducos', self.response.data.decode('utf-8'))
```

Assim temos uma nova mensagem de erro:

```
AssertionError: 'Eduardo Cuducos' not found in "b''"
```

Nossa página está vazia, logo o teste não consegue encontrar meu nome na página. Vamos resolver isso lá no `app.py`:

```python
@meu_web_app.route('/')
def pagina_inicial():
    return 'Eduardo Cuducos'
```

Agora temos os testes passando, e podemos verificar isso vendo que temos o nome na tela do navegador.

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.015s

OK
```

### Apresentando o conteúdo com HTML

O Python e o Flask cuidam principalmente do back-end da apliacação web — o que ocorre “por trás dos panos” no lado do servidor.

Mas temos também o front-end, que é o que o usuário vê, a interface com a qual o usuário interage. Normalmente o front-end é papel de outras linguagens, como o HTML, o CSS e o JavaScript.

Vamos começar com um HTML básico, criando a pasta `templates` e dentro dela o arquivo `home.html`:

```html
<!DOCTYPE HTML>
<html>
  <head>
	<title>Eduardo Cuducos</title>
  </head>
  <body>
    <h1>Eduardo Cuducos</h1>
    <p>Sociólogo, geek, cozinheiro e fã de esportes.</p>
  </body>
</html>
```

Se a gente abrir essa página no navegador já podemos ver que ela é um pouco menos do que o que a gente tinha antes. Então vamos alterar nosso `test_content()` para garantir que ao invés de termos somente a _string_ com nosso nome na aplicação, tempos esse templete renderizado:

```python
def test_content(self):
    response_str = self.response.data.decode('utf-8')
    self.assertIn('<title>Eduardo Cuducos</title>', str(response_str))
    self.assertIn('<h1>Eduardo Cuducos</h1>', str(response_str))
    self.assertIn('<p>Sociólogo, ', str(response_str))
```

Assim vemos nossos testes falharem:

```
F..
======================================================================
FAIL: test_content (__main__.TestHome)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 18, in test_content
    self.assertIn('<title>Eduardo Cuducos</title>', str(self.response.data))
AssertionError: '<title>Eduardo Cuducos</title>' not found in "b'Eduardo Cuducos'"

----------------------------------------------------------------------
Ran 3 tests in 0.017s

FAILED (failures=1)
```

Criamos um HTML, mas ainda não estamos pedindo para o Flask utilizá-lo. Temos nossa `home.html` dentro da pasta `templates` pois é justamente lá que o Flask vai buscar templates. Sabendo disso, podemos fazer nosso método `index()` retornar não a string, mas o template:

```python
from flask import Flask, render_template

…

@meu_web_app.route('/')
def pagina_inicial():
    return render_template('home.html')
```

Assim voltamos a ter testes passando — e a página fica um pouco mais apresentável.

### Formatando o conteúdo com CSS

Para não perder muito o foco do Python, TDD e Flask, vamos utilizar um framework CSS que se chama [Bootstrap](http://getbootstrap.com/). Incluindo o CSS desse framework no nosso HTML, e utilizando algumas classes especificas dele, conseguimos dar uma cara nova para nossa aplicação.

Vamos escrever um teste para verificar se estamos mesmo carregando o Bootstrap:

```python
def test_bootstrap_css(self):
    response_str = self.response.data.decode('utf-8')
    self.assertIn('bootstrap.min.css', response_str)
```

Os testes falham. Temos que linkar o CSS do Bootstrap em nosso HTML. Ao invés de baixar o Bootstrap, vamos utilizar o [servidor CDN que eles mesmo recomendam](http://getbootstrap.com/getting-started/#download-cdn). É só incluir essa linha no `<head>` do nosso HTML:

```html
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
```

Agora, com os testes passando, vamos utilizar as classes do Bootstrap para formatar melhor nossa página. Vamos retirar nosso `<h1>` e `<p>` e, ao invés disso, partir do componente [Jumbotron](http://getbootstrap.com/components/#jumbotron) fazendo algumas pequenas alterações:

```html
<div class="container">
  <div class="jumbotron">
    <img src="https://avatars.githubusercontent.com/u/4732915?v=3&s=128" alt="Eduardo Cuducos" class="img-circle">
    <h1>Eduardo Cuducos</h1>
    <p>Sociólogo, geek, cozinheiro e fã de esportes.</p>
    <p><a class="btn btn-primary btn-lg" href="http://twitter.com/cuducos" role="button">Me siga no Twitter</a></p>
  </div>
</div>
```

Com essa página “incrementada” podemos ainda refinar nossos testes, garantindo que sempre temos a foto e o link:

```python
def test_profile_image(self):
    response_str = self.response.data.decode('utf-8')
    self.assertIn('<img src="', response_str)
    self.assertIn('class="img-circle"', response_str)

def test_link(self):
    response_str = self.response.data.decode('utf-8')
    self.assertIn('href="http://twitter.com/cuducos"', response_str)
    self.assertIn('>Me siga no Twitter</a>', response_str)
```

Pronto, agora temos uma página formatada para mostrar para nossos colegas, com todos os testes passando:

```
......
----------------------------------------------------------------------
Ran 6 tests in 0.024s

OK
```


## 5. Conteúdos dinâmicos

### Passando variáveis para o contexto do template

O problema da nossa página é que ela é estática. Vamos usar o Python e o Flask para que quando a gente acesse `/cuducos` a gente veja a minha página, com meus dados. Mas caso a gente acesse `/z4r4tu5tr4`, a gente o conteúdo referente ao outro Eduardo que palestrou no Grupy comigo.

Antes de mudar nossas URLS, vamos refatorar nossa aplicação e — importantíssimo! — os testes tem que continuar passando. A ideia é evitar que o conteúdo esteja “fixo” no template. Vamos fazer o conteúdo ser passado do método `pagina_principal()` para o template.

A ideia é extrair todo o conteúdo do nosso HTML criando um dicionário no `app.py`:

```python
CUDUCOS = {'nome': 'Eduardo Cuducos',
           'descricao': 'Sociólogo, geek, cozinheiro e fã de esportes.',
           'url': 'http://twitter.com/cuducos',
           'nome_url': 'Twitter',
           'foto': 'https://avatars.githubusercontent.com/u/4732915?v=3&s=128'}
```

E, na sequência, usar esse dicionário para passar uma variável chamada `perfil` para o contexto do template:

```python
@meu_web_app.route('/')
def pagina_inicial():
    return render_template('home.html', perfil=CUDUCOS)
```

Por fim, vamor utilizar, ao invés das minhas informações, a variável `perfil` no template:

```html
<!DOCTYPE HTML>
<html>
  <head>
    <title>{{ perfil.nome }}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container">
      <div class="jumbotron">
        <img src="{{ perfil.foto }}" alt="{{ perfil.nome }}" class="img-circle">
        <h1>{{ perfil.nome }}</h1>
        <p>{{ perfil.descricao }}</p>
        <p><a class="btn btn-primary btn-lg" href="{{ perfil.url }}"
            role="button">Me siga no {{ perfil.nome_url }}</a></p>
      </div>
    </div>
  </body>
</html>
```

Feito isso, temos todas as informações disponíveis no nosso ambinete Python, e não mais no HTML. E os testes nos garantem que no final das contas, para o usuário, a página não mudou — ou seja, estamos mostrando as informações corretamente.

### Criando conteúdo dinâmico

Vamos agora criar um outro dicionário para termos informações de outras pessoas. E vamos juntar todos os perfis em uma variável chamada `PERFIS`:

```python
MENDES = {'nome': 'Eduardo Mendes',
          'descricao': 'Apaixonado por software livre e criador de lambdas.',
          'url': 'http://github.com/z4r4tu5tr4',
          'nome_url': 'GitHub',
          'foto': 'https://avatars.githubusercontent.com/u/6801122?v=3&s=128'}

PERFIS = {'cuducos': CUDUCOS,
          'z4r4tu5tr4': MENDES}
```

Agora, se utilizarmos nossa `pagina_principal()` com o primeiro perfil, nossos testes passam. Podemos passar o outro perfil e ver, no navegador, que já temos a nossa página com outras informações:

```python
@meu_web_app.route('/')
def pagina_inicial():
    return render_template('home.html', perfil=PERFIS['z4r4tu5tr4'])
```

Mas se rodarmos os testes assim, veremos duas falhas:

```
.F..F.
======================================================================
FAIL: test_content (__main__.TestHome)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 19, in test_content
    self.assertIn('<title>Eduardo Cuducos</title>', str(response_str))
AssertionError: '<title>Eduardo Cuducos</title>' not found in '<!DOCTYPE HTML>\n<html>\n  <head>\n    <title>Eduardo Mendes</title>\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">\n  </head>\n  <body>\n    <div class="container">\n      <div class="jumbotron">\n        <img src="https://avatars.githubusercontent.com/u/6801122?v=3&amp;s=128" alt="Eduardo Mendes" class="img-circle">\n        <h1>Eduardo Mendes</h1>\n        <p>Apaixonado por software livre e criador de lambdas.</p>\n        <p><a class="btn btn-primary btn-lg" href="http://github.com/z4r4tu5tr4"\n            role="button">Me siga no GitHub</a></p>\n      </div>\n    </div>\n  </body>\n</html>'

======================================================================
FAIL: test_link (__main__.TestHome)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "tests.py", line 34, in test_link
    self.assertIn('href="http://twitter.com/cuducos"', response_str)
AssertionError: 'href="http://twitter.com/cuducos"' not found in '<!DOCTYPE HTML>\n<html>\n  <head>\n    <title>Eduardo Mendes</title>\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">\n  </head>\n  <body>\n    <div class="container">\n      <div class="jumbotron">\n        <img src="https://avatars.githubusercontent.com/u/6801122?v=3&amp;s=128" alt="Eduardo Mendes" class="img-circle">\n        <h1>Eduardo Mendes</h1>\n        <p>Apaixonado por software livre e criador de lambdas.</p>\n        <p><a class="btn btn-primary btn-lg" href="http://github.com/z4r4tu5tr4"\n            role="button">Me siga no GitHub</a></p>\n      </div>\n    </div>\n  </body>\n</html>'

----------------------------------------------------------------------
Ran 6 tests in 0.024s

FAILED (failures=2)
```

Os testes nos dizem que bagunçamos as informações. Os testes de conteúdo não encontram mais `Eduardo Cuducos` na página, nem o link para `http://twitter.com/cuducos`.

Vamos arrumar isso fazendo um caso de teste para cada perfil. Vamos mudar também nosso esquema de URL. Ao invés de testar a raíz da aplicação, vamos testar se em `/nome-do-usuário` vemos as informações desse usuário.

Vamos renomear `TestGet` para `TestCuducos` e mudar a URL no `setUp()`:

```python
class TestCuducos(unittest.TestCase):

    def setUp(self):
        app = meu_web_app.test_client()
        self.response = app.get('/cuducos')
```

Agora podemos duplicar toda essa classe renomeando-a para `TestZ4r4tu5tr4`, substituindo as informações pertinentes:

```python
class TestZ4r4tu5tr4(unittest.TestCase):

    def setUp(self):
        app = meu_web_app.test_client()
        self.response = app.get('/z4r4tu5tr4')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn('text/html', self.response.content_type)

    def test_content(self):
        response_str = self.response.data.decode('utf-8')
        self.assertIn('<title>Eduardo Mendes</title>', str(response_str))
        self.assertIn('<h1>Eduardo Mendes</h1>', str(response_str))
        self.assertIn('<p>Apaixonado por software livre', str(response_str))

    def test_bootstrap_css(self):
        response_str = self.response.data.decode('utf-8')
        self.assertIn('bootstrap.min.css', response_str)

    def test_profile_image(self):
        response_str = self.response.data.decode('utf-8')
        self.assertIn('<img src="', response_str)
        self.assertIn('class="img-circle"', response_str)

    def test_link(self):
        response_str = self.response.data.decode('utf-8')
        self.assertIn('href="http://github.com/z4r4tu5tr4"', response_str)
        self.assertIn('>Me siga no GitHub</a>', response_str)
```

Testes prontos… e falhando, claro. Não mudamos nosso esquema de URLs no Flask. Voltemos ao `app.py`.

Podemos começar com algo repetitivo, mas simples:

```pyhton
@meu_web_app.route('/cuducos')
def pagina_inicial_cuducos():
    perfil = PERFIS['cuducos']
    return render_template('home.html', perfil=perfil)


@meu_web_app.route('/z4r4tu5tr4')
def pagina_inicial_z4r4tu5tr4():
    perfil = PERFIS['z4r4tu5tr4']
    return render_template('home.html', perfil=perfil)
```

Como resultado, temos nossa aplicação com conteúdo dinâmico, com testes passando e funcionando!

Podemos melhorar um pouco mais. Essa repetição dos métodos `pagina_inicial_cuducos()` e `pagina_inicial_z4r4tu5tr4()` é facilmente evitada no Flask:

```pyhton
@meu_web_app.route('/<perfil>')
def pagina_inicial(perfil):
    perfil = PERFIS[perfil]
    return render_template('home.html', perfil=perfil)
```

Agora o Flask recebe uma variável `perfil` depois da `/` (e sabemos que é uma variável pois envolvemos o nome `perfil` entre os sinais de `<` e `>`). E utilizamos essa variável para escolhar qual perfil passar para nosso tempate.

## Considerações finais

Se chegou até aqui, vale a pena ressaltar que esse post tem apenas o objetivo de introduzir a ideia básica do TDD. Ou seja: ver como o hábito, o método de programar pouco a pouco (_baby steps_) e sempre começando com os testes te dão dois benefícios sensacionais: eles não só garantem que a aplicação funcionará como esperado, mas eles guiam o próprio processo de desenvolvimento. As mensagens de erro te dizer – muitas vezes literalmente — o qual é a próxima linha de código que você vai escrever.

E, se chegou até aqui, talvez você queira se aprofundar nos assuntos dos quais falamos. Além de inúmeros posts aqui do blog, ressalto mais algumas referências.

Leituras recomendadas para conhecer mais sobre Flask:

* Em português: [Tutorial](http://pythonclub.com.br/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python) (ainda incompleto) do [Bruno Rocha](https://twitter.com/rochacbruno)
* Em inglês: [Tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) ou [livro](http://flaskbook.com) do [Miguel Grinberg](https://twitter.com/miguelgrinberg)

Leitura recomendada para conhecer mais sobre TDD:

* Em inglês: [Livro](http://shop.oreilly.com/product/0636920029533.do) do [Harry Percival](https://twitter.com/hjwp)
* Em inglês: essa [resposta](http://stackoverflow.com/questions/4904096/whats-the-difference-between-unit-functional-acceptance-and-integration-test/4904533#4904533) no Stack Overflow sobre _unit_, _integration_, _functional_ e _acceptance test_.

> Quem aprendeu alguma coisa nova?
>
> — [Raymond Hettinger](https://twitter.com/raymondh)
