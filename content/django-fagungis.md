Title: Sobre o six e como Publicação de projetos com o Django-Fagungis
Date: 2014-05-13 16:00
Tags: Django, Fabric, Gunicorn, Nginx, Supervisor, Deploy, django-fagungis
Category: Python, Django, Deploy
Slug: deploy-com-django-fagungis
Author: Rômulo Collopy
Email:  romulo.collopy@gmail.com
Github: romulocollopy
Site: http://collopy.pro.br
Twitter: romulocollopy
Facebook: romulocollopy

### Django Fagungis

Django-Fagungis é um projeto original do [Denis Darii](http://github.com/dnx), [disponível no Pypi para instalação via pip](https://pypi.python.org/pypi/django-fagungis/0.0.17). A idéia do projeto é simples: automatizar o deploy de projetos Django para servidores com acesso root, utilizando o [Fabric](http://www.fabfile.org/), uma biblioteca e ferramenta de linha de comando em Python (2.5-2.7) que usa o protocolo SSH para o deploy de aplicações e realização de tarefas administrativas no sistema, não restrita a projetos Python.

Porém, nesse artigo, **não vamos usar a versão original do Django-Fagungis**. Em vez dela, **usaremos um fork** feito por [Damian Moore](https://github.com/damianmoore/).

Por isso, a instalação não será feita diretamente pelo pip, mas pelo repositório do Damian, em [https://github.com/damianmoore/django-fagungis](https://github.com/damianmoore/django-fagungis).

`pip install git+https://github.com/damianmoore/django-fagungis.git`

__Pediu a senha de root? Que tal criar um virtualenv primeiro?__

Atualmente, trabalho mais com Python3 que com Python2, porém o Fabric ainda não foi completamente portado para o Python3, por isso, sempre crio um virtualenv para trabalhar com ele.

No caso do Django-Fagungis creio que você tem um argumento a mais para usar um virtualenv: existem forks mais atuais que o projeto disponóvel no pip e possivelmente você vai querer testar diferentes versões.

### Então, vamos ao passo a passo.

Digamos que você queira criar um projeto chamado simpleproject, em Python3, em um virtualenv. (Eu vou usar ~/dev/simpleproject).

    mkdir -p ~/dev/simpleproject.com
    cd ~/dev/simpleproject
    pip install --upgrade virtualenv
    virtualenv --unzip-setuptools --python=/usr/bin/python3.4 .
    source bin\activate
    pip install django
    django-admin.py startproject simpleproject .


__Oops__, temos um problema, pois o fabric não suporta o Python3. Então criamos outro virtualenv para o django-fagungis. Você pode fazer isso em qualquer lugar. Nesse exemplo vou instalar em:

`~/dev/tools/django-fagungis-damianmoore`

__Notem que deixei o nome do usuário github na pasta para lembrar que estou usando um fork.__

Agora vou até a pasta e crio o virtualenv com Python2

    deactivate
    mkdir -p ~/dev/tools/django-fagungis-damianmoore
    cd ~/dev/tools/django-fagungis-damianmoore
    virtualenv --unzip-setuptools --python=/usr/bin/python2.7 .
    source bin\activate

*Pode ser que você não precise dizer o caminho do executável do python para a versão 2.7*

E instalo o django-fagungis::
    
    pip install git+https://github.com/damianmoore/django-fagungis.git

E copio o fabfile.py de exemplo para meu projeto:

    cp ~/dev/tools/django-fagungis-damianmoore/lib/python2.7/site-packages/fagungis/example_fabfile.py ~/dev/simpleproject/fabfile.py

Feito isso, podemos voltar ao projeto e editar o fabfile para as configurações do seu projeto. A configuração é bem simples e o arquivo é autoexplicativo.

Seu projeto deverá estar em um repositório, seja ele no bitbicket, github, ou qualquer lugar onde seu servidor possa acessá-lo (e com as devidas permissões). Nesse caso, vou supor que seu projeto está no github:

Mude
`def example():` para `def simpleproject():`

E as variáveis env.

    env.project = 'simpleproject_production'
    env.repository = 'https://github.com/seu-username/simpleproject.git'
    env.repository_type = 'git'
    env.hosts = ['root@simpleproject.org', ]
    env.additional_packages = ['git-core',]


**Agora, algumas configurações mais sensíveis:**

O Django e o Nginx têm um tratamento particular para a url static, por isso a automatixação fica mais fácil se você não usar essa url no seu projeto.

Dê preferência para usar configurações como a seguir:

    #  django media url and root dir
    env.django_media_url = '/media/'
    env.django_media_root = env.code_root
    #  django static url and root dir
    env.django_static_url = '/assets/'
    env.django_static_root = env.code_root

E, em seu settings.py 

    from unipath import Path
    PROJECT_ROOT = Path(__file__).parent
    
    #...
    
    STATIC_URL = '/assets/'
    STATIC_ROOT = PROJECT_ROOT.parent.child('assets')

**Se você escolheu usar Python3** no seu projeto, adicione o path para o python3 no virtenv_options

    env.virtenv_options = ['distribute', 'no-site-packages','python=/usr/bin/python3', ]

Estamos com tudo quase pronto. Você já pode tentar o deploy do seu projeto, mas para isso terá que ativar o virtualenv onde instalou o django-fagungis. Como esse processo é um pouco chato, criei um script para fazer isso e voltar para o seu projeto. 

Crie um arquivo fagungis.sh e grave na pasta onde ele está instalado (`~/dev/tools/django-fagungis-damianmoore` em nosso caso)

    SCRIPT_NAME="${BASH_SOURCE[0]}"
    SCRIPT_DIR="$( dirname "$SCRIPT_NAME" )"

    source $SCRIPT_DIR/bin/activate
    fab $1 $2

    PROJECT="$(cd $(dirname $0) && pwd)"
    source $PROJECT/bin/activate

E em seu .bashrc, adicione um alias para ele:

     alias fagungis='~/dev/tools/django-fagungis-damianmoore/fagungis.sh'

Agora é só ir até a raiz do seu projeto, onde está salvo o fabfile.py e digitar:

    fagungis simpleproject setup
    fagungis simpleproject deploy

**lembre-se que para as mudanças no .bashrc terem efeito, você deverá recarregá-lo com** `source ~/.bashrc` **ou reabrir a janela do terminal**

Se tudo correu certo, seu projeto já está rodando no servidor. Mas em alguns casos o [Gunicorn](http://docs.gunicorn.org/en/latest/run.html) tem um problema com a sintaxe antiga e você precisa ir no pacote do fagungis e mudar o último exec do script: `~/dev/tools/django-fagungis-damianmoore/lib/python2.7/site-packages/fagungis/scripts/rungunicorn.sh`

A chamada do gunicorn deve ficar assim:

    exec %(virtenv)s/bin/gunicorn -w %(gunicorn_workers)s \
        --user=%(django_user)s --group=%(django_user_group)s \
        --settings=%(django_project_settings)s \
        --bind=%(gunicorn_bind)s --log-level=%(gunicorn_loglevel)s \
        --log-file=%(gunicorn_logfile)s 2>>%(gunicorn_logfile)s \
        %(project)s.wsgi:application

Salve o arquivo e tente de novo.

    fagungis simpleproject setup
    fagungis simpleproject deploy

Se seu projeto Django tem a configuração simples, deve estar tudo funcionando. Não esqueça que se você usar pacotes como [python_decouple](https://pypi.python.org/pypi/python-decouple), deverá enviar o settings.ini para a pasta do projeto no servidor. 

O Django-Fagungis não cria automaticamente seu servidor de banco de dados, então ainda te resta esssa tarefa, caso ele fique no mesmo servidor do seu projeto. Mas isso fica para um próximo artigo do PythonClub.

