Configurando o Django-TinyMCE no Django 1.6-[Nível Básico]
#########################################################


:date: 2014-07-13
:tags: django-tinymce, configurar django-tinymce, django-tinymce configuration, 
:category: Django-TinyMCE
:slug: configurando-o-django-tinyMCE-no-django-1.6-[Nível Básico]
:author: Josué
:email: josue.bfr@gmail.com
:summary: Como Configurar o Django-TinyMCE no Django 1.6
:github: JackFill

Esse pequeno tutorial tem como foco a configuração do Django-TinyMCE no Django. Por isso decidi abordar apenas a parte prática e não explanar seus pormenores, vantagens, desvantagens e etc. 
Então, vamos ao que realmente importa!

O **Django-TinyMCE** é uma aplicação desenvolvida em python para modificar a exibição padrão do widget TextArea de formulários Django.
A documentação, [oficial](http://django-tinymce.readthedocs.org/en/latest/index.html) o descreve desse modo:

> django-tinymce is a Django application that contains a widget to  render a form field as a TinyMCE editor.

Ou seja,

> O django-tinymce é uma aplicação Django que contém um widget para renderizar um campo de formulário como um editor [TinyMCE](http://www.tinymce.com/).

Este editor permite uma customização de estilos, tamanhos, cores... de fontes além de trabalhar com adição de links, imagens, etc. Informação do próprio site TinyMCE .

Sua configuração pode ser um pouco trabalhosa para aqueles que não são apegados a detalhes. Caso você se encaixe nesse grupo, não se preocupe. Aqui você vai aprender a configurá-lo de modo fácil e correto.

> OBS:O conteúdo abordado abaixo leva em consideração que o leitor já tenha o [pip](https://pypi.python.org/pypi/pip), [python 2.7](https://www.python.org/download/releases/2.7.6/) , o [Django 1.6](https://www.djangoproject.com/m/releases/1.6/Django-1.6.5.tar.gz) instalado em um sistema operacional Windows ™ e um projeto django já  criado.

Se você não sabe como instalar o python veja [esses passos](https://docs.djangoproject.com/en/dev/intro/install/#install-python).
Se você não sabe como instalar o Django veja [aqui](https://docs.djangoproject.com/en/dev/intro/install/#install-django) como proceder.
Se você não sabe como criar um projeto Django, veja [aqui](https://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project) como proceder.
É recomendado ao iniciante no desenvolvimento Django o tutorial [oficial](https://docs.djangoproject.com/en/dev/intro/tutorial01).
Você pode baixar o django no formato .rar [aqui](https://github.com/django/django) , bastando clicar em **download zip** .
![Baixando Django-TinyMCE pelo GitHub](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/tinymce.pn.png)


Vamos aos processos...

1.Baixe o Django-TinyMCE [aqui](https://github.com/aljosa/django-tinymce).

>Se você já tem o pip instalado basta fazer isso :
>  Vá até o diretório Scripts e crie um arquivo contendo o código **pip install django-tinymce** e espere ele baixar e instalar o TinyMCE automaticamente.

![Baixando Django-TinyMCE pelo PIP-diretório ](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/pip.PNG)
![Baixando Django-TinyMCE pelo PIP-script ] (https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/pip.JPG)

Se você não tem o pip instalado na sua máquina, siga os passos seguintes.

2.Descompacte o arquivo baixado no passo 1.
3.Crie na pasta descompactada o arquivo **install.bat**.
![Baixando Django-TinyMCE setup.py](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/mce-bat.jpg)

4.abra o arquivo **install.bat** e adicione o código:
>python setup.py install
>pause  

![Code](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/code.jpg)

5.Feche o arquivo.Execute-o, clicando duas vezes sobre ele.

6.Aguarde até os arquivos serem instalados.

7.Certifique-se de que eles foram instalados no diretório correto. Se não o foram, isso deve ter sido uma coisa *incompreensível* do windows&trade;.
O diretório correto é:

pythonxx¹ -> lib² -> site-package³. Onde xx é a versão do python instalado em seu pc. 
¹ ![Diretório de instalação](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/python.png)
² ![Diretório de instalação](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/lib.png)
³ ![Diretório de instalação](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/desenho.png)


8.Se tudo ocorreu bem, vá ao arquivo de configuração do seu projeto,  *settings.py*  e:

Localize  o seguinte código:

 >INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
)

9.Adicione o tinymce a ele:

>INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ***'tinymce',***
 )

 ![Plugando o TinyMCE no Django](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/instaled-apps.png)

 >Nota: execute o [collectstatic](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic).

 10.Agora abra o arquivo *urls.py* do seu projeto.Localize essas linhas:

> urlpatterns = patterns('', 
>        url(r'^admin/',include(admin.site.urls)),
  )

  
11.Adicione o TinyMCE e as configurações necessárias ao seu *urls.py*:
>....
>....
> **from django.conf.urls.static import static** 
> **from django.conf import  settings**
> 
> urlpatterns = patterns( ' ',
		 ....
		 ....
		 *suas outras urls*
>        url(r'^admin/', include(admin.site.urls)),
>        **url(r'^tinymce/', include('tinymce.urls'))**,
> ) 

>**if settings.DEBUG:**
>    urlpatterns += patterns('',
>    url(r'^media/(?P.*)$',  'django.views.static.serve', {
>        'document_root': settings.MEDIA_ROOT,'show_indexes': True,}),
>    url(r'^static/(?P.*)$', 'django.views.static.serve', {
>       'document_root': settings.STATIC_ROOT, 'show_indexes': True,}),
>         
>    url(r'^js/(?P.*)$', 'django.views.static.serve', {  
>     'document_root': 'static/js'  }),   
> **)**

![configurando as urls](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/urls.py.jpg)


10.Abra o arquivo de configuração do seu projeto, o *settings.py* . Adicione os seguintes códigos:

> **TINYMCE_JS_URL = os.path.join(STATIC_URL, 'tiny_mce/tiny_mce.js' )**
> **TINYMCE_JS_ROOT = STATIC_ROOT + 'tiny_mce/'**
> 
> **TINYMCE_DEFAULT_CONFIG = {**
>         **'plugins':  "table, spellchecker, paste, searchreplace",**
>         **'theme':  "advanced",** 
>         **'cleanup_on_startup':  True,**
>         **'custom_uno_redo_levels':  10,**
>   **}**
**TINYMCE_SPELLCHECKER = True**
**TINYMCE_COMPRESSOR = True**

 OBS: Se você estiver usando o filebrowser, adicione o código abaixo. Se você não o usa, não adicione.
 
> **TINYMCE_FILEBROWSER = True**

![Adicionando configurações path e complementais ](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/settings.py.jpg)


Observe que as variáveis **STATIC_URL** e **STATIC_ROOT** devem está corretamente configuradas.

![ Configuração de arquivos estáticos ](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/settings.jpg)

Um detalhe importante que não devo deixar de informar é: 
No [site](http://django-tinymce.readthedocs.org/en/latest/installation.html#configuration), o desenvolvedor informa que se deve setar o **TINYMCE_JS_URL**  com o caminho **MEDIA_ROOT** e **TINYMCE_JS_ROOT** com o caminho **MEDIA_URL**.

Eu tentei isso, mas sempre ocorria um erro. O widget não aparecia no campo.
A recomendação [oficial](https://docs.djangoproject.com/en/1.6/howto/static-files/) do django informa que os arquivos .css, .js e imagens devem ficar em uma pasta chamada **static** , dentro do projeto criado.Isso resolveu o erro.

![Diretório dos arquivos estáticos](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/static.png)

Continuando...

11.Abra o arquivo *forms.py* do seu app. Adicione o seguinte código ao seu formulário criado.

> **from tinymce.widgets import TinyMCE** 
> ......
> **content = forms.CharField(widget = TinyMCE(attrs={'cols':100, 'rows':50}))**

![Configurando o forms](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/forms.py.jpg)

Veja esse [exemplo](http://django-tinymce.readthedocs.org/en/latest/usage.html#python-code) para ter uma ideia melhor sobre o uso . Eu utilizei a palavra content por ter me baseado no formulário da documentação oficial do django.

12.Agora, no *admin.py*, adicione o seguinte código:

> **from django.conf import settings**
> 
> **form = FormAddArtigo**
>		**class Meta: js = (settings.STATIC_URL +**
> 		**'/tiny_mce/tiny_mce.js', '/textarea.js')**

![Configurando o Admin](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/admin.py.jpg)

Detalhe: **Eu exclui o nome da classe admin. Coloque o nome da sua classe admin**.

E chegamos ao fim.O resultado deve ser esse:

![Resultado final](https://github.com/pythonclub/pythonclub.github.io/content/images/josue/tinymce/textarea.jpg)
