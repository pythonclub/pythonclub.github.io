title: Debugging em python (sem IDE)
Slug: debugging-em-python-sem-ide
Date: 2015-02-15 22:30
Tags: python,pdb,ipython,ipdb,debugging
Author: Diego Garcia
Email:  drgarcia1986@gmail.com
Github: drgarcia1986
Site: http://www.codeforcloud.info
Twitter: drgarcia1986
Linkedin: drgarcia1986
Category: debugging 


<figure style="float:right;">
<img src="/images/drgarcia1986/debugging.png">
</figure>
</br>
Um dos principais motivos que ainda levam desenvolvedores Python a recorrerem a IDEs pesadas e que requerem instalação é o **debugging**. 
Devs que vieram de linguagens como _DotNet_, _Java_ e _Delphi_ por exemplo, estão acostumados a IDEs super pesadas e inchadas que no final das contas, além do debugging, só servem para drenar memória RAM. 
Brincadeiras a parte, não a motivos para você não dar uma chance ao **VIM** ou ao **Sublime**, pois para fazer debugging em scripts python, tudo que você precisa é o **PDB**. 

<!-- MORE -->

# PDB
O `pdb` é um módulo _buit-in_ que funciona como um console interativo, onde é posssível realizar debug de códigos python. 
Nele é possível fazer um _step-by-step_ do código, verificando o valor de variaveis, definindo breakpoints, manipulando valores, etc. 
É possível inclusive realizer _step-into_ em métodos. Ou seja, tudo que uma boa ferramenta de debug precisa ter.

## Comandos
Antes de partirmos para prática, é importante conhecer alguns comandos básicos para já começar o uso do pdb de forma efetiva.

Durante o debugging, eventualmente seu script irá _estacionar_ em pontos de paradas, possívelmente definidos por você, neste momento, os comandos a seguir poderão ser utilizados.

### q (quit)
Sai da execução do script.

### n (next)
Avança para a próxima linha do script.

### p (print)
Executa o comando `print` do python, por exemplo:
```python
> /script.py(1)<module>()
-> foo = "foo var"
(Pdb) p foo
'foo var'
```
> Vale ressaltar que no exemplo acima, não é necessário utilizar o comando `p`, basta digitar o nome da variável e pressionar `enter`, o efeito seria o mesmo.

### c (continue)
Avança o debug até o próximo **breakpoint** ou até ocorrer uma **exception**.

### l (list)
Lista algumas linhas do código que estão em volta da linha atual.
Por padrão serão apresentadas 11 linhas (5 acima e 5 abaixo).

### s (step into)
Ao realizar a navegação através do comando `n` o debug **não** irá _entrar_ em métodos que possívelmente forem invocados.
Para que o debug entre no método que está sendo invocado na linha corrente, basta trocar o comando `n`, pelo comando `s`.
```python
> /home/user/foo.py(20)<module>()
-> foo.bar('barz')
(Pdb) s
--Call--
> /home/user/foo.py(3)bar()
-> def bar(self, the_bar):
(Pdb)
```

### r (return)
Já o comando `r` libera a execução do script até sair da função atual.

### b (breakpoint)
Cria um breakpoint em uma determinada linha ou método, por exemplo.
```python
> /script.py(1)<module>()
(Pdb) b 21
Breakpoint 1 at /script.py:21
``` 
No comando acima, setamos um breakpoint na linha 21 de nosso script.
```python
> /script.py(1)<module>()
(Pdb) b foo
Breakpoint 1 at /script.py:30
``` 
Já no exemplo acima, setamos o breakpoint para o método `foo`.
O pdb informa qual linha ele setou o breakpoint, em nosso exemplo o método `foo` está na linha 30 do script.

### a (arguments)
O comando `a` mostra os argumentos que foram passados para a função atual.

```python
> /home/user/foo.py(20)<module>()
-> foo.bar('barz')
(Pdb) s
--Call--
> /home/user/foo.py(3)bar()
-> def bar(self, the_bar):
(Pdb) a
the_bar = "barz"
```

### ENTER
Se você pressionar o `ENTER` sem nenhum comando no pdb, ele irá repetir o último comando executado. 

## Debug na prática
Vamos utilizar um script python simples e didático como exemplo.

```python
class NumberList(object):
    def __init__(self):
        self.numbers = list()

    def add(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError
        self.numbers.append(number)

    def sum(self):
        result = 0
        for i in self.numbers:
            result += i
        return result


if "__main__" == __name__:
	numbers = NumberList()

	numbers.add(5)
	assert numbers.sum() == 5

	numbers.add(10)
	assert numbers.sum() == 15

	print "The End"
```
Esse script possui uma classe chamada `NumberList` que armazena uma lista de numeros e retorna a soma deles. 
Além destas classe, esse script também realiza algumas operações como instanciar essa classe e realizar alguns testes de asserção.
Salve esse script em um arquivo chamado `numbers.py` para ser utilizado em nossos exemplos.

## Modos de uso do pdb

Na prática o pdb se assemelha bastante ao prompt interativo do python, com a diferença dos caracteres identificadores.
Enquanto que no prompt interativo do python o identificador é o `>>>`, no pdb o identificador é `(Pdb)`.
Existem algumas maneiras de usar o pdb, depende da forma como você pretende realizer o debug. 

### pdb.py
Uma delas é através da chamada do script `pdb.py` passando como paramêtro o script para ser feito do debug, por exemplo:

```bash
python -m pdb numbers.py
```
Isso fará com que o pdb seja iniciado na primeira linha do script `numbers.py`, no caso, a declaração da classe `NumberList()`.
Caso você execute o comando `n`, a próxima linha será o `if "__main__" == __name__:` e assim por diante.
Utilizando desta maneira, você pode verificar linha a linha do script ou _setar_ um breakpoint assim que entrar no debug, por exemplo, se você quer criar um breakpoint na execução do método `sum()` de uma instância da classe `NumberList()`, basta executar o comando `b numbers.sum`.

```python
(venv)user@machine:~/$ python -m pdb numbers.py 
> /home/user/numbers.py(4)<module>()
-> class NumberList(object):
(Pdb) n
> /home/user/numbers.py(20)<module>()
-> if __name__ == "__main__":
(Pdb) n
> /home/user/numbers.py(21)<module>()
-> numbers = NumberList()
(Pdb) n
> /home/user/numbers.py(23)<module>()
-> numbers.add(5)
(Pdb) b numbers.sum
Breakpoint 1 at /home/user/numbers.py:13
(Pdb)
```

Ou para simplificar, também poderiamos setar o breakpoint pelo número da linha.

```python
(venv)user@machine:~/$ python -m pdb numbers.py 
> /home/user/numbers.py(4)<module>()
-> class NumberList(object):
(Pdb) b 13
Breakpoint 1 at /home/user/numbers.py:13
(Pdb) 
```
### pdb.set_trace()
Outra forma é utilizando o método `set_trace()` do pacote `pdb`.
Com o `pdb.set_trace()` você pode definir onde será o seu breakpoint via código, por exemplo, faremos uma alteração em nosso script para setar um breakpoint no método `NumberList().sum()`.
```python
class NumberList(object):
    def __init__(self):
        self.numbers = list()

    def add(self, number):
        if not isinstance(number, (int, float)):
            raise TypeError
        self.numbers.append(number)

    def sum(self):
		import pdb
        pdb.set_trace()

        result = 0
        for i in self.numbers:
            result += i
        return result

"""
Resto do script omitido
"""
```
Dessa forma, ao executar o script (sem a necessidade de ser via pdb) e passar pelo método `pdb.set_trace()` será iniciado um prompt interativo do pdb.

```python
(venv)user@machine:~/$ python numbers.py 
> /home/user/numbers.py(16)sum()
-> result = 0
(Pdb) 
```

## ipdb
Uma das desvantagens do prompt interativo do python é a falta de _syntax highlighting_ e _code completion_, com o pdb não é diferente, porém, assim como podemos recorrer ao [ipython](http://ipython.org/) para isso, também podemos utilizar o [ipdb](https://github.com/gotcha/ipdb).
O `ipdb` é uma espécie de wrapper para o pdb que faz uso das rotinas de debug do `IPython`.
A maneira de uso se assemelha bastante ao pdb, bastando trocar o pacote `pdb` pelo pacote `ipdb`.

```python
import ipdb

foo = "foo"
ipdb.set_trace()
bar = "bar"
```

Para instalar o ipdb basta utilizar o `pip`

```
pip install ipdb
``` 
Com certeza recomendo o uso do `ipdb` principalmente por ser mais intuitivo.

**Referências**<br \>
[Documentação Oficial](https://docs.python.org/2/library/pdb.html)<br />
[ipdb](https://github.com/gotcha/ipdb)
