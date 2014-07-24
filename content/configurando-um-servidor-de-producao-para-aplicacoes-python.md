Title: Configurando um servidor de produção para aplicações Python
Slug: configurando-um-servidor-de-producao-para-aplicacoes-python
Date: 2014-07-24 14:42
Tags: django,web,tutorial,wsgi,gunicorn,nginx,supervisor,servidor,producao
Author: Igor Santos
Email:  igr.exe@gmail.com
Github: igr-santos
Bitbucket: igrsantos
Site: http://pythonclub.com.br
Gittip: igr-santos
Category: Servidor Web


### Entendendo do que se trata
Sempre tive muita dificuldade de configurar um servidor para rodar meus projetos ***Python*** e ***Django***, nunca me dei bem com o ***Apache***. Foi buscando outras maneiras de servir minhas aplicações ***Python Web*** que encontrei o ***Nginx*** e o ***Gunicorn***, então resolvi compartilhar minha experiência com essas ferramentas, e como organizo um ambiente com vários projetos ***Python WSGI***.


### Preparando nosso ambiente
Abaixo algumas das ferramentas que serão utilizadas para preparar o nosso ambiente de ***Produção***.

- Servidor Python WSGI ([Gunicorn](http://docs.gunicorn.org/en/19.0/))
- Proxy ([Nginx](http://nginx.org/en/docs/))
- Controlador/Monitor de processos ([Supervisor](http://supervisord.org/))
- Ambientes Python isolados ([Virtualenwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/))

1. Instalando o gerenciador de pacotes, o proxy e o controlador de processos.

    ```bash
    sudo apt-get install python-pip nginx supervisor
    ```

    **Utilidades**
    > - **Pip**: Gerenciador de pacotes Python.
    > - **Nginx**: Usado como proxy e como server de arquivos estáticos.
    > - **Supervisor**: Gerenciar o processo de start/stop da nossa aplicação.

2. Organizando meu ambiente com ***Virtualenvwrapper***.

    Instalando o ***Virtualenvwrapper*** para ter ambientes isolados, prossibilitando diferentes projetos ***Python***, no mesmo servidor.

    ```bash
    pip install virtualenvwrapper
    ```
    Nosso filesystem será organizado da seguinte forma:

    ```bash
    # -- /home/myusr
    #    -- /www             [Projetos]
    #    -- /env             [Ambientes]
    mkdir ~/www ~/env
    ```

    **Como funciona?**

    O ***Virtualenvwrapper*** irá criar os projetos dentro do `~/www` e os ambientes dentro do `~/env`, basta configurar algumas variáveis no seu `~/.bashrc`.

    ```bash
    # ~/.bashrc
    ...
    export PROJECT_HOME=~/www
    export WORKON_HOME=~/env
    source /usr/local/bin/virtualenvwrapper.sh

    ```

    Atualize o seu `~/.bashrc` e crie um projeto.

    ```bash
    mkproject myproject
    ```

3. Configurando ***Nginx*** e ***Supervisor*** da maneira simples.

    **O que fazer agora?**

    Vamos configurar o Nginx e o Supervisor para ele trabalhar na nossa estrutura de arquivos.

    Edite o arquivo `/etc/nginx/nginx.conf`,

    ```
    ##
    # Virtual Host Configs
    ##
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;

    # encontra a configuracao dos seus projetos
    include /home/myusr/www/*/nginx.conf;
    ```

    e edite o `/etc/supervisor/supervisord.conf`,

    ```
    [include]
    ;files = /etc/supervisor/conf.d/*.conf

    # encontra a configuracao dos seus projetos
    files = /home/myusr/www/*/supervisor.conf
    ```

    Agora eles estão prontos para buscar as configurações dentro da nossa pasta de projetos, cada projeto vai ter uma configuração unica, e quando quiser removê-lo vai fazer isso de forma simples, excluindo a pasta do projeto.



### Fazendo as coisas funcionarem
Agora que temos todos as ferramentas necessárias instaladas e nosso ambiente configurado e bem organizado, vamos colocar para funcionar o nosso projeto.

1. Configurando meu ambiente ***WSGI*** com ***Gunicorn***.

    Vamos ativar nosso ambiente virtual e instalar o ***Gunicorn***

    ```bash
    workon myproject
    pip install gunicorn
    ```

    **Qual próximo passo então?**

    Vamos criar nossos arquivos de configuração, e logs do nosso projeto.

    ```bash
    cd ~/www/myproject
    mkdir static media logs project
    touch nginx.conf supervisor.conf start.sh
    touch logs/access.log logs/error.log logs/gunicorn.log logs/suprevisor.log
    ```

    No momento nosso filesystem se parece com esse:

    ```bash
    -- home/myusr/
      -- www/                   [Projetos]
        -- myproject/
          -- nginx.conf         [Config do Nginx]
          -- supervisor.conf    [Config do Supervisor]
          -- start.sh           [Script Gunicorn]
          -- project/           [Fonte do nosso projeto]
          -- logs/              [Logs]
            -- access.log       [Log de acesso Nginx]
            -- error.log        [Log de erro Nginx]
            -- gunicorn.log
            -- supervisor.log
      -- env/                   [Ambientes]
    ```

    **Como configurar meu projeto?**

    Vamos começar pelo `start.sh`, ele vai ser responsável por iniciar a sua aplicação ***WSGI*** usando o servidor ***Gunicorn***.

    ```bash
    #!/bin/bash
    # Diretorio e arquivo de log
    set -e
    LOGFILE=/home/myusr/www/myproject/logs/gunicorn.log
    LOGDIR=$(dirname $LOGFILE)
    # Numero de processo simultaneo, modifique de acordo com seu processador
    NUM_WORKERS=3
    # Usuario/Grupo que vai rodar o gunicorn
    USER=myusr
    #GROUP=root
    # Endereço local que o gunicorn irá rodar
    ADDRESS=127.0.0.1:8000
    # Ativando ambiente virtual e executando o gunicorn para este projeto
    source /home/myusr/envs/myproject/bin/activate
    cd /home/myusr/www/myproject/project/
    test -d $LOGDIR || mkdir -p $LOGDIR
    exec gunicorn -w $NUM_WORKERS --bind=$ADDRESS --user=$USER --log-level=debug --log-file=$LOGFILE 2>>$LOGFILE myproject.wsgi:application
    ```

    Na linha 6, *ADDRESS*, diz que o nosso projeto vai rodar localhost com a porta 8000, esse mesmo ip:porta será usado na configuração do `nginx.conf`, as linhas abaixo fazem o processo de ativar o ambiente virtual e navegar para pasta do fonte do projeto, para que o ***Gunicorn*** possa encontrar o arquivo `wsgi.py`, esse é o arquivo que configura o ambiente de produção no ***Django***.

    Agora vamos configurar o `nginx.conf`, para que ele possa escutar o nosso dominio na porta 80 e redirecionar a requisição para a nossa aplicação no *127.0.0.1:8000*.

    ```
    upstream myproject.com.br {
        server 127.0.0.1:8000;
    }

    server {
        listen 80;
        server_name myproject.com.br;
        client_max_body_size 50M;

        access_log /home/myusr/www/myproject/logs/access.log;
        error_log /home/myusr/www/myproject/logs/error.log;

        location /static/ {
            alias /home/myusr/www/myproject/static/;
        }
        location /media/ {
            alias /home/myusr/www/myproject/media/;
        }
        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;

            if (!-f $request_filename) {
                proxy_pass http://myproject.com.br;
                break;
            }
        }
    }
    ```

    Criamos um *upstream* que representa a nossa aplicação, e configuramos o *server* para escutar nosso dominio na porta 80 e redirecionar tudo com *location /* para nosso *upstream*, no *location /static/* e *localtion /media/* criamos um alias para nossa pasta de arquivos, assim o ***Nginx*** passa a servir os arquivos estáticos e de midia.

    **Falta pouco!**

    Precisamos só de configurar o ***Supervisor*** para iniciar nosso projeto automaticamente, veja o `supervisor.conf` de exemplo.

    ```
    [program:myproject]
    command=/home/myusr/www/myproject/start.sh
    user=myusr
    stdout_logfile=/home/myusr/www/myproject/logs/supervisor.log
    redirect_stderr=true
    autostart=true
    autorestart=true
    ```

    Ufa!, é um arquivo bem simples só precisamos informar o que queremos executar e com qual usuário ele fará isso, agora vamos iniciar nosso projeto.

    ```bash
    sudo service nginx restart
    sudo /etc/init.d/supervisor start myproject
    ```

### Pronto!
Pronto agora você tem um ambiente bem estruturado rodando sua aplicação, um detalhe é que eu me limitei a instalar o ***Gunicorn*** dentro do ambiente virtual, caso um dia queira um outro **web server** que não seja o ***WSGI*** com outros projetos, é só instalar outro **server** no ambiente virtual do projeto, criar um **script** para iniciar o projeto, e voilá!
