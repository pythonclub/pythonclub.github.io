Title: Deploy rápido e simples com Dokku
Slug: deploy-rapido-simples-com-dokku
Date: 2016-11-23 17:30
Tags: python,deploy,django,dokku
Author: Júnior Carvalho
Email:  joseadolfojr@gmail.com
Github: juniorcarvalho
twitter: @joseadolfojr
Linkedin: juniorcarvalhorj
Category: Python, Deploy

Sempre busquei alternativas para deploy simples como o heroku. Vou mostrar neste passo-a-passo uma forma simples e rápida utilizando o [Dokku].

[Dokku] é a menor implementação PaaS que você já viu. De uma forma simples e rápida consegue-se configurar um servidor para deploy. Se existe alguma dúvida sobre PaaS, SaaS, etc., uma pesquisa rápida no google vai retornar várias referências.

Nesse exemplo vou utilizar uma vps básica na [DigitalOcean]. Uma máquina 512 MB / 20 Gb/ 1 CPU, rodando Ubuntu Server 16.04.1. É possível criar uma máquina já com [Dokku] instalado e pré-configurado mas vou fazer com uma máquina 'limpa' para servir de base para outras vps.
### Instalando
Com o servidor em execução vamos acessar via ssh pelo terminal. No caso de utilizar OS Windows, utilize o [putty] para acessar o servidor.

```
ssh [ip-do-servidor] -l root
```
No primeiro acesso confirme com yes o questionamento sobre a autenticidade. No caso da [DigitalOcean] vai ser solicitado a mudança de senha nesse primeiro acesso.

Seguindo a documentação do [Dokku] vamos realizar a instação. Este processo demora +- uns 10 minutos.
```
wget https://raw.githubusercontent.com/dokku/dokku/v0.7.2/bootstrap.sh
sudo DOKKU_TAG=v0.7.2 bash bootstrap.sh
```
Finalizado o script de instação vamos adicionar a chave publica de nosso usuário de desenvolvimento para conseguir fazer o deploy no servidor recem criado.
### Chaves
Na nossa máquina de desenvolvimento, vamos checar se nosso usuário tem uma chave pública:
```
ls -al ~/.ssh
```
Por padrão os arquivos das chaves públicas podem ser:

 - id_dsa.pub
 - id_ecdsa.pub
 - id_ed25519.pub
 - id_rsa.pub


No meu caso eu tenho o id_rsa.pub, então vou ler o conteúdo, seleciona-lo e copiar:
```
cat ~/.ssh/id_rsa.pub
```

Para gerar a chave: (caso não exista nenhum arquivo .pub na pasta ~/.ssh)
``` 
ssh-keygen -t rsa
```
Aceite as três opções pedidas por default. (não inserir password)
Para OS Windows achei este artigo. [ssh Windows] (não testei)
### Inserindo a chave pública no servidor
Com nossa chave pública copiada (ctrl+c) vamos abrir o browser e digitar o ip do nosso servidor. Vai aparecer uma tela como a da imagem a seguir:
<figure style="float:center;">
<img src="/images/juniorcarvalho/dokku-setup.jpg">
</figure>
</br>
No campo Public Key, colamos nossa chave (Ctrl+V) e depois é so clicar em Finish Setup. Feito isto você vai ser redirecionado para página da documentação do [Dokku].
### Criando nossa APP
No terminal, conectado no nosso servidor:
```
dokku apps:create [nome-app]
```
No meu caso:
```
dokku apps:create fjfundo
```
Para listar as apps existentes:
```
dokku apps
```
Quando você cria um novo aplicativo, por padrão o [dokku] nao fornece nenhum banco de dados como MySql ou PostgreSQL. É preciso instalar plugins. [Dokku] tem plugins oficiais para banco de dados. Neste passo-a-passo vou utilizar o PostgreSQL.

### Instalando o plugin postgres e configurando o serviço de banco de dados
No terminal, conectado no nosso servidor:
```
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```
Criando o serviço postgres: 

```
dokku postgres:create [nome-servico]
```
No meu caso:
```
dokku postgres:create fjfundo-database
```
Vamos criar o link entre os serviços de banco de dados e nossa app.
```
dokku postgres:link [nome-servico] [nome-app]
```
No meu caso:
```
dokku postgres:link fjfundo-database fjfundo
```

### Configurando e executando nosso primeiro deploy.
Na nossa máquina cliente vamos configurar o git para fazer o primeiro deploy.
Vamos adicionar nosso repositorio remoto dokku da seguinte forma:
```
git remote add dokku dokku@[ip-do-servidor]:[nome-app]
```
No meu caso:
```
git remote add dokku dokku@xxx.xxx.xxx.xxx:fjfundo
```
No meu caso antes de fazer o deploy eu tenho que configurar algumas variáveis de ambiente como DEBUG e SECRET_KEY. Para esta configuração executo os comandos no servidor. Vou seguir a documentação existente em [Environment Variables]
```
dokku config:set fjfundo DEBUG='False'
dokku config:set fjfundo SECRET_KEY='sua secret_key'
```
Para listar as variáveis de ambiente de nossa app:
```
dokku config [nome da app]
```
Feito isto vamos ao nosso primeiro deploy: ( na nossa máquina cliente/dev)
```
git push dokku master --force
```
Pronto! Agora é so acessar nossa aplicação. No final do deploy o [dokku] mostra a url de conexão. Caso precise obter a url use o comando no servidor:
```
dokku url [nome-app]
```
### Criando as tabelas do banco de dados

Nossa app está no ar mais ainda não tem as tabelas de nossa base de dados.
```
dokku run fjfundo python manage.py migrate
```
Troque fjfundo pelo nome da sua app.

### Considerações finais
Ainda estou estudando e aprendendo a utilizar o [dokku]. Utilizo apenas em ambiente de desenvolvimento mas pretendo utilizar em produção. 
Ainda tenho muito que aprender e fica aqui meu email, joseadolfojr@gmail.com, para quem tiver alguma dúvida e quizer também contribuir para meus estudos.


[Dokku]: http://dokku.viewdocs.io/dokku/
[DigitalOcean]: https://m.do.co/c/2f45101e7ccf
[putty]:http://www.putty.org/
[ssh Windows]: http://adrianorosa.com/blog/seguranca/como-criar-ssh-key-pair-windows.html
[Environment Variables]: http://dokku.viewdocs.io/dokku/configuration/environment-variables/