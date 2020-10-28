Title: Fazendo backup do banco de dados no Django
Date: 2020-10-27 22:19
Tags: Python,Django,backup
Category: Python
Slug: fazendo-backup-do-banco-de-dados-no-django
Author: Jackson Osvaldo
Email:  jacksonosvaldo@live.com
Github: JacksonOsvaldo
About_author: Um curioso apaixonado por livros, tecnologia e programação.

## Apresentação

Em algum momento, durante o seu processo de desenvolvimento com Django, pode ser que surja a necessidade de criar e restaurar o banco de dados da aplicação. Pensando nisso, resolvi fazer um pequeno tutorial, básico, de como realizar essa operação.

Nesse tutorial, usaremos o [django-dbbackup](https://github.com/django-dbbackup/django-dbbackup), um pacote desenvolvido especificamente para isso.

## Configurando nosso ambiente

Primeiro, partindo do início, vamos criar uma pasta para o nosso projeto e, nela, isolar o nosso ambiente de desenvolvimento usando uma [virtualenv](https://virtualenv.pypa.io/en/latest/index.html):

```shell
mkdir projeto_db && cd projeto_db #criando a pasta do nosso projeto

virtualenv -p python3.8 env && source env/bin/activate #criando e ativando a nossa virtualenv
```

Depois disso e com o nosso ambiente já ativo, vamos realizar os seguintes procedimentos:

```shell
pip install -U pip #com isso, atualizamos a verão do pip instalado
```

## Instalando as dependências

Agora, vamos instalar o [Django](https://www.djangoproject.com/) e o pacote que usaremos para fazer nossos backups.

```shell
pip install Django==3.1.2 #instalando o Django

pip install django-dbbackup #instalando o django-dbbackup
```

## Criando e configurando projeto

Depois de instaladas nossas dependências, vamos criar o nosso projeto e configurar o nosso pacote nas configurações do Django.

```shell
django-admin startproject django_db . #dentro da nossa pasta projeto_db, criamos um projeto Django com o nome de django_db.
```

Depois de criado nosso projeto, vamos criar e popular o nosso banco de dados.

```shell
python manage.py migrate #com isso, sincronizamos o estado do banco de dados com o conjunto atual de modelos e migrações.
```

Criado nosso banco de dados, vamos criar um superusuário para podemos o painel admin do nosso projeto.

```shell
python manage.py createsuperuser
```

Perfeito. Já temos tudo que precisamos para executar nosso projeto. Para execução dele, é só fazermos:

```shell
python manage.py runserver
```

Você terá uma imagem assim do seu projeto:

![](https://jacksonosvaldo.github.io/img/django_db.png)

## Configurando o django-dbbackup

Dentro do seu projeto, vamos acessar o arquivo settings.py, como expresso abaixo:

```shell
django_db/
├── settings.py
```

Dentro desse arquivos iremos, primeiro, adiconar o django-dbbackup às apps do projeto:

```python
INSTALLED_APPS = (
    ...
    'dbbackup',  # adicionando django-dbbackup
)
```

Depois de adicionado às apps, vamos dizer para o Django o que vamos salvar no backup e, depois, indicar a pasta para onde será encaminhado esse arquivo. Essa inserção deve ou pode ser feita no final do arquivo _settings.py_:

```python
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage' #o que salvar
DBBACKUP_STORAGE_OPTIONS = {'location': 'backups/'} # onde salvar
```

Percebam que dissemos para o Django salvar o backup na pasta _backups_, mas essa pasta ainda não existe no nosso projeto. Por isso, precisamos criá-la [fora da pasta do projeto]:

```shell
mkdir backups
```

## Criando e restaurando nosso backup

Já temos tudo pronto. Agora, vamos criar o nosso primeiro backup:

```shell
python manage.py dbbackup
```

Depois de exetudado, será criado um arquivo -- no nosso exemplo, esse arquivo terá uma extensão .dump --, salvo na pasta _backups_. Esse arquivo contem todo backup do nosso banco de dados.

Para recuperarmos nosso banco, vamos supor que migramos nosso sistema de um servidor antigo para um novo e, por algum motivo, nossa base de dados foi corrompida, inviabilizando seu uso. Ou seja, estamos com o sistema/projeto sem banco de dados -- ou seja, exlua ou mova a a sua base dados .sqlite3 para que esse exemplo seja útil --, mas temos os backups. Com isso, vamos restaurar o banco:

```shell
python manage.py dbrestore
```

Prontinho, restauramos nosso banco de dados. O interessante do django-dbbackup, dentre outras coisas, é que ele gera os backups com datas e horários específicos, facilitando o processo de recuperação das informações mais recentes.

Por hoje é isso, pessoal. Até a próxima. ;) 
