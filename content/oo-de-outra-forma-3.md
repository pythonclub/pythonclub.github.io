Title: Orientação a objetos de outra forma: Herança
Slug: oo-de-outra-forma-3
Date: 2021-04-26 17:00
Category: Python
Tags: python, orientação a objetos
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Algo que ajuda no desenvolvimento é a reutilização de código. Em orientação a objetos, essa reutilização pode ocorrer através de herança, onde um objeto pode se comportar como um objeto da sua própria classe, como também da classe que herdou.

## Adicionando funcionalidades

Uma das utilidades da herança é estender uma classe para adicionar funcionalidades. Pensando no contexto das postagens anteriores, poderíamos querer criar um usuário e senha para algumas pessoas poderem acessar o sistema. Isso poderia ser feito adicionando atributos usuário e senha para as pessoas, além de uma função para validar se os dados estão corretos, e assim permitir o acesso ao sistema. Porém isso não pode ser feito para todas as pessoas, e sim apenas para aqueles que possuem permissão de acesso.

### Sem orientação a objetos

Voltando a solução com dicionários (sem utilizar orientação a objetos), isso consistiria em criar um dicionário com a estrutura de uma pessoa, e em seguida estender essa estrutura com os novos campos de usuário e senha nesse mesmo dicionário, algo como:

```python
# Arquivo: pessoa.py

def init(pessoa, nome, sobrenome, idade):
    pessoa['nome'] = nome
    pessoa['sobrenome'] = sobrenome
    pessoa['idade'] = idade


def nome_completo(pessoa):
    return f"{pessoa['nome']} {pessoa['sobrenome']}"
```

```python
# Arquivo: pessoa_autenticavel.py

def init(pessoa, usuario, senha):
    pessoa['usuario'] = usuario
    pessoa['senha'] = senha


def autenticar(pessoa, usuario, senha):
    return pessoa['usuario'] == usuario and pessoa['senha'] == senha
```

```python
import pessoa
import pessoa_autenticavel

p = {}
pessoa.init(p, 'João', 'da Silva', 20)
pessoa_autenticavel.init(p, 'joao', 'secreta')

print(pessoa.nome_completo(p))
print(pessoa_autenticavel.autenticar(p, 'joao', 'secreta'))
```

Porém nessa solução é possível que o programador esqueça de chamar as duas funções `init` diferentes, e como queremos que todo dicionário com a estrutura de `pessoa_autenticavel` contenha também a estrutura de `pessoa`, podemos chamar o `init` de pessoa dentro do `init` de `pessoa_autenticavel`:

```python
# Arquivo: pessoa_autenticavel.py

import pessoa


def init(p, nome, sobrenome, idade, usuario, senha):
    pessoa.init(p, nome, sobrenome, idade)
    p['usuario'] = usuario
    p['senha'] = senha


...  # Demais funções
```

```python
import pessoa
import pessoa_autenticavel

p = {}
pessoa_autenticavel.init(p, 'João', 'da Silva', 20, 'joao', 'secreta')

print(pessoa.nome_completo(p))
print(pessoa_autenticavel.autenticar(p, 'joao', 'secreta'))
```

Nesse caso foi necessário alterar o nome do argumento `pessoa` da função `pessoa_autenticavel.init` para não conflitar com o outro módulo importado com esse mesmo nome. Porém ao chamar um `init` dentro de outro, temos a garantia de que o dicionário será compatível tanto com a estrutura pedida para ser criada pelo programador, quanto pelas estruturas pais dela.

### Com orientação a objetos

```python
class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'


class PessoaAutenticavel(Pessoa):
    def __init__(self, nome, sobrenome, idade, usuario, senha):
        Pessoa.__init__(self, nome, sobrenome, idade)
        self.usuario = usuario
        self.senha = senha

    def autenticar(self, usuario, senha):
        return self.usuario == usuario and self.senha == senha


p = PessoaAutenticavel('João', 'da Silva', 20, 'joao', 'secreta')

print(Pessoa.nome_completo(p))
print(PessoaAutenticavel.autenticar(p, 'joao', 'secreta'))
```

A principal novidade desse exemplo é que ao declarar a classe `PessoaAutenticavel` (filha), foi declarado a classe `Pessoa` (pai) entre parênteses, isso faz o interpretador Python criar uma cópia dessa classe estendendo-a com as novas funções que estamos criando. Porém pode ser um pouco redundante chamar `Pessoa.__init__` dentro da função `__init__` sendo que já foi declarado que ela estende `Pessoa`, podendo ser trocado por `super()`, que aponta para a classe que foi estendida. Exemplo:

```python
class PessoaAutenticavel(Pessoa):
    def __init__(self, nome, sobrenome, idade, usuario, senha):
        super().__init__(nome, sobrenome, idade)
        self.usuario = usuario
        self.senha = senha

    ...  # Demais funções
```

Assim se evita repetir o nome da classe, e já passa automaticamente a referência para `self`, assim como quando usamos o açúcar sintático apresentado na primeira postagem dessa série. E esse açúcar sintática também pode ser usado para chamar tanto as funções declaradas em `Pessoa` quanto em `PessoaAutenticavel`. Exemplo:

```python
p = PessoaAutenticavel('João', 'da Silva', 20, 'joao', 'secreta')

print(p.nome_completo())
print(p.autenticar('joao', 'secreta'))
```

Esse método também facilita a utilização das funções, uma vez que não é necessário lembrar em qual classe que cada função foi declarada. Na verdade, como `PessoaAutenticavel` estende `Pessoa`, seria possível executar também `PessoaAutenticavel.nome_completo`, porém eles apontam para a mesma função.

## Sobrescrevendo uma função

A classe `Pessoa` possui a função `nome_completo` que retorna uma `str` contento nome e sobrenome. Porém no Japão, assim como em outros países asiáticos, o sobrenome vem primeiro, e até [estão pedindo para seguir a tradição deles ao falarem os nomes de japoneses](https://noticias.uol.com.br/ultimas-noticias/efe/2019/06/24/japao-quer-voltar-a-ordem-tradicional-dos-nomes-abe-shinzo-nao-shinzo-abe.htm), como o caso do primeiro-ministro, mudando de Shinzo Abe para Abe Shinzo.

### Com orientação a objetos

Isso também pode ser feito no sistema usando herança, porém em vez de criar uma nova função com outro nome, é possível criar uma função com o mesmo nome, sobrescrevendo a anterior, porém apenas para os objetos da classe filha. Algo semelhante ao que já foi feito com a função `__init__`. Exemplo:

```python
class Japones(Pessoa):
    def nome_completo(self):
        return f'{self.sobrenome} {self.nome}'


p1 = Pessoa('João', 'da Silva', 20)
p2 = Japones('Shinzo', 'Abe', 66)

print(p1.nome_completo())  # João da Silva
print(p2.nome_completo())  # Abe Shinzo
```

Essa relação de herança traz algo interessante, todo objeto da classe `Japones` se comporta como um objeto da classe `Pessoa`, porém a relação inversa não é verdade. Assim como podemos dizer que todo japonês é uma pessoa, mas nem todas as pessoas são japonesas. Ser japonês é um caso mais específico de pessoa, assim como as demais nacionalidades.

### Sem orientação a objetos

Esse comportamento de sobrescrever a função `nome_completo` não é tão simples de replicar em uma estrutura de dicionário, porém é possível fazer. Porém como uma pessoa pode ser tanto japonês quanto não ser, não é possível saber de antemão para escrever no código `pessoa.nome_completo` ou `japones.nome_completo`, que diferente do exemplo da autenticação, agora são duas funções diferentes, isso precisa ser descoberto dinamicamente quando se precisar chamar a função.

Uma forma de fazer isso é guardar uma referência para a função que deve ser chamada dentro da própria estrutura. Exemplo:

```python
# Arquivo: pessoa.py

def init(pessoa, nome, sobrenome, idade):
    pessoa['nome'] = nome
    pessoa['sobrenome'] = sobrenome
    pessoa['idade'] = idade
    pessoa['nome_completo'] = nome_completo


def nome_completo(pessoa):
    return f"{pessoa['nome']} {pessoa['sobrenome']}"
```

```python
# Arquivo: japones.py

import pessoa


def init(japones, nome, sobrenome, idade):
    pessoa(japones, nome, sobrenome, idade)
    japones['nome_completo'] = nome_completo


def nome_completo(japones):
    return f"{pessoa['sobrenome']} {pessoa['nome']}"
```

```python
import pessoa
import japones

p1 = {}
pessoa.init(p1, 'João', 'da Silva', 20)
p2 = {}
japones.init(p2, 'Shinzo', 'Abe', 66)

print(p1['nome_completo'](p1))  # João da Silva
print(p2['nome_completo'](p2))  # Abe Shinzo
```

Perceba que a forma de chamar a função foi alterada. O que acontece na prática é que toda função que pode ser sobrescrita não é chamada diretamente, e sim a partir de uma referência, e isso gera um custo computacional adicional. Como esse custo não é tão alto (muitas vezes sendo quase irrelevante), esse é o comportamento adotado em várias linguagens, porém em C++, por exemplo, existe a palavra-chave `virtual` para descrever quando uma função pode ser sobrescrita ou não.

## Considerações

Herança é um mecanismo interessante para ser explorado com o objetivo de reaproveitar código e evitar repeti-lo. Porém isso pode vir com alguns custos, seja computacional durante sua execução, seja durante a leitura do código, sendo necessário verificar diversas classes para saber o que de fato está sendo executado, porém isso também pode ser usado para ocultar e abstrair lógicas mais complicadas, como eu já comentei em outra [postagem](https://dev.to/acaverna/encapsulamento-da-logica-do-algoritmo-298e).

Herança também permite trabalhar com generalização e especialização, podendo descrever o comportamento mais geral, ou mais específico. Ou simplesmente só adicionar mais funcionalidades a uma classe já existente.

Assim como foi utilizado o `super()` para chamar a função `__init__` da classe pai, é possível utilizá-lo para chamar qualquer outra função. Isso permite, por exemplo, tratar os argumentos da função, aplicando modificações antes de chamar a função original, ou seu retorno, executando algum processamento em cima do retorno dela, não precisando rescrever toda a função.

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
