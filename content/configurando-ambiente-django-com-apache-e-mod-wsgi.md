Title: Configurando ambiente Django com Apache e mod_wsgi
Date: 2015-03-02 00:20
Tags: python, django, apache, mod_wsgi, virtualenv, virtualenvwrapper
Category: Django
Slug: configurando-ambiente-django-com-apache-e-mod-wsgi
Author: Guilherme Louro
Email:  guilherme-louro@hotmail.com
Github: guilouro
Twitter: guilhermelouro
Facebook: guilherme.louro.3


### Entendendo a necessidade

Muitas vezes encontramos dificuldade em colocar nossas aplicações para funcionar em um servidor devido ao pouco conhecimento em infra, principalmente aqueles que vieram do php, onde, subir um site e já o ver funcionando no ambiente final se trata apenas de subir os arquivos para a pasta **www** e pronto, certo? Não, não é bem por aí ...

Normalmente quando configuramos a hospedagem de um domínio através de um software de gestão de alojamento web *([cpanel](http://cpanel.net) é  o mais conhecido)* automaticamente o sistema configura o VirtualHost específico para o seu domínio cadastrado, ja direcionando a path para a sua pasta *www* ou **public_html**. Mas como isso é feito? Não entrarei em detalhes de como o cpanel funciona, mas irei demonstrar aqui como configuramos um servidor com apache para receber nossa aplicação.

### Mas por que o Apache?

A partir do momento que eu mudei meu foco, saindo do PHP para trabalhar com **Python**, eu acabei "abandonando" o Apache para trabalhar com Nginx. Porém, me deparei com um projeto onde tinha que funcionar em uma Hospedagem compartilhada na qual só funciona o apache. Como não vi nada relacionado a essa configuração aqui no **Pythonclub**, achei que seria útil para muitos que podem cair em uma situação parecida com a minha, ou simplesmente prefira usar o Apache do que o Nginx.

Caso o seu interesse seja mesmo usar o Nginx <strike>(pode parar por aqui)</strike>, acho ótimo!!! Te dou todo apoio e ainda te indico um ótimo post para isso, do nosso amigo [Igor Santos](https://github.com/igr-santos).

- [Configurando um servidor de produção para aplicações Python](http://pythonclub.com.br/configurando-um-servidor-de-producao-para-aplicacoes-python.html) (Nginx)

Agora, chega de conversa e vamos ao que interessa.

### Como fazer?

Existem várias maneiras de se fazer o Django trabalhar com apache, uma delas é a combinação Apache + mod_wsgi e será dessa forma que faremos. Com mod_wsgi podemos implementar qualquer aplicação Python que suporte a interface **Python WSGI**.

##### Instalando alguns pacotes necessários

*Apache + mod_wsgi*

```bash
$ apt-get install apache2 libapache2-mod-wsgi
```

*Python setup tools + pip*

```bash
$ apt-get install python-setuptools
$ apt-get install python-pip
```

### Vamos testar o WSGI?

Vamos fazer um teste com uma aplicação simples em python.

Começe criando um diretório na raiz do apache *(DocumentRoot)*

```bash
$ mkdir /var/www/wsgi_test
```

Em seguida vamos criar nossa app de teste ...

```bash
$ vim /var/www/app.wsgi
```

... e escrever nossa app python compatível com WSGI

```python
def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]
```

Vamos criar agora um host para usar como nosso domínio da aplicação teste

```bash
$ vim /etc/hosts
```

Adicione esta linha ao seu arquivo hosts

```bash
127.0.0.1 wsgi_test
```

E vamos configurar nosso VirtualHost no Apache.

```bash
$ vim /etc/apache2/sites-available/wsgi_test
```

```apache
<VirtualHost *:80>
    ServerName wsgi_test
    DocumentRoot /var/www/wsgi_test
    <Directory /var/www/wsgi_test>
        Order allow,deny
        Allow from all
    </Directory>
    WSGIScriptAlias / /var/www/wsgi_test/app.wsgi
</VirtualHost>
```

Ative-o

```bash
$ a2ensite wsgi_test
```

*Obs: esse comando cria um link simbólico do wsgi_test para a pasta sites-enabled. Você pode fazer isso manualmente.*

Reinicie o apache:

```bash
$ service apache2 reload
```

Feito isso abra o <strike>internet explorer</strike> seu navegador preferido e acesse [http://wsgi_test](http://wsgi_test). Se você está vendo a mensagem *"Hello World"* pode comemorar, o wsgi está funcionando com o apache.

### Configurando Django com WSGI

Até o momento entendemos como funciona a configuração do apache para receber uma aplicação Python com WSGI. Podemos usar essa ideia para qualquer aplicação python, porém veremos como fica essa configuração para trabalhar com **Django**.

##### Criando o ambiente

É sempre bom trabalharmos com ambientes virtuais em nossas aplicações python, para isso temos o [virtualenv](https://virtualenv.pypa.io/en/latest/). Eu, particularmente, prefiro usar o [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/), que separa os ambientes virtuais das aplicações. Caso você não conheça, indico o post do [Arruda](https://virtualenvwrapper.readthedocs.org/en/latest/) que foi o que me guiou quando comecei a usar. [Usando VirtualEnvWrapper](http://www.arruda.blog.br/programacao/python/usando-virtualenvwrapper/)

No meu caso usei o virtualenvwrapper e meu filesystem é o seguinte:

```bash
+-- /home/guilouro
|   +-- .virtualenvs  #[Ambientes]
|   +-- www           #[Projetos]
```

O Virtualenvwrapper criará meus projetos dentro de **www** e os ambientes em **.virtualenvs**. Mas para que isso aconteça temos que adicionar algumas linhas em nosso `~/.bashrc`

```bash
# adicione no final do arquivo ~/.bashrc
# ...
export PROJECT_HOME=~/www
export WORKON_HOME=~/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Atualize com o comando:

```bash
source ~/.bashrc
```

##### Criando nosso projeto

```bash
$ mkproject wsgi
```

Com as configurações anteriores o virtualenvwrapper já irá ativar o ambiente e levar você para a pasta do projeto. Mas para ativar é muito simples, basta usar:

```bash
$ workon wsgi
```

Com o nosso ambiente virtual criado partiremos então para a criação do nosso projeto django. Utilizarei a versão mais atual até o momento, nesse caso 1.7

```bash
$ pip install django
```

Não entrarei em detalhes para a configuração inicial do django, portanto irei usar um template que eu criei para a inicialização dos meus projeto. Criamos então o projeto dessa forma:

```bash
# startproject pelo template
$ django-admin.py startproject --template https://github.com/guilouro/django-boilerplate/archive/master.zip wsgitest .
# instala os pacotes
$ pip install -r requirements.txt
# faz a migração
$ python manage.py migrate
```

Você encontra esse template aqui -> [django-boilerplate](https://github.com/guilouro/django-boilerplate)

##### Criando um site no apache para o projeto

Primeiramente, vamos criar um domínio fictício para responder com o nosso projeto ao ser acessado.

```bash
$ vim /etc/hosts

127.0.0.1   djangowsgi.com
```

Agora vamos configurar o apache:

```bash
$ vim /etc/apache2/sites-available/djangowsgi
```

```apache
WSGIDaemonProcess djangowsgi.com python-path=/home/guilouro/www/wsgi:/home/guilouro/.virtualenvs/wsgi/lib/python2.7/site-packages
WSGIProcessGroup djangowsgi.com

<VirtualHost *:80>
    ServerName djangowsgi.com
    WSGIScriptAlias / /home/guilouro/www/wsgi/wsgitest/wsgi.py

    <Directory /home/guilouro/www/wsgi>
        <Files wsgi.py>
            Order allow,deny
            Allow from all
        </Files>
    </Directory>

    Alias /media/ /home/guilouro/www/wsgi/media/
    Alias /static/ /home/guilouro/www/wsgi/static/

    <Directory /home/guilouro/www/wsgi/static>
        Order allow,deny
        Allow from all
    </Directory>

    <Directory /home/guilouro/www/wsgi/media>
        Order allow,deny
        Allow from all
    </Directory>

</VirtualHost>
```

Reinicie novamente o apache:

```bash
$ service apache2 reload
```

Explicarei agora um pouco do que foi usado nessa configuração

**WSGIScriptAlias:** é a url na qual você estará servindo sua aplicação (/ indica a url raiz), e a segunda parte é a localização de um "arquivo WSGI".

### Modo daemon

 O modo *daemon* é o modo recomendado para a execução do mod_wsgi(em plataformas não-windows). Ele gera um processo independente que lida com as solicitações e pode ser executado como um usuário diferente do servidor web. Um dos pontos positivos dele é que a cada alteração em seu projeto você não precisa restartar o apache, basta executar um `touch` no seu arquivo `wsgi.py`

##### Directivas para o daemon

**WSGIDaemonProcess:** Foi atribuido a ele o nosso servername e utilizamos `python-path` por se tratar de um projeto que esta em ambiente virtual. Passamos então nossas paths nele.

**WSGIProcessGroup:** Atribuímos o servername a ele

#### Testando a aplicação

Agora acesse [http://djangowsgi.com](http://djangowsgi.com) e corre para o abraço.

Espero que tenha ficado claro. Qualquer dúvida ou problema deixe nos comentários e vamos juntos tentar resolver.

---
##### Referências:

- modwsgiwiki - [https://code.google.com/p/modwsgi/wiki/](https://code.google.com/p/modwsgi/wiki/)
- Django Portuguese Readthedock [https://django-portuguese.readthedocs.org](https://django-portuguese.readthedocs.org)
- Blogalizado - [http://www.blogalizado.com.br/deploy-de-aplicacao-django-no-apache-com-mod_wsgi/](http://www.blogalizado.com.br/deploy-de-aplicacao-django-no-apache-com-mod_wsgi/)
- Documentação oficial do django - [https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/modwsgi/](https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/modwsgi/)