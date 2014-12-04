Title: Desenvolvendo com Bottle - Parte 1
Slug: desenvolvendo-com-bottle-parte-1
Date: 2014-12-03 15:05
Tags: bottle,python
Author: Eric Hideki
Email:  eric8197@gmail.com
Github: erichideki
Site: http://ericstk.wordpress.com
Twitter: erichideki
Category: begginers, bottle, tutorial

# Texto originalmente escrito em:

[https://realpython.com/blog/python/developing-with-bottle-part-1/]

Eu amo [bottle]. Ele é simples, rápido e poderoso micro-framework Python, perfeito para pequenas aplicações web e rápida prototipação. É também perfeita ferramenta de ensino para aqueles que estão começando agora com desenvolvimento web.

Vamos dar um rápido exemplo.

> Este tutorial espera que você esteja em um ambiente baseado em Unix - e.g, Mac OSX, sistemas Linux, ou no Linux rodando uma Virtual Machine no Windows. Eu irei estar usando Sublime Text 2 como meu editor de texto.

#Começando

Primeiramente, vamos criar um diretório para trabalhar:

```
$ mkdir bottle
$ cd bottle
```

Depois, você precisa ter pip, virtualenv, e git instalados.

[virtualenv] é uma ferramenta Python que torna fácil gerenciar módulos Python necessários para um particular projeto. Ele também mantém os módulos isolados para que não entre em conflito com outros projetos.[pip], entretanto, é um gerenciador de pacotes usado para gerenciar a instalaçao de bibliotecas e módulos.

Para ajudar com a instalação do pip(e todas as dependências) em um ambiente Unix, siga as instruções nesse [Gist]. Se você está no Windows, por favor veja esse [vídeo] para sua ajuda.

Uma vez com o pip instalado, execute os seguintes comandos para instalar o virtualenv:

```
$ pip install virtualenv
```

Agora nós podemos facilmente configurar nosso ambiente local executando:

```
$ virtualenv --no-site-packages testenv
$ source testenv/bin/activate
```

Instalar o Bottle:

```
$ pip install bottle
```

Agora criamos o arquivo *requirements.txt*, que permitirá você instalar os exatos módulos e dependências iguais no caso de você querer usar esse aplicativo em qualquer outro local. Clique [aqui] para aprender mais.

```
pip freeze > requirements.txt
```

Finalmente, vamos colocar nossa aplicação em um controle de versão usando Git. Para mais informações sobre o Git, por favor veja esse [site], que inclui instruções de instalação.

```
$ git init
$ git add .
$ git commit -m "initial commit"
```

##Escrevendo sua aplicação

Agora estamos preparados para escrever nossa aplicação com Bottle. Crie seu arquivo de aplicação, *app.py*, que irá carregar todo o nosso primeiro aplicativo:

```
import os
from bottle import route, run, template

index_html = '''Minha primeira aplicação! Por {{ autor }}'''

@route('/:qualquer')
def alguma_coisa(qualquer=''):
    return template(index_html, autor=qualquer)

@route('/')
def index():
    return template(index_html, autor='Seu nome aqui:')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
```

Salve o arquivo.

Agora você pode executar sua aplicação localmente:

```
$ python app.py
```

Você poderá ser capaz de conectar a [http://localhost:8080/abc] e ver sua aplicação rodando!
Mude ```abc``` para seu nome. Dê refresh no navegador.

#O que tá acontecendo?

1. O decorator ```@route``` diz que a aplicação deve interpretar o caminho depois do ```/``` como variável ```qualquer```.
2. Isto é passado para a função sendo como um argumento```(def alguma_coisa(qualquer='')```.
3. Nós então passamos isto para a função do template sendo um argumento(```autor=qualquer```)
4. O template então renderiza a variável autor com ```{{ autor }}```

#Shell script

Quer começar de forma rápida? Crie um inicializador de aplicação em poucos segundos usando o Shell script.

```
mkdir bottle
cd bottle
pip install virtualenv
virtualenv --no-site-packages testenv
source testenv/bin/activate
pip install bottle
pip freeze > requirements.txt
git init
git add .
git commit -m "initial commit"

cat >app.py <<EOF
import os
from bottle import route, run, template

index_html = '''Minha primeira aplicação wweb! Por {{=<% %>=}}{{ autor }}<%={{ }}=%>'''

@route('/:qualquer')
def alguma_coisa(qualquer=''):
   return template(index_html, autor=qualquer)

@route('/')
def index():
   return template(index_html, autor='Seu nome aqui:')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
EOF

chmod a+x app.py

git init
git add .
git commit -m "Updated"
```

Baixe esse script através dessa [Gist-list], e então execute o seguinte comando:

```
$ bash bottle.sh
```

#Próximos passos

A partir desse ponto, é tão fácil adicionando uma nova ```@route```-decorated functions() para criar novas páginas, assim como fizemos com essas duas páginas.

Criar o HTML é simples: Nessa aplicação, nós apenas adicionamos HTML na mesma linha e arquivo.Isto é fácil de modificar(usando, por exemplo, ```open('index.html').read())``` para ler o template de um arquivo.

Referências para a [documentação] do Bottle para mais informações.

[https://realpython.com/blog/python/developing-with-bottle-part-1/]:https://realpython.com/blog/python/developing-with-bottle-part-1/
[bottle]:http://bottlepy.org/docs/stable/
[virtualenv]:https://pypi.python.org/pypi/virtualenv
[pip]:https://pypi.python.org/pypi/pip
[Gist]:https://gist.github.com/mjhea0/5692708
[vídeo]:https://www.youtube.com/watch?v=MIHYflJwyLk
[aqui]:https://pip.pypa.io/en/latest/user_guide.html#requirements-files
[site]:http://git-scm.com/book/pt-br/v1/Primeiros-passos-No%C3%A7%C3%B5es-B%C3%A1sicas-de-Git
[http://localhost:8080/abc]:http://localhost:8080/abc
[Gist-list]:https://gist.github.com/mjhea0/5784132
[documentação]:http://bottlepy.org/docs/dev/
