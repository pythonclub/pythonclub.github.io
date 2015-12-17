Title: Workflow com Git flow
Slug: workflow-com-git-flow
Date: 2015-10-27 02:02
Tags: desenvolvimento
Author: André Luiz
Email:  contato@xdvl.info
Github: dvl
Site: http://dvl.rocks/
Twitter: xdvl
Category: Workflow

Esse é um artigo rápido que visa descrever como venho trabalhando com o Git Flow, antes de mais nada o Git Flow é uma forma de gerenciar branchs e tags em repositórios Git originalmente descrita [aqui](http://nvie.com/posts/a-successful-git-branching-model/) e que originou [uma extensão](https://github.com/nvie/gitflow) para o Git pelo mesmo autor.

Partindo do principio que você já possui o ``git-flow`` instalado, na raiz do seu repositório use o comando ``git flow init`` para configurar o git flow no seu repositório atual, serão feitas algumas perguntas para as quais eu habitualmente uso sempre a opção default.

Git flow instalado, configuração já feita, vamos a um *how to* de como agir no dia-a-dia.

##### Quero iniciar o desenvolvimento de uma nova feature

```
$ git flow feature start nome-da-feature
```

O comando acima iria criar uma nova branch chamada ``feature/nome-da-feature`` partindo do conteúdo atual da branch ``develop``, a partir daqui você deve realizar todo seu trabalho nessa branch que acabou de ser criada.

##### Quero publicar minha feature para outra pessoa mexer ou continuar de outro computador.

Antes de mais nada faça commit de todas sua alterações como de costume e então execute o comando abaixo:

```
$ git flow feature publish nome-da-feature
```

Esse comando simplesmente ira fazer um ``git push`` para o servidor remoto criando a branch caso não exista.

Então a outra pessoa (ou você mesmo de outro computador) deverá usar o comando abaixo.

```
$ git flow feature pull nome-da-feature
```

##### Terminei minha feature e agora?

Depois de commitar todas sua alterações use o comando:

```
$ git flow feature finish nome-da-feature
```

Esse comando ira executar um merge da sua feature na branch ``develop`` e então ira remover a branch ``feature/nome-da-feature`` da sua maquina local e do  servidor remoto (e sim, é esse o comportamento desejado, não queremos 200 branchs defasadas depois de alguns meses de projeto e queremos poder eventualmente reutilizar o nome de alguma feature em uma futura melhoria por exemplo).

##### Ok, já tenho todas as minhas features prontas, mergeadas na develop e agora preciso coloca-las no ar.

Esse é o momento no qual devemos iniciar a criação de um release, para isso utilize o comando

```
$ git flow release start 1.2.0
```

Aonde ``1.2.0`` é o nome do release, a partir desse nome será gerada uma tag ao finalizarmos o release, pode ser usado o nome que você quiser **eu** me habituei em criar release com usando como nome o número da versão que está indo para o ar baseado sempre no [SemVer](http://semver.org/lang/pt-BR/).

O comando acima ira criar uma nova branch partindo da ``develop``, caso você tenha algum ajuste para fazer no seu código essa é a hora.

##### E agora quero validar isso no meu servidor de homologação.

Eu particularmente não gosto de criar uma tag nova cada vez que algo vai ser homologado, então o que faço é o seguinte:

```
$ git flow release publish 1.2.0
```

Para que o release em andamento seja enviado para o servidor remoto, então no meu servidor de homologação eu executo os seguintes comandos:

```
$ git remote update
$ git checkout feature/1.2.0
```

Caso note que algo precise de ajustes os realizo na minha maquina local, faço um novo publish e então no servidor:

```
$ git pull
```

##### Está tudo OK e agora?

```
$ git flow release finish 1.2.0
```

Nesse momento será feito merge do release na ``master`` na ``develop``, tanto as branchs locais quanto remotas usadas pelo release serão deletas, e uma tag com o nome do release será gerada.

Então esse é o momento de enviarmos todas essas alterações para o servidor remoto:

```
$ git checkout master
$ git push origin master

$ git checkout develop
$ git push origin develop

$ git push --tag
```

Com isso finalizamos um release utilizan... espera aí, tem mais.

##### Preciso fazer deploy disso agora!

No seu servidor de produção baixe a tag nova.

```
$ git remote update
```

E então altere sua branch atual para a tag da versão que será feita o deploy

```
$ git checkout 1.2.0
```

Pronto, deploy finalizado.

##### Calma aí, alguma coisa quebrou!!

Nesse momento você deve iniciar um hotfix, o hotfix é bem parecido com o release com o porem que ele sempre parte da ``master``.

```
$ git flow hotfix start 1.2.1
```

Para o hotfix eu utilizo o mesmo principio de nomes do release, no exemplo acima será criada uma branch com o nome ``hotfix/1.2.1`` que pode ser testada em homologação usando a mesma estratégia que mostramos anteriormente para o release.

Para finalizar utilize o comando

```
$ git flow hotfix finish 1.2.1
```

Nesse momento será feito merge na ``master`` e ``develop``, serão apagada as branchs locais e remotas e uma tag com o nome do hotfix será criada, não esqueça de fazer push das branchs e tag, e então você poderá fazer deploy disso da mesma forma que fizemos com o release.

## Dicas

##### Desative o ``fast-forward`` para os merges.

Assim você não perde o tracking dos merges no ``git log``

```
$ git config --global --add merge.ff false
```

##### Por algum motivo bizarro não quero que as branchs aonde as features são desenvolvidas sejam deletas.

Ok... você que manda, utilize para isso a flag ``-k`` no finish

```
$ git flow feature finish -k nome-da-feature
```

##### Instale o utilize o ``gitk`` para entender melhor aonde começa e termina uma branch e evitar se perder.

```
$ sudo apt-get install gitk

$ gitk --all
```
