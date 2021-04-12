Title: Orientação a objetos de outra forma: Classes e objetos
Slug: oo-de-outra-forma-1
Date: 2021-04-12 15:00
Category: Python
Tags: python, orientação a objetos
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Nas poucas e raríssimas lives que eu fiz na [Twitch](https://www.twitch.tv/eduardoklosowski), surgiu a ideia de escrever sobre programação orientada a objetos em [Python](https://www.python.org/), principalmente por algumas diferenças de como ela foi implementada nessa linguagem. Aproveitando o tema, vou fazer uma série de postagens dando uma visão diferente sobre orientação a objetos. E nessa primeira postagem falarei sobre classes e objetos.

## Usando um dicionário

Entretanto, antes de começar com orientação a objetos, gostaria de apresentar e discutir alguns exemplos sem utilizar esse paradigma de programação.

Pensando em um sistema que precise manipular dados de pessoas, é possível utilizar os [dicionários](https://docs.python.org/pt-br/3/library/stdtypes.html#mapping-types-dict) do Python para agrupar os dados de uma pessoa em uma única variável, como no exemplo a baixo:

```python
pessoa = {
    'nome': 'João',
    'sobrenome': 'da Silva',
    'idade': 20,
}
```

Onde os dados poderiam ser acessados através da variável e do nome do dado desejado, como:

```python
print(pessoa['nome'])  # Imprimindo João
```

Assim, todos os dados de uma pessoa ficam agrupados em uma variável, o que facilita bastante a programação, visto que não é necessário criar uma variável para cada dado, e quando se manipula os dados de diferentes pessoas fica muito mais fácil identificar de qual pessoa aquele dado se refere, bastando utilizar variáveis diferentes.

### Função para criar o dicionário

Apesar de prático, é necessário replicar essa estrutura de dicionário toda vez que se desejar utilizar os dados de uma nova pessoa. Para evitar a repetição de código, a criação desse dicionário pode ser feita dentro de uma função que pode ser colocada em um módulo `pessoa` (arquivo, nesse caso com o nome de `pessoa.py`):

```python
# Arquivo: pessoa.py

def nova(nome, sobrenome, idade):
    return {
        'nome': nome,
        'sobrenome': sobrenome,
        'idade': idade,
    }
```

E para criar o dicionário que representa uma pessoa, basta importar esse módulo (arquivo) e chamar a função `nova`:

```python
import pessoa

p1 = pessoa.nova('João', 'da Silva', 20)
p2 = pessoa.nova('Maria', 'dos Santos', 18)
```

Desta forma, garante-se que todos os dicionários representando pessoas terão os campos desejados e devidamente preenchidos.

### Função com o dicionário

Também é possível criar algumas funções para executar operações com os dados desses dicionários, como pegar o nome completo da pessoa, trocar o seu sobrenome, ou fazer aniversário (o que aumentaria a idade da pessoa em um ano):

```python
# Arquivo: pessoa.py

def nova(nome, sobrenome, idade):
    ...  # Código abreviado


def nome_completo(pessoa):
    return f"{pessoa['nome']} {pessoa['sobrenome']}"


def trocar_sobrenome(pessoa, sobrenome):
    pessoa['sobrenome'] = sobrenome


def fazer_aniversario(pessoa):
    pessoa['idade'] += 1
```

E sendo usado como:

```python
import pessoa

p1 = pessoa.nova('João', 'da Silva', 20)
pessoa.trocar_sobrenome(p1, 'dos Santos')
print(pessoa.nome_completo(p1))
pessoa.fazer_aniversario(p1)
print(p1['idade'])
```

Nesse caso, pode-se observar que todas as funções aqui implementadas seguem o padrão de receber o dicionário que representa a pessoa como primeiro argumento, podendo ter outros argumentos ou não conforme a necessidade, acessando e alterando os valores desse dicionário.

## Versão com orientação a objetos

Antes de entrar na versão orientada a objetos propriamente dita dos exemplos anteriores, vou fazer uma pequena alteração para facilitar o entendimento posterior. A função `nova` será separada em duas partes, a primeira que criará um dicionário, e chamará uma segunda função (`init`), que receberá esse dicionário como primeiro argumento (seguindo o padrão das demais funções) e criará sua estrutura com os devidos valores.

```python
# Arquivo: pessoa.py

def init(pessoa, nome, sobrenome, idade):
    pessoa['nome'] = nome
    pessoa['sobrenome'] = sobrenome
    pessoa['idade'] = idade


def nova(nome, sobrenome, idade):
    pessoa = {}
    init(pessoa, nome, sobrenome, idade)
    return pessoa


...  # Demais funções do arquivo
```

Porém isso não muda a forma de uso:

```python
import pessoa

p1 = pessoa.nova('João', 'da Silva', 20)
```

### Função para criar uma pessoa

A maioria das linguagens de programação que possuem o paradigma de programação orientado a objetos faz o uso de classes para definir a estrutura dos objetos. O Python também utiliza classes, que podem ser definidas com a palavra-chave `class` seguidas de um nome para ela. E dentro dessa estrutura, podem ser definidas funções para manipular os objetos daquela classe, que em algumas linguagens também são chamadas de métodos (funções declaradas dentro do escopo uma classe).

Para converter o dicionário para uma classe, o primeiro passo é implementar uma função para criar a estrutura desejada. Essa função deve possui o nome `__init__`, e é bastante similar a função `init` do código anterior:

```python
class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade
```

As diferenças são que agora o primeiro parâmetro se chama `self`, que é um padrão utilizado no Python, e em vez de usar colchetes e aspas para acessar os dados, aqui basta utilizar o ponto e o nome do dado desejado (que aqui também pode ser chamado de atributo, visto que é uma variável do objeto). A função `nova` implementada anteriormente não é necessária, a própria linguagem cria um objeto e passa ele como primeiro argumento para o `__init__`. E assim para se criar um objeto da classe `Pessoa` basta chamar a classe como se fosse uma função, ignorando o argumento `self` e informando os demais, como se estivesse chamando a função `__init__` diretamente:

```python
p1 = Pessoa('João', 'da Silva', 20)
```

Nesse caso, como a própria classe cria um contexto diferente para as funções (escopo ou *namespace*), não está mais sendo utilizado arquivos diferentes, porém ainda é possível fazê-lo, sendo necessário apenas fazer o `import` adequado. Mas para simplificação, tanto a declaração da classe, como a criação do objeto da classe `Pessoa` podem ser feitas no mesmo arquivo, assim como os demais exemplos dessa postagem.

### Outras funções

As demais funções feitas anteriormente para o dicionário também podem ser feitas na classe `Pessoa`, seguindo as mesmas diferenças já apontadas anteriormente:

```python
class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    def trocar_sobrenome(self, sobrenome):
        self.sobrenome = sobrenome

    def fazer_aniversario(self):
        self.idade += 1
```

Para se chamar essas funções, basta acessá-las através do contexto da classe, passando o objeto criado anteriormente como primeiro argumento:

```python
p1 = Pessoa('João', 'dos Santos', 20)
Pessoa.trocar_sobrenome(p1, 'dos Santos')
print(Pessoa.nome_completo(p1))
Pessoa.fazer_aniversario(p1)
print(p1.idade)
```

Essa sintaxe é bastante semelhante a versão sem orientação a objetos implementada anteriormente. Porém quando se está utilizando objetos, é possível chamar essas funções com uma outra sintaxe, informando primeiro o objeto, seguido de ponto e o nome da função desejada, com a diferença de que não é mais necessário informar o objeto como primeiro argumento. Como a função foi chamada através de um objeto, o próprio Python se encarrega de passá-lo para o argumento `self`, sendo necessário informar apenas os demais argumentos:

```python
p1.trocar_sobrenome('dos Santos')
print(p1.nome_completo())
p1.fazer_aniversario()
print(p1.idade)
```

Existem algumas diferenças entre as duas sintaxes, porém isso será tratado posteriormente. Por enquanto a segunda sintaxe pode ser vista como um [açúcar sintático](https://pt.wikipedia.org/wiki/A%C3%A7%C3%BAcar_sint%C3%A1tico) da primeira, ou seja, uma forma mais rápida e fácil de fazer a mesma coisa que a primeira, e por isso sendo a recomendada.

## Considerações

Como visto nos exemplos, programação orientada a objetos é uma técnica para juntar variáveis em uma mesma estrutura e facilitar a escrita de funções que seguem um determinado padrão, recebendo a estrutura como argumento, porém a sintaxe mais utilizada no Python para chamar as funções de um objeto (métodos) posiciona a variável que guarda a estrutura antes do nome da função, em vez do primeiro argumento.

No Python, o argumento da estrutura ou objeto (`self`) aparece explicitamente como primeiro argumento da função, enquanto em outras linguagens essa variável pode receber outro nome (como `this`) e não aparece explicitamente nos argumentos da função, embora essa variável tenha que ser criada dentro do contexto da função para permitir manipular o objeto.

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
