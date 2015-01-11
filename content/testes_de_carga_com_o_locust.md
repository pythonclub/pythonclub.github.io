Title: Testes de carga com o Locust
Slug: testes-de-carga-com-o-locust
Date: 2015-01-11 18:00
Tags: locust,web,tutorial,test,load-testing
Author: Diego Garcia
Email:  drgarcia1986@gmail.com
Github: drgarcia1986
Site: http://www.codeforcloud.info
Twitter: drgarcia1986
Category: load-testing



<figure style="float:right;">
<img style="border-radius: 50%;" src="/images/drgarcia1986/the_locust.jpg">
</figure>
</br>
Quanto de carga sua aplicação web aguenta? Se conseguiu responder essa pergunta, como você fez para medir esse desempenho? Se você não conseguiu responder nenhuma das questões anteriores, ou apenas uma, ou até mesmo respondeu as duas mas em algum momento utilizou a palavra _complicado_ para descrever como testou, chegou a hora de resolver esse problema de uma forma muito simples.

<!-- MORE -->

> Esse texto foi publicado originalmente em meu blog, no endereço [http://www.codeforcloud.info/](http://www.codeforcloud.info/).

## Locust
O Locust é uma ferramenta open source escrita em python para testes de carga em aplicações web (independente da técnologia). A principal caracteristica do Locust é a forma como são escritos os testes, simples códigos python. Com poucas linhas de código é possível escrever testes de carga que vão realmente colocar sua aplicação em um campo de batalha.

### Instalação
Para quem já usa python a facilidade de uso já começa na instalação, basta utilizar o comando ``pip install locustio`` e a instalação está feita.
Para instalar o Locust em um ambiente unix com _virtualenv_, basta criar o virtualenv:
```bash
user@machine:~/locust$ virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip...done.
```
Ativar o virtualenv
```bash
user@machine:~/locust$ source venv/bin/activate
(venv)user@machine:~/locust$
```
E instalar o Locust
```bash
(venv)user@machine:~/locust$ pip install locustio
```
Para confirmar se o Locust está instalado, use o comando ``locust`` com a opção ``-V``
```bash
(venv)user@machine:~/locust$ locust -V
[2015-01-08 22:59:28,251] machine/INFO/stdout: Locust 0.7.2
```
> Não se preocupe se aparecerem mensagens de _warning_ alertando sobre a ausência do _zmq_, a ausência desse pacote não afeta nossa demostração.

### Aplicação para testes
Para demonstrar a utilização do Locust, vamos criar um simples webservice que realiza conversões de tempo (por ex. _hora para segundo_).

Na criação desse webservice, utilizaremos o **Flask** por ser um dos frameworks mais simples e utilizados atualmente. Como o Locust utiliza o Flask internamente, ele já está instalado em nosso virtualenv.

> Como o foco do post não é falar do _Flask_, não entrarei em detalhes do framework, se você não está familiarizado com ele, recomendo a leitura deste [excelente artigo](/what-the-flask-pt-1-introducao-ao-desenvolvimento-web-com-python) do Bruno Rocha.

Crie um arquivo chamado **converter.py** com o seguinte código:
```python
from flask import Flask


converter = {'DH': lambda d: d * 24,     # day to hours
             'HM': lambda h: h * 60,     # hour to minutes
             'MS': lambda m: m * 60,     # minute to seconds
             'DM': lambda d: d * 1440,   # day to minutes
             'DS': lambda d: d * 86400,  # day to seconds
             'HS': lambda h: h * 3600}   # hour to seconds

app = Flask(__name__)

@app.route('/<rule>/<int:value>')
def conversion(rule, value):
	try:
		return str(converter[rule.upper()](value))
	except KeyError:
		return "Rule for conversion not found", 404


if __name__ == "__main__":
    app.run()
```
Para testar essa aplicação basta inicia-la:
```bash
(venv)user@machine:~/locust$ python converter.py
 * Running on http://127.0.0.1:5000/
```
E realizar uma requisição:
```http
curl http://127.0.0.1:5000/hm/3
180
```

### Criando as _Locust Tasks_
Agora que já temos o que testar, vamos finalmente escrever nosso script Locust. Como eu disse anteriormente, os scripts Locust são scripts python, sem nenhum segredo. 

Os testes são baseados em **Tasks** que são criadas em uma classe que herda da classe ``TaskSet`` do Locust. Na classe _TaskSet_ o que determina se um método é uma _task_ é a presença do decorator ``@task``.

O Locust trabalha com o conceito de requests baseados em clientes com caracteristicas especificas. O principal atributo das classes de cliente _Locust_ é o atributo ``task_set``, que recebe a classe onde as tasks de teste estão especificadas. Como o foco é o teste de aplicações web, o protocolo em questão é o protocolo **HTTP**, sendo assim, a classe base para criação desses _clientes_ é a classe ``HttpLocust``.

Não se assuste, como estamos falando de **Python**, a explicação é praticamente maior que o código :). 

Para testar alguns métodos de nosso webservice, crie um arquivo chamado **locust_script.py** com o código a seguir.

```python
from locust import TaskSet, task, HttpLocust

class ConverterTasks(TaskSet):
    @task
    def day_to_hour(self):
        self.client.get('/dh/5')
        
    @task
    def day_to_minute(self):
        self.client.get('/dm/2')
        

class ApiUser(HttpLocust):
    task_set = ConverterTasks
    min_wait = 1000
    max_wait = 3000
```
No código acima, criamos a classe ``ConverterTasks`` onde especificamos nossas tasks para os testes através do decorator ``@task`` e a class ``ApiUser`` onde especificamos o nosso cliente Locust do tipo ``HttpLocust``, preenchendo o atributo ``task_set`` com a classe ``ConverterTask``.

Como nosso cliente Locust é do tipo **HttpLocust**, foi possível utilizar o objeto ``self.client`` em nosso **task_set**. Note que o objeto _self.client_ da classe _ConverterTasks_ consiste em um cliente http.

Os atributos ``min_wait`` e ``max_wait`` especificam o tempo mínimo e máximo em milisegundos que o teste deve aguardar entre a execução de uma task e outra. O valor padrão desses atributos é _1000_ (1 segundo).

### Executando os testes
Com o script locust escrito, é chegada a hora da mágica, vamos finalmente ver o Locust em ação. Se certifique que seu webservice está no ar e inicie seu script Locust com o seguinte comando:
```bash
(venv)user@machine:~/locust$ locust -f locust_script.py –H http://127.0.0.1:5000
```
A opção ``-f`` específica o arquivo com script Locust e a opção ``-H`` específica o endereço do webservice que será testado.
Ao executar esse comando, o Locust será iniciado na porta **8089** (porta padrão que pode ser alterada através da opção ``-P``).

Ao abrir no browser a url http://127.0.0.1:8089 será apresentada a seguinte tela:

![locust](/images/drgarcia1986/locust_inicial.png)

O campo **Number of users to simulate** é referente a quantidade de usuários simultâneos que serão utilizados para o teste, já o campo **Hatch rate** é referente a quantidade de usuários que serão adicionados ao teste por segundo (até atingir o numéro de usuários específicado na opção anterior). Específique as opções anteriores e clique em **Start swarming** para que os testes sejam iniciados e seja apresentada a seguinte tela.

![locust](/images/drgarcia1986/locust.png)

Talvez as informações mais importantes apresentadas nessa tela é o **RPS** (request per seconds) e os **failures**.
Note que os resultados são apresentados por cada _Task_ e são totalizados no final da listagem.

### Definindo _peso_ para os teste
É possível determinar o _peso_ de uma _task_ através do parâmetro opcional **weight** do decarator ``@task``. Por exemplo, imagine que no cenário real são mais requisições para conversão de _dias para minutos_ do que de _dias para horas_, sendo assim nossos testes devem seguir essa mesma lógica.

```python
from locust import TaskSet, task, HttpLocust

class ConverterTasks(TaskSet):
    @task(3)
    def day_to_hour(self):
        self.client.get('/dh/5')
        
    @task(6)
    def day_to_minute(self):
        self.client.get('/dm/2')
        

class ApiUser(HttpLocust):
    task_set = ConverterTasks
    min_wait = 1000
    max_wait = 3000
```

Da forma como foi especificado, para cada requisição de conversão de _dia para horas_, serão executadas duas de _dia para minutos_.

### Utilizando outros Verbos HTTP
Nesse nosso exemplo só utilizamos o método http _GET_, até mesmo porque nosso webservice só possui métodos GET, porém, é possível utilizar os outros verbos HTTP, por exemplo:

```python
from locust import TaskSet, task, HttpLocust

class RegistersTasks(TaskSet):
    @task
    def create_person(self):
        self.client.post('/person', {'name': 'Foo', 'email': 'foo@bar.net'})
        
    @task
    def create_group(self):
        self.client.post('/group', {'name': 'Bar'})
        
class WebsiteUser(HttpLocust):
    task_set = RegistersTasks
    min_wait = 1000
    max_wait = 3000        
```

O cliente HTTP presente no objeto ``self.client`` é baseado na biblioteca [Requests](http://docs.python-requests.org/en/latest/), sendo assim, os métodos http (GET, POST, PUT, DELETE, OPTIONS) estão disponiveis.

### Testando com valores dinámicos
No teste do conversor de tempo, utilizamos valores fixos, porém, para se apróximar mais da realidade, o ideal seria testar com valores aleatórios. Como estamos falando de código Python, isso é muito simples, bastar alterar de:
```python
self.client.get('/dh/5')
```
para:
```python
from random import randint


self.client.get('/dh/%d' % randint(1, 10))
```
Mas isso geraria um problema, pois o Locust agrupa o relatório de testes por url, como estamos realizando até 10 chamadas diferentes para o mesmo recurso, teriamos até 10 chamadas diferentes sendo listas e contabilizadas separadamente.

![locust](/images/drgarcia1986/locust_random.png)

Para resolver esse problema, podemos nomear os requests independente da url, atráves do parâmetro ``name`` dos métodos do client HTTP. Sendo assim nosso código poderia ficar da seguinte forma:

```python
from locust import TaskSet, task, HttpLocust
from random import randint

class ConverterTasks(TaskSet):
    @task
    def day_to_hour(self):
        self.client.get('/dh/%d' % randint(1, 10), name='/dh/[int]')
        
    @task
    def day_to_minute(self):
        self.client.get('/dm/%d' % randint(1, 10), name='/dm/[int]')
        

class ApiUser(HttpLocust):
    task_set = ConverterTasks
    min_wait = 1000
    max_wait = 3000
```

Com isso o relatório volta a ser apresentado da maneira esperada.

![locust](/images/drgarcia1986/locust_name.png)

### Sessão de usuário
O cliente http da classe ``HttpLocust`` preserva os cookies entre os requests, possibilitando realizar logins e consumir métodos remotos que dependem de uma sessão de usuário ativa.

Para validar esse conceito, criaremos uma aplicação simples que possui login de usuário e um recurso protegido pela sessão. Somente o necessário para ver o Locust em ação.

```python
from flask import Flask, session, request, redirect, url_for, abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a7b05c4e06fe0502af4a3d42dd41327b'

users = {'john': {'password': 'mypass', 'name': 'John Lee'},
         'bob': {'password': 'secret', 'name': 'Robert Brown'}}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = users.get(request.form['username'])
        if not user:
            return 'User not found', 404
        if user['password'] != request.form['password']:
            return 'Wrong password', 401
        session['user'] = user
        return redirect(url_for('home'))
    else:  # GET
        return '''
            <form action="" method="POST">
                <p>User <input type=text name=username></p>
                <p>Pass <input type=password name=password></p>
                <p><input type=submit value=SignIn></p>
           </form>
        '''

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user' in session:
        return '''
            <h1>Welcome %s</h1>
            <p>For logout click <a href=%s>here</a></p>
        ''' % (session['user']['name'], url_for('logout'))
    else:
        abort(401)

@app.route('/')
def index():
    return '''
        <h1>Flask with session :)</h1>
        <p>Click <a href=%s>here</a> to login page</p>
    ''' % url_for('login')


if __name__ == '__main__':
    app.run()
```
A aplicação representada no código acima consiste em uma página inicial (``/``), uma página de login (``/login``), uma página de logout (``/logout``) e uma página home do usuário (``/home``) que só está acessivel para usuários logados. Obviamente esse é só um exemplo didático. 

Se criarmos um script Locust para testar essa aplicação e nele não realizaros o login do usuário, teriamos uma série de falhas para consumir o método remoto ``/home``.

![locust](/images/drgarcia1986/locust_session_fail.png)

Porém a classe ``TaskSet`` do Locust possui o método ``on_start`` que consiste no método que será executado (apenas uma vez) antes do cliente Locust iniciar as tasks. Será nele que iremos realizar o _login_ do usuário.

```python
from locust import TaskSet, task, HttpLocust


class SessionTasks(TaskSet):
    def on_start(self):
        self.client.post('/login', {'username': 'john', 
                                    'password': 'mypass'})

    @task(1)
    def home(self):
        self.client.get('/home')

    @task(4)
    def index(self):
        self.client.get('/')


class WebsiteUser(HttpLocust):
    task_set = SessionTasks
    min_wai=1000
    max_wait=3000
```
Como estamos realizando o login do usuário sempre que o cliente Locust inicia suas _tasks_, os cookies de sessão já estarão armazenados nos controles do objeto ``self.client``, com isso, é possível testar até mesmo os métodos que dependem de autenticação para serem consumidos.

![locust](/images/drgarcia1986/locust_session_success.png)

### Escalando os testes
O Locust é baseado em eventos, graças a isso é possível simular milhares de usuários concorrentes na mesma máquinas, porém em alguns casos esse numero não é o suficiente. Pensando nessa necessidade, o Locust possibilita trabalhar de forma distribuida, através do conceito de **Master** e **Slave**.

> Segundo a documentação do Locust, recomenda-se instalar a biblioteca [ZeroMQ](http://zeromq.github.io/pyzmq/index.html) para melhorar o desempenho dos testes distribuidos. Essa á razão do _warning_ no momento da execução.

Para iniciar uma instância _master_ do Locust, basta utilizar o parâmetro ``--master``.

```bash
(venv)user@machine:~/locust$ locust -f locust_script.py -H http://127.0.0.1:5000 --master
```
Essa instancia do Locust não irá simular nenhum cliente para teste, apenas irá disponibilizar a interface web com as estatisticas dos testes realizados e irá aguardar a conexão dos _slaves_, poís esses serão os responsáveis pela realização dos testes.

Agora, para iniciar uma instância _slave_ do Locust, são utilizados dois parâmetros, o ``--slave`` que determina que essa instância é um slave e o parâmetro ``--master-host`` com a localização do _master_.

```bash
(venv)user@machine:~/locust$ locust -f locust_script.py --slave --master-host=192.168.0.15
```
> Tanto a máquina **master** quanto as máquinas **slave** precisam ter o Locust instalado e possuir uma cópia do script de testes que será executado de forma distribuida.

Com as instâncias slaves iniciadas, basta acessar no browser o Locust (da máquina _master_) e ver os testes em ação.

![locust](/images/drgarcia1986/locust_distributed.png)

**Referências**<br>
[Site Oficial](http://locust.io/)<br>
[Documentação](http://docs.locust.io/en/latest/index.html)
