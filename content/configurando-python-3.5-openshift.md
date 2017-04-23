Title: Configurando OpenShift com Python 3.5 + Flask + Gunicorn
Slug: configurando-python-3.5-openshift-flask-gunicorn
Date: 2017-04-23 20:37:39
Category: Python
Tags: python,tutorial,install,cloud
Author: Horácio Dias
Email: horacio.dias92@gmail.com
Gravatarid:57db1afcce141efc81193425d4a5bbf0
Github: nenodias
Linkedin: nenodias92
Facebook: nenodias
Summary: Tutorial básico de como configurar o python 3.5 com o openshift + flask + gunicorn, utilizando o diy (Do It Yourself), carregando um cartridge customizado ...

Configurando OpenShift com Python 3.5

### Introdução

O [OpenShift](https://www.openshift.com/) é uma plataforma de PasS que possibilita aos desenvolvedores "subir" aplicações na nuvem de uma maneira simples e rápida. Ele funciona a partir de gears(engrenagens) que representam máquinas que irão rodar as aplicações. Dentro de cada gear é possível instalar serviços, os são chamados de "cartridges".

Existem 3 planos:

+ Online (gratuito, com três gears)
+ Enterprise (pago com suporte)
+ Origin (versão da comunidade e pode ser utilizado livremente)

Um problema que me deparei ao utilizar o Openshift é que ele não possui um cartridge com Python3.5. Porém existe uma forma um pouco mais complicada de resolver esse problema.

Após fazer seu cadastro no OpenShift e instalar o [client tools](https://developers.openshift.com/managing-your-applications/client-tools.html) que contém as ferramentas necessárias para configurar nossa aplicação.

Após tudo isso vamos colocar a mão na massa, abra seu terminal e vamos lá.

### Criando a aplicação

``` shell
rhc app create <app-name> https://raw.githubusercontent.com/Grief/openshift-cartridge-python-3.5/master/metadata/manifest.yml diy-0.1
```
Substituindo "<app-name>" pelo nome de sua aplicação.
O arquivo manifest.yml criado por Changaco(github) e "forkeado" por Grief(github) contém as configurações de um cartridge customizado que contém o python 3.5.

Para os curiosos o conteúdo do arquivo
```
---
Name: python
Cartridge-Short-Name: PYTHON
Display-Name: Only Python
Description: 'An embedded cartridge that provides only python, nothing else.'
Version: '3.5.0'
Versions: ['3.5.0', '2.7.11']
License: The Python License
License-Url: http://docs.python.org/3/license.html
Vendor: python.org
Cartridge-Version: 0.0.2
Cartridge-Vendor: praisebetoscience
Categories:
- service
- python
- embedded
Website: https://github.com/praisebetoscience/openshift-cartridge-python-3.5
Help-Topics:
  Developer Center: https://www.openshift.com/developers
Provides:
- python
Publishes:
Subscribes:
  set-env:
    Type: ENV:*
    Required: false
  set-doc-url:
    Type: STRING:urlpath
    Required: false
Scaling:
  Min: 1
  Max: -1
Version-Overrides:
  '2.7.11':
    Display-Name: Python 2.7
    License: The Python License, version 2.7
    Provides:
    - python-2.7
    - python
    - python(version) = 2.7
  '3.5.0':
    Display-Name: Python 3.5
    License: The Python License, version 3.5
    Provides:
    - python-3.5
    - python
    - python(version) = 3.5
```

Após isso sua aplicação já estárá executando, caso deseje acessar o endereço da mesma deverá ser http://<app-name>-<username>.rhcloud.com.
Você verá que a página do seu projeto não é nada mais do que o diy (Dot It Yourself), que é uma aplicação Ruby de exemplo que você pode alterar, e é o que vamos fazer.

Se você acessar o diretório do seu projeto verá que existe um diretório ".openshift", dentro desse diretório existe um outro diretório chamado "action_hooks", e dentro desse diretório existem dois arquivos "start" e "stop".

+ "<app-name>/.openshift/action_hooks/start"
+ "<app-name>/.openshift/action_hooks/stop"

Os dois arquivos são respectivamente os comandos para "subir" e "pausar" sua aplicação.

### Flask
Vamos criar um projeto de exemplo, bem simples, que apenas nos retorne a versão do python utilizada.
Primeiramente vamos criar nosso requirements.txt, com gunicorn e o flask.

"requirements.txt"
```
gunicorn
flask
```

Depois disso vamos criar o arquivo app.py que conterá nossa aplicação.

"app.py"
```
import sys
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return sys.version

```
 Após isso basta fazer o commit de suas alterações.

 ``` shell
 git add .
 git commit -am 'Minhas alterações'
 ```

Após isso você verá que sua aplicação não está rodando, pois ainda não alteramos os arquivos "start" e "stop".

### Configurando o Gunicorn no Start e Stop
O projeto diy do openshift nos deixa uma variável de ambiente $OPENSHIFT_DIY_IP com o IP da máquina, dessa forma podemos passar a variável e porta ao gunicorn.

"start"
``` shell
#!/bin/bash
nohup $HOME/python/usr/bin/pip3 install -r $OPENSHIFT_REPO_DIR/requirements.txt
cd $OPENSHIFT_REPO_DIR
nohup $HOME/python/usr/bin/gunicorn app:app --bind=$OPENSHIFT_DIY_IP:8080 |& /usr/bin/logshifter -tag diy &
```

A primeira linha é o [Shebang](https://pt.wikipedia.org/wiki/Shebang), o que significa que esse arquivo será executado pelo bash.
Na segunda linha vemos [nohup](https://pt.wikipedia.org/wiki/Nohup), que executa os comandos em uma sessão separada, vemos logo apóes vemos o uma chamada ao pip para instalar nossas dependências.
Na terceira linha vemos o nohup, e depois o gunicorn inicializa nossa aplicação flask.

Isso só funciona pois o cartridge customizado instala o python3.5 dentro da pasta home do servidor do openshift.

"stop"
``` shell
#!/bin/bash
source $OPENSHIFT_CARTRIDGE_SDK_BASH

# The logic to stop your application should be put in this script.
if [ -z "$(ps -ef | grep gunicorn | grep -v grep)" ]
then
    client_result "Application is already stopped"
else
    kill `ps -ef | grep gunicorn | grep -v grep | awk '{ print $2 }'` > /dev/null 2>&1
fi
```
Podemos ver que o comando ps procura algum processo do gunicorn, caso ele exista o kill será chamado.

Após isso, é só fazer o commit das alterações e você verá sua aplicação rodando.

Espero que o post ajude a quem quer subir alguma aplicação com python3.5 e só tem o heroku como opção.

### Referências
- [Imaster](https://www.profissionaisti.com.br/2015/04/openshift-paas-de-verdade/)
