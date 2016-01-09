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

Quando estamos aprendendo algo, o início geralmente é difícil. Conseguir absorver novos conceitos e entender como as coisas funcionam não é uma das tarefas mais simples, porém nessas horas precisamos lembrar do conceito de 'babysteps' (Um passo de cada vez), ter paciência e persistir. 

A diferença entre uma pessoa experiente comparado a um iniciante é que a pessoa experiente errou muito mais vezes do que um iniciante, e com o tempo aprendeu com os erros.

E na área de programação temos inúmeros tutoriais e cursos espalhados pela internet, e geralmente as pessoas começam a aprender por conta própria. E quando acontece um problema (e isso irá acontecer inevitavelmente) e não sabemos como solucioná-lo, se torna um obstáculo chato. 

Neste artigo irei mostrar algumas formas de poder encontrar soluções para seus problemas enquanto aprende a programar. 

Os exemplos se aplicam a Python, mas podem ser exemplificados para qualquer outra linguagem ou tecnologia (se você trabalha com outras tecnologias como PHP ou Ruby, deixe nos comentários quais ferramentas utilizam para encontrar soluções dos seus problemas).

**Dica:** Veja essa palestra fantástica do [Josh Kaufman sobre as primeiras 20 horas de aprendizado](http://tedxtalks.ted.com/video/The-First-20-Hours-How-to-Learn)

## Python console

Uma grande feature do Python é seu console interativo, por ele conseguimos testar nossos códigos e alguns scripts em tempo real. Vejamos um exemplo:

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

Na variável **a** criamos um *set* com os nomes *Eric, Python e JavaScript*, e depois criamos uma *tupla* com os nomes *Django e Flask*. 

Ao tentarmos juntar **a + b**, o interpretador Python nos retorna um erro: *TypeError: unsupported operand type(s) for +: 'set' and 'tuple'*. Ou seja, o que ele diz é que não podemos somar um set a uma tupla.

O interpretador Python realiza as operações em tempo real, e se caso o que você deseja fazer não estiver correto, o interpretador irá informar o erro. Se o erro não for explícito para você, basta copiar e colar o erro no Google e encontrará os motivos do erro.

Para resolver esse problema, uma das soluções apresentada é transformar nosso set em uma tupla, onde fazemos a conversão em tempo de execução com o comando **tuple(a) + b**. 

## [Ipython](http://ipython.org/)

Que tal termos um interpretador Python mais poderoso e com mais funcionalidades que o tradicional? O [Ipython](http://ipython.org/) foi criado especificamente esse objetivo.

Vamos explorá-lo um pouco:


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

Criamos uma variável **nome** onde é um simples String "Eric". E se digitarmos **nome.** e apertar TAB, o Ipython irá apresentar diversas operações que podemos fazer com essa variável. 

Por exemplo, **nome.startswith** verifica se a primeira letra ou número começa com o parâmetro passado a ele. 

Na primeira tentativa verificamos se a variável começa com a letra *O*, e ele me retornou **False**, ou seja, não é verdade. 

Na segunda tentativa tentamos com a letra **E**, e ele me retornou **True**, o que é verdade já que o nome **Eric** começa com a letra "E".

O Ipython vai muito mais além do que isso, vá e dê uma olhada na página oficial e o que ele pode fazer. 

E temos também o [Ipython Notebook](http://ipython.org/notebook.html) que é FANTÁSTICO, amplamente utilizado para computação científica.

## [Dreampie](http://www.dreampie.org/)

Quando queremos testar algo mais elaborado, ter um console que permita criamos nossos códigos de forma mais organizada além do Interpretador padrão do Python e o IPython, podemos utilizar o [Dreampie](http://www.dreampie.org/) que é ideal para isso.

Vamos a outro exemplo:

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

<img src="https://raw.githubusercontent.com/erichideki/pythonclub.github.io/pelican/content/images/erichideki/dreampie.jpg" alt="Preview da tela do Dreampie.">

### O que aconteceu? 

Temos uma lista de dicionários desordenado e queremos ordenar de acordo com os parâmetros que queremos. Com isso, utilizamos duas bibliotecas que já estão por padrão com o Python: *[operator](https://docs.python.org/2/library/operator.html?highlight=itemgetter#operator.itemgetter) e [pprint](https://docs.python.org/2/library/pprint.html)*. 

Dentro da biblioteca **operator** temos a funcionalidade **itemgetter**, onde através dos parâmetros que passamos, ele irá fazer a seleção. Já o **pprint** irá mostrar o resultado da nossa seleção de forma mais bonita. Vamos explicar detalhadamente o que cada coisa faz.

Criamos nossa lista de dicionários:

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

Bacana, né? E também utilizamos a mesma lógica para ordenar de acordo com o **id**.

Se quiser saber mais a respeito do Ipython, indico o artigo do [Python Help que fala a respeito](https://pythonhelp.wordpress.com/2011/02/22/dreampie-o-shell-python-que-voce-sempre-sonhou/).

# [Python Tutor](http://www.pythontutor.com/)

Ao observarmos uma funcionalidade queremos entender o que ele faz, e muitas vezes o que cada coisa no código faz não fica muito bem claro em nossas ideias. Por isso o Python Tutor existe! Ele exibe passo-a-passo o que está acontecendo no código.

<iframe width="800" height="500" frameborder="0" src="http://www.pythontutor.com/visualize.html#code=prefix+%3D+%22Hello+%22%0A%0An1+%3D+raw_input(%22Enter+your+name%22%29%0A%0An2+%3D+raw_input(%22Enter+another+name%22%29%0A%0Ares+%3D+prefix+%2B+n1+%2B+%22+and+%22+%2B+n2%0Aprint(res%29&mode=display&origin=opt-frontend.js&cumulative=false&heapPrimitives=false&textReferences=false&py=2&rawInputLstJSON=%5B%5D&curInstr=0"> </iframe>

Clique em **Forward** e veja o que acontece.

# Outras opções

Também existem outras ferramentas que podem auxiliar e melhorar seu código:

- **Anaconda para Sublime Text** - [http://damnwidget.github.io/anaconda/](http://damnwidget.github.io/anaconda/)
- **Autopep8** - [https://pypi.python.org/pypi/autopep8](https://pypi.python.org/pypi/autopep8)
- **Jedi** - [https://github.com/davidhalter/jedi](https://github.com/davidhalter/jedi)
- **Pyflakes** - [https://pypi.python.org/pypi/pyflakes](https://pypi.python.org/pypi/pyflakes)
- **PDB** - [https://docs.python.org/2/library/pdb.html](https://docs.python.org/2/library/pdb.html)

## Locais onde podemos postar nossas dúvidas

Vale sempre lembrar que é muito importante consultar a documentação oficial do Python, seja a [versão 2](https://docs.python.org/2/) ou a [versão 3](https://docs.python.org/3/).

Também existem outro lugar muito legal, o **[Stackoverflow](http://pt.stackoverflow.com/)**. Se ainda o problema persistir, acesse as listas de discussões da comunidade Python no Brasil. 

- **Python Brasil** - [https://groups.google.com/forum/#!forum/python-brasil](https://groups.google.com/forum/#!forum/python-brasil)
- **Django Brasil** - [https://groups.google.com/forum/#!forum/django-brasil](https://groups.google.com/forum/#!forum/django-brasil)
- **Web2py Brasil** - [https://groups.google.com/forum/#!forum/web2py-users-brazil](https://groups.google.com/forum/#!forum/web2py-users-brazil)
- **Flask Brasil** - [https://groups.google.com/forum/#!forum/flask-brasil](https://groups.google.com/forum/#!forum/flask-brasil)
- **Comunidades locais da comunidade Python ao redor do Brasil** - [http://pythonbrasil.github.io/wiki/comunidades-locais](http://pythonbrasil.github.io/wiki/comunidades-locais)

Deixe nos comentários seu feedback, e se tiver outra dica que não foi citado, não deixe de indicar.