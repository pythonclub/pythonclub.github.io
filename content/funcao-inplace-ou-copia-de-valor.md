Title: Funções in place ou cópia de valor
Slug: funcao-inplace-ou-copia-de-valor
Date: 2021-03-29 12:00
Category: Python
Tags: python, funções
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Eventualmente observo dificuldades de algumas pessoas em usar corretamente alguma função, seja porque a função deveria ser executada isoladamente, e utilizado a própria variável que foi passada como argumento posteriormente, seja porque deveria se atribuir o retorno da função a alguma variável, e utilizar essa nova variável. No Python, essa diferença pode ser observada nos métodos das listas `sort` e `reverse` para as funções `sorted` e `reversed`, que são implementadas com padrões diferentes, *in place* e cópia de valor respectivamente. Assim pretendo discutir esses dois padrões de funções, comentando qual a diferença e o melhor caso de aplicação de cada padrão.

## Função de exemplo

Para demonstrar como esses padrões funcionam, será implementado uma função que recebe uma lista e calcula o dobro dos valores dessa lista. Exemplo:

```python
entrada = [5, 2, 8, 6, 4]

# Execução da função

resultado = [10, 4, 16, 12, 8]
```

### Função com in place

A ideia do padrão *in place* é alterar a própria variável recebida pela função (ou o próprio objeto, caso esteja lidando com orientação a objetos). Neste caso, bastaria calcular o dobro do valor de cada posição da lista, e sobrescrever a posição com seu resultado. Exemplo:

```python
from typing import List, NoReturn


def dobro_inplace(lista: List[int]) -> NoReturn:
    for i in range(len(lista)):
        lista[i] = 2 * lista[i]


valores = [5, 2, 8, 6, 4]
retorno = dobro_inplace(valores)

print(f'Variável: valores | Tipo: {type(valores)} | Valor: {valores}')
print(f'Variável: retorno | Tipo: {type(retorno)} | Valor: {retorno}')
```

Resultado da execução:

```
Variável: valores | Tipo: <class 'list'> | Valor: [10, 4, 16, 12, 8]
Variável: retorno | Tipo: <class 'NoneType'> | Valor: None
```

Com essa execução é possível observar que os valores da lista foram alterados, e que o retorno da função é nulo (`None`), ou seja, a função alterou a própria lista passada como argumento. Outro ponto importante a ser observado é a assinatura da função (tipo dos argumentos e do retorno da função), que recebe uma lista de inteiros e não tem retorno (`NoReturn`). Dessa forma embora seja possível chamar essa função diretamente quando está se informando os argumentos de outra função, como `print(dobro_inplace(valores))`, a função `print` receberia `None` e não a lista como argumento.

### Função com cópia de valor

A ideia do padrão cópia de valor é criar uma cópia do valor passado como argumento e retornar essa cópia, sem alterar a variável recebida (ou criando um novo objeto, no caso de orientação a objetos). Neste caso, é necessário criar uma nova lista e adicionar nela os valores calculados. Exemplo:

```python
from typing import List


def dobro_copia(lista: List[int]) -> List[int]:
    nova_lista = []

    for i in range(len(lista)):
        nova_lista.append(2 * lista[i])

    return nova_lista


valores = [5, 2, 8, 6, 4]
retorno = dobro_copia(valores)

print(f'Variável: valores | Tipo: {type(valores)} | Valor: {valores}')
print(f'Variável: retorno | Tipo: {type(retorno)} | Valor: {retorno}')
```

Resultado da execução:

```
Variável: valores | Tipo: <class 'list'> | Valor: [5, 2, 8, 6, 4]
Variável: retorno | Tipo: <class 'list'> | Valor: [10, 4, 16, 12, 8]
```

Com essa execução é possível observar que a variável `valores` continua com os valores que tinha antes da execução da função, e a variável retorno apresenta uma lista com os dobros, ou seja, a função não altera a lista passada como argumento e retorna uma nova lista com os valores calculados. Observado a assinatura da função, ela recebe uma lista de inteiros e retorna uma lista de inteiros. Isso permite chamar essa função diretamente nos argumentos para outra função, como `print(dobro_copia(valores))`, nesse caso a função `print` receberia a lista de dobros como argumento. Porém caso o retorno da função não seja armazenado, parecerá que a função não fez nada, ou não funcionou. Então em alguns casos, quando o valor anterior não é mais necessário, pode-se reatribuir o retorno da função a própria variável passada como argumento:

```python
valores = dobro_copia(valores)
```

### Função híbrida

Ainda é possível mesclar os dois padrões de função, alterando o valor passado e retornando-o. Exemplo:

```python
from typing import List


def dobro_hibrido(lista: List[int]) -> List[int]:
    for i in range(len(lista)):
        lista[i] = 2 * lista[i]

    return lista


valores = [5, 2, 8, 6, 4]
retorno = dobro_hibrido(valores)

print(f'Variável: valores | Tipo: {type(valores)} | Valor: {valores}')
print(f'Variável: retorno | Tipo: {type(retorno)} | Valor: {retorno}')
```

Resultado da execução:

```
Variável: valores | Tipo: <class 'list'> | Valor: [10, 4, 16, 12, 8]
Variável: retorno | Tipo: <class 'list'> | Valor: [10, 4, 16, 12, 8]
```

Nesse caso, pode-se apenas chamar a função, como também utilizá-la nos argumentos de outras funções. Porém para se ter os valores originais, deve-se fazer uma cópia manualmente antes de executar a função.

## Exemplo na biblioteca padrão

Na biblioteca padrão do Python, existem os métodos `sort` e `reverse` que seguem o padrão *in place*, e as funções `sorted` e `reversed` que seguem o padrão cópia de valor, podendo ser utilizados para ordenar e inverter os valores de uma lista, por exemplo. Quando não é mais necessário uma cópia da lista com a ordem original, é preferível utilizar funções *in place*, que alteram a própria lista, e como não criam uma cópia da lista, utilizam menos memória. Exemplo:

```python
valores = [5, 2, 8, 6, 4]
valores.sort()
valores.reverse()
print(valores)
```

Se for necessário manter uma cópia da lista inalterada, deve-se optar pelas funções de cópia de valor. Exemplo:

```python
valores = [5, 2, 8, 6, 4]
novos_valores = reversed(sorted(valores))
print(novos_valores)
```

Porém esse exemplo cria duas cópias da lista, uma em cada função. Para criar apenas uma cópia, pode-se misturar funções *in place* com cópia de valor. Exemplo:

```python
valores = [5, 2, 8, 6, 4]
novos_valores = sorted(valores)
novos_valores.reverse()
print(novos_valores)
```

Também vale observar que algumas utilizações dessas funções podem dar a impressão de que elas não funcionaram, como:

```python
valores = [5, 2, 8, 6, 4]

sorted(valores)
print(valores)  # Imprime a lista original, e não a ordenada

print(valores.sort())  # Imprime None e não a lista
```

## Considerações

Nem sempre é possível utilizar o padrão desejado, *strings* no Python (`str`) são imutáveis, logo todas as funções que manipulam elas seguiram o padrão cópia de valor, e para outros tipos, pode ocorrer de só existir funções *in place*, sendo necessário fazer uma cópia manualmente antes de chamar a função, caso necessário. Para saber qual padrão a função implementa, é necessário consultar sua documentação, ou verificando sua assinatura, embora ainda possa existir uma dúvida entre cópia de valor e híbrida, visto que a assinatura dos dois padrões são iguais.

Os exemplos aqui dados são didáticos. Caso deseja-se ordenar de forma reversa, tanto o método `sort`, quanto a função `sorted` podem receber como argumento `reverse=True`, e assim já fazer a ordenação reversa. Assim como é possível criar uma nova lista já com os valores, sem precisar adicionar manualmente item por item, como os exemplos:

```python
valores = [5, 2, 8, 6, 4]
partes_dos_valores = valores[2:]
novos_valores = [2 * valor for valor in valores]
```

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
