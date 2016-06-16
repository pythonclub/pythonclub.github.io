Title: Python webassets & Elm
Date: 2016-06-14 17:25
Tags: elm, webassets, flask, django
Category: Webassets
Slug: python-webassets-elm
Author: Eduardo Cuducos
About_author: Sociólogo, geek, cozinheiro e fã de esportes.
Email:  cuducos@gmail.com
Github: cuducos
Site: http://cuducos.me
Twitter: cuducos
Linkedin: cuducos

Se você é geek e me conhece, ou se me segue nas redes sociais, já ouviu eu falar de [Elm](http://elm-lang.org/). É uma solução para _front-end_ com componentes reativos — mas Elm não é JavaScript. É uma outra linguagem, outro ambiente, outro compilador etc.

É uma linguagem que muito me impressionou. Sou novato, engatinhando, tentando levantar e tomando belos tombos. Mas hoje resolvi um desses tombos: como integrar o Elm que uso para _front-end_ com _back-ends_ em Python.

A resposta foi o [webassets-elm](https://github.com/cuducos/webassets-elm) — pacote que escrevi hoje e já está [disponível no PyPI](https://pypi.python.org/pypi/webassets-elm).

Nesse texto vou fazer uma pequena introdução sobre interfaces reativas, sobre Elm em si, e depois explico um pouco do problema que o [webassets-elm](https://github.com/cuducos/webassets-elm) resolve — spoiler: é gambiarra.

## O que é um _front-end_ com componente reativo?

Componentes reativos são elementos na interface do usuário que seguem a [programação reativa](https://en.wikipedia.org/wiki/Reactive_programming): “um paradigma de programação orientado ao fluxo de dados e a propagação de mudanças” — como a Wikipédia define.

Mas o que isso quer dizer? Comecemos com um exemplo básico **não** reativo:

```python
a = 40
b = 2
c = a + b
print(c)  # 42

a = 11
print(c) # 42
```
Se esse bloco fosse reativo, ao mudar o valor de `a`, a alteração deveria também mudar o valor de `c` — ou seja, o segundo `print(c)` deveria resultar em `13`, não em `42`.

Isso é muito útil quando gerenciamos interfaces complexas no _front-end_: ao invés de gerenciarmos vários `div`, `span` com suas classes e conteúdos, definimos uma estrutura de dados e as _regras_ para renderização desses dados em HTML. Alterando os dados, o HTML é atualizado automaticamente.

Isso seria uma carroça de lerdeza se tivéssemos que atualizar o [DOM](https://pt.wikipedia.org/wiki/Modelo_de_Objeto_de_Documentos) cada vez que nossos dados fossem alterados — afinal [não é o JavaScript que é lento, o DOM é que é](https://www.youtube.com/watch?v=hQVTIJBZook). Por isso mesmo todos as alternativas para _front-end_ reativo — [Elm](http://elm-lang.org/), [React](https://facebook.github.io/react/), [Vue](https://vuejs.org/) e muitas outras — trabalham com um DOM virtual: todas as alterações são feitas primeiro nesse (eficiente) DOM virtual, que é comparado com o DOM real e então apenas as alterações mínimas são feitas no (lento) DOM real para que a interface seja atualizada. Simples assim.

## Por quê Elm?

Mas por quê Elm? Se praticamente a única linguagem que roda em navegador é JavaScript, que sentido faz aprender Elm? Elm é mais fácil que JavaScript? Essas são perguntas com as quais me habituei. Então vou falar aqui em linhas gerais o que normalmente respondo.

Não posso negar que JavaScript é mais fácil de aprender — no sentido de que a curva de aprendizado é bem menor. Só que daí até escrever JavaScript de qualidade tem um abismo de distância (alô, _[technical debt](https://medium.com/@joaomilho/festina-lente-e29070811b84#.80xxnrf4f)_).

O que eu gostei no Elm é que, apesar de a curva de aprendizado ser muito maior que a do JavaScript, a linguagem já te força a escrever código com certa qualidade. Por exemplo:

* **Interface reativa de acordo com “melhores práticas”**: pensar na arquitetura do código é totalmente opcional no JavaScript, mas escrever algo com qualidade vai requerer que você aprenda JavaScript (sem [jQuery](http://jquery.com)), como usar [JavaScript de forma funcional](https://www.youtube.com/playlist?list=PL0zVEGEvSaeEd9hlmCXrk5yUyqUag-n84), [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise), [React](https://facebook.github.io/react/), [Redux](http://redux.js.org) ou ainda [Vue](https://vuejs.org/), para dar alguns exemplos. Então, se juntar a curva de aprendizado de todas coisas, vai ser uma curva de aprendizado parecida com a do próprio Elm (que já é funcional pois é um [Heskell](https://www.haskell.org) simplificado, já tem [sua própria arquitetura](http://guide.elm-lang.org/architecture/index.html) etc.)
* **Erros**: Com JavaScript (incluindo jQuery, ReactJs, Vue etc.) pode acontecer de passar erros para a produção ou homologação — um caso raro no qual uma função espere `x`, mas receba `y`, um loop infinito, uma função ou variável não definida, um objeto não encontrado. Com Elm, não: o compilador já elimina trocentos mil possibilidades de erro na compilação (como dizem na home do Elm, no _runtime exceptions_). Isso porquê o Elm já trabalha com tipagem e com objetos imutáveis, e consegue verificar possibilidades que o cérebro humano demoraria para imaginar. Se tem alguma possibilidade de teu código receber `String` quando espera `Integer`, ou de cair em um `import` cíclico, ele não compila se você não corrigir. Ele é chato, mas não deixa passar erro.
* **Mensagens de erro**: Se o Elm é chato por não compilar se houver possibilidade de erro, suas mensagens não são nada chatas. Na minha opinião uma das coisas mais chatas de desenvolver com JavaScript é que a console é muito ruim: as mensagens são vagas, é o terror do `undefined is not a function`, `NaN` etc. Já as mensagens de erro do compilador do Elm são muito educativas, te mostram o que está errado, onde está errado e, muitas vezes, como resolver.

![Compiler errors for humans](http://elm-lang.org/assets/blog/error-messages/0.15.1/naming.png)

Por fim, o JavaScript é muito verboso. Muito. Elm é mais conciso. Sem contar que ninguém vai se perder tentando descobrir se tem que fechar o parênteses antes das chaves, ou depois do ponto-e-vírgula.

Enfim, se se interessam por Elm, além dos links que coloquei no texto, sugiro mais esses (todos em inglês):

* [Elm em 7 minutos](https://egghead.io/lessons/elm-elm-in-5-minutes)
* [Por quê Elm — parte 1](http://ohanhi.github.io/master-elm-1-why-elm.html)
* [Introdução ao Elm](https://youtu.be/3_M2G9U51GA)

## Webassets & webassets-elm

Para quem não conhece, o [webassets](http://webassets.readthedocs.io/) é pacote muito utilizado no mundo Python para compilar, dar um _minify_ e comprimir CSS, JS etc. Por exemplo ele tem filtros que transfromam o todos os [SASS](http://sass-lang.com) em CSS e, depois, junta tudo em um único `.css` bem compacto.

A integração com [Flask](http://flask.pocoo.org) ou [Django](http://djangoproject.com) é super fácil e útil com o [flask-assets](http://flask-assets.readthedocs.io/) ou [django-assets](http://django-assets.readthedocs.org/). Com isso sua própria aplicação gera, no servidor, seus _assets_. Em ambiente de desenvolvimento e produção a geração dos _assets_ passa a ocorrer automaticamente (sem necessidade de _watchers_ ou de rodar manualmente `sass`, `coffee`, `browserify`, `webpack`, `grunt`, `gulp` etc.).


O [webassets-elm](https://github.com/cuducos/webassets-elm) nada mais é, então, do que um filtro para o _webassets_ saber o que fazer com arquivos `.elm` — ou seja para transformar meus arquivos em Elm em `.js` para o navegador saber o que fazer com eles (isso é o que chamamos de _compilar_ no Elm). Parece simples, e a arquitetura do _webassets_ ajuda muito: eles mesmos oferecem um objeto [`ExternalTool`](https://github.com/miracle2k/webassets/blob/master/src/webassets/filter/__init__.py#L400-L456) para facilitar a criação de filtros personalizados.


O que quero é que na hora que eu rodar minha aplicação em Flask ou em Django, se eu tiver alterado qualquer arquivo `.elm` (ou `.sass`), por exemplo, automaticamente a aplicação já gere um `.js` (ou `.css`) atualizado.

O problema é que toda a arquitetura do _webassets_ é pensada tendo o [`stdout`](https://en.wikipedia.org/wiki/Standard_streams#Standard_output_.28stdout.29) como padrão. E o `elm-make` (comando que compila os arquivos Elm) [só grava em arquivo, não joga o resultado para o `stdout`](https://github.com/elm-lang/elm-make/issues/39). 

Faz sentido o _webassets_ ser assim: muitas vezes o que interessa é só o resultado das compilações, já que esses resultados podem ser processados novamente (um _minify_, por exemplo) antes de se juntar a outros resultados para, finalmente, salvar um asset `.css` ou `.js`.

Então, a única complicação no _webassets-elm_ é essa — aí mora a famosa _gambiarra_, o famoso _jeitinho brasileiro_ enquanto o `elm-make` não oferece uma forma de compilar para o `stdout`.

### Estrutura de um filtro do _webassets_

Normalmente um [filtro para o _webassets_ é simples](https://webassets.readthedocs.io/en/latest/custom_filters.html), veja esse exemplo (simplificado) de [um filtro para utilizar o Browserify](https://github.com/renstrom/webassets-browserify/blob/master/webassets_browserify/__init__.py).

```python
class Browserify(ExternalTool):

    name = 'browserify'

    def input(self, infile, outfile, **kwargs):
        args = [self.binary or 'browserify']
        args.append(kwargs['source_path'])
        self.subprocess(args, outfile, infile)
```

Basicamente dentro de `input(…)`, que recebe o arquivo de entrada (`infile`) e o arquivo de saída (`outfile`), definimos qual o binário a ser chamado (`browserify`, por padrão, no exemplo) e adicionamos os argumentos que queremos passar para o binário (`kwargs['source_path']`). Tudo muito parecido com o [`subprocess` nativo do Python](https://docs.python.org/3.5/library/subprocess.html).

Em outras palavras, se o `source_path` for `/home/johndoe/42.sass`, é como se digitássemos `browserify /home/johndoe/42.sass` no terminal e o _webassets_ juntaria o resultado desse comando no arquivo final (`outfile`).

### Estrutura do _webassets-elm_

Mas o `elm-make` não funciona assim. Ele gera uma arquivo. Se chamarmos `elm-make hello.elm` ele gera um `index.html` (com o JavaScript compilado dentro). Podemos gerar apenas um JavaScript usando o argumento `--output`. Por exemplo, podemos usar `elm-make hello.elm --output hello.js` e teríamos apenas o JavaScript compilado no arquivo `hello.js`.

Por esse motivo o _webassets-elm_ precisou de [uma gambiarra](https://github.com/cuducos/webassets-elm/blob/master/webassets_elm/__init__.py#L25-L43). Primeiro ele chama o `elm-make` gravando um arquivo temporário:

```python
tmp = mkstemp(suffix='.js')
elm_make = self.binary or 'elm-make'
write_args = [elm_make, kw['source_path'], '--output', tmp[1], '--yes']
with TemporaryFile(mode='w') as fake_write_obj:
    self.subprocess(write_args, fake_write_obj)
```
            
Depois usa o `cat` (ou `type`, no Windows) para jogar o conteúdo desse arquivo temporário para o `stdout`:

```python
cat_or_type = 'type' if platform == 'win32' else 'cat'
read_args = [cat_or_type, tmp[1]]
self.subprocess(read_args, out)
```

Não sei se é a melhor solução, mas foi o que resolveu por enquanto. Qualquer palpite, crítica, _pull request_, [RT](https://twitter.com/cuducos/status/742698891343204353), estrelinha no GitHub, _issue_, contribuição é bem-vinda ; )