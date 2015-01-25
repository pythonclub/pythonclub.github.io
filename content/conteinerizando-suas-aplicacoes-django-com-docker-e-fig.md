Title: Conteinerizando suas aplicações django com docker e fig
Slug: conteinerizando-suas-aplicacoes-django-com-docker-e-fig
Date: 2015-01-25 13:00
Tags: django, docker, fig
Author: Hudson Brendon
Email:  contato.hudsonbrendon@gmail.com
Github: hudsonbrendon
Twitter: hudsonbrendon
Facebook: hudson.brendon
Category: Django

![Docker](/images/hudsonbrendon/django-fig.png)


Se você como eu é um desenvolvedor incansável quando o assunto é automatizar ao máximo seu workflow de trabalho,este post foi feito para você. O [fig](http://www.fig.sh/) utilizando-se do docker, torna a criação de ambientes de desenvolvimento algo muito simples.


#Instalação

A instalação do fig é bem simples, primeiro você terá que ter o docker instalado em sua máquina, caso não tenha, siga esse [tutorial](http://hudsonbrendon.com/docker-introducao-e-aplicacao.html) onde exemplifico a instalação do mesmo de forma bem simples. Com o docker pronto, é hora de instalar o fig, essa ferramenta é um pacote python, e a forma mais simples de instalá-la é através do pip, que é o gerenciador de pacotes do python, caso não o tenha instalado em sua máquina, acesse o [site oficial](https://pip.pypa.io/en/latest/installing.html) e veja a forma mais simples para você obtê-lo. Com tudo pronto, execute no terminal.

```bash
$ pip install -U fig
```

#Utilizando o fig com django

Com o docker e o fig devidamente instalados em sua máquina, é hora de integrar o django com essa maravilhosa ferramenta, para tanto, criaremos um diretório com um nome qualquer, aqui chamado de "app", e dentro do mesmo criaremos um arquivo chamado "Dockerfile", com o seguinte conteúdo.

```bash
FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
```
Em seguinda criaremos um arquivo chamado "requirements.txt", com os seguintes pacotes.

```bash
Django
psycopg2
```
E por fim um arquivo, "fig.yml", com a configuração abaixo.

```bash
db:
  image: postgres
web:
  build: .
  command: python manage.py runserver 0.0.0.0:8000
  volumes:
    - .:/code
  ports:
    - "8000:8000"
  links:
  - db
```
#Quem é quem no jogo do bicho

Com os arquivos criados é hora de entender qual a função de cada um no workflow.

* **Dockerfile** - É o arquivo que especifica como uma imagem no docker será criada, os pacotes que serão instalados, usuários que serão criados, portas que serão expostas, diretórios que serão compartilhados entre o host e um container, etc. Para mais informações [acesse](http://hudsonbrendon.com/docker-introducao-e-aplicacao.html).

* **requirements.txt** - É um arquivo que guarda todas as dependências de um projeto python.

* **fig.yml** - É o arquivo de configuração do fig, é composto por blocos e cada bloco corresponde a um container, podendo eles serem "linkados", o fig utilizará esse arquivo como base para criar os conteineres necessários, e executar tudo que foi especificado no mesmo.

Com os arquivos finalizados, é hora de criar uma aplicação em django, para isso basta.

```bash
$ fig run web django-admin.py startproject figexample .
```
E o resultado será esse:

```bash
$ ls
Dockerfile       fig.yml          figexample       manage.py        requirements.txt
```
Com a aplicação em mãos, a primeira coisa que você deve fazer é abrir o arquivo settings.py de sua aplicação, e configurar o banco de dados da mesma. Para isso no arquivo figexample/settings.py basta especificar as configurações abaixo no banco de dados.

```python
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': 'postgres',
'USER': 'postgres',
'HOST': 'db',
'PORT': 5432,
  }
}
```
Com o banco configurado é hora de subir sua aplicação, na pasta raiz do projeto use.

```bash
$ fig up
```
O fig se encarregará de criar todos os conteineres, linkalos, e startar sua aplicação na porta 8000, acesse seu [localhost:8000](http://localhost:8000/) e você verá sua aplicação em execução.


Para rodar os comandos do django, você pode fazer da seguinte forma.

```bash
$ fig run <bloco> <comando>
```
Por exemplo.

```bash
$ fig run web ./manage.py syncdb
```
Lembrando que esse comando sempre será o padrão.

#Conclusão

Como você pode ver, o fig em conjunto com o docker torna seu workflow algo extremamente simples e eficaz. O melhor disso tudo, é que, para trabalhar com esse mesmo ambiente em uma nova máquina, você apenas precisará do fig e docker instalados, acessar a rais do projeto e executar um fig up, gerando com isso,uma comodidade jamais vista.
