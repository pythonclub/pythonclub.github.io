Title: Deploy App Django no Openshift
Slug: deploy-app-django-openshift
Date: 2014-09-05 18:00
Tags: tutorial,django,openshift,paas
Author: Elio Duarte
Email:  elio.esteves.duarte@gmail.com
Github: eliostvs
Category: Django

Recentemente quis testar o Django no Openshift mas não encontrei nenhum tutorial atualizado sobre o assunto, por isso resolvi escrever um.
Nosso objetivo é ter um app bem básico em Django rodando no [Openshift Online][openshift-online].
Eu utilizei o Ubuntu 14.04 nesse tutorial mas excluindo a parte de instalação do programa *rhc*, ele serve para qualquer sistema unix-like.

### O que é?

[Openshift Origin](http://openshift.github.io/) é um PaaS opensource mantido pela RedHat.
A empresa também tem um serviço de hospedagem, o [Openshift Online][openshift-online], com planos pagos e gratuitos.
No plano gratuito você pode utilizar até três *small gears*, containers onde a sua aplicação irá rodar.
Cada *small gear* possui:

* 512MB de RAM
* 100MB de swap
* 1GB de espaço em disco

Em cada *gear* você pode ter um ou mais *cartridges*, funcionalidades que sua app poderá utilizar.
Existem *cartridges* que habilitam uma linguagem (Python, Ruby, Java), um banco de dados (PostgreSQL, MongoDB), um serviço (Cron, MMS), etc.

### Criação de conta e login

Você precisa ter uma conta no [Openshift Online][openshift-online] e o programa **rhc** instalado em sua máquina.

Crie uma conta gratuita clicando [aqui](https://www.openshift.com/app/account/new).

Depois instale o programa **ruby** e o **rhc**:

    :::bash

    sudo apt-get update && apt-get install -y ruby
    sudo gem install rhc

Clique [aqui](http://openshift.github.io/documentation/oo_client_tools_installation_guide.html) para ver como instalar o **rhc** em outras plataformas.

Faça o login:

    :::bash

    rhc setup

Por fim confirme que você consegue conectar em sua conta executando:

    :::bash

    rhc apps
    No applications. Use 'rhc create-app'.

### Criando um app no Openshift

Crie um app com nome de **django** usando o *cartridge* **Python 2.7**:

    :::bash

    rhc create-app -a django -t python-2.7
    Application Options
    -------------------
    Domain:     stvs
    Cartridges: python-2.7
    Gear Size:  default
    Scaling:    no

    Creating application 'django' ... done

    Waiting for your DNS name to be available ... done

    Cloning into 'django'...

    Your application 'django' is now available.

    URL:        http://django-stvs.rhcloud.com/
    SSH to:     5409ae505973ca58d200015e@django-stvs.rhcloud.com
    Git remote: ssh://5409ae505973ca58d200015e@django-stvs.rhcloud.com/~/git/django.git/
    Cloned to:  /home/usuario/django

No retorno do comando podemos ver algumas informações básicas do app, inclusive a URL, que já está funcionando.
Acesse o endereço e veja a página padrão que foi criada.

### Definindo dependências

Acesse o repositório que foi criado ao executar `rhc app-create`, ele terá o nome do seu app:

    :::bash

    cd django/

Existem duas formas de definir as dependências do seu app Python no Openshift, pelo arquivo **setup.py** ou pelo **requirements.txt**.
Durante o processo de **deploy** o Openshift automaticamente executa `python setup.py install` e `pip -r requirements.txt` na raiz do repositório.

Usaremos somente o **requirements.txt**, então exclua o **setup.py**.

    :::bash

    rm setup.py

Faça *commit* mas não execute `git push` ainda.

    :::bash

    git commit -am 'removido setup.py'

Adicione o Django no *requirements.txt*:

    :::bash

    echo 'Django==1.7' > requirements.txt

Crie um virtualenv para testar se o **requirements.txt** está correto:

    :::bash

    pyenv virtualenv 2.7.8 openshift
    pyenv activate openshift
    pip install -r requirements.txt

Por fim, faça um novo *commit*.

### Criando o projeto Django

De agora em diante não direi mais para você fazer o *commit* o tempo todo mas é uma boa prática que você o faça a cada etapa.

Execute o comando abaixo para criar o arquivo **.gitignore** e adicionar algumas entradas nele.
Esse arquivo irá impedir que alguns arquivos desnecessários sejam adicionados ao git.

    :::bash

    cat > .gitignore <<EOF
    *.pyc
    *.sqlite3
    EOF

Crie um projeto Django com o nome **openshift**:

    :::bash

    django-admin.py startproject openshift

Acesse o projeto e crie um *app* com nome **exemplo**:

    :::bash

    cd openshift
    django-admin.py startapp exemplo

Execute o *migrate* inicial e depois inicie o servidor de teste:

    :::bash

    python manage.py migrate
    python manage.py runserver

Acesse o endereço *127.0.0.1:8000* e verifique se você consegue ver a mensagem **It worked!**

### Configurando o projeto

Ao executar o *deploy* da sua aplicação, o Openshift irá procurar pelo WSGI *entry-point* em alguns arquivos.
Um desses arquivos é o **wsgi.py** na raiz do repositório.
O WSGI *entry-point* nada mais é do que o *callable* do servidor WSGI.
No nosso caso usamos uma variavel mas poderia ser um método ou uma função, o importante é que ele tenha o nome de **application**.

Execute o comando abaixo para criar o WSGI *entry-point*:

    :::bash

    cat > wsgi.py <<EOF
    #!/usr/bin/python

    import os
    import sys
    from django.core.wsgi import get_wsgi_application

    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'openshift'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'openshift.production'

    application = get_wsgi_application()
    EOF

Abra o arquivo de configuração padrão do seu projeto Django:

    :::bash

    vi openshift/openshift/settings.py

Adicione o app **exemplo** em **INSTALLED_APPS**:

    :::python

    INSTALLED_APPS = (
       'django.contrib.admin',
       ...
        'exemplo',
       )

Salve e depois abra o arquivo de configuração que usaremos em produção.

    :::bash

    vi openshift/openshift/production.py

Comece importando todas as configuração do arquivo de configuração padrão:

    :::python

    from settings import *

Desabilite o modo **debug**:

    :::python

    DEBUG = False

Existem várias variáveis de ambiente dentro de um *gear*, utilizaremos as seguintes delas em nossa configuração:

* **OPENSHIFT_APP_DNS**: nome completo do domínio da sua aplicação, no meu caso é *http://django-stvs.rhcloud.com/*.
* **OPENSHIFT_DATA_DIR**: diretório para dados persistentes.
* **OPENSHIFT_REPO_DIR**: diretório onde estão os arquivos do *deploy* atual.
* **OPENSHIFT_SECRET_TOKEN**: hash gerado automaticamente quando o *gear* é criado.

Você pode ver outras variáveis disponíveis [aqui](https://developers.openshift.com/en/managing-environment-variables.html).

Copie as configurações:

    :::python

    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS']]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'db.sqlite3'),
        }
    }

Os *cartridges* padrões de Python, utilizam o diretório *wsgi/static* para servir arquivos estáticos pelo Apache.
Ele ainda não existe, para criá-lo execute:

    :::bash

    mkdir -p wsgi/static
    touch wsgi/static/.gitkeep

Por fim adicione a linha abaixo em sua configuração:

    :::python

    STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'static')


Criando uma view simples
------------------------

Vamos criar uma *view* básica somente para testar nosso projeto.

Adicione a url abaixo no arquivo *openshift/openshift/urls.py*:

    :::python

    urlpatterns = patterns('',
        url(r'^$', 'exemplo.views.home', name='home'),
        ...

Depois crie a *view* em *openshift/exemplo/views.py*:

    :::python

    from django.http import HttpResponse

    def home(request):
        return HttpResponse('Hello World!')

Execute novamente o servidor de teste, acesse o endereço '127.0.0.1:8000/' e confirme que a mensagem **Hello World!** aparece.

Fazendo deploy
--------------

Na raiz do repositório, existe um diretório oculto chamado **.openshift**.
Vamos listar seu conteúdo:

    :::bash

    cd .openshift
    tree
    .
    ├── action_hooks
    │   └── README.md
    ├── cron
    │   ├── daily
    │   ├── hourly
    │   ├── minutely
    │   ├── monthly
    │   ├── README.cron
    │   └── weekly
    │       ├── chrono.dat
    │       ├── chronograph
    │       ├── jobs.allow
    │       ├── jobs.deny
    │       └── README
    ├── markers
    │   └── README.md
    └── README.md

Cada diretório dentro dele tem uma função especial.

#### Cron

Essa pasta serve para agendar a execução de scripts.
Ela funciona igual aos diretórios **cron** em qualquer distribuição Linux.
Você precisa adicionar o *cartridge* **cron** ao seu app para que os agendamentos funcionem.

    :::bash

    rhc cartridge add -a django -c cron-1.4

#### Markers

Nesta pasta você pode criar arquivos que alteram o comportamento do Openshift durante algumas ações.
Por exemplo, se você criar o arquivo **hot_deploy** o servidor Apache não será reiniciado durante o processo de **build**.
Outras **markers** disponíveis estão detalhadas [aqui](http://openshift.github.io/documentation/oo_cartridge_guide.html#markers-7).

#### Action Hooks

O funcionamento dessa pasta é bem parecido com o da pasta **markers**.
Em algumas ações o Openshift vai procurar determinados arquivos dentro dela e executá-los em uma determinada ordem.
Para listar quais são as ações disponíveis execute o comando `rhc app --help`:

    :::bash

    rhc app --help
    Usage: rhc app <action>

    Creates and controls an OpenShift application.  To see the list of all applications use the rhc domain show command.  Note that delete is not reversible
    and will stop your application and then remove the application and repo from the remote server. No local changes are made.

    List of Actions
    configure     Configure several properties that apply to an application
    create        Create an application
    delete        Delete an application from the server
    deploy        Deploy a git reference or binary file of an application
    force-stop    Stops all application processes
    reload        Reload the application's configuration
    restart       Restart the application
    scale-down    Scale down the application's web cartridge
    scale-up      Scale up the application's web cartridge
    show          Show information about an application
    start         Start the application
    stop          Stop the application
    tidy          Clean out the application's logs and tmp directories and tidy up the git repo on the server

Por exemplo, na ação **build**, os arquivos serão procurados e executados na seguinte ordem:

- pre_build
- build
- prepare
- deploy
- post_deploy

Não é preciso que nenhum arquivo exista, essa é só uma forma de controlar o comportamento do seu app.
Para saber mais sobre *action hooks* clique [aqui](http://openshift.github.io/documentation/oo_user_guide.html#cartridge-control-action-hooks).

No nosso caso, só vamos usar o arquivo **deploy**:

    :::bash

    touch .openshift/action_hooks/deploy

É preciso que o arquivo seja executável, então:

    :::bash

    chmod +x .openshift/action_hooks/deploy

Em nosso *deploy*, apenas vamos atualizar o schema do banco e recolher os arquivos estáticos.
Note que precisamos informar o arquivo de configuração que usaremos em produção, que é diferente daquele que está no arquivo **manage.py**.

    :::bash

    cat > .openshift/action_hooks/deploy <<EOF
    PYTHONPATH=\$OPENSHIFT_REPO_DIR/openshift
    django-admin.py migrate --settings='openshift.production' --pythonpath=\$PYTHONPATH
    python \$PYTHONPATH/manage.py collectstatic -c --noinput --settings='openshift.production' --pythonpath=\$PYTHONPATH
    EOF

Feito isso, faça *commit* e depois execute `git push`.
O *push* irá disparar o processo de **build**.
Você verá varias mensagens em seu terminal mas no final irá aparecer:

    ::bash

    ...
    remote: Git Post-Receive Result: success
    remote: Activation status: success
    remote: Deployment completed with status: success
    ...

Essa saída mostra que o **deploy** foi executado com sucesso.
Se você acessar a URL da sua app aparecerá **'Hello World!'**.
Pronto seu projeto Django está rodando no Openshift!

Aguardo feedback com dúvidas, sugestões, correções etc nos comentários.

Abraços e bons projetos!

Bonus
-----

* Execute o `rhc tail` para visualizar o arquivos de log do seu app, ótimo para visualizar problemas.
* Acesse a [documentação oficial](http://openshift.github.io/documentation/) para saber mais detalhes sobre o Openshift.
* [Aqui](https://github.com/eliostvs/django-kb-example) tem um *quickstart* de uma base de conhecimento para você utilizar no Openshift.

[openshift-online]: https://www.openshift.com/products/online
