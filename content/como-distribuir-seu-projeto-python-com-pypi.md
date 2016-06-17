Title: Como distribuir sua aplicação Python com PyPI
Slug: como-distribuir-sua-aplicacao-python-com-pypi
Date: 2016-06-17 13:47:24
Category: Python
Tags: python, pypi, tutorial, desenvolvimento, pypi, pip
Author: Michell Stuttgart
Email: michellstut@gmail.com
Github: mstuttgart
Linkedin: michellstut
Facebook: michell.stuttgart
Site: http://codigoavulso.com.br

Imagine a seguinte situação: você passou alguns dias (ou mesmo meses) desenvolvendo uma módulo python, escreveu testes, implementou funcionalidades e depois de alguns ajustes, chegou a hora de liberar seu software para que outros desenvolvedores possam utilizá-lo. Qual o melhor modo de distribuí-lo?

Caro leitor, se você costuma programar em Python (seja profissionalmente ou não) provavelmente já instalou outros módulos usando o [PyPI](https://pypi.python.org/pypi), através do comando abaixo:

```bash
pip install nomedomodulo
```

Não seria interessante usar o mesmo método para distribuir a sua aplicação? Sim? Então mãos a obra.

### Sobre o PyPI - Python Package Index

O site [PyPI](https://pypi.python.org/pypi), é um repositório de *softwares* desenvolvidos na linguagem Python. Em outras palavras, ele garante que seu pacote Python sempre esteja disponível para a instalação. O seu funcionamente é simples, porém algumas configurações inicias devem ser feitas para que tudo funcione corretamente.

### Crie uma conta

Primeiramente, para distribuir seus pacotes usando o [PyPI](https://pypi.python.org/pypi), precisamos criar uma conta em ambos os sites:

* [PyPI Live](https://pypi.python.org/pypi?%3Aaction=register_form)
* [PyPI Test](https://testpypi.python.org/pypi?%3Aaction=register_form)

Recomendo que você utilize o mesmo email e senha para ambos os sites. Posteriormente, isso tornará mais fácil o processo de configuração.

###  Configurando o ambiente

O próximo passo é criar um arquivo `.pypirc` em sua `home`. Esse arquivo contem informações de auteticação, tanto para o [PyPI Live](https://pypi.python.org/pypi) quando para o [PyPI Test](https://testpypi.python.org/pypi).

```bash
touch ~/.pypirc
```

Apesar de não ser obrigatório a criação desse aquivo, ele facilita muito nosso trabalho, uma vez que você não precisaremos inserir nosso email e senha toda vez que formos enviar nosso código para o [PyPI Live](https://pypi.python.org/pypi).

Abra o arquivo `.pypirc` em seu editor de texto favorito, e insira as informações abaixo.

```bash
[distutils]
index-servers =
  pypi
  pypitest

[pypi]
repository=https://pypi.python.org/pypi
username=seu_nomedeusuario
password=sua_senha

[pypitest]
repository=https://testpypi.python.org/pypi
username=seu_nomedeusuario
password=sua_senha

```
Em *username* insira seu nome de usuário e *password*, insira sua senha. Faça isso tanto para o `pypi` quanto para o `pypitest`.

Um observação importante é que, caso a sua senha possua espaço, não a coloque entre aspas. Por exemplo, se a sua senha for "batuque da viola doida", coloque exatamente o mesmo texto em *password*.


```bash
password=batuque da viola doida
```

### Preparando o seu módulo Python

Todo pacote distribuído pelo [PyPI](https://pypi.python.org/pypi) precisa ter uma arquivo `setup.py` em seu diretório raiz. E se seu projeto também usa um arquivo *readme* em *markdown* (normalmente chamado `README.md`) você também precisará criar um arquivo chamado `setup.cfg`no diretório raiz do módulo.

Como exemplo, iremos utilizar o módulo [codigo_avulso_test_tutorial](https://github.com/mstuttgart/codigo-avulso-test-tutorial) que criei para ser utilizado como exemplo em nossos tutoriais. Assim, temos a seguinte estrutura básica de diretórios:

```bash
.
├── codigo_avulso_test_tutorial
│   ├── circulo.py
│   ├── figura_geometrica.py
│   ├── __init__.py
│   └── quadrado.py
├── LICENSE
├── README.md
├── setup.cfg
├── setup.py
└── test
    ├── circulo_test.py
    ├── figura_geometrica_test.py
    ├── __init__.py
    └── quadrado_test.py

```
Aqui, o que nos interessa são os arquivos `setup.py` e `setup.cfg`. Dentro do arquivo `setup.py` temos várias informações sobre nossa aplicação que serão usadas pelo [PyPI](https://pypi.python.org/pypi).

```python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='codigo-avulso-test-tutorial',
    version='0.1.1',
    url='https://github.com/mstuttgart/codigo-avulso-test-tutorial',
    license='MIT License',
    author='Michell Stuttgart',
    author_email='michellstut@gmail.com',
    keywords='tutorial test unittest codigoavulso',
    description=u'Tutorial de teste unitário em Python para o blog Código Avulso',
    packages=['codigo_avulso_test_tutorial'],
    install_requires=[],
)
```
O nome de cada *tag* é autoexplicativo, então não vou entrar em detalhes. Basta você usar o código acima e substituir com os dados do seu pacote.

O próximo passo é adicionar o seguinte conteúdo no arquivo `setup.cfg` (caso você o tenha criado).

```bash
[metadata]
description-file = README.md
```
Esse arquivo irá dizer ao [PyPI](https://pypi.python.org/pypi) onde seu arquivo *readme* está.

### Publicando sua aplicação Python

Agora iremos estudar os passos para enviar nossa aplicação para [PyPI](https://pypi.python.org/pypi), para que ela fique disponível para ser instalada através do `pip`.

#### Enviando para PyPI Test

Primeiramente, vamos registrar nossa aplicação no [PyPI Test](https://testpypi.python.org/pypi). Esse passo serve para verificarmos se está tudo certo com nosso pacote e também validar se já não existe outro módulo com o mesmo nome.
Registramos nossa aplicação com o seguinte comando:

```bash
python setup.py register -r pypitest
```

Se tudo ocorrer bem teremos a seguinte saída (Server responde 200):

```bash
running register
running egg_info
creating codigo_avulso_test_tutorial.egg-info
writing codigo_avulso_test_tutorial.egg-info/PKG-INFO
writing top-level names to codigo_avulso_test_tutorial.egg-info/top_level.txt
writing dependency_links to codigo_avulso_test_tutorial.egg-info/dependency_links.txt
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
reading manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
running check
Registering codigo-avulso-test-tutorial to https://testpypi.python.org/pypi
Server response (200): OK
```
Caso exista outro pacote com o mesmo nome, teríamos de escolher outro nome para o nosso pacote. Agora com nosso pacote devidamente registrado, executamos o comando abaixo para que o pacote seja enviado para o [PyPI Test](https://testpypi.python.org/pypi).

```bash
python setup.py sdist upload -r pypitest
```

Se tudo ocorrer bem (Server responde 200), você verá uma saída semelhante a esta e já poderá ver sua aplicação na lista do [PyPI Test](https://testpypi.python.org/pypi).

```bash
running sdist
running egg_info
writing codigo_avulso_test_tutorial.egg-info/PKG-INFO
writing top-level names to codigo_avulso_test_tutorial.egg-info/top_level.txt
writing dependency_links to codigo_avulso_test_tutorial.egg-info/dependency_links.txt
reading manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
writing manifest file 'codigo_avulso_test_tutorial.egg-info/SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt

.
.
.

creating dist
Creating tar archive
removing 'codigo-avulso-test-tutorial-0.1.1' (and everything under it)
running upload
Submitting dist/codigo-avulso-test-tutorial-0.1.1.tar.gz to https://testpypi.python.org/pypi
Server response (200): OK

```

#### Enviando para PyPI Live

Agora é pra valer. Executamos o mesmo passos para o [PyPI Test](https://testpypi.python.org/pypi).

```bash
python setup.py register -r pypi
```

Tudo ocorrendo bem, enviamos nosso pacote:

```bash
python setup.py sdist upload -r pypi
```

Parabéns! Com esse ultimo passo, publicamos o nosso pacote Python com sucesso! Agora ele pode ser [visualizado na lista de aplicações](https://pypi.python.org/pypi/codigo-avulso-test-tutorial/0.1.1) do [PyPI](https://pypi.python.org/pypi) e ser instalado usando `pip`.

```bash
pip install nomedopacote
```

Ou, para o nosso exemplo:

```bash
pip install codigo_avulso_test_tutorial
```

### Conclusão

É isso pessoal. Neste tutorial vimos como distribuir nossa aplicação Python, desde a crição na conta no [PyPI](https://pypi.python.org/pypi) até o registro e *upload* da nossa aplicação. Espero que tenham gostado e caso tenham alguma dúvida, deixem um comentário.

Obrigado pela leitura e até o próximo tutorial.

### Referências

* [Documentação oficial](https://wiki.python.org/moin/CheeseShopTutorial#Submitting_Packages_to_the_Package_Index)
* [How to Host your Python Package on PyPI with GitHub](https://www.codementor.io/python/tutorial/host-your-python-package-using-github-on-pypi)
* [How to submit a package to PyPI](http://peterdowns.com/posts/first-time-with-pypi.html)
