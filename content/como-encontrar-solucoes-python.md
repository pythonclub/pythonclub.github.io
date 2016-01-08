Title: Como encontrar soluções aos seus problemas em Python
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

Como encontrar soluções aos seus problemas em Python
----------------------------------------------------

Quando estamos aprendendo algo, o início geralmente é difícil. Conseguir absorver novos conceitos e entender como as coisas funcionam não é uma das tarefas mais simples, porém nessas horas precisamos lembrar do conceito de 'babysteps' (Um passo de cada vez). A diferença entre uma pessoa experiente comparado a um iniciante é que a pessoa experiente errou muito mais vezes do que você, e aprendeu com os erros.

Então, quando estamos aprendendo programação, temos inúmeros tutorials e cursos espalhados, e quando acontece um problema e não sabemos como solucioná-lo, se torna um obstáculo chato. 

Nesse artigo irei mostrar algumas formas de poder encontrar soluções aos seus problemas enquanto aprende a programar. Os exemplos se aplicam a Python, mas podem ser exemplificados em qualquer outra linguagem ou tecnologia (se você trabalha com outras tecnologias como PHP ou Ruby, deixe nos comentários quais ferramentas utilizam para encontrar soluções aos seus problemas).

Dica: Veja essa palestra fantástica do [Josh Kaufman sobre as primeiras 20 horas de aprendizado](http://tedxtalks.ted.com/video/The-First-20-Hours-How-to-Learn)

## Python console

Uma grande feature do Python é seu console interativo, por ele conseguimos testar nossos códigos e testar alguns scripts antes de colocarmos em nosso projeto.

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

Python console
Ipython
Dreampie
Python Tutor
Documentação Python
Stackoverflow
Google Groups
Gist
