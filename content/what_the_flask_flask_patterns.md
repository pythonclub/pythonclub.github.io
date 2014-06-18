Title: What the Flask? Pt-2 Flask Patterns - boas práticas na estrutura de aplicações Flask
Slug: what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask
Date: 2014-06-15 02:22
Tags: flask,web,tutorial,what-the-flask
Author: Bruno Cezar Rocha
Email:  rochacbruno@gmail.com
Github: rochacbruno
Bitbucket: rochacbruno
Site: http://brunorocha.org
Twitter: rochacbruno
Linkedin: rochacbruno
Gittip: rochacbruno
Category: Flask



What The Flask - 2/6
-----------

> **CONTEXT PLEASE:** Esta é a segunda parte da série **What The Flask**, 6 artigos para se tornar um **Flasker** (não, não é um cowboy que carrega sua garrafinha de whisky para todo lado). A primeira parte está aqui no [PythonClub](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python) e o app está no [github](https://github.com/rochacbruno/wtf/tree/pt-1).

<figure style="float:left;margin-right:30px;">
<img src="/images/rochacbruno/cowboy_flask.jpg" alt="a flasker" style="width:90%">
<figcaption>Professional Flask Developer</figcaption>
</figure>

1. [**Hello Flask**](/what_the_flask_introducao_ao_desenvolvimento_web_com_python.html): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask): Estruturando de aplicações Flask - **<-- Você está aqui**
3. **Plug & Use**: extensões essenciais para iniciar seu projeto
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask e para o Jinja2
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.

> **Você sabia?** Flask quer dizer "Frasco/Frasqueira", ou seja, aquela garrafinha ali da foto acima que geralmente os cowboys, os Irlandeses, o John Wayne, os bebados profissionais e os hipsters gostam de utilizar para tomar desde vodka, whisky, vinho e até suco de caju (no caso dos [hipsters](http://www.cafepress.com/+hipster+flasks)). Bom você pode estar se perguntando: Por que colocar esse nome em um framework? Antes do Flask já existia o Bottle "garrafa" que surgiu com a idéia revolucionária de ser um framework de um [arquivo só](https://github.com/defnull/bottle/blob/master/bottle.py). Como o criador do Flask é meio contrário a esta idéia de colocar um monte de código Python em um único arquivo ele decidiu ironizar e fazer uma piada de 1 de abril e então criou um framework chamado [Denied](http://denied.immersedcode.org/) que era uma piada ironizando o Bottle e outros micro frameworks, mas as pessoas levaram a sério e gostaram do [estilo do denied!](http://denied.immersedcode.org/screencast.mp4) A partir disso ele decidiu pegar as boas idéias tanto do Bottle como do Denied e criar algo sério e então surgiu o Flask. O nome vem da idéia de que **Bottle**/Garrafa é para tomar de goladas, mas **Flask**/Frasco você toma **uma gota por vez**, desta forma você aprecia melhor a bebida e até hoje o slogan do Flask é " Development one drop at time".

# Flask Patterns
### Parte 2 - Boas práticas na estrutura de aplicações Flask

> **NOTE:** As dicas deste artigo são baseadas nesta parte da [documentação oficial do flask](http://flask.pocoo.org/docs/patterns/) com algumas adaptações levando em consideração a experiência que já tive na organização de apps Flask. Isso não quer dizer que esse é o único jeito de desenvolver em Flask, nem que é o melhor, lembre-se, o Flask é micro e te dá a liberdade para organizar as coisas como você bem entender, mas como eu já quebrei a cabeça resolvendo um monte de pequenos problemas vou compartilhar a receita que tem dado certo para mim.

- [One file to rule them all?](#one_file_is_bad_if_you_are_big)
- [O problema do Ovo e da Galinha](#circular_imports)
- [Azul da cor do mar ♫](#blueprints)
- [A fantástica fábrica de web apps](#app_factory)
- [Você pode ter mais de um app](#multiple_apps)
- [Configurações para todo lado](#config)
- [Logando e debugando](#log)
- [Testing](#testing)

## <a href="#one_file_is_bad_if_you_are_big" name="one_file_is_bad_if_you_are_big">One file to rule them all?</a>

O exemplo mais básico de um projeto Flask é um one-file application, e normalmente você pode começar dessa maneira mas se eu projeto começar a crescer