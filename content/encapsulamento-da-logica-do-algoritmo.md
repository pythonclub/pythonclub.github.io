Title: Encapsulamento da lógica do algoritmo
Slug: encapsulamento-da-logica-do-algoritmo
Date: 2021-03-02 15:00
Category: Python
Tags: python, poo
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Programador, formado em redes de computadores, estuda DevOps

Muitas listas de exercícios de lógica de programação pedem em algum momento que um valor seja lido do teclado, e caso esse valor seja inválido, deve-se avisar, e repetir a leitura até que um valor válido seja informado. Utilizando a ideia de [otimização do algoritmo passo a passo](https://dev.to/acaverna/otimizando-o-algoritmo-passo-a-passo-4co0), começando com uma solução simples, pretendo estudar como reduzir a duplicação de código alterando o algoritmo, encapsulando a lógica em funções, e encapsulando em classes.

## Exercício

Um exemplo de exercício que pede esse tipo de validação é a leitura de notas, que devem estar entre 0 e 10. A solução mais simples, consiste em ler um valor, e enquanto esse valor for inválido, dar o aviso e ler outro valor. Exemplo:

```python
nota = float(input('Digite a nota: '))
while nota < 0 or nota > 10:
    print('Nota inválida')
    nota = float(input('Digite a nota: '))
```

Esse algoritmo funciona, porém existe uma duplicação no código que faz a leitura da nota (uma antes do *loop* e outra dentro). Caso seja necessário uma alteração, como a mudança da nota para um valor inteiro entre 0 e 100, deve-se alterar os dois lugares, e se feito em apenas um lugar, o algoritmo poderia processar valores inválidos.

### Alterando o algoritmo

Visando remover a repetição de código, é possível unificar a leitura do valor dentro do *loop*, uma vez que é necessário repetir essa instrução até que o valor válido seja obtido. Exemplo:

```python
while True:
    nota = float(input('Digite a nota: '))
    if 0 <= nota <= 10:
        break
    print('Nota inválida!')
```

Dessa forma, não existe mais a repetição de código. A condição de parada, que antes verificava se o valor era inválido (o que pode ter uma leitura não tão intuitiva), agora verifica se é um valor válido (que é geralmente é mais fácil de ler e escrever a condição). E a ordem dos comandos dentro do *loop*, que agora estão em uma ordem que facilita a leitura, visto que no algoritmo anterior era necessário tem em mente o que era executado antes do *loop*.

Porém esses algoritmos validam apenas o valor lido, apresentando erro caso seja informado um valor com formato inválido, como letras em vez de números. Isso pode ser resolvido tratando as exceções lançadas. Exemplo:

```python
while True:
    try:
        nota = float(input('Digite a nota: '))
        if 0 <= nota <= 10:
            break
    except ValueError:
        ...
    print('Nota inválida!')
```

### Encapsulamento da lógica em função

Caso fosse necessário ler várias notas, com os algoritmos apresentados até então, seria necessário repetir todo esse trecho de código, ou utilizá-lo dentro de uma estrutura de repetição. Para facilitar sua reutilização, evitando a duplicação de código, é possível encapsular esse algoritmo dentro de uma função. Exemplo:

```python
def nota_input(prompt):
    while True:
        try:
            nota = float(input(prompt))
            if 0 <= nota <= 10:
                break
        except ValueError:
            ...
        print('Nota inválida!')
    return nota


nota1 = nota_input('Digite a primeira nota: ')
nota2 = nota_input('Digite a segunda nota: ')
```

### Encapsulamento da lógica em classes

Em vez de encapsular essa lógica em uma função, é possível encapsulá-la em uma classe, o que permitiria separar cada etapa do algoritmo em métodos, assim como ter um método responsável por controlar qual etapa deveria ser chamada em qual momento. Exemplo:

```python
class ValidaNotaInput:
    mensagem_valor_invalido = 'Nota inválida!'

    def ler_entrada(self, prompt):
        return input(prompt)

    def transformar_entrada(self, entrada):
        return float(entrada)

    def validar_nota(self, nota):
        return 0 <= nota <= 10

    def __call__(self, prompt):
        while True:
            try:
                nota = self.transformar_entrada(self.ler_entrada(prompt))
                if self.validar_nota(nota):
                    break
            except ValueError:
                ...
            print(self.mensagem_valor_invalido)
        return nota


nota_input = ValidaNotaInput()


nota = nota_input('Digite a nota: ')
```

Vale observar que o método `__call__` permite que o objeto criado a partir dessa classe seja chamado como se fosse uma função. Nesse caso ele é o responsável por chamar cada etapa do algoritmo, como: `ler_entrada` que é responsável por ler o que foi digitado no teclado, `transformar_entrada` que é responsável por converter o texto lido para o tipo desejado (converter de `str` para `float`), e `validar_nota` que é responsável por dizer se o valor é válido ou não. Vale observar que ao dividir o algoritmo em métodos diferentes, seu código principal virou uma espécie de código comentado, descrevendo o que está sendo feito e onde está sendo feito.

Outra vantagem de encapsular a lógica em classe, em vez de uma função, é a possibilidade de generalizá-la. Se fosse necessário validar outro tipo de entrada, encapsulando em uma função, seria necessário criar outra função repetindo todo o algoritmo, alterando apenas a parte referente a transformação do valor lido, e validação, o que gera uma espécie de repetição de código. Ao encapsular em classes, é possível se aproveitar dos mecanismos de herança para evitar essa repetição. Exemplo:

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


nome_input = ValidaNomeInput()
nota_input = ValidaNotaInput()


nome = nome_input('Digite o nome: ')
nota = nota_input('Digite a nota: ')
```

Dessa forma, é possível reutilizar o código já existente para criar outras validações, sendo necessário implementar apenas como converter a `str` lida do teclado para o tipo desejado, e como esse valor deve ser validado. Não é necessário entender e repetir a lógica de ler o valor, validá-lo, imprimir a mensagem de erro, e repetir até que seja informado um valor válido.

## Considerações

É possível encapsular a lógica de um algoritmo em funções ou em classes. Embora para fazê-lo em uma classe exija conhecimentos de programação orientada a objetos, o seu reaproveitamento é facilitado, abstraindo toda a complexidade do algoritmo, que pode ser disponibilizado através de uma biblioteca, exigindo apenas a implementações de métodos simples por quem for a utilizar.

Ainda poderia ser discutido outras formas de fazer essa implementação, como passar funções como parâmetro e a utilização de [corrotinas](https://docs.python.org/pt-br/3/library/asyncio-task.html) no encapsulamento do algoritmo em função, assim como a utilização de [classmethod](https://docs.python.org/pt-br/3/library/functions.html#classmethod), [staticmethod](https://docs.python.org/pt-br/3/library/functions.html#staticmethod) e [ABC](https://docs.python.org/pt-br/3/library/abc.html) no encapsulamento do algoritmo em classes.

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
