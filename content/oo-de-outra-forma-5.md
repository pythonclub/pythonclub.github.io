Title: Orientação a objetos de outra forma: ABC
Slug: oo-de-outra-forma-5
Date: 2021-05-10 12:00
Category: Python
Tags: python, orientação a objetos
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Na discussão sobre [herança e mixins](https://dev.to/acaverna/orientacao-a-objetos-de-outra-forma-heranca-multiplas-e-mixins-31eb) foram criadas várias classes, como `Autenticavel` e `AutenticavelComRegistro` que adicionam funcionalidades a outras classes e implementavam tudo o que precisavam para seu funcionamento. Entretanto podem existir casos em que não seja possível implementar todas as funções na própria classe, deixando com que as classes que a estende implemente essas funções. Uma forma de fazer isso é través das [ABC](https://docs.python.org/pt-br/3/library/abc.html) (*abstract base classes*, ou classes base abstratas).

## Sem uso de classes base abstratas

Um exemplo de classe que não é possível implementar todas as funcionalidades foi dada no texto [Encapsulamento da lógica do algoritmo](https://dev.to/acaverna/encapsulamento-da-logica-do-algoritmo-298e), que discutia a leitura de valores do teclado até que um valor válido fosse lido (ou que repete a leitura caso um valor inválido tivesse sido informado). Nesse caso a classe `ValidaInput` implementava a lógica base de funcionamento, porém eram suas classes filhas (`ValidaNomeInput` e `ValidaNotaInput`) que implementavam as funções para tratar o que foi lido do teclado e verificar se é um valor válido ou não.

```python
class ValidaInput:
    mensagem_valor_invalido = 'Valor inválido!'

    def ler_entrada(self, prompt):
        return input(prompt)

    def transformar_entrada(self, entrada):
        raise NotImplementedError

    def validar_valor(self, valor):
        raise NotImplementedError

    def __call__(self, prompt):
        while True:
            try:
                valor = self.transformar_entrada(self.ler_entrada(prompt))
                if self.validar_valor(valor):
                    break
            except ValueError:
                ...
            print(self.mensagem_valor_invalido)
        return valor


class ValidaNomeInput(ValidaInput):
    mensagem_valor_invalido = 'Nome inválido!'

    def transformar_entrada(self, entrada):
        return entrada.strip().title()

    def validar_valor(self, valor):
        return valor != ''


class ValidaNotaInput(ValidaInput):
    mensagem_valor_invalido = 'Nota inválida!'

    def transformar_entrada(self, entrada):
        return float(entrada)

    def validar_valor(self, valor):
        return 0 <= valor <= 10
```

Entretanto, esse código permite a criação de objetos da classe `ValidaInput` mesmo sem ter uma implementação das funções `transformar_entrada` e `validar_valor`. E a única mensagem de erro ocorreria ao tentar executar essas funções, o que poderia estar longe do problema real, que é a criação de um objeto a partir de uma classe que não prove todas as implementações das suas funções, o que seria semelhante a uma classe abstrata em outras linguagens.

```python
obj = ValidaInput()

# Diversas linhas de código

obj('Entrada: ')  # Exceção NotImplementedError lançada
```

## Com uso de classes base abstratas

Seguindo a documentação da [ABC](https://docs.python.org/pt-br/3/library/abc.html), para utilizá-las é necessário informar a metaclasse `ABCMeta` na criação da classe, ou simplesmente estender a classe `ABC`, e decorar com `abstractmethod` as funções que as classes que a estenderem deverão implementar. Exemplo:

```python
from abc import ABC, abstractmethod


class ValidaInput(ABC):
    mensagem_valor_invalido = 'Valor inválido!'

    def ler_entrada(self, prompt):
        return input(prompt)

    @abstractmethod
    def transformar_entrada(self, entrada):
        ...

    @abstractmethod
    def validar_valor(self, valor):
        ...

    def __call__(self, prompt):
        while True:
            try:
                valor = self.transformar_entrada(self.ler_entrada(prompt))
                if self.validar_valor(valor):
                    break
            except ValueError:
                ...
            print(self.mensagem_valor_invalido)
        return valor
```

Desta forma, ocorrerá um erro já ao tentar criar um objeto do tipo `ValidaInput`, dizendo quais são as funções que precisam ser implementadas. Porém funcionará normalmente ao criar objetos a partir das classes `ValidaNomeInput` e `ValidaNotaInput` visto que elas implementam essas funções.

```python
obj = ValidaInput()  # Exceção TypeError lançada

nome_input = ValidaNomeInput()  # Objeto criado
nota_input = ValidaNotaInput()  # Objeto criado
```

Como essas funções não utilizam a referência ao objeto (`self`), ainda é possível decorar as funções com `staticmethod`, como:

```python
from abc import ABC, abstractmethod


class ValidaInput(ABC):
    mensagem_valor_invalido = 'Valor inválido!'

    @staticmethod
    def ler_entrada(prompt):
        return input(prompt)

    @staticmethod
    @abstractmethod
    def transformar_entrada(entrada):
        ...

    @staticmethod
    @abstractmethod
    def validar_valor(valor):
        ...

    def __call__(self, prompt):
        while True:
            try:
                valor = self.transformar_entrada(self.ler_entrada(prompt))
                if self.validar_valor(valor):
                    break
            except ValueError:
                ...
            print(self.mensagem_valor_invalido)
        return valor


class ValidaNomeInput(ValidaInput):
    mensagem_valor_invalido = 'Nome inválido!'

    @staticmethod
    def transformar_entrada(entrada):
        return entrada.strip().title()

    @staticmethod
    def validar_valor(valor):
        return valor != ''


class ValidaNotaInput(ValidaInput):
    mensagem_valor_invalido = 'Nota inválida!'

    @staticmethod
    def transformar_entrada(entrada):
        return float(entrada)

    @staticmethod
    def validar_valor(valor):
        return 0 <= valor <= 10
```

Isso também seria válido para funções decoradas com `classmethod`, que receberiam a referência a classe (`cls`).

## Considerações

Não é necessário utilizar ABC para fazer o exemplo discutido, porém ao utilizar essa biblioteca ficou mais explícito quais as funções que precisavam ser implementados nas classes filhas, ainda mais que sem utilizar ABC a classe base poderia nem ter as funções, com:

```python
class ValidaInput:
    mensagem_valor_invalido = 'Valor inválido!'

    def ler_entrada(self, prompt):
        return input(prompt)

    def __call__(self, prompt):
        while True:
            try:
                valor = self.transformar_entrada(self.ler_entrada(prompt))
                if self.validar_valor(valor):
                    break
            except ValueError:
                ...
            print(self.mensagem_valor_invalido)
        return valor
```

Como Python possui [duck-typing](https://docs.python.org/pt-br/3/glossary.html#term-duck-typing), não é necessário uma grande preocupação com os tipos, como definir e utilizar interfaces presentes em outras implementações de orientação a objetos, porém devido à herança múltipla, ABC pode ser utilizada como interface que não existe em Python, fazendo com que as classes implementem determinadas funções. Para mais a respeito desse assunto, recomendo as duas lives do dunossauro sobre ABC ([1](https://www.youtube.com/watch?v=yLHV1__nZZw) e [2](https://www.youtube.com/watch?v=erAXvsuihPQ)), e a apresentação do Luciano Ramalho sobre [type hints](https://www.youtube.com/watch?v=AJK2LqrlnTE).

Uma classe filha também não é obrigada a implementar todas as funções decoradas com `abstractmethod`, mas assim como a classe pai, não será possível criar objetos a partir dessa classe, apenas de uma classe filha dela que implemente as demais funções. Como se ao aplicar um `abstractmethod` tornasse a classe abstrata, e qualquer classe filha só deixasse de ser abstrata quando a última função decorada com `abstractmethod` for sobrescrita. Exemplo:

```python
from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def func1(self):
        ...

    @abstractmethod
    def func2(self):
        ...


class B(A):
    def func1(self):
        print('1')


class C(B):
    def func2(self):
        print('2')


a = A()  # Erro por não implementar func1 e func2
b = B()  # Erro por não implementar func2
c = C()  # Objeto criado
```

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
