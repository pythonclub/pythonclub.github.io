Title: Como encontrar soluções para seus problemas com Python
Slug: como-encontrar-solucoes-python
Date: 2015-01-08 11:30
Tags: python,blog,tutorial,aulas
Author: Eric Hideki
Email:  eric8197@gmail.com
Github: erichideki
Bitbucket: erichideki
Site: http://ericstk.wordpress.com
Twitter: erichideki
Category: Python

Como encontrar soluções para seus problemas com Python
----------------------------------------------------

Quando estamos aprendendo algo, o início geralmente é difícil. Conseguir absorver novos conceitos e entender como as coisas funcionam não é uma das tarefas mais simples, porém nessas horas precisamos lembrar do conceito de 'babysteps' (Um passo de cada vez). A diferença entre uma pessoa experiente comparado a um iniciante é que a pessoa experiente errou muito mais vezes do que você, e aprendeu com os erros.

Então, quando estamos aprendendo programação, temos inúmeros tutorials e cursos espalhados, e quando acontece um problema e não sabemos como solucioná-lo, se torna um obstáculo chato. 

Nesse artigo irei mostrar algumas formas de poder encontrar soluções aos seus problemas enquanto aprende a programar. Os exemplos se aplicam a Python, mas podem ser exemplificados em qualquer outra linguagem ou tecnologia (se você trabalha com outras tecnologias como PHP ou Ruby, deixe nos comentários quais ferramentas utilizam para encontrar soluções aos seus problemas).

**Dica:** Veja essa palestra fantástica do [Josh Kaufman sobre as primeiras 20 horas de aprendizado](http://tedxtalks.ted.com/video/The-First-20-Hours-How-to-Learn)

## Python console

Uma grande feature do Python é seu console interativo, por ele conseguimos testar nossos códigos e alguns scripts antes de colocarmos em nosso projeto.

```python
Python 3.4.3 (default, Oct 14 2015, 20:28:29) 
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> a = {'Eric', 'Python', 'JavaScript'}
>>> b = ('Django', 'Flask')
>>> a + b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'set' and 'tuple'
>>> tuple(a) + b
('JavaScript', 'Eric', 'Python', 'Django', 'Flask')
```

### O que aconteceu? 

Na variável *a* criamos uma *lista* com os nomes *Eric, Python e JavaScript*, e depois criamos uma *tupla* com os nomes *Django e Flask*. Ao tentarmos juntar **a + b**, o interpretador Python nos retorna um erro: *TypeError: unsupported operand type(s) for +: 'set' and 'tuple'*. Ou seja, o que ele diz é que não podemos somar uma lista a uma tupla.

O interpretador Python realiza as operações em tempo real, e se caso o que você deseja fazer não estiver correto, o interpretador irá informar o erro. Se o erro não for explícito para você, basta copiar e colar o erro no Google que provavelmente irá encontrar os motivos do erro persistir.

Para resolver esse problema, uma das soluções apresentada é transformar nossa lista em uma tupla, onde fazemos a conversão em tempo de execução com o comando *tuple(a) + b*. Legal né?

## [Ipython](http://ipython.org/)

Que tal termos um interpretador Python mais poderoso? O [Ipython](http://ipython.org/) tem exatamente esse objetivo.

Vamos explorar outro exemplo:


```python
$ipython

Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
Type "copyright", "credits" or "license" for more information.

IPython 1.2.1 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: nome = "Eric"

In [2]: nome.
nome.capitalize  nome.isalnum     nome.lstrip      nome.splitlines
nome.center      nome.isalpha     nome.partition   nome.startswith
nome.count       nome.isdigit     nome.replace     nome.strip
nome.decode      nome.islower     nome.rfind       nome.swapcase
nome.encode      nome.isspace     nome.rindex      nome.title
nome.endswith    nome.istitle     nome.rjust       nome.translate
nome.expandtabs  nome.isupper     nome.rpartition  nome.upper
nome.find        nome.join        nome.rsplit      nome.zfill
nome.format      nome.ljust       nome.rstrip      
nome.index       nome.lower       nome.split    

In [2]: nome.startswith("O")
Out[2]: False

In [3]: nome.startswith("E")
Out[3]: True

In [4]: len(nome)
Out[4]: 4

In [5]: nome.lower()
Out[5]: 'eric'

```

### O que aconteceu? 

O Ipython acompanha mais algumas funcionalidades que o interpretador Python padrão. Por exemplo, criamos uma variável *nome* onde é um simples String "Eric". E se digitarmos *nome.* e apertar TAB, o Ipython irá apresentar diversas operações que podemos fazer. Por exemplo, *nome.startswith* verifica se a primeira letra ou número começa com o parâmetro passado. Na primeira tentativa verificamos se a variável começa com a letra *O*, e ele me retornou **False**, ou seja, não é verdade. Na segunda tentativa tentamos com a letra **E**, e ele me retornou **True**, o que é verdade já que o nome **Eric** começa com a letra "E".

O Ipython vai muito mais além do que isso. Indico que dê uma olhada na página oficial e o que ele pode fazer. Além também do Ipython Notebook que é FANTÁSTICO (Coloque em sua to do list conhecer Ipython Notebook).

## [Dreampie](http://www.dreampie.org/)

Quando queremos testar uma funcionalidade, ter um console onde possamos de forma simples testar, o [Dreampie](http://www.dreampie.org/) é excelente.

```python
Python 2.7.6 (default, Jun 22 2015, 17:58:13) 
[GCC 4.8.2] on linux2
Type "copyright", "credits" or "license()" for more information.
DreamPie 1.1.1
>>> colunas = [
...     {'pnome': 'Eric', 'unome': 'Hideki', 'id': 4},
...     {'pnome': 'Luciano', 'unome': 'Ramalho', 'id': 2},
...     {'pnome': 'David', 'unome': 'Beazley', 'id': 8},
...     {'pnome': 'Tim', 'unome': 'Peters', 'id': 1},
... ]
>>> from operator import itemgetter
>>> colunas_por_nome = sorted(colunas, key=itemgetter('pnome'))
>>> colunas_por_id = sorted(colunas, key=itemgetter('id'))
>>> from pprint import pprint
>>> pprint(colunas_por_nome)
[{'id': 8, 'pnome': 'David', 'unome': 'Beazley'},
 {'id': 4, 'pnome': 'Eric', 'unome': 'Hideki'},
 {'id': 2, 'pnome': 'Luciano', 'unome': 'Ramalho'},
 {'id': 1, 'pnome': 'Tim', 'unome': 'Peters'}]
>>> pprint(colunas_por_id)
[{'id': 1, 'pnome': 'Tim', 'unome': 'Peters'},
 {'id': 2, 'pnome': 'Luciano', 'unome': 'Ramalho'},
 {'id': 4, 'pnome': 'Eric', 'unome': 'Hideki'},
 {'id': 8, 'pnome': 'David', 'unome': 'Beazley'}]
```

<img src="/images/erichideki/dreampie.jpg" alt="dreampie" style="width:100%">

### O que aconteceu? 

Temos uma lista de dicionários 'desordenado', e queremos ordenar de acordo com os parâmetros que queremos. Com isso, utilizamos duas bibliotecas que já estão por padrão com o Python: *[operator](https://docs.python.org/2/library/operator.html?highlight=itemgetter#operator.itemgetter) e [pprint](https://docs.python.org/2/library/pprint.html)*. 

Dentro da biblioteca *operator* temos a funcionalidade **itemgetter**, onde através dos parâmetros que passamos, ele irá fazer a seleção. Já o **pprint** irá mostrar o resultado da nossa seleção de forma mais bonita.

Então criamos nossa lista de dicionários:

```python
>>> colunas = [
...     {'pnome': 'Eric', 'unome': 'Hideki', 'id': 4},
...     {'pnome': 'Luciano', 'unome': 'Ramalho', 'id': 2},
...     {'pnome': 'David', 'unome': 'Beazley', 'id': 8},
...     {'pnome': 'Tim', 'unome': 'Peters', 'id': 1},
... ]
```

Importamos a biblioteca operator e sua funcionalidade itemgetter:

```python
>>>from operator import itemgetter
```

E criamos nossa funcionalidade para ordenar a lista de dicionários de acordo com o parâmetro selecionado, que nesse caso será o primeiro nome, o **pname**:

```python
>>> colunas_por_nome = sorted(colunas, key=itemgetter('pnome'))
```

Finalizando, utilizamos o **pprint** para exibir o resultado:

```python
>>>pprint(colunas_por_nome)
```

Bacana, né?

Se quiser saber mais a respeito do Ipython, indico o artigo do [Python Help que fala a respeito](https://pythonhelp.wordpress.com/2011/02/22/dreampie-o-shell-python-que-voce-sempre-sonhou/).

# [Python Tutor](http://www.pythontutor.com/)

Ao criarmos uma funcionalidade, ou senão queremos entender o que ele faz, muitas vezes o que cada coisa faz não fica muito bem claro. Por isso o Python Tutor existe! Ele exibe passo-a-passo o que está acontecendo no código.

<iframe width="800" height="500" frameborder="0"
        src="http://www.pythontutor.com/visualize.html#code=prefix+%3D+%22Hello+%22%0A%0An1+%3D+raw_input(%22Enter+your+name%22%29%0A%0An2+%3D+raw_input(%22Enter+another+name%22%29%0A%0Ares+%3D+prefix+%2B+n1+%2B+%22+and+%22+%2B+n2%0Aprint(res%29&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=false&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0">
</iframe>

Clique em **Forward** e veja o que acontece.

## Locais onde podemos postar nossas dúvidas

Vale sempre lembrar que é muito importante consultar a documentação oficial do Python, seja a [versão 2](https://docs.python.org/2/) ou a [versão 3](https://docs.python.org/3/).

Também existem outro lugar muito legal, que é o **[Stackoverflow](http://pt.stackoverflow.com/)**. Se ainda o problema persistir, acesse as listas de discussões da comunidade Python no Brasil. 

**Python Brasil** - [https://groups.google.com/forum/#!forum/python-brasil](https://groups.google.com/forum/#!forum/python-brasil)
**Django Brasil** - [https://groups.google.com/forum/#!forum/django-brasil](https://groups.google.com/forum/#!forum/django-brasil)
**Web2py Brasil** - [https://groups.google.com/forum/#!forum/web2py-users-brazil](https://groups.google.com/forum/#!forum/web2py-users-brazil)
**Flask Brasil** - [https://groups.google.com/forum/#!forum/flask-brasil](https://groups.google.com/forum/#!forum/flask-brasil)
**Comunidades locais da comunidade Python ao redor do Brasil** - [http://pythonbrasil.github.io/wiki/comunidades-locais](http://pythonbrasil.github.io/wiki/comunidades-locais)

Deixe nos comentários seu feedback, e se tiver outra dica que não foi citado, não deixe de indicar.