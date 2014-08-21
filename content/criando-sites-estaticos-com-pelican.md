Title: Criando sites estáticos com Pelican Framework
Slug: criando-sites-estáticos-com-pelican
Date: 2014-08-21 21:30
Tags: tutorial,pelican,blog,framework
Author: Arthur Alves
Email:  arthur.4lves@gmail.com
Github: arthur-alves
Twitter: Arthur_4lves
Facebook: Arthur4lves
Category: Pelican

<figure style="float:right;">
<img style="border-radius: 50%;" src="/images/arthur-alves/captaoboing.png">
</figure>
</br>  
###O que é?  

As vezes temos a necessidade de criar algo rápido, como por exemplo um blog ou uma landing page, e não desejamos utilizar ferramentas muito robustas como Django, Web2py, etc. Na verdade eu faço isso mas é um exagero. Em um outro projeto meu queria uma solução muito rápida e simples, e é ai que entrou o Pelican, o framework/gerador de páginas estáticas feito em Python. Existem outros geradores em diversas linguagens, mas como nós sabemos, tudo em python é muito mais divertido.  
</br>   
###Configurando o ambiente  
<small>**Obs**: *Se já tiver um virtualenv instalado pule esta parte*</small>  
</br>
Instale no seu ambiente o Python Package Index, ou famoso **pip**:  

    sudo apt-get install python-pip

Recomendo fortemente o uso do **virtualenv**, é muito simples de instalar. 
 
    pip install virtualenv  

E logo vamos instalar o assistente dele, o **Virtualenvwrapper** (Opcional):  

    pip install virtualenvwrapper  

Crie uma pasta na sua **home**, como por exemplo, "mkdir .venvs", e configure também seu ~/.bashrc com as seguintes linhas:

    export WORKON_HOME=~/.venvs  
    source /usr/local/bin/virtualenvwrapper.sh  

Depois valide:

    . ~/.bashrc  

Agora crie seu virtualenv com o seguinte comando:  
    
    mkvirtualenv pelican  


</br>
###Instalando o Pelican  

Agora que o ambiente está pronto, vamos instalar o Pelican. Basta fazer o seguinte:  

    pip install pelican markdown

<small>**Obs**: *Por padrão o Pelican utiliza o rst, mas vou utilizar o markdown. Se não quiser, remova o markdown da instalação.*</small>  

Crie uma pasta separada para trabalhar com o Pelican e iniciarmos nossas tarefas.
Feito isso, vamos iniciar com o comando abaixo:  

    pelican-quickstart  

Este comando lhe fará uma série de perguntas sobre seu site, basta responder de acordo com suas necessidades. As opções em maísculas são as default, veja abaixo:

    Where do you want to create your new web site? [.]  #pasta onde você quer salvar seu projeto
    What will be the title of this web site? #Titulo do site  
    Who will be the author of this web site? #Seu nome aqui  
    What will be the default language of this web site? [en] - #pt para portugues  
    Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) - #Url do seu blog  
    What is your URL prefix? #www.seublog.dev  
    Do you want to enable article pagination? (Y/n) - #Paginação  
    How many articles per page do you want? [10] - #Itens por paginação  
    Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) - Sim - #Facilita muito  
    Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) - #Um server para testes  
    Do you want to upload your website using FTP? (y/N)  - #Opcional  
    Do you want to upload your website using SSH? (y/N) - #Opcional  
    Do you want to upload your website using Dropbox? (y/N) - #Opcional  
    Do you want to upload your website using S3? (y/N) - #Opcional  
    Do you want to upload your website using Rackspace Cloud Files? (y/N) - #Opcional  
    Do you want to upload your website using GitHub Pages? (y/N) - #Opcional  


Feito isso ele irá criar uma estrutura com esta abaixo:  

>├── content  
│                    └── teste.md  # este arquivo é o que vamos adicionar  
├── output  
├── develop_server.sh  
├── fabfile.py  
├── Makefile  
├── pelicanconf.py  
└── publishconf.py  

</br>

Seguindo a estrutura acima, dentro da pasta **content**, crie o arquivo **teste.md** para iniciarmos
nosso primeiro post.  

E vamos digitar o seguinte:  

    Title: Hello Pelican!  
    Date: 2014-08-19 17:00  
    Category: Python  
    Tags: pelican, markdown  
    Slug: primeiro-artigo  
    Author: Arthur Alves  
    Summary: Um resumo sobre o post do Pelican  

    #Testando nosso primeiro post no Pelican  

    Pelican é um gerador de páginas estáticas criado em python para facilitar nossa vida, na 
    criação de blogs, landingpages ou site estáticos.  

</br>
Salve o nosso arquivo, volte para a pasta raiz do projeto e vamos ver o nosso resultado com o seguinte comando:  

    make html && make serve  

ou  

    ./develop_server.sh start  

Este último é melhor para se trabalhar, pois a cada alteração ele atualiza automaticamente sem necessidade de reiniciar o comando, que é o caso do **make html && make serve**.  

Se você respondeu "Y", no pelican-quickstart para gerar seu **make file**, estes comandos irão funcionar. 
E você pode ver seu resultado em [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

Mas se não gerou, não tem problema, você pode fazer da seguinte forma: na pasta raiz do projeto digite:  

    pelican content -s pelicanconf.py  -o output

Com este comando você está dizendo para o Pelican que você quer que todos os arquivos da pasta content, seja transformada em html de acordo com o arquivo de configuração **pelicanconf.py**, (que foi gerado automaticamente pelo **pelican-quickstart** lembra?) e deverá ser enviado para a pasta output.  
Feito isso ele vai gerar os "htmls" na pasta output do projeto. E você pode ver o resultado com o template padrão do Pelican.

### Temas e um pouco do arquivo pelicanconf.py.  

Abra seu arquivo **pelicanconf.py**, e veja seu conteudo. Repare que existe algumas variáveis que com a ajuda do **[Jinja2](http://jinja.pocoo.org/docs/)**, ele popula algumas informações no template, vejamos por exemplo abaixo.

    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    AUTHOR = u'Arthur Alves' # Autor do site
    SITENAME = u'Meu Blog Pelican' # Nome do site 
    SITEURL = 'blogdoarthur.dev' # url do site
    
    TIMEZONE = 'America/Sao_Paulo' 
    
    DEFAULT_LANG = u'pt'  

Altere conforme a sua necessidade. Em **TIMEZONE**, caso o seu seja diferente, você pode alterar conforme esta página no [Wikipedia](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Vamos agora instalar um tema, utilizando o comando facilitador **pelican-themes**, digite no seu terminal:  

    pelican-themes -l  

Repare que ele te apresenta todos os temas que você possui. E se quiser instalar outro tema, recomendo que procure no site [pelican-themes do github](https://github.com/getpelican/pelican-themes), veja pelas screenshots qual te agrada mais. Se quiser baixar todos clone o diretório, ou clique em download Zip ou clicando [aqui](https://github.com/getpelican/pelican-themes/archive/master.zip).  

Depois de escolhido seu tema, vamos usar o seguinte comando na pasta raiz do seu projeto para instalá-los:  

    pelican-themes --install caminho/onde/baixou/seu-tema/favorito  

Esse comando é muito simples, ele só cria uma pasta com o nome de **themes**, dentro da raiz do projeto e coloca o tema lá, você pode fazer isso manualmente claro. No seu arquivo **pelicanconf.py**, crie uma variável como esta abaixo com o caminho:  

    THEME = u'themes/o-tema-que-escolheu'  


Depois disso só digitar novamente:  

   make html && make serve  

E seu tema está instalado. Mais sobre configurações deste arquivo leia na [Doc do Pelican](http://docs.getpelican.com/).

</br>

###Curiosidades e erros.  

O nome **Pelican** é um anagrama de **calepin**, que significa bloco de notas em francês.  

O site do Python Club é feito com o framework Pelican. 

Se você teve algum erro de encode ou coisa do tipo:  

    UnicodeEncodeError: 'ascii' codec can't encode character u'\xc9' in position 13: ordinal not in range(128)  

Isso significa que sua versão do Pelican é mais antiga, pois isso já foi corrigido e você pode instalar direto do repositório.:  

    pip install -e "git+https://github.com/getpelican/pelican.git#egg=pelican"  

Ou então trocar a variável $LANG, que deu certo com algumas pessoas no [github](https://github.com/getpelican/pelican), digite no terminal o seguinte:  

    export LANG=en.UTF-8  

Pois é, funciona. Mas prefira instalar a versão mais nova, já com o patch.  

Bem pessoal, é simples, mas espero que ajude o pessoal a ficar mais íntimo do Pelican e ajudar com o [pythonclub](http://pythonclub.com.br/).
