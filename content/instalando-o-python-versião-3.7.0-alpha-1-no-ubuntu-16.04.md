Title: Instalando o Python versião 3.7.0 alpha 1 no Ubuntu 16.04
Slug: instalando-o-python-versião-3.7.0-alpha-1-no-ubuntu-16.04.md
Date: 2017-01-16 20:37:39
Category: Python
Tags: python,tutorial,install
Author: Welton Vaz
Email: weltonvaz@gmail.com
Github: weltonvaz
Linkedin: welton-vaz-de-souza
Facebook: weltonv
Site: http://www.weltonvaz.com/


Instalando o Python versião 3.7.0 alpha 1 no Ubuntu 16.04

A versão mais recente do Python, a 3.7.0 alfa 1, pode agora ser baixada ou clonada do GitHub facilmente. Um das linguagens mais fáceis de usar e aprender, o Python foi criada nos anos 90 e é elogiada por sua fácil leitura de código e necessidade de poucas linhas de código, comparada a outras linguagens. Agora mais proxima da comunidade no Github!

Depois disso os caminhos mudaram e conheci a profissão de Analista de Suporte e me ocupo disso desde então. Atualmente voltei a aprender uma linguagem, antes de mais nada, dei uma atualizada em lógica de programação, por sinal existe muitas boas apostilas e cursos gratuitos na Internet, dois caminhos muito bons.

Sobre linguagem de programação, existem várias. Neste quesito comecei a conhecer a linguagem Python e logo me apaixonei pela simplicidade, beleza e eficiência.

Depois disso tudo, você tem que instalar a linguagem em sua máquina. Por padrão, o Ubuntu 16.04 instala a versão 3.4, mas se você quiser, pode usar a versão 3.7.0a0

Obs.: Execute os comandos como root, ou usando o comando sudo no terminal.

```shell
git clone https://github.com/python/cpython
cd cpython
apt-get install build-essential libssl-dev libffi-dev python3-dev
./configure
make
make test
make install

# Se vc quiser usar váras versões do Python 2.7, 3.6 e 3.7 use o comando abaixo
make altinstall
```
Observação: via apt instalei as dependências do python, no caso o openssl, porque o pip apresenta vários problemas com certificados na instalação dos modúlos, mas, isso é para outro artigo

Depois disso é só entrar no interpretador:

```shell
python3.7
```
Tela do interpretador Python
```shell
Python 3.7.0a0 (default, Feb 16 2017, 18:59:44) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 

```
### Referências
Para ler mais sobre a linguagem: 
* [Python] - Site oficial da Linguagem Python!
* [This is Python version 3.7.0 alpha 1] - Git da proxima versão do Python, hospedado no Github!
* [Python-Brasil] - A comunidade Python Brasil reune grupos de usuários em todo o Brasil interessados em difundir e divulgar a linguagem de programação.

[Python]: <http://python.org>
[Python-Brasil]: <http://python.org.br/>
[This is Python version 3.7.0 alpha 1]:<https://github.com/python/cpython>