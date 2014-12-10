Title: Integrando o Django com Cloudinary
Date: 2014-12-09 23:08
Tags: Django, Cloudinary, Heroku
Category: deploy-infraestrutura
Slug: integrando-django-com-cloudinary
Author: Dyesten Paulon
Email: dyesten.pt@gmail.com
Github: dyesten
Facebook: dyesten.paulon



### O que é?

O Cloudinary é um serviço de gerenciamento de imagens e arquivos na nuvem, muito útil por exemplo para utilização junto ao Heroku, que não oferece o serviço de hospedagem de arquivos. Além de nos oferecer o serviço de hospedagem de imagens, o Cloudinary disponibiliza diversas manipulações, uso de efeitos, detecção facial e muitos outros recursos para as imagens enviadas.

### O que é preciso?

Para iniciarmos é preciso se __cadastrar__ no site. O cadstro pode ser feito com uma conta gratuita limitada.

[Cadastro Gratuito](https://cloudinary.com/users/register/free)

<br>
Ao finalizar o cadastro, uma tela como a exibida abaixo estará disponível. Atenção nos itens Cloud name, API Key e API Secret, eles serão úteis mais adiante.

![Cadastro Cloudinary](/images/dyesten/cadastro_cloudinary.png)

<br>

### Configurando o ambiente

A instação do pacote pode ser feita via __pip__:
    
	pip install cloudinary

Ou baixando o pacote pelo [link](https://pypi.python.org/pypi/cloudinary/1.0.18)


### Configurando o settings
<small>_Obs.: focaremos apenas nas configurações do cloudinary._</small>

Primeiramente no INSTALLED_APPS incluiremos a linha __'cloudinary'__ e a linha com nossa app:

	INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'cloudinary',
		'cloudinary_example.core',
	)

Ainda no settings adicione ao seu arquivo os parâmetros de configuração do Cloudinary:

<small>_Obs.: estes parâmetros são os mesmo da imagem inicial. E os abaixo apresentados são apenas ficticios_</small>

	CLOUDINARY = {
		'cloud_name' : seu_app_cloud,
		'api_key' : '00998877665544',
		'api_secret': 'DBseuAPPAKI-mtb7ZklCCBuJNoNetp'
	}

### Models

Faremos a importação do Cloudinary e em seguida definiremos nossa classe __'Imagens'__:

	from django.db import models
	from cloudinary.models import CloudinaryField

	class Imagens(models.Model):
	  imagem = CloudinaryField('imagem')

<small>_Obs.: execute o syncdb. No caso de utilização do South, acresencete o seguinte código:_</small>
	
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ["^cloudinary\.models\.CloudinaryField"])

### Forms
Agora vamos importar o modelo em nosso __forms__, e definiremos nossa Classe em seguida:

	from django import forms
	from cloudinary_example.core.models import Imagens

	class ImagensForm(forms.ModelForm):
		class Meta:
			model = Imagens


Agora vamos criar o formulário para fazermos o upload das imagens.
Antes vamos definir uma rota para nossa __views__, chamaremos ela de _'galeria'_:

	urlpatterns = patterns('cloudinary_example.core.views',
		url(r'^galeria/$', 'galeria', name='galeria'),
	)

Criaremos agora uma __views__ mais simples possível para chegar até nosso __template__:
	
	from django.shortcuts import render_to_response
	from cloudinary_example.core.forms import ImagensForm
	
	def galeria(request):
		return render_to_response('galeria.html', {'form':ImagensForm})
		
		
Agora vamos criar nosso template _'galeria.html'_ com o seguinte código:

	{% extends 'base.html' %}
	{% load cloudinary %}

	{% block content %}
		<form action="." method="post" enctype="multipart/form-data">
		{% csrf_token %}
			<table border=1 align="center">
				<tr>
					<td style="padding:10px;margin:20px;">
						<label for="imagens">Imagens:</label>
					</td>
					
					<td style="padding:10px;margin:20px;">
						{{ form.imagem }}
					</td>
				</tr>
				
				<tr align="center">
					<td colspan='2' style="padding:10px;margin:20px;">
						<input type="submit" value="Upload">
					</td>
				</tr>
			</table>
	{% endblock content%}

![Template Inicial](/images/dyesten/template_inicial.png)


Legal mas nossa _views_ ainda não tem a ação para salvar a imagem no Cloudinary, agora vamos voltar e realizar a ação para salvar a imagem.
Primeiro vamos incluir as importações do nosso model.

	from cloudinary_example.core.models import Imagens

Vamos alterar nosso método _'galeria'_ para o seguinte:

	from django.shortcuts import render
	from cloudinary_example.core.forms import ImagensForm
	from cloudinary_example.core.models import Imagens

	def galeria(request):
		if request.method == 'POST':
			form = ImagensForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()

		return render(request, 'galeria.html', {'form':ImagensForm})


Ok, agora nossa imagem já pode ser salva no Cloudinary e nosso banco de dados. E como recuperar as imagens para exibição?
Neste exemplo vamos utilizar as mesma _views_ e o mesmo _template_ para exibição. Para isso vamos alterar nossa _views_ para buscar os id’s de nossas imagens salvos no banco, 
altere o seu return para o seguinte:

	return render(request, 'galeria.html', {'form':ImagensForm, 'imgs':Imagens.objects.all()})

Já em seu template, adicione o seguinte código:
	
	<table align="center">
		{% for img in imgs %}
			<tr>
				<td>{% cloudinary img.imagem %}</td>
			</tr>
		{% empty %}
			<tr>
				<td>Sem Itens na Lista</td>
			</tr>
		{% endfor %}
	</table>

Com apenas este código acima, é possível buscarmos as imagens assim que carregadas.

Alguns detalhes importantes:

* A tag {% cloudinary img.imagem %} é equivalente a uma tag html <img>:

	<small><_img src="http://res.cloudinary.com/suapasta/image/upload/v001122334455/codigodasuaimagem.jpg"></small>

* Se é uma tag HTML, podemos utiliza-la sempre assim? A resposta é utilize a que se sentir mais confortável, não há qualquer problema.
* Alguns parâmetros podem ser adicionados a sua tag, como por exemplo, height, width, crop e muitos outros:
	
	{% cloudinary img.imagem height=500 width=400 crop="fill" %}

Consulte a [documentação](http://cloudinary.com/documentation/django_image_manipulation) para mais exemplos de manipulação.


### Extra

E como carregar múltiplos arquivos? O Django e Cloudinary te dão suporte total a essa ação de forma simples.

Vamos começar alterando nosso __forms__. Primeiro adicionaremos a importação da biblioteca do Cloudinary:
	
	from cloudinary.forms import CloudinaryJsFileField


Em seguida, incluiremos após a class meta a linha que indica que nosso campo file input deve ser multiple:
	
	imagem = CloudinaryJsFileField( attrs={'multiple': 1, 'name':'imagens'} )


E nossa view sofre uma pequena alteração para percorrer os itens do request Files:
	
	def galeria(request):
		if request.method == 'POST':
			form = ImagensForm(request.POST, request.FILES)
			for f in request.FILES.getlist('imagens'):
				Imagens(imagem=f).save()

		return render(request, 'galeria.html', {'form':ImagensForm, 'imgs':Imagens.objects.all()})

Tudo pronto, agora já temos um galeria simples. 
O código está disponível no [GitHub](https://github.com/dyesten/cloudinary_example/).

