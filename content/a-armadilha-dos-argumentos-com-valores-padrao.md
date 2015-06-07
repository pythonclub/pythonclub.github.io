title: A armadilha dos argumentos com valores padrão
Slug: a-armadilha-dos-argumentos-com-valores-padrao
Date: 2015-06-07 11:00
Tags: python,mutable,function,class,anti-pattern
Author: Diego Garcia
Email:  drgarcia1986@gmail.com
Github: drgarcia1986
Site: http://www.codeforcloud.info
Twitter: drgarcia1986
Linkedin: drgarcia1986
Category: anti-patterns


<figure style="float:left;">
<img src="/images/drgarcia1986/is_a_trap.png">
</figure>
</br>
Algo muito comum em várias linguagens de programação é a possibilidade de definir _valores default_ (valores padrão) para argumentos de funções e métodos, tornando a utilização desses opcional.
Isso é ótimo, principalmente para manter retrocompatibilidade, porém, o python possui uma pequena armadilha que caso passe despercebida, pode causar sérios problemas, muitas vezes difíceis de serem detectados.
Essa armadilha ocorre quando usamos valores de tipos `mutáveis` como valor default de argumentos.

<!-- MORE -->

### O que são tipos mutáveis e imutáveis?
Segundo a [documentação oficial do python](https://docs.python.org/3.4/reference/datamodel.html), o valor de alguns objetos pode mudar, esses objetos que podem ter seu valor alterado após serem criados são chamados de mutáveis, enquanto que os objetos que não podem ter seus valores alterados após serem criados são chamados de imutáveis (simples assim).

* **Tipos mutáveis**:

Listas, Dicionários e tipos definidos pelo usuário.

* **Tipos imutáveis**:

Numeros, Strings e Tuplas.

> Apesar de serem imutáveis, a utilização de um valor mutável (uma lista por exemplo) dentro de uma tupla, pode causar o efeito _[tuplas mutáveis](http://pythonclub.com.br/tuplas-mutantes-em-python.html)_, onde visualmente o valor da tupla é alterado, mas por trás dos panos o valor da tupla não muda, o que muda é o valor do objeto pelo qual a tupla está se referenciando.

### A armadilha
Como disse no começo desse blogpost, é muito comum a utilização de valores default em agurmentos de funções e métodos, por essa razão, nos sentimos seguros em fazer algo desse tipo:

```python
def my_function(my_list=[]):
    my_list.append(1)
    print(my_list)
```

Porém, levando esse exemplo em consideração, o que irá acontecer se invocarmos essa função 3 vezes?

```python
>>> my_function()
[1]
>>> my_function()
[1, 1]
>>> my_function()
[1, 1, 1]
```
Sim, o valor do argumento `my_list` mudou em cada vez que executamos a função sem passar algum valor para ele.

### Por que isso acontece?
Isso acontece porque o python processa os valores default de cada argumentos de uma função (ou método) quando essa for definida, após esse processamento o valor é atribuido ao objeto da função. 
Ou seja, por questões de optimização, seguindo nosso exemplo, o python não cria uma lista vazia para o argumento `my_list` a cada vez que a função `my_function` for invocada, ele reaproveita uma lista que foi criada no momento em que essa função foi importada.

```python
>>> my_function.func_defaults
([],)
>>> id(my_function.func_defaults[0])
140634243738080
>>> my_function()
[1]
>>> my_function.func_defaults
([1],)
>>> id(my_function.func_defaults[0])
140634243738080
>>> my_function()
[1, 1]
>>> my_function.func_defaults
([1, 1],)
>>> id(my_function.func_defaults[0])
140634243738080
```
> Note que a identificação do argumento (no caso `my_list`) não muda, mesmo executando a função várias vezes.

Outro exemplo seria utilizar o resultado de funções como valores default de argumentos, por exemplo, uma função com um argumento que recebe como default o valor de `datetime.now()`. 

```python
def what_time_is_it(dt=datetime.now()):
    print(dt.strftime('%d/%m/%Y %H:%M:%S'))
```
O valor do argumento `dt` sempre será o _datetime_ do momento em que o python carregou a função e não o _datetime_ de quando a função foi invocada.

```python
>>> what_time_is_it()
07/06/2015 08:43:55
>>> time.sleep(60)
>>> what_time_is_it()
07/06/2015 08:43:55
```

### Isso também acontece com classes?
Sim e de uma forma ainda mais perigosa.

```python
class ListNumbers():
    def __init__(self, numbers=[]):
        self.numbers = numbers

    def add_number(self, number):
        self.numbers.append(number)

    def show_numbers(self):
        print(numbers)
```
Assim como no caso das funções, no exemplo acima o argumento `numbers` é definido no momento em que o python importa a classe, ou seja, a cada nova instância da classe `ListNumbers`, será aproveitada a mesma lista no argumento `numbers`.
 
```python
>>> list1 = ListNumbers()
>>> list2 = ListNumbers()
>>> list1.show_numbers()
[]
>>> list2.show_numbers()
[]
>>> list2.add_number(1)
>>> list1.show_numbers()
[1]
>>> list2.show_numbers()
[1]
>>> list1.numbers is list2.numbers
True
```

### Por que isso não acontece com Strings?
Porque strings são `imutáveis`, o que significa que a cada alteração de valor em uma variavel que armazena uma strings, o python cria uma nova instância para essa variável.

```python
>>> a = 'foo'
>>> id(a)
140398402003832
>>> a = 'bar'
>>> id(a)
140398402003872  # o penúltimo número muda :)
```

Em argumentos com valores default, não é diferente.

```
def my_function(my_str='abc'):
    my_str += 'd'
    print(my_str)
```
No exemplo acima, sempre que for executado o `inplace add` (`+=`) será criada outra váriavel para `my_str` sem alterar o valor default do argumento. 

```python
>>> my_function()
abcd
>>> my_function.func_defaults
('abc',)
>>> my_function()
abcd
>>> my_function.func_defaults
('abc',)
```

### Como se proteger?
A maneira mais simples de evitar esse tipo de surpresa é utilizar um [valor sentinela](http://en.wikipedia.org/wiki/Sentinel_value) como por exemplo `None`, nos argumentos opcionais que esperam tipos mutáveis:

```python
def my_function(my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(1)
    print(my_list)
```

Pronto, sem surpresas e sem armadilhas :).

```python
>>> my_function()
[1]
>>> my_function()
[1]
>>> my_function()
[1]
```

### Referências

* [Fluent Python (Mutable types as parameter defaults: bad idea)](http://shop.oreilly.com/product/0636920032519.do)
* [Python Anti-Patterns (Using a mutable default value as an argument)](http://docs.quantifiedcode.com/python-anti-patterns/correctness/mutable_default_value_as_argument.html)
