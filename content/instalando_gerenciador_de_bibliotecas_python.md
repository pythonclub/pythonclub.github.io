Title: Instalando e configurando o PIP - O gerenciador de pacotes Python
Slug: instalando-e-configurando-o-pip-o-gerenciador-de-pacotes-python
Date: 2015-10-05 02:22
Tags: python,pip,pacote,biblioteca,pypi
Author: Fábio C. Barrionuevo da Luz
Email:  bnafta@gmail.com
Github: luzfcb
Twitter: luzfcb
Gittip: luzfcb
Category: pip
Status: draft

<style>
.centralizar{

display: flex;   justify-content: center;   align-items: center;
}

</style>


# <a name="introducao" href="#introducao">Introdução</a>

> Tá com pressa, pule para a <a name="pule-para-instalacao" href="{filename}instalando_gerenciador_de_bibliotecas_python.md#instalando-o-pip">instalação</a>

Talvez quase toda a criança tenha sonhado com aquele carrinho de controle remoto ou aquela boneca fada que fala. Você passa o ano todo pedindo aos seus pais.

Chega o natal, dia 25, bem cedo você vê seu pai com um pacote brilhante e bem embalado, ele te fala: *só vai poder abrir de noite*.

São 23:50h, você passou o dia todo namorando o pacote brilhante e então finalmente sua mãe fala: *Pode abrir filho*. Você rasga com todas as suas forças a embalagem brilhante, pega o brinquedo e pensa: *vou brincar agora mesmo*. Coloca o brinquedo no chão, aperte os botões e ......... nada acontece.

Então a dura realidade lhe atinge: O brinquedo veio sem baterias. É meia noite e a essa hora, seu pai não vai sair para comprar baterias.

Seu sentimento é este:

<div class="centralizar">
<figure>
<img src="{filename}/images/luzfcb/crying-waterfalls.gif" alt="voce chorando" style="width:100%">
</figure>
</div>

Para a nossa felicidade, Python é um brinquedo sério para adultos, que já vem com as baterias incluidas para você poder começar a brincar o quanto antes.

Quando você instala a [maquina virtual Python](https://www.python.org/downloads/), ela já te entrega, por padrão, uma [grande quantidade e variadade de bibliotecas python](https://docs.python.org/3/library/index.html) para fazer quase tudo, citando alguns poucos, desde criar [arquivos de configuração](https://docs.python.org/3/library/configparser.html), criar [arquivos temporários](https://docs.python.org/3.5/library/tempfile.html), criar [interfaces graficas](https://docs.python.org/3/library/tk.html), [compactar e descompactar arquivos](https://docs.python.org/3/library/archiving.html) à [programação concorrente](https://docs.python.org/3/library/concurrency.html) e [programação assincrona](https://docs.python.org/3/library/asyncio.html).


Mas e se eu quiser adicionar foguetes e lasers no meu brinquedo novo? Vou ter que esperar o proximo ano?
A resposta é NÃO. Para isso, nós temos o [**pip**](https://pip.pypa.io)


# Indice:

1. [Mas que raios é *pip*?](#mas-que-raios-e-pip)
2. [Instalando o *pip*.](#instalando-o-pip)
	2.1 [Instalando o pip utilizando o módulo *ensurepip*.](#instalando-utilizando-ensurepip)
	2.2 [Instalando o pip utilizando o *get_pip*.py.](#instalando-o-pip-utilizando-o-get-pip)
	2.3 [Instalando o pip utilizando o gerenciador de pacotes da distribuição.](#instalando-o-pip-utilizando-o-gerenciador-de-pacotes-da-distribuicao)
3. [Utilizando o *pip*.](#utilizando-o-pip)
	- [ ](# )



# 1 <a name="mas-que-raios-e-pip" href="#mas-que-raios-e-pip">Mas que raios é *pip*?</a>

O **pip** é o gerenciador de pacotes oficial de Python. Ele permite, entre várias outras coisas, pesquisar, baixar, instalar, atualizar e desinstalar qualquer uma das mais de **66.625** bibliotecas Python disponiveis no [**PyPI**](https://pypi.python.org/pypi) (servidor oficial de pacotes python) ou fazer o mesmo para qualquer biblioteca python diponivel no Github, Gitlab, Bitbucket entre outros, que possua na raiz um arquivo chamado `setup.py`.

Para quem vem de outras linguagens de programação, no que tange o gerenciamento de dependencias, o **pip** é algo *similar* ao [Maven](https://maven.apache.org/) e [Gradle](https://gradle.org/) de Java, ou [Composer](https://getcomposer.org/) de PHP, ou [npm](https://www.npmjs.com/) de NodeJS, ou [gem](https://rubygems.org/pages/download) de Ruby .

# 2 <a name="instalando-o-pip" href="#instalando-o-pip">Instalando o pip</a>

Basicamente, há tres formas de instalar o **pip**:

2.1 - utilizar o módulo *ensurepip*
2.2 - utilizar o instalador *get-pip.py*
2.3 - utilizar o gerenciador de pacotes da distribuição(no caso de você estiver utilizando Linux)

### 2.1 <a name="instalando-utilizando-ensurepip" href="#instalando-utilizando-ensurepip">Instalando o **pip** utilizando o módulo *ensurepip*</a>

A instalação é simples. Basicamente abra o terminal e execute o comando abaixo:

```bash
sudo -H python3.4 -m ensurepip --upgrade
```

> Se você receber uma mensagem de erro: `/usr/bin/python3.4: No module named ensurepip` , muito provavelmente você deverá utilizar a [forma 2](#instalando-o-pip-utilizando-o-get-pip).
> Troque python3.4 pela sua versão do python, por exemplo: python2.7 ou python3.5



### 2.2 <a name="instalando-o-pip-utilizando-o-get-pip" href="#instalando-o-pip-utilizando-o-get-pip">Instalando o **pip** utilizando o *get_pip*.py</a>

Abra o link [https://bootstrap.pypa.io/get-pip.py](https://bootstrap.pypa.io/get-pip.py) e salve na pasta Home de seu usuario, abra o terminal no Linux/Mac ou CMD no Windows e execute o comando abaixo:

No Windows:

```bash
python3.4 get_pip.py --upgrade
```

No Linux e no Mac:

```bash
sudo -H python3.4 get_pip.py --upgrade
```

No Linux ou Mac, você pode executar o download e instalação em uma unica linha:

```bash
wget -H https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py; sudo -H python3.4 /tmp/get-pip.py --upgrade;
```


> **ATENÇÃO:** Você **Sempre** deve utilizar o ``sudo`` com o parametro ``-H`` (H maiúsculo) ao instalar pacotes python a nivel de sistema operacional, porque se não fizer assim, você terá problemas de permissão.

Eu particularmente, evito ao maximo instalar pacotes python a nivel de sistema operacional.

Os únicos pacotes python que eu sempre a nivel de sistema operacional são o proprio `pip`, o `virtualenv` e o `virtualenvwrapper`

Eu os instalo, em um unico comando:

```bash
wget -H https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py; sudo -H python3.4 /tmp/get-pip.py virtualenv virtualenvwrapper --upgrade;
```

> **Problemas conhecidos:** Infelizmente, `get-pip.py` sobreescreve o comando `pip`, vinculando-o a ultima versão do Python que você utilizou para executar o `get-pip.py`, ou seja, se você utilizou Python3.4 para executar `get-pip.py`, o comando `pip` vai instalar pacotes no Python3.4, se logo após, você executar `get-pip.py` utilizando Python2.7, `pip` vai instalar pacotes no Python2.7 e não mais no Python3.4.

> Esse problema já foi reportado nos issues [#2936](https://github.com/pypa/pip/issues/2936) e [#2973](https://github.com/pypa/pip/issues/2973).


Exemplo:
<script type="text/javascript" src="https://asciinema.org/a/27354.js" id="asciicast-27354" async></script>


### 2.3 <a name="instalando-o-pip-utilizando-o-gerenciador-de-pacotes-da-distribuicao" href="#instalando-o-pip-utilizando-o-gerenciador-de-pacotes-da-distribuicao">Instalando o **pip** utilizando o gerenciador de pacotes da distribuição</a>

> Esse é o método que eu menos recomendo, porque a grande maioria das distribuições Linux possui uma versão muito antiga do *pip* no repositório, geralmente a versão 1.5.3, o que é muito ruim porque, alem dessa versão do *pip* ser muito antiga (na data em que escrevi esse artivo a ultima versão disponivel era a 7.1.2), a versão 1.5.3 tem vários bugs chatos.


No Ubuntu, no Debian e derivados, você pode instalar o *pip* utilizando o apt-get. Abra o terminal e faça:

Primeiramente, atualize as informações sobre pacotes:

```bash
sudo apt-get update
```
e para instalar pip para Python2:

```bash
sudo apt-get install python-pip
```
ou para instalar pip para Python3:

```bash
sudo apt-get install python3-pip
```

# 3 <a name="utilizando-o-pip" href="#utilizando-o-pip">Utilizando o pip</a>

*pip* é uma ferramenta de linha de comando e um módulo python, então existem duas formas de utilizar o *pip*:

1. Utilizando o comando `pipX.Y` onde `X` e `Y` são equivalentes a versão do interpretador Python que você está utilizando, por exemplo o *pip* para `Python2.7` é `pip2.7`, e o para `Python3.4` é `pip3.4`.
```bash
pip3.4 --help
```
2. Utilizando o pip diretamente pelo módulo Python.
```bash
python3.4 -m pip --help
```

> Eu recomendo utilizar essa forma, porque evita confusão na hora de instalar pacotes, como descrito acima, em "Problemas conhecidos."

Como toda ferramenta de linha de comando, você pode ver todos os parametros suportados e mostrar o texto de ajuda utilizando o parametro `--help`.

```bash
pip3.4 --help
```
O resultado é esse:

```bash
luzfcb@luzfcb:~/$ pip3.4 --help

Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output.
  --log <path>                Path to a verbose appending log.
  --proxy <proxy>             Specify a proxy in the form [user:passwd@]proxy.server:port.
  --retries <retries>         Maximum number of retries each connection should attempt (default 5 times).
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists: (s)witch, (i)gnore, (w)ipe, (b)ackup.
  --trusted-host <hostname>   Mark this host as trusted, even though it does not have valid or any HTTPS.
  --cert <path>               Path to alternate CA bundle.
  --client-cert <path>        Path to SSL client certificate, a single file containing the private key and the certificate in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine whether a new version of pip is available for download. Implied with --no-index.
```

Cada um dos comandos descritos na sessão `Commands` tambem pode possuir alguns parametros adicionais.

Você pode ver esses parametros adicionais, acessando a ajuda expandida, simplesmente executando:

```bash
pip3.4 comando-que-voce-quer-ajuda --help
```

Exemplo:

```bash
pip3.4 install --help
```


## <a name="pesquisando-bibliotecas-pacotes-python-utilizando-o-pip" href="#pesquisando-bibliotecas-pacotes-python-utilizando-o-pip">Pesquisando bibliotecas (pacotes) python utilizando o pip</a>


```bash
pip3.4 search nome-da-biblioteca
```

## <a name="listando-bibliotecas-pacotes-python-atualmente-instaladas" href="#listando-bibliotecas-pacotes-python-atualmente-instaladas">Listando as bibliotecas python atualmente instaladas</a>


```bash
pip3.4 list
```


## <a name="instalando-bibliotecas-pacotes-python-utilizando-o-pip" href="#instalando-bibliotecas-pacotes-python-utilizando-o-pip">Instalando bibliotecas (pacotes) python utilizando o pip</a>

Instalar é bem simples:

```bash
pip3.4 install virtualenv
```

Você tambem pode instalar vários pacotes de uma vez só:

```bash
pip3.4 install virtualenv virtualenvwrapper
```

Por padrão, o pip tentará obter a versão mais recente disponivel para o pacote python. Isso é bom, contudo, você pode querer instalar uma versão especifica da biblioteca

```bash
pip3.4 install virtualenv==12.1.1
```

Novamente, vou utilizar o virtualenv como exemplo. O virtualenv possui disponivel, em ordem da mais recente para a mais antiga, as versões `13.1.2`, `13.1.1`, `13.1.0`, `13.0.3`, `13.0.2`, `13.0.1`, `13.0.0`, `12.1.1`, `12.1.0`
Agora, vamos supor que você queira que o pip baixe a ultima versão disponivel abaixo da versão `13.1.2`, ou seja a versão `13.1.1`.

```bash
pip3.4 install virtualenv<13.1.2
```

E se eu quiser instalar qualquer versão entre a `13.0.2` e a versão 12.1.0, exceto a versão `13.0.1` e `13.0.0`:

```bash
pip3.4 install "virtualenv>=12.1.0,<13.0.2,!=13.0.1,!=13.0.0"
```

> O *pip* faz cache dos pacotes baixados, ou seja, depois que você instala determinada versão, o pip vai tentar obter o pacote primeiramente apartir do cache e em seguida via internet.
> O *pip* salva o cache na pasta `~/.cache/pip`

## <a name="atualizando-bibliotecas-pacotes-python-utilizando-o-pip" href="#atualizando-bibliotecas-pacotes-python-utilizando-o-pip">Atualizando bibliotecas (pacotes) python utilizando o pip</a>


```bash
pip3.4 install virtualenv --upgrade
```

## <a name="desinstalando-bibliotecas-pacotes-python-utilizando-o-pip" href="#desinstalando-bibliotecas-pacotes-python-utilizando-o-pip">Desinstalando bibliotecas (pacotes) python utilizando o pip</a>


```bash
pip3.4 uninstall virtualenv
```
Por padrão, ao desinstalar bibliotecas, o pip vai pedir uma confirmação sua antes de efetivamente desinstalar o pacotes, para forçar o pip a concordar automaticamente com a desinstalação utilize o parametro `--yes`

```bash
pip3.4 uninstall virtualenv --yes
```



# Perguntas Frequentes:

```bash
fabio@luzfcb:~$ wget -H https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py; sudo -H python3.4 /tmp/get-pip.py virtualenv virtualenvwrapper --upgrade

--2015-10-05 16:58:32--  https://bootstrap.pypa.io/get-pip.py
Resolvendo bootstrap.pypa.io (bootstrap.pypa.io)... 23.235.46.175
Conectando-se a bootstrap.pypa.io (bootstrap.pypa.io)|23.235.46.175|:443... conectado.
A requisição HTTP foi enviada, aguardando resposta... 200 OK
Tamanho: 1412744 (1,3M) [text/x-python]
Salvando em: “/tmp/get-pip.py”

100%[================================>] 1.412.744    438KB/s   em 3,2s   

2015-10-05 16:58:37 (438 KB/s) - “/tmp/get-pip.py” salvo [1412744/1412744]

FINALIZADO --2015-10-05 16:58:37--
Tempo total decorrido: 5,0s
Baixados: 1 arquivos, 1,3M em 3,2s (438 KB/s)
[sudo] password for fabio: 
Sinto muito, tente novamente.
[sudo] password for fabio: 
Collecting pip
  Using cached pip-7.1.2-py2.py3-none-any.whl
Collecting setuptools
  Downloading setuptools-18.3.2-py2.py3-none-any.whl (462kB)
    100% |████████████████████████████████| 462kB 124kB/s 
Collecting virtualenv
  Downloading virtualenv-13.1.2-py2.py3-none-any.whl (1.7MB)
    100% |████████████████████████████████| 1.7MB 204kB/s 
Collecting virtualenvwrapper
  Downloading virtualenvwrapper-4.7.1-py2.py3-none-any.whl
Collecting wheel
  Downloading wheel-0.26.0-py2.py3-none-any.whl (63kB)
    100% |████████████████████████████████| 65kB 648kB/s 
Collecting virtualenv-clone (from virtualenvwrapper)
  Downloading virtualenv-clone-0.2.6.tar.gz
setuptools must be installed to install from a source distribution

```


# E o que vem depois?

No próximo artigo eu falarei de como gerenciar as dependencias python de seu projeto utilizando o *pip*

Até a próxima.

> Gostou deste artigo? Ele lhe foi util?
