Title: Abrangência de Listas e Dicionários
Slug: abrangencia-de-listas-e-dicionarios-com-python
Date: 2017-01-16 10:37:39
Category: Python
Tags: python,tutorial,list comprehensions
Author: Michell Stuttgart
Email: michellstut@gmail.com
Github: mstuttgart
Linkedin: mstuttgart
Site: https://mstuttgart.github.io

A utilização de listas em Python é algo trivial. A facilidade provida pela linguagem aliada a simplicidade da estrutura de dados *list* a torna, ao lado dos dicionários *dict*, uma das estrutura de dados mais utilizadas em Python. Aqui neste tutorial irei compartilhar algo que aprendi trabalhando com listas e dicionário em Python, mais especificamente no que diz respeito a *abrangência* de listas (e dicionários).

## Abrangência de listas

A abrangência de listas, ou do inglês *list comprehensions*, é um  termo utilizado para descrever uma sintaxe compacta que o Python nos oferece para criamos uma lista baseada em outra lista. Pareceu confuso? Ok, vamos aos exemplos!

### Exemplo 1
Vamos supor que temos a seguinte lista de valores:

```python
valores = [1, 2, 3, 4, 5]
```
Queremos gerar uma outra lista contendo o dobro de cada um desses números, ou seja,

```python
[2, 4, 6, 8, 10]
```
Inicialmente, podemos montar o seguinte código como solução:

```python
# Recebe o nosso resultado
valores_dobro = []

for val in valores:
    valores_dobro.append(val * 2)

print(valores_dobro)

>>>
[2, 4, 6, 8, 10]

```

A solução acima é uma solução simples e resolve nosso problema, entretanto para algo tão simples precisamos de 4 linhas de código. Este exemplo é uma situação onde a *abrangência de lista* pode ser útil. Podemos compactar a criação da lista `valores_dobro` da seguinte maneira:

```python
valores_dobro = [valor*2 for valor in valores]
```
Bacana não? O exemplo seguinte podemos incrementar mais o exemplo acima.

### Exemplo 2

Vamos supor que desejamos criar uma lista onde apenas os valores pares (resto da divisão por 2 é zero) serão multiplicados por 2. Abaixo temos a nossa lista de valores:

```python
valores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

Assim como no exemplo anterior, podemos resolver utilizando um algoritmo básico.

```python
# Lista que recebera o nosso resultado
valores_dobro = []

for valor in valores:
    if valor % 2 == 0:
        valores_dobro.append(valor * 2)

print(valores_dobro)

>>>
[4, 8, 12, 16, 20]

```
Podemos também resolver o mesmo problema utilizando as funções nativas *map* e *filter*:

```python
valores_dobro = map(lambda valor: valor * 2, filter(lambda valor: valor % 2 == 0, valores))
```
Muito mais complicada não é? Apesar de resolver nosso problema, expressões como a acima são difíceis de ler e até mesmo de escrever. Em casos como esse, podemos novamente compactar nosso algoritmo utilizando a *abrangência de lista*.

```python
valores_dobro = [valor * 2 for valor in valores if valor % 2 == 0]
```
Muito mais simples, não? Vamos para o próximo exemplo.

### Exemplo 3

De maneira semelhante a lista, nós também podemos aplicar a abrangência em lista e dicionários. Segue um exemplo onde temos o seguinte dicionário:

```python
 dicionario = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
```

Vamos criar um segundo dicionário contendo apenas as chaves que são consoantes, ou seja, `b`, `c`, `d` e `f`, sendo que o valor para cada uma dessas chaves deve ser o dobro do valor armazenado na respectiva chave do dicionário original. Complicado? Em outras palavras, o novo dicionário deve ficar assim:

```python
 novo_dicionario = {'b': 4, 'c': 6, 'd': 8, 'f': 12}
```

Utilizando um algoritmo genérico, podemos resolver o problema da seguinte maneira:

```python
novo_dicionario = {}

for chave, valor in dicionario:
    if chave in ['b', 'c', 'd', 'f']:
        novo_dicionario[chave] = 2 * valor

print(novo_dicionario)

>>
{'b': 4, 'c': 6, 'd': 8, 'f': 12}

```
Aplicando agora a abrangência, conseguimos compactar o código acima de maneira interessante:

```python
novo_dicionario = {chave: 2 * valor for chave, valor in dicionario.items() if chave in ['b', 'c', 'd', 'f']}
```

## Conclusão

Chegamos ao final de mais um tutorial! Sempre temos de ter em mente que tão importante quanto escrever um código que funciona, é mantê-lo (seja por você ou por outro programador). Neste ponto, a abrangência de lista (e outras estruturas de dados) nos ajudam a escrever um código claro e fácil de dar manutenção.

Até o próximo tutorial pessoal!

## Referências

* [Python eficaz: 59 maneiras de programar melhor em Python; Slatkin, Brett; Novatec Editora, 2016.](https://novatec.com.br/livros/python-eficaz/)
