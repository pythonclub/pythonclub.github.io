Title: Orientação a objetos de outra forma: Property
Slug: oo-de-outra-forma-6
Date: 2021-05-17 18:00
Category: Python
Tags: python, orientação a objetos
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Seguindo com a série, chegou a hora de discutir sobre encapsulamento, ou seja, ocultar detalhes de implementação de uma classe do resto do código. Em algumas linguagens de programação isso é feito utilizando `protected` ou `private`, e às vezes o acesso aos atributos é feito através de funções *getters* e *setters*. Nesse texto vamos ver como o Python lida com essas questões.

## Métodos protegidos e privados

Diferente de linguagens como Java e PHP que possuem palavras-chave como `protected` e `private` para impedir que outras classes acessem determinados métodos ou atributos, Python deixa tudo como público. Porém isso não significa que todas as funções de uma classe podem ser chamadas por outras, ou todos os atributos podem ser lidos e alterados sem cuidados.

Para que quem estiver escrevendo um código saiba quais as funções ou atributos que não deveriam ser acessados diretamente, segue-se o padrão de começá-los com `_`, de forma similar aos arquivos ocultos em sistemas UNIX, que começam com `.`. Esse padrão já foi seguido na classe `AutenticavelComRegistro` da postagem sobre [mixins](https://dev.to/acaverna/orientacao-a-objetos-de-outra-forma-heranca-multiplas-e-mixins-31eb), onde a função que pega a data do sistema foi nomeada `_get_data`. Entretanto isso é apenas uma sugestão, nada impede dela ser chamada, como no exemplo a baixo:

```python
from datetime import datetime


class Exemplo:
    def _get_data(self):
        return datetime.now().strftime('%d/%m/%Y %T')


obj = Exemplo()
print(obj._get_data())
```

Porém algumas bibliotecas também utilizam o `_` para indicar outras informações como metadados do objeto, e que podem ser acessados sem muitos problemas. Assim é possível utilizar esse símbolo duas vezes (`__`) para indicar que realmente essa variável ou função não deveria ser acessada de fora da classe, apresentando erro de que o atributo não foi encontrado ao tentar executar a função, porém ela ainda pode ser acessada:

```python
from datetime import datetime


class Exemplo:
    def __get_data(self):
        return datetime.now().strftime('%d/%m/%Y %T')


obj = Exemplo()
print(obj.__get_data())  # AttributeError
print(obj._Exemplo__get_data())  # Executa a função
```

## Property

Os *getters* e *setters* muitas vezes são usados para impedir que determinadas variáveis sejam alteradas, ou validar o valor antes de atribuir a variável, ou ainda processar um valor a partir de outras variáveis. Porém como o Python incentiva o acesso direto as variáveis, existe a *property*, que ao tentar acessar uma variável ou alterar um valor, uma função é chamada. Exemplo:

```python
class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        self._nome = nome
        self.sobrenome = sobrenome
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @property
    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'

    @nome_completo.setter
    def nome_completo(self, valor):
        valor = valor.split(' ', 1)
        self._nome = valor[0]
        self.sobrenome = valor[1]

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        if valor < 0:
            raise ValueError
        self._idade = valor

    def fazer_aniversario(self):
        self.idade += 1
```

Nesse código algumas variáveis são acessíveis através de *properties*, de forma geral, as variáveis foram definidas começando com `_` e com uma *property* de mesmo nome (sem o `_`). O primeiro caso é o `nome`, que possui apenas o *getter*, sendo possível o seu acesso como `obj.nome`, porém ao tentar atribuir um valor, será lançado um erro (`AttributeError: can't set attribute`). Em relação ao `sobrenome`, como não é necessário nenhum tratamento especial, não foi utilizado um *property*, porém futuramente pode ser facilmente substituído por um sem precisar alterar os demais códigos. Porém a função `nome_completo` foi substituída por um *property*, permitindo tanto o acesso ao nome completo da pessoa, como se fosse uma variável, quanto trocar `nome` e `sobrenome` ao atribuir um novo valor para essa *property*. Quanto a `idade` utiliza o *setter* do *property* para validar o valor recebido, retornando erro para idades inválidas (negativas).

Vale observar também que todas as funções de *getter* não recebem nenhum argumento (além do `self`), enquanto as funções de *setter* recebem o valor atribuído à variável.

Utilizando a [ABC](https://dev.to/acaverna/orientacao-a-objetos-de-outra-forma-abc-89b), ainda é possível informar que alguma classe filha deverá implementar alguma *property*. Exemplo:

```python
from abc import ABC


class Pessoa(ABC):
    def __init__(self, nome, sobrenome, idade):
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    @property
    @abstractmethod
    def nome_completo(self):
        ...


class Brasileiro(Pessoa):
    @property
    def nome_completo(self):
        return f'{self.nome} {self.sobrenome}'


class Japones(Pessoa):
    @property
    def nome_completo(self):
        return f'{self.sobrenome} {self.nome}'
```

## Considerações

Diferente de algumas linguagens que ocultam as variáveis dos objetos, permitindo o seu acesso apenas através de funções, Python seguem no sentido contrário, acessando as funções de *getter* e *setter* como se fossem variáveis, isso permite começar com uma classe simples e ir adicionando funcionalidades conforme elas forem necessárias, sem precisar mudar o código das demais partes da aplicação, além de deixar transparente para quem desenvolve, não sendo necessário lembrar se precisa usar *getteres* e *setteres* ou não.

De forma geral, programação orientada a objetos consiste em seguir determinados padrões de código, e as linguagens que implementam esse paradigma oferecem facilidades para escrever código seguindo esses padrões, e às vezes até ocultando detalhes complexos de suas implementações. Nesse contexto, eu recomendo a palestra do autor do [htop](https://htop.dev/) feita no FISL 16, onde ele comenta como usou [orientação a objetos em C](http://hemingway.softwarelivre.org/fisl16/high/41f/sala_41f-high-201507091200.ogv). E para quem ainda quiser se aprofundar no assunto de orientação a objetos no Python, recomendo os vídeos do [Eduardo Mendes](https://www.youtube.com/playlist?list=PLOQgLBuj2-3L_L6ahsBVA_SzuGtKre3OK) (também conhecido como dunossauro).

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
