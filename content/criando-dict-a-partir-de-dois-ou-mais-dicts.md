Title: Criando dicts a partir de outros dicts
Slug: crie_dict-a-partir-de-outros-dicts
Date: 2019-10-01 20:20:29
Category: Python
Tags: Python, Dict
Author: Michell Stuttgart
Email: michellstut@gmail.com
Github: mstuttgart
Linkedin: mstuttgart
Site: https://mstuttgart.github.io
Summary: Crie dicts a partir de outros dicts

Neste tutorial, será abordado o processo de criação de um *dict* ou dicionário, a partir de um ou mais *dicts* em Python. 

Como já é de costume da linguagem, isso pode ser feito de várias maneiras diferentes.

## Abordagem inicial

Pra começar, vamos supor que temos os seguintes dicionários:

```python
dict_1 = {
    'a': 1,
    'b': 2,
}

dict_2 = {
    'b': 3,
    'c': 4,
}
```

Como exemplo, vamos criar um novo dicionário chamado **new_dict** com os valores de **dict_1** e **dict_2** logo acima. Uma abordagem bem conhecida é utilizar o método *update*.

```python
new_dict = {}

new_dcit.update(dict_1)
new_dcit.update(dict_2)
```

Assim, temos que **new_dict** será:

```python
>> print(new_dict)
{
    'a': 1,
    'b': 3,
    'c': 4,
}
```

Este método funciona bem, porém temos de chamar o método *update* para cada *dict* que desejamos mesclar em **new_dict**. Não seria interessante se fosse possível passar todos os *dicts* necessários já na inicialização de **new_dict**?

### Novidades do Python 3

O Python 3 introduziu uma maneira bem interessante de se fazer isso, utilizando os operadores `**`.

```python
new_dict = {
    **dict_1,
    **dict_2,
}

```

Assim, de maneira semelhante ao exemplo anterior, temos que **new_dict** será :

```python
>> print(new_dict['a'])
1
>> print(new_dict['b'])
3
>> print(new_dict['c'])
4
```

## Cópia real de *dicts*

Ao utilizamos o procedimento de inicialização acima, devemos tomar conseiderar alguns fatores. Apenas os valores do primeiro nível serão realmente duplicados no novo dicionário. Como exemplo, vamos alterar uma chave presente em ambos os *dicts* e verificar se as mesmas possuem o mesmo valor:

```python
>> dict_1['a'] = 10
>> new_dict['a'] = 11
>> print(dict_1['a'])
10
>> print(new_dict['a'])
11
```

Porém isso muda quando um dos valores de **dict_1** for uma *list*, outro *dict* ou algum objeto complexo. Por exemplo:

```python
dict_3 = {
    'a': 1,
    'b': 2,
    'c': {
        'd': 5,
    }
}
```

e agora, vamos criar um novo *dict* a partir desse:

```python
new_dict = {
    **dict_3,
}

```

Como no exemplo anterior, podemos imaginar que foi realizado uma cópia de todos os elementos de **dict_3**, porém isso não é totalmente verdade. O que realmente aconteceu é que foi feita uma cópia *superficial* dos valores de **dict_3**, ou seja, apenas os valores de *primeiro nível* foram duplicados. Observe o que acontece quando alteramos o valor do *dict* presente na chave **c**.

```python
>> new_dict['c']['d'] = 11
>> print(new_dict['c']['d'])
11
>> print(dict_3['c']['d'])
11 
# valor anterior era 5

```

No caso da chave **c**, ela contem uma referência para outra estrutura de dados (um *dict*, no caso). Quando alteramos algum valor de **dict_3['c']**, isso reflete em todos os *dict* que foram inicializados com **dict_3**. Em outras palavras, deve-se ter cuidado ao inicializar um *dict* a partir de outros **dicts** quando os mesmos possuírem valores complexos, como *list*, *dict* ou outros objetos (os atributos deste objeto não serão duplicados).

De modo a contornar este inconveniente, podemos utilizar o método *deepcopy* da *lib* nativa [copy](https://docs.python.org/2/library/copy.html). Agora, ao inicializarmos **new_dict**:

```python
import copy

dict_3 = {
    'a': 1,
    'b': 2,
    'c': {
        'd': 5,
    }
}

new_dict = copy.deepcopy(dict_3)
```

O método *deepcopy* realiza uma cópia recursiva de cada elemento de **dict_3**, resolvendo nosso problema. Veja mais um exemplo:

```python
>> new_dict['c']['d'] = 11
>> print(new_dict['c']['d'])
11
>> print(dict_3['c']['d'])
5 
# valor não foi alterado
```

## Conclusão

Este artigo tenta demonstrar de maneira simples a criação de *dicts*, utilizando os diversos recursos que a linguagem oferece bem como os prós e contras de cada abordagem. 

## Referências

Para mais detalhes e outros exemplos, deem uma olhada neste *post* do forum da Python Brasil [aqui](https://groups.google.com/forum/#!topic/python-brasil/OhUqYQ32M7E).

É isso pessoal. Obrigado por ler!
