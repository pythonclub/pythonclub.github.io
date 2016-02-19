Title: Paralelismo em Python usando concurrent.futures
Slug: paralelismo-em-python-usando-concurrent.futures
Date: 2016-02-19 09:00
Tags: python, concorrencia, paralelismo
Author: José Cordeiro de Oliveira Junior
Email:  cordjr@gmail.com
Github: cordjr
Site: http://letsgetincode.com.br
Linkedin: https://br.linkedin.com/in/josé-cordeiro-de-oliveira-junior-10a17b49
Twitter: cordjr
Category: Python


 Esse post tem por objetivo abordar o uso da bliblioteca [concurrent.futures](https://docs.python.org/dev/library/concurrent.futures.html) para realizar operações paralelas em Python. Dito isto, gostaria de contextualizar de forma simples _paralelismo_ e _concorrência_:

 - **Concorrência:** é quando um computador que possui apenas um core parece estar realizando duas ou mais operações ao mesmo tempo, quando na verdade está alternando a execução destas operações de forma tão rápida que temos a ilusão de que tudo é executado simultaneamente.
e
 - **Paralelismo:** é quando um computador que possui dois ou mais cores executa operações realmente de forma paralela, utilizando para isso os cores disponíveis, ou seja, se um determinado computador tem 2 cores posso ter duas operações sendo executadas paralelamente cada uma em um core diferente.

 Infelizmente o GIL (Global Interpreter Lock do Python) é restritivo quanto ao uso de threads paralelas em Python, porém o módulo `cuncurrent.futures` permite que possámos utilizar múltiplos cores. Para isso, este módulo "engana" o GIL criando novos interpretadores como subprocessos do interpretador principal. Desta maneira, cada subprocesso tem seu próprio GIL e, por fim, cada subprocesso tem um ligação com o processo principal, de forma que recebem instruções para realizar operações e retornar resultados.

 Agora que já vimos um pouco de teoria vamos colocar em prática o uso do `concurrent.futures`. Vamos supor que tenhámos um lista de preços e que queremos aumentar em 10% o valor de cada item.
 
 Vamos então criar uma função que gere uma lista de preços:

```python
def generate_list():
    result = []
    for i in range(0, 20):
        result.append(pow(i, 2) * 42)

    return result
```

Agora vamos criar uma função que calcule o preço acrescido de 10%.

```python
def increase_price_by_10_percent(price):
    price += price / 10 * 100
    return price
```

Dando continuidade, definiremos mais três funções.

```python
def increase_price_serial(price_list, increase_function):
    start = datetime.now()
    result = list(map(increase_function, price_list))
    end = datetime.now()
    print("Took {}s to increase the values".format((end - start).total_seconds()))

def increase_price_with_threads(price_list, increase_function):
    start = datetime.now()
    pool = ThreadPoolExecutor(max_workers=2)
    results = list(pool.map(increase_function, price_list))
    end = datetime.now()
    print("Took {}s to increase the prices with python Threads".format((end - start).total_seconds()))

def increase_price_with_subprocess(price_list, increase_function):
    start = datetime.now()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(increase_function, price_list))
    end = datetime.now()
    print("Took {} to increase the prices with sub proccess".format((end - start).total_seconds()))
```

Note que as funções `increase_price_serial`, `increase_price_with_threads` e `increase_price_with_subprocess` são bem semelhantes, todas tem dois parâmetros:

 - o `price_list`, que é a lista de preços onde iremos fazer as operações ;
  - e o `increase_function` que é função que realizará as operações de acréscimo em cada item da lista.
 
 A diferença entre estas funções está na forma em que as operações de acréscimo serão executadas conforme explicarei a seguir:

- `increase_price_serial`: aqui a função passada pelo parâmetro `increase_function` será executada  para cada item da `price_list` de forma sequencial.
- `increase_price_with_threads`: aqui já começamos a fazer uso da classe `ThreadPoolExecutor`, que pertencente a lib `concurrent.futures`, e que vai nos permitir executar a `increase_function` de forma concorrente. Note que ao instanciar `ThreadPoolExecutor` estamos passando o parâmetro `max_workers=2`, isto está indicando o numero máximo de threads que será usado para executar as operações.
- `increase_price_with_subprocess`: nesta função estamos fazendo uso da classe `ProcessPoolExecutor` que tem a funionalidade bastante semelhante à classe `ThreadPoolExecutor` exceto pelo fato de que esta classe permite que a função `increase_function()` seja executada realmente de forma paralela. Essa "mágica" é conseguida da seguinte forma:
    1. Cada item da lista de preços é serializado através do `pickle`;
    2. Os dados serializados são copiados do processo principal para os processos filhos por meio de um socket local;
    3. Aqui o `pickle` entra em cena novamente para deserializar os dados para os subprocessos;
    4. Os subprocessos importam o módulo Python que contém a função que será utilizada; no nosso caso, será importado o módulo onde `increase_function` está localizada;
    5. As funções são executadas de forma paralela em cada subprocesso;
    6. O resultado destas funções é serializado e copiado de volta para o processo principal via socket;
    6. Os resultados são desserializados e mesclados em uma lista para que possam ser retornados;

 Nota-se que a classe `ProcessPoolExecutor` faz muitos "malabarismos" para que o paralelismo seja realmente possível.
 
### Os resultados

Na minha máquina, que tem mais de um core, executei o seguinte código:

```python
    prices = generate_list()
    increase_price_serial(prices, increase_price_by_10_percent)
    increase_price_with_threads(prices, increase_price_by_10_percent)
    increase_price_with_subprocess(prices, increase_price_by_10_percent)
```

Trazendo os seguintes resultados:

|Função                           |#|Execução            |#|Tempo gasto          |
|:--------------------------------|#|:------------------:|#|--------------------:|
| `increase_price_serial`         |#|Sequencial          |#|  2.2e-05 secs       |
| `increase_price_with_threads`   |#|Concorrente         |#|    0.001646 secs    |
| `increase_price_with_subprocess` |#|Paralela            |#|  0.016269  secs     |

Veja que `increase_price_with_subproces`, mesmo sendo executada paralelamente, levou mais tempo que `increase_price_serial`. Isso ocorreu pois a função `increase_price_by_10_percent`, que é utilizada para fazer operações  nos itens da lista, é uma função que não exige muito trabalho do processador. Desta forma, o  `ProcessPoolExecutor` leva mais tempo fazendo o processo de paralelização propriamente dito do que realmente executando as operações de cálculo.

Vamos criar neste momento uma função que realize operações mais complexas:

```python
def increase_price_crazy(price):
    price += price / 10 * 100
    new_prices = []
    for i in range(0, 200000):
        new_prices.append(price + pow(price, 2))
    new_prices = map(sqrt, new_prices)
    new_prices = map(sqrt, new_prices)

    return max(price, min(new_prices))
```
> **Nota:** Está função  foi criada apenas para  efeitos didáticos. 

Vamos agora ulilizar esta função no lugar da função `increase_price_by_10_percent`:

```python
    increase_price_serial(prices, increase_price_crazy)
    increase_price_with_threads(prices, increase_price_crazy)
    increase_price_with_subprocess(prices, increase_price_crazy)
``` 

Obtendo o reultado abaixo:

|Função                           |#|Execução            |#|Tempo gasto          |
|:--------------------------------|#|:------------------:|#|--------------------:|
| `increase_price_serial`         |#|Sequencial          |#|  4.10181 secs       |
| `increase_price_with_threads`   |#|Concorrente         |#|  4.566346 secs      |
| `increase_price_with_subprocess` |#|Paralela            |#|  2.082025 secs      |

> **Nota:** os valores de tempo gasto vão variar de acordo com o hardware disponível.

Veja que agora função `increase_price_with_subprocess` foi a mais rápida. Isto se deve o fato de que a nossa nova função ne cálculo `increase_price_crazy` demanda muito mais processamento , assim, o overhead para que se paralelize as operações tem um custo inferior ao custo de processamento das operações de cálculo.

## Conclusão

Podemos concluir que é possível executar operações paralelas em python utilizando `ProcessPoolExecutor`, porém paralelizar nem sempre vai garantir que determinada operação vai ser  mais performática. Temos sempre que avaliar a situação que temos em mãos.

Espero que este post tenha contribuído de alguma forma com conhecimento de vocês, sugestões e criticas serão bem vindas, obrigado!.

> **Disclaimer:** Existem varios conceitos  como, locks, deadlocks, futures, data races e etc. que não foram abordados aqui para que o post não ficasse muito longo e complexo.
A Versão do python utilizada foi a 3.5, a lib `concurrent.futures` está dispónivel desde a versão 3.2 do Python, no entanto, exite um backport para a versão 2.7  que é facilmente instalável via 'pip install futures'.





O código completo pode ser encontrado [aqui](https://github.com/cordjr/concurrent.futtures.sample/blob/master/main.py).











