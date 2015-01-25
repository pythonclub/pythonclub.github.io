Title: Publicando seu Hello World no Heroku
Slug: publicando-seu-hello-world-no-heroku
Date: 2015-01-25 11:30
Tags: web,tutorial,heroku,flask,git,deploy
Author: Diego Garcia
Email:  drgarcia1986@gmail.com
Github: drgarcia1986
Site: http://www.codeforcloud.info
Twitter: drgarcia1986
Linkedin: drgarcia1986
Category: heroku



<figure style="float:left;">
<img style="border-radius: 50%;" src="/images/drgarcia1986/heroku.png">
</figure>
</br>

O que é uma aplicação web se ela não está efetivamente na web? Não precisa ser efetivamente uma aplicação de produção, as vezes precisamos validar protótipos, compartilhar ferramentas online ou até mesmo publicar uma aplicação pela satisfação de publicar. Para isso não é necessário se preocupar com infraestrutura ou gastar dinheiro em aluguel de servidores. Existem diversas opções gratuitas e simples para isso, uma delas é o **Heroku**.

<!-- MORE -->

## Heroku

O Heroku é uma das opção mais populares de [plataforma como serviço](http://pt.wikipedia.org/wiki/Plataforma_como_servi%C3%A7o) que suporta app escritos em diversas linguagens, dentre elas, **Python**. Nele existem [planos pagos e gratuitos](https://www.heroku.com/pricing) de acordo com o uso do serviço. 
Para conhecer um pouco do processo de _deploy_ do heroku, criaremos um simples **Hello World** utilizando **Flask**.

### O que você irá precisar?
#### Uma conta no Heroku
Não se preocupe, você pode criar uma conta gratuita e usufruir do serviço sem problemas. Entre no [_Sign up_](https://signup.heroku.com/) e crie uma conta informando seu nome e seu e-mail.

#### Git
O Heroku utiliza o Git para realizar o deploy dos app. Você verá mais adianta que um simples `git push` é o suficiente para enviarmos nosso app para o heroku.

#### Python, Pip, VirtualEnv
Bem, você vai criar sua aplicação em python não? Além da boa organização e isolamento para seu ambiente proporcionado pelo **virtualenv**, manter seu app em um virtualenv proporciona algumas praticidades.

### Instalando o Toolbet
O **Toolbet** é uma poderosa ferramente de linha de comando do heroku. É através dela que iremos criar nosso app no heroku.
No ubuntu (ou outras distribuições baseadas no debian) para instalar não poderia ser diferente, basta usar o todo poderoso `apt-get`.
```bash
user@machine:~/$ sudo apt-get install heroku 
```

> Se você estiver usando outro sistema operacional, você pode baixar o instalador direto do [site oficial](https://toolbelt.heroku.com/).

Após a instalação, faça o login no heroku através do toolbet para se certificar que tudo deu certo.
```bash
user@machine:~/$ heroku login
Enter your Heroku credentials.
Email: your@email.com
Password (typing will be hidden): 
Authentication successful.
```

### Preparando o App
Iremos agora criar nosso app que será compartilhado com o mundo. Nesse processo não tera nada de anormal, apenas a criação de uma aplicação web como qualquer outra.
Criaremos um diretório chamado `heroku_hello_world`.
```bash
user@machine:~/$ mkdir heroku_hello_world
user@machine:~/$ cd heroku_hello_world
user@machine:~/heroku_hello_world$
```
Nele iremos criar um `virtualenv` e ativa-lo.
```bash
user@machine:~/heroku_hello_world$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip...done.
user@machine:~/heroku_hello_world$ source venv/bin/activate
(venv)user@machine:~/heroku_hello_world$
```
Como disse anteriormente, iremos fazer o deploy de um simples **Hello World**. A intenção aqui é ter um **how-to** de como fazer o deploy de um app simples no heroku. Sendo assim, o **Flask** é uma excelente opção para isso. Para instalar o Flask em nosso virtualenv, use o `pip`.
```bash
(venv)user@machine:~/heroku_hello_world$ pip install flask
```
E finalmente vamos criar nosso _Hello World_ no arquivo `hello.py`.
```python
import os
from flask import Flask


app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello World</hi>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

```
Um detalhe importante fica por conta da variável `port`. No heroku não é possível subir o app na porta 5000 (porta default do Flask), mas o heroku seta a variável de ambiente `PORT` em seu ambiente, definindo em qual porta a aplicação deve rodar. Da maneira como está implementado nosso app, iremos conseguir podar tanto no heroku como localmente (através da porta 5000).

O heroku precisa conhecer as dependências de nosso app para que, no momento do deploy ele construa o ambiente de forma correta. Seguindo o padrão, o heroku procura pelas dependências através do arquivo `requirements.txt`. Como já isolamos nosso app em um virtualenv, basta utilizar o `pip freeze` para listar os packages instalados e direcionar a saida desse comando para o arquivo _requirements.txt_
```bash
(venv)user@machine:~/heroku_hello_world$ pip freeze > requirements.txt
```
### Preparando o Deploy
Iremos criar agora o arquivo `Procfile`, onde será escrito o comando que o heroku deverá usar para executar nosso app, basicamente o mesmo comando que utilizaríamos para rodar a aplicação localmente. Esse arquivo (assim como o _requirements.txt_) deverá estar na raiz da aplicação.

```bash
(venv)user@machine:~/heroku_hello_world$ echo "web: python hello.py" > Procfile
```
Agora que já possuímos todos os arquivos necessários, iremos iniciar o processo efetivo de deploy da aplicação. Como disse anteriormente, o heroku utiliza o git, sendo assim, nossa aplicação deverá estar em um repositório. Para isso, basta criar um repositório no diretório atual através do comando `git init`.
```bash
(venv)user@machine:~/heroku_hello_world$ git init
Initialized empty Git repository in /home/user/heroku_hello_world/.git/
```
Para não _sujar_ nosso repositório com arquivos desnecessários como por exemplo o virtualenv, crie um arquivo chamado `.gitignore` na raiz do repositório e nele iremos determinar quais arquivos o git deve ignorar.
```
*.pyc
venv
```
Vamos adicionar e commitar nossos arquivos nesse repositório através dos comandos `git add .` para adicionar todos os arquivos e `git commit` para criar nosso commit inicial.
```bash
(venv)user@machine:~/heroku_hello_world$ git add .
(venv)user@machine:~/heroku_hello_world$ git commit -m 'initial commit'
[master (root-commit) 33f63b5] initial commit
 4 files changed, 25 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 Procfile
 create mode 100644 hello.py
 create mode 100644 requirements.txt
(venv)user@machine:~/heroku_hello_world$
```
Agora vamos criar nosso app no heroku através do commando `heroku apps:create [nome do app]`. O nome da aplicação deverá ser único, pois o heroku utiliza o nome da aplicação para compor a url.
```bash
(venv)user@machine:~/heroku_hello_world$ heroku apps:create dg-hello-world
Creating dg-hello-world... done, stack is cedar-14
https://dg-hello-world.herokuapp.com/ | https://git.heroku.com/dg-hello-world.git
Git remote heroku added
```
> É importante ter realizado o login no heroku através do toolbet antes.

No resultado do comando `heroku apps:create` já são apresentadas duas das coisas mais importantes para nosso app, a url de acesso e repositório git onde deverá ser enviada nossa aplicação.

> Se você executou esse comando no mesmo diretório onde criou seu repositório do git, o heroku já cria o apontamento para o repositório remoto com o nome de `heroku`, não sendo necessário utilizar o comando `git remote add`.

Basicamente a url será no padrão `https://[nome do app].herokuapp.com/`.

### Efetivando o Deploy
Finalmente iremos realizar o deploy de nossa aplicação. Todos os passos anteriores foram passos preparatórios, o que significa que basta executá-los uma vez. Daqui em diante, para fazer o deploy de nosso app, basta enviar os commits do repositório local, para o repositório do heroku, através do comando `git push heroku master`.
```bash
(venv)user@machine:~/heroku_hello_world$ git push heroku master
```
E pronto, basta agora acessar a url do seu app (no caso desse exemplo foi [https://dg-hello-world.herokuapp.com/](https://dg-hello-world.herokuapp.com/)) e compartilhar com seus amigos =].

**Referências**<br \>
[(Heroku) Getting Started With Python](https://devcenter.heroku.com/articles/getting-started-with-python)<br />
[Deployment on the Heroku Cloud](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-the-heroku-cloud)
