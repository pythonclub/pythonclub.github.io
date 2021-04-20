Title: Orientação a objetos de outra forma: Métodos estáticos e de classes
Slug: oo-de-outra-forma-2
Date: 2021-04-19 17:00
Category: Python
Tags: python, orientação a objetos
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores e estuda DevOps

Na [postagem anterior](https://dev.to/acaverna/orientacao-a-objetos-de-outra-forma-classes-e-objetos-3mfd) foi apresentado o `self`, nessa postagem será discutido mais a respeito desse argumento, considerando opções para ele e suas aplicações.

## Métodos estáticos

Nem todas as funções de uma classe precisam receber uma referência de um objeto para lê-lo ou alterá-lo, muitas vezes uma função pode fazer o seu papel apenas com os dados passados como argumento, por exemplo, receber um nome e validar se ele possui pelo menos três caracteres sem espaço. Dessa forma, essa função poderia ser colocada fora do escopo da classe, porém para facilitar sua chamada, e possíveis alterações (que será discutido em outra postagem), é possível colocar essa função dentro da classe e informar que ela não receberá o argumento `self` com o decorador `@staticmethod`:

```python
class Pessoa:
    ...  # Demais funções

    @staticmethod
    def valida_nome(nome):
        return len(nome) >= 3 and ' ' not in nome
```

Dessa forma, essa função pode ser chamada diretamente de um objeto pessoa, ou até mesmo diretamente da classe, sem precisar criar um objeto primeiro:

```python
# Chamando diretamente da classe
print(Pessoa.valida_nome('João'))

# Chamando através de um objeto do tipo Pessoa
p1 = Pessoa('João', 'da Silva', 20)
print(p1.valida_nome(p1.nome))
```

E essa função também pode ser utilizada dendro de outras funções, como validar o nome na criação de uma pessoa, de forma que caso o nome informado seja válido, será criado um objeto do tipo Pessoa, e caso o nome seja inválido, será lançado uma exceção:

```python
class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        if not self.valida_nome(nome):
            raise ValueError('Nome inválido')

        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

    ...  # Demais funções

    @staticmethod
    def valida_nome(nome):
        return len(nome) >= 3 and ' ' not in nome


p1 = Pessoa('João', 'da Silva', 20)  # Cria objeto
p2 = Pessoa('a', 'da Silva', 20)  # Lança ValueError: Nome inválido
```

## Métodos da classe

Entretanto algumas funções podem precisar de um meio termo, necessitar acessar o contexto da classe, porém sem necessitar de um objeto. Isso é feito através do decorador `@classmethod`, onde a função decorada com ele, em vez de receber um objeto como primeiro argumento, recebe a própria classe.

Para demonstrar essa funcionalidade será implementado um *id* auto incremental para os objetos da classe `Pessoa`:

```python
class Pessoa:
    total_de_pessoas = 0

    @classmethod
    def novo_id(cls):
        cls.total_de_pessoas += 1
        return cls.total_de_pessoas

    def __init__(self, nome, sobrenome, idade):
        self.id = self.novo_id()
        self.nome = nome
        self.sobrenome = sobrenome
        self.idade = idade

p1 = Pessoa('João', 'da Silva', 20)
print(p1.id)  # Imprime 1
p2 = Pessoa('Maria', 'dos Santos', 18)
print(p2.id)  # Imprime 2
print(Pessoa.total_de_pessoas)  # Imprime 2
print(p1.total_de_pessoas)  # Imprime 2
print(p2.total_de_pessoas)  # Imprime 2
```

Nesse código é criado uma variável `total_de_pessoas` dentro do escopo da classe `Pessoas`, e que é compartilhado tanto pela classe, como pelos objetos dessa classe, diferente de declará-la com `self.` dentro do `__init__`, onde esse valor pertenceria apenas ao objeto, e não é compartilhado com os demais objetos. Declarar variáveis dentro do contexto da classe é similar ao se declarar variáveis com `static` em outras linguagens, assim como o `@classmethod` é semelhante a declaração de funções com `static`.

As funções declaradas com `@classmethod` também podem ser chamadas sem a necessidade de se criar um objeto, como `Pessoa.novo_id()`, embora que para essa função específica isso não faça muito sentido, ou receber outros argumentos, tudo depende do que essa função fará.

## Considerações

Embora possa parecer confuso identificar a diferença de uma função de um objeto (função sem decorador), função de uma classe (com decorador `@classmethod`) e função sem acesso a nenhum outro contexto (com decorador `@staticmethod`), essa diferença fica mais clara ao se analisar o primeiro argumento recebido por cada tipo de função. Podendo ser a referência a um objeto (`self`) e assim necessitando que um objeto seja criado anteriormente, ser uma classe (`cls`) e não necessitando receber um objeto, ou simplesmente não recebendo nenhum argumento especial, apenas os demais argumentos necessários para a função. Sendo diferenciados pelo uso dos decoradores.

Na orientação a objetos implementada pelo Python, algumas coisas podem ficar confusas quando se mistura com nomenclaturas de outras linguagens que possuem implementações diferentes. A linguagem Java, por exemplo, utiliza a palavra-chave `static` para definir os atributos e métodos de classe, enquanto no Python um método estático é aquele que não acessa nem um objeto, nem uma classe, devendo ser utilizado o escopo da classe e o decorador `@classmethod` para se criar atributos e métodos da classe.

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
