Title: Python com Unittest, Travis CI, Coveralls e Landscape (Parte 1 de 4)
Slug: python-com-unittest-travis-ci-coveralls-e-landscape-parte-1-de-4
Date: 2016-05-06 01:42:18 -0300
Category: Python
Tags: git, travis-ci, python, coveralls, landscape, test, tutorial
Author: Michell Stuttgart
Email: michellstut@gmail.com
Github: mstuttgart
Linkedin: michellstut
Facebook: michell.stuttgart
Site: http://codigoavulso.com.br

Fala pessoal, tudo certo?

Durante o desenvolvimento de um software, tão importante quanto escrever um código organizado e que siga as melhores práticas, é garantir que o mesmo cumpra os requisitos a que ele se propõe. Em outras palavras, garantir que o software funcione de maneira adequada.

O processo de testes de um software faz parte do seu desenvolvimento, porém muitas vezes ele é encarado como algo tedioso e desnecessário. Entretanto, todo bom desenvolvedor sabe que investir tempo escrevendo testes para seu software está longe de ser "desperdício de tempo". O processo de teste, quando feito por uma pessoa, além de sujeitos a falhas é tedioso e demorado. Tendo isso em mente, podemos lançar mão de ferramentas que realizarão o processo de teste por nós. Em Python, umas das ferramentes da bibloteca padrão destinada a teste é a `Unittest`, que usaremos nesse tutorial.

Nesta série de postagem, irei mostrar o passo-a-passo na criação de testes unitários para um pequeno projeto que vamos criar no github. Vou explicar como configurar a ferramenta [Travis](https://travis-ci.org/), que será responsável por executar os nossos testes no github. A ferramenta [Coveralls](https://coveralls.io/), que mapeia nosso código, e nos indica o quanto dele está coberto por testes. E como bônus, adicionar ao nosso projeto o [Landscape](https://landscape.io), ferramenta que monitora a "saúde" do nosso código.

### Iniciando nosso projeto

Inicialmente, criei no [github](https://github.com/) um repositório que vai receber meu código e que posteriormente será configurado para rodar nossos testes. No meu caso, o repositório foi esse [codigo-avulso-test-tutorial](https://github.com/mstuttgart/codigo-avulso-test-tutorial). Após realizar o clone, criei a seguite estrutura de diretorios:

```
.
├── codigo_avulso_test_tutorial
│   └── __init__.py
├── LICENSE
├── README.md
└── test
    └── __init__.py

```

O diretório `codigo_avulso_test_tutorial` receberá o código da nossa aplicação e o diretório `test` receberá o código de teste.
O nosso projeto consiste de um grupo de classes representando figuras geométricas (quadrados, círculos e etc). Teremos uma classe base chamada `FiguraGeometrica` que possui dois métodos, a saber: `get_area` e `get_perimetro`, sendo ambos metódos abstratos. Cada uma dessas classes filhas de `FiguraGeometrica` irá possuir sua própria implementação desses métodos.

Dentro do diretório `codigo_avulso_test_tutorial`, irei criar os fontes do nosso código:

```bash
touch figura_geometrica.py circulo.py quadrado.py
```

Dentro do diretório `test`, irei criar os fontes do nosso código de teste:

```bash
touch figura_geometrica_test.py circulo_test.py quadrado_test.py
```

Uma observação importante é que os arquivos de teste devem ter o nome terminado em `test`, para que o módulo de Unittest encontre os nossos arquivos de teste automaticamente. Após a criação dos arquivos, teremos a seguinte estrutura de diretório:

```
.
├── codigo_avulso_test_tutorial
│   ├── circulo.py
│   ├── figura_geometrica.py
│   ├── __init__.py
│   └── quadrado.py
├── LICENSE
├── README.md
└── test
    ├── circulo_test.py
    ├── figura_geometrica_test.py
    ├── __init__.py
    └── quadrado_test.py
```

Iniciemos agora a implementação do nosso projeto. Mas antes vamos dar uma olhada em alguns conceitos.

### Test Driven Development (TDD)

Neste momento, leitor, você deve estar se perguntando: "Não deveríamos escrever primeiro o nosso código e depois escrever os testes?".

Não necessariamente. O processo de escrever os testes antes do código é chamado de `TDD -  Test Driven Development`. Segundo a [wikipedia](https://pt.wikipedia.org/wiki/Test_Driven_Development):

> "Test Driven Development (TDD) ou em português Desenvolvimento guiado por testes é uma técnica de desenvolvimento de software que baseia em um ciclo curto de repetições: Primeiramente o desenvolvedor escreve um caso de teste automatizado que define uma melhoria desejada ou uma nova funcionalidade. Então, é produzido código que possa ser validado pelo teste para posteriormente o código ser refatorado para um código sob padrões aceitáveis. Kent Beck, considerado o criador ou o 'descobridor' da técnica, declarou em 2003 que TDD encoraja designs de código simples e inspira confiança[1] . Desenvolvimento dirigido por testes é relacionado a conceitos de programação de Extreme Programming, iniciado em 1999,[2] mas recentemente tem-se criado maior interesse pela mesma em função de seus próprios ideais.[3] Através de TDD, programadores podem aplicar o conceito de melhorar e depurar código legado desenvolvido a partir de técnicas antigas.[4]"

### Criando o setup.py

Antes de começar a implementar o códigos de teste, vamos criar o arquivo `setup.py`. Esse arquivo contém informações sobr e o nosso módulo python e facilita em muito a utilização dos testes. Então, vamos criar o arquivo `setup.py` na pasta raiz do nosso projeto.

```bash
touch setup.py
```

A estrutura do nosso projeto agora está assim:

```
.
├── codigo_avulso_test_tutorial
│   ├── circulo.py
│   ├── figura_geometrica.py
│   ├── __init__.py
│   └── quadrado.py
├── LICENSE
├── README.md
├── setup.py
└── test
    ├── circulo_test.py
    ├── figura_geometrica_test.py
    ├── __init__.py
    └── quadrado_test.py
```

Abra o `setup.py` em um editor e adicione as informações conforme exemplo abaixo:

```python
# -*- coding: utf-8 -*-
from setuptools import setup
setup(
    name='codigo-avulso-test-tutorial',
    packages=['codigo_avulso_test_tutorial', 'test'],
    test_suite='test',
)
```

No código acima, `name` representa o nome do seu projeto, `packages` são os diretórios do seu projeto que possuem código fonte e `test_suite` indica o diretório onde estão os fontes de teste. É importante declarar esse diretório pois o Unittest irá procurar dentro dele os arquivos de teste que iremos escrever.

### Criando testes para a classe FiguraGeometrica
Agora, vamos usar a lógica do TDD. Primeiro criamos o código de teste de uma classe para em seguida criamos o código da mesma. Das classes que criamos, o arquivo `figura_geometrica.py` servirá como uma classe base para as outras classes. Então vamos começar por elá.

Abra o arquivo `figura_geometrica_test.py` e seu editor preferido e adicione o código abaixo:

```python

# -*- coding: utf-8 -*-
from unittest import TestCase
from codigo_avulso_test_tutorial.figura_geometrica import FiguraGeometrica

# O nome da classe deve iniciar com a palavra Test
class TestFiguraGeometrico(TestCase):

    # Serve para incializar variavei que usaremos
    # globalmente nos testes
    def setUp(self):
        TestCase.setUp(self)
        self.fig = FiguraGeometrica()

    # Retorna uma NotImplementedError
    # O nome do metodo deve comecar com test
    def test_get_area(self):
        self.assertRaises(NotImplementedError, self.fig.get_area)

    # Retorna uma NotImplementedError
    # O nome do metodo deve comecar com test
    def test_get_perimetro(self):
        self.assertRaises(NotImplementedError, self.fig.get_perimetro)

```
Como podemos observar no código acima, a seguinte linha:

```python
def test_get_area(self):
    self.assertRaise(self.fig.test_get_area(), NotImplementedError)
```

Realiza o seguinte teste. Com o objeto `self.fig` criado no método `setUp()`, tentamos chamar o método `test_get_perimetro` da classe `FiguraGeometrica`, porém ele verifica se ocorreu a exceção `NotImplementedError`. Isso é feito porque a classe `FiguraGeometrica` é uma classe abstrata e possui ambos os métodos `get_area` e `get_perimetro` vazios. Isso irá ficar mais claro quando adicionarmos o código da classe `FiguraGeometrica`. Então, abra o arquivo `figura_geometrica.py` em seu editor e vamos adicionar o seguinte código:

```python
# -*- coding: utf-8 -*-

class FiguraGeometrica(object):

    # Retorna a area da figura
    def get_area(self):
        raise NotImplementedError

    # Retorna o perimetro da figura
    def get_perimetro(self):
        raise NotImplementedError

```

A class acima é bem simples. Ela possui um método que retorna a área e outro que retorna o perímetro da figura. Ambos são métodos *abstratos*, ou seja, devem ser implementados nas classes filhas da classe `FiguraGeometrica`. Se criarmos um objeto dessa classe e chamarmos um dos dois métodos, uma exceção do tipo `NotImplementedError` será lançada, pois ambos os métodos possuem escopo vazio.

Finalmente podemos executar o teste da nossa classe. Usando o terminal, no diretorio em que o arquivo `setup.py` está, execute o seguinte comando:

```bash
python setup.py test
```

Esse nosso comando vai executar a nossa classe `TestFiguraGeometrica`. Se tudo estiver correto, teremos a seguinte saída:

```
running test
running egg_info
writing codigo_avulso_test_tutorial.egg-info/PKG-INFO
writing top-level names to codigo_avulso_test_tutorial.egg-info/top_level.txt
writing dependency_links to codigo_avulso_test_tutorial.egg-info/dependency_links.txt
reading manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
running build_ext
test_get_area (test.figura_geometrica_test.TestFiguraGeometrico) ... ok
test_get_perimetro (test.figura_geometrica_test.TestFiguraGeometrico) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

Caso apareça uma resposta diferente, dê uma olhada na própria saída do teste. Ele indica onde está o erro. Provavelmente, pode ter sido algum erro de digitação, pois os exemplos deste tutorial foram todos testados.

### Criando testes para a classe Quadrado

Vamos criar agora outras classes que realmente fazem algo de útil e seus respectivos testes. Começando pela classe Quadrado, vamos escrever um teste para a mesma no arquivo `quadrado_test.py`.

```python
# -*- coding: utf-8 -*-

from unittest import TestCase
from codigo_avulso_test_tutorial.quadrado import Quadrado

class TestQuadrado(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.fig = Quadrado()

    def test_get_area(self):
        # Verificamos se o resultado é o esperado
        # de acordo com a formula de area do quadrado
        self.fig.lado = 2
        self.assertEqual(self.fig.get_area(), 4)
        self.fig.lado = 7.0
        self.assertEqual(self.fig.get_area(), 49.0)

    def test_get_perimetro(self):
        self.fig.lado = 2
        self.assertEqual(self.fig.get_perimetro(), 8)
        self.fig.lado = 7.0
        self.assertEqual(self.fig.get_perimetro(), 28.0)

```

Em seguida, adicionamos o código da classe `Quadrado` no arquivo `quadrado.py`:

```python
# -*- coding: utf-8 -*-

from figura_geometrica import FiguraGeometrica

class Quadrado(FiguraGeometrica):

    def __init__(self):
      self.lado = 0

    # Retorna a area do quadrado
    def get_area(self):
        return self.lado**2

    # Retorna o perimetro do quadrado
    def get_perimetro(self):
        return 4 * self.lado

```

Assim como fizemos no exemplo anterior, executamos os testes:

```bash
python setup.py test
```

Se tudo estiver certo, teremos a seguinte saída.

```
running test
running egg_info
writing codigo_avulso_test_tutorial.egg-info/PKG-INFO
writing top-level names to codigo_avulso_test_tutorial.egg-info/top_level.txt
writing dependency_links to codigo_avulso_test_tutorial.egg-info/dependency_links.txt
reading manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
running build_ext
test_get_area (test.quadrado_test.TestQuadrado) ... ok
test_get_perimetro (test.quadrado_test.TestQuadrado) ... ok
test_get_area (test.figura_geometrica_test.TestFiguraGeometrico) ... ok
test_get_perimetro (test.figura_geometrica_test.TestFiguraGeometrico) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

Uma detalhe interessante a ser observado é que agora os testes da classe `Quadrado` estão sendo executados junto com os testes da classe `FiguraGeometrica` sem que fosse necessário alterar nenhuma configuração do projeto, ou adicionar algum novo diretório no arquivo `setup.py`. Isso acontece por que usamos a sufixo `_test` no nome dos nossos código fonte de teste e também adicionamos o diretório `test` na tag `test_suite` no arquivo `setup.py`. Desse modo, quando executamos os testes, o módulo python `Unittest` percorre o diretório `test`, carrega automaticamente todos os arquivos com sufixo `_test` e executa os testes dentro deles. Bacana não é?

### Criando testes para a classe Circulo
Para encerrarmos o tutorial, vamos agora implementar os testes da classe Círculo.

```python
# -*- coding: utf-8 -*-
import math
from unittest import TestCase
from codigo_avulso_test_tutorial.circulo import Circulo

class TestCirculo(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.fig = Circulo()

    def test_get_area(self):
        # Utilizamos a formula diretamente por conveniencia
        # já que math.pi e double e sendo assim, possui
        # muitas casas decimais
        self.fig.raio = 2
        area = math.pi * self.fig.raio**2
        self.assertEqual(self.fig.get_area(), area)

        self.fig.raio = 7.0
        area = math.pi * self.fig.raio**2
        self.assertEqual(self.fig.get_area(), area)

    def test_get_perimetro(self):
        self.fig.raio = 2
        perimetro = 2 * math.pi * self.fig.raio
        self.assertEqual(self.fig.get_perimetro(), perimetro)

        self.fig.raio = 7.0
        perimetro = 2 * math.pi * self.fig.raio
        self.assertEqual(self.fig.get_perimetro(), perimetro)

```

E agora a classe Circulo:

```python
# -*- coding: utf-8 -*-
import math
from figura_geometrica import FiguraGeometrica

class Circulo(FiguraGeometrica):

    def __init__(self):
      self.raio = 0

    # Retorna a area do circulo
    def get_area(self):
        return math.pi * self.raio**2

    # Retorna o perimetro do circulo
    def get_perimetro(self):
        return 2 * math.pi * self.raio

```

Finalmente, rodamos os testes agora com a presença da classe circúlo:

```bash
python setup.py test
```

Se tudo estiver certo, teremos a seguinte saída.

```
running test
running egg_info
writing codigo_avulso_test_tutorial.egg-info/PKG-INFO
writing top-level names to codigo_avulso_test_tutorial.egg-info/top_level.txt
writing dependency_links to codigo_avulso_test_tutorial.egg-info/dependency_links.txt
reading manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
running build_ext
test_get_area (test.quadrado_test.TestQuadrado) ... ok
test_get_perimetro (test.quadrado_test.TestQuadrado) ... ok
test_get_area (test.figura_geometrica_test.TestFiguraGeometrico) ... ok
test_get_perimetro (test.figura_geometrica_test.TestFiguraGeometrico) ... ok
test_get_area (test.circulo_test.TestCirculo) ... ok
test_get_perimetro (test.circulo_test.TestCirculo) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK

```

### Conclusão
Com os testes ok, só nos resta subir o código para o github:

```
git add --all
git commit -m "[NEW] Adicionado classes e testes"
git push origin master
```

Esse tutorial ficou bem extenso, mas espero que tenha sido útil pra vocês. No próxima parte do tutorial, vamos ver como configurar o Travis, para que ele execute nossos testes quando realizarmos um `push` ou um `pull request` para o github. Também veremos o Coveralls que emite relatórios do quando do seu código está coberto por testes, algo muito interessante para ver se um *software* é bem testado.

Os testes que escrevemos foram bem simples, apenas para fim de exemplo. Porém em uma aplicação séria, deve-se ter cuidado na hora de escrever os testes, de maneira a garantir que todas as possibilidades de erros sejam cobertas. A filosofia do TDD de escrever os testes antes do código da nossa aplicação, é algo que exige prática. Eu mesmo ainda não me sinto completamente a vontade seguindo esse fluxo de trabalho. Mas, escrever os testes primeiro te ajuda a manter seu código coerente e funcional, pois vocẽ vai precisar fazê-lo passar pelos testes.

É isso pessoal. Obrigado por ler até aqui. Até a próxima postagem!

**Publicado originalmente:** [python-com-unittest-travis-ci-coveralls-e-landscape-parte-1-de-4](http://codigoavulso.com.br/python-com-unittest-travis-ci-coveralls-e-landscape-parte-1-de-4.html)
