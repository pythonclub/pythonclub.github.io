---
title: Raspando a Web com Python: Introdução
slug: raspando-a-web-com-python-parte-1
summary: É possível usar Python puro para processar XML e calcular os gastos da copa! Primeiro post numa série sobre raspagem de dados com Python, LXML e Scrapy (y otras cositas más).
date: 2015-07-08 12:40 -0300
author: Capi Etheriel
about_author: Capi Etheriel é membro da rede Transparência Hacker e adora trabalhar com Web Scraping.
site: https://barraponto.blog.br
email:  barraponto@gmail.com
github: barraponto
twitter: barraponto
category: Python
tags: python,blog,scraping
---

Todo projeto que deseja raspar dados da web se resume ao seguinte *loop*:

1. Fazer uma requisição para uma URL;
2. Processar a resposta (HTML, XML ou JSON);
3. Extrair os dados;
4. Deduzir as próximas URLs a visitar;
5. Repetir o loop.

A parte mais difícil aqui é processar o HTML. É um processo todo delicado, o
HTML é cheio de detalhes para tolerar tags que não fecham, símbolos largados
nos lugares errados e por aí vai. Por isso é difícil ter um *parser*
(processador) de HTML nas bibliotecas-padrão de qualquer linguagem, seja
Python, Ruby, Javascript ou PHP. Já XML e JSON são formatos muito mais estritos
e tem parsers nativos em qualquer linguagem.

Vamos ver como pegar os gastos da Copa do Mundo 2014, [expostos em
XML](http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento).
Alguns browsers vão exibir o XML como uma árvore, facilitando a visualização da
estrutura -- meu browser favorito, o
[Firefox](https://www.mozilla.org/firefox/), faz isso.

Nesse XML você pode ver um elemento maior, o `collection`, com muitos elementos
`copa:empreendimento` dentro. Esse prefixo `copa:` corresponde a um
*namespace*, um recurso do XML para poder misturar elementos de vocabulários
distintos. É importante prestar atenção nisso para podermos informar o nosso
parser de XML.

Para começar o loop, vamos carregar a URL e popular uma árvore de elementos --
uma abstração do Python para podermos manipular mais facilmente esses dados:

```python
from xml.etree import ElementTree
from urllib.request import urlopen

data_url = "http://www.portaltransparencia.gov.br/copa2014/api/rest/empreendimento"

with urlopen(data_url) as datafile:
    data = ElementTree.parse(datafile)
```

Repare como carregar uma URL no Python 3 tem uma sintaxe confortável, idêntica
à sintaxe de abrir arquivos. Agora pra seguir o loop, vamos extrair o que nos
interessa: o gasto (`valorTotalPrevisto`) de cada empreendimento iniciado ou
concluído (cujo `andamento` não esteja no estado `1`, `Não iniciado`).

```python
spending = [float(element.find('./valorTotalPrevisto').text)
            for element in data.iterfind('.//copa:empreendimento',
                                         namespaces={'copa': data_url[:46]})
            if element.find('./andamento/id').text != '1']
```

Pegar elementos de um `ElementTree` é fácil usando o método `iterfind` (retorna
um iterável, pra usar com for) ou `findall` (retorna uma lista propriamente
dita). Já pegar o conteúdo de um elemento exige apenas chamar o atributo
`.text`. Fácil, não?

Isso daria certo se os dados fossem consistentes, mas... outro porém! O XML é
estrito -- as tags fecham, os símbolos estão no lugar certo, está tudo certo,
mas **os dados em si não são consistentes**. Nem todo elemento
`copa:empreendimento` tem um elemento `valorTotalPrevisto` dentro. E agora?

É simples: vamos encapsular o processamento desse valor em um método simples,
que retorna zero quando não existe valor total previsto (pra facilitar a soma,
depois).

```python
def get_cost(element):
    cost = element.find('./valorTotalPrevisto')
    return 0 if (cost is None) else float(cost.text)
```

Agora basta chamar o `get_cost` na nossa compreensão de lista:

```python
spending = [get_cost(element)
            for element in data.iterfind('.//copa:empreendimento',
                                         namespaces={'copa': data_url[:46]})
            if element.find('./andamento/id').text != '1']
```

E aí podemos finalmente somar todos os valores encontrados e imprimir usando o
poderoso método `format` do Python
([estude!](http://python.pro.br/material/cartao-format.pdf)).

```python
print('Foram gastos {total:.2f} dinheiros do governo brasileiro'.format(
    total=sum(spending)))
```

Bônus: Uma versão mais idiomática (PYTHONICA) do código está disponível no meu
[Gist](https://gist.github.com/barraponto/21c705006635a1a72407). Fique à vontade
para contribuir, comentar, melhorar, etc :)

Agradecimentos ao Fernando Masanori que [começou a brincadeira com esses
dados](https://gist.github.com/fmasanori/c648d753e7d0176ff172)!
