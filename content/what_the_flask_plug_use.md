Title: What the Flask? Pt-3 Plug & Use - extensões essenciais para iniciar seu projeto
Slug: what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto
Date: 2015-02-09 00:00
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



What The Flask - 3/6
-----------

> Finalmente!!! A terceira parte da série **What The Flask**, mas ainda não acabou, serão 6 artigos para se tornar um **Flasker**, neste capítulo falaremos sobre como instalar e configurar as principais extensões do Flask para torna-lo uma solução full-stack com bootstrap no front-end, ORM para banco de dados, admin parecido com o Django Admin, Cache, Sistema de filas (celery/huey), Controle de Acesso, Envio de email, API REST e Login Social.

<figure style="float:left;margin-right:30px;width:35%">
<img src="/images/rochacbruno/lego_snake.jpg" alt="snake" >
<figcaption>Extending Flask</figcaption>
</figure>

1. [**Hello Flask**](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python): Introdução ao desenvolvimento web com Flask
2. [**Flask patterns**](/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask): Estruturando aplicações Flask
3. [**Plug & Use**](/what-the-flask-pt-3-plug-use-extensoes-essenciais-para-iniciar-seu-projeto): extensões essenciais para iniciar seu projeto. **<-- Você está aqui**
4. **DRY**: Criando aplicativos reusáveis com Blueprints
5. **from flask.ext import magic**: Criando extensões para o Flask e para o Jinja2
6. **Run Flask Run**: "deploiando" seu app nos principais web servers e na nuvem.

<br>

> **Micro framework?** Bom, o Flask foi criado com a premissa de ser um micro-framework, o que significa que ele não tem a intenção de entregar de bandeja para você todas as coisas que você precisa em único pacotinho e nem comandos mágicos que você roda e instantaneamente tem todo o seu projeto pronto. A idéia do Flask é ser pequeno e te dar o controle de tudo o que acontece no seu aplicativo, mas ao mesmo tempo o Flask se preocupa em ser facilmente extensivel, para isso os desenvolvedores pensaram em padrões que permitem que as extensões sejam instaladas de modo que não haja conflitos (lembra dos BluePrints do capítulo anterior?), além dos BluePrints tem também os patterns para desenvolvimento de extensions que ajuda a tornar a nossa vida mais fácil, nesta parte dessa série vamos instalar e configurar algumas das principais extensões do Flask (todas testadas por mim em projetos reais).


# CMS de notícias

Nesta série estamos desenvolvendo um mini CMS para publicação de notícias, o código está disponível no [github](http://github.com/rochacbruno/wtf) e para cada fase da evolução do projeto tem uma branch diferente. Esse aplicativo de notícias tem os seguintes requisitos:

- Controle de acesso para que apenas editores autorizados publiquem notícias
- Interface administrativa para notícias, categorias, tags, media e usuários
- Front end usando o Bootstrap
- Cache das notícias para minimizar o acesso ao banco de dados
- Banco de dados MongoDB
- Sistema de comentários nas noticias com a possibilidade de login social (Oauth)
- Envio de email para o autor a cada novo comentário (sistema de envio assincrono em uma fila Celery)
- Publicação de notícia em HTML, Feed Atom
- API REST para consulta e publicação de notícias (para app mobile)

# Quais extensões usaremos?

> **NOTE:** Existem várias extensões para Flask, algumas são aprovadas pelos desenvolvedores e entram para a lista disponível no site oficial, algumas entram para a listagem do metaflask (projeto em desenvolvimento), e uma grande parte está apenas no github. Como existem várias extensões que fazem a mesma coisa, as vezes é dificil escolher qual delas utilizar, eu irei mostrar aqui apenas as que eu utilizo e que já tenho experiência, mas isso não quer dizer que sejam as melhores, sinta-se a vontade para tentar com outras e incluir sua sugestão nos comentários.

- [Flask Bootstrap](#bootstrap) - Para deixar as coisas bonitinhas
- [Flask MongoEngine](#mongoengine) - Para armazenar os dados em um banco que é fácil fácil!
- [Flask-Admin](#flask_admin) - Um admin tão poderoso quanto o Django Admin
- [Flask Security](#flask_security) - Controle de acesso
- [Flask Cache](#flask_cache) - Para não estressar o Mongo
- [Flask Email](#flask_email) - Para avisar os autores que tem novo comentário
- [Flask Queue](#flask_queue) - Pare enviar o email assincronamente e não bloquear o request
- [Flask Classy](#flask_classy) - Um jeito fácil de criar API REST e Views 
- [Flask Oauth e OauthLib](#flask_oauth) - Login com o Feicibuque e tuinter

> **TL;DR:** A versão final do app deste artigo esta no [github](https://github.com/rochacbruno/wtf/tree/extended), os apressados podem querer executar o app e explorar o seu código antes de ler o artigo completo.

## <a href="#bootstrap" name="bootstrap">Deixando as coisas bonitinhas com o Bootstrap!</a>

Atualmente a versão do nosso CMS está funcional porém bem feinha, não trabalhamos no design das páginas pois obviamente este não é o nosso objetivo, mas mesmo assim podemos deixar as coisas mais bonitinhas.

<figure style="border:1px solid black;">
<img src="/images/rochacbruno/wtf_index.png" alt="wtf_index" >
<figcaption>Atual Layout do nosso CMS</figcaption>
</figure>

Com a ajuda do Bootstrap e apenas uns ajustes básicos no front end podemos transformar o layout em algo muito mais apresentável.









> A versão final do app está no [github](https://github.com/rochacbruno/wtf/tree/almost_perfect)

Nesta versão é possivel executar os tests com ``nosetests tests/`` na raiz do projeto! **escreva mais testes!**

Também temos o **multiple_run** que utiliza o DispatcherMiddleware para juntar dois apps, experimente executar ``python multiple_run.py`` e você verá que o app de noticias será servido no "/" mas se acessar "/another" estará acessando a outra app contida no arquivo "wtf/another_app.py".

Nos próximos capítulos iremos evoluir este app para o uso de algumas extensões essenciais, uncluiremos controle de login, cache, interface de administração, suporte a html e markdown nas noticias e outras coisas.

> **END:** Sim chegamos ao fim desta segunda parte da série **W**hat **T**he **F**lask. Eu espero que você tenha aproveitado as dicas aqui mencionadas. Nas próximas 4 partes iremos nos aprofundar no uso e desenvolvimento de extensões e blueprints e também questṍes relacionados a deploy de aplicativos Flask. Acompanhe o PythonClub, o meu [site](http://brunorocha.org) e meu [twitter](http://twitter.com/rochacbruno) para ficar sabendo quando a próxima parte for publicada.

<hr />

> **PUBLICIDADE:** Estou iniciando um curso online de Python e Flask, para iniciantes abordando com muito mais detalhes e exemplos práticos os temas desta série de artigos e muitas outras coisas envolvendo Python e Flask, o curso será oferecido no CursoDePython.com.br, ainda não tenho detalhes especificos sobre o valor do curso, mas garanto que será um preço justo e acessível. Caso você tenha interesse por favor preencha este [formulário](https://docs.google.com/forms/d/1qWx4pzNVSPQmxsLgYBjTve6b_gGKfKLMSkPebvpMJwg/viewform?usp=send_form) pois dependendo da quantidade de pessoas interessadas o curso sairá mais rapidamente.

<hr />

> **PUBLICIDADE 2:** Também estou escrevendo um livro de receitas **Flask CookBook** através da plataforma LeanPub, caso tenha interesse por favor preenche o formulário na [página do livro](https://leanpub.com/pythoneflask)


Muito obrigado e aguardo seu feedback com dúvidas, sugestões, correções etc na caixa de comentários abaixo.

Abraço! "Python é vida!"

