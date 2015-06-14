Title: Instalando o PyCharm no Ubuntu (e irmãos)
Slug: instalando-pycharm-ubuntu
Date: 2015-06-14 12:58
Tags: python,blog,tutorial,pycharm
Author: Erick Müller
Email:  erick.muller@gmail.com
Github: ehriq
Bitbucket: ehriq
Twitter: ehriq
Category: Python


O objetivo aqui é instalar o PyCharm no Ubuntu e distribuições "irmãs" (como o Mint); estou instalando a versão **Community Edition**, que acredito que é a que muita gente que começa com essa poderosa IDE vai instalar pra dar os primeiros passos, experimentar.

(aliás, bom avisar antes de começar: fiz o guia baseado no Ubuntu 14.04 e no Linux Mint 17.1; mas já fiz o mesmo procedimento em versões anteriores tanto do PyCharm quanto do Ubuntu, e com a versão "Professional" do PyCharm, e funcionou bem.)  


## Parte 1 - instalar o Java

As aplicações da JetBrains não são exatamente compatíveis com a versão do Java que vem por padrão no Ubuntu. Por isso, precisamos atualizar. 

Abra o terminal e execute os comandos abaixo:

```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
sudo apt-get install oracle-java8-installer -y
sudo apt-get install oracle-java8-set-default -y
```

Após os comandos acima, veja se a instalação está correta, executando no console:

```bash
java -version
```

a saída esperada é algo como:

```
java version "1.8.0_45"
Java(TM) SE Runtime Environment (build 1.8.0_45-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.45-b02, mixed mode)
```

## Parte 2 - pip e virtualenv

O PyCharm usa o **pip** para baixar módulos/bibliotecas/extensões (como quiser chamar) do python, e o **virtualenv** para criar os queridos ambientes virtuais que mantém a sanidade dos programadores python. Então, para tirar proveito dessas funcionalidades, é bom garantir que estejam instalados também. 

Para isto, abra o console e:

```
cd ~/Downloads
wget -c https://bootstrap.pypa.io/get-pip.py
sudo -H python2 get-pip.py
sudo -H python3 get-pip.py
sudo -H pip2 install virtualenv
```


## Parte 3 - copiar o PyCharm

- clique no link ao lado para ir à página de [Download do PyCharm](https://www.jetbrains.com/pycharm/download/)
- clique em "Download Community"
- grave o arquivo no diretório que quiser




## Parte 4 - instalar o PyCharm

Com os pré-requisitos prontos e instalados, vamos ao prato principal: 

```
sudo tar -C /opt/ -xzf <diretorio_onde_gravou_o_download>/pycharm-community-4.5.1.tar.gz
```

- Abra o navegador de arquivos e vá ao diretório */opt/pycharm-community-4.5.1*
- Entre no diretório 'bin' e, com dois cliques sobre, execute o script *'pycharm.sh'*
- Se aparecer uma janela perguntando como rodar o programa, clique no último botão (*'Executar'* ou *'Run'*)
- Dê "OK" na janela que abrir 
- E na próxima janela, deixe todas as últimas opções selecionadas. Ao clicar em *'OK'* o PyCharm vai pedir a senha de 'root' para criar as entradas no menu. 

<center>
<img src="/images/ehriq/ConfigPyCharm.png" alt="Tela de configuração final">
</center>

Pronto, é isso. O software está instalado, e pronto para uso.
