Title: Class Based Views no Django
Slug: class-based-views-django
Date: 2015-10-26 14:50
Tags: python,blog,tutorial,django,cbv
Author: Raphael Passini Diniz
Email:  raphapassini@gmail.com
Github: raphapassini
Bitbucket: raphapassini
Twitter: raphapassini
Category: Django

Esse tutorial tem como objetivo explicar o básico sobre Class Based Views
no Django. Por motivos de agilidade vou usar ``CBV`` para me referir as
``Class Based Views``.

Segundo a documentação do Django sobre CBV:

> CBV's permitem você estruturar as suas views e reutilizar código aproveitando
  heranças e mixinis

O Django já vem CBV's genéricas que atendem as necessidades da maioria das aplicações.
Essas views genéricas são flexiveis o sufiente para você poder adaptá-las as
suas necessidades.

Nesse tutorial eu vou falar brevemente sobre os 4 grupos de CBV's que existem
no Django atualmente:

- [Base views](#base_views)
    - [View](#view)
    - [TemplateView](#template_view)
    - [RedirectView](#redirect_view)
- [Display views](#display_views)
    - [DetailView](#detail_view)
    - [ListView](#list_view)
- [Editing views](#editing_views)
    - [Model based Views](#model_view)
    - [CreateView, UpdateView, DeleteView](#create_update_delete_view)
- [Date views](#date_views)
    - [ArchiveView](#archive_view)
    - [YearView](#year_view)
    - [MonthView](#month_view)
    - [WeekView](#week_view)
    - [DayView](#day_view)
    - [TodayView](#today_view)
    - [DateDetailView](#date_detail_view)
- [Conclusão](#conclusao)
- [Referências](#ref)

 Antes de começarmos a falar sobre as CBV's vamos ver como apontar uma rota
 do Django para uma CBV:

```python

from django.conf.urls import url
from django.views.generic import TemplateView
from meuapp.views import AboutView

urlpatterns = [
    url(r'^about/', AboutView.as_view()),
]
```

## <a name="base_views"></a>Base Views

As classes listadas abaixo contém muito da funcionalidade necessária para criar
views no Django. Essas classes são a base sob a qual as outras CBV's são
construídas.

### <a name="view"></a>View

A classe génerica *master*. **Todas** as outras classes herdam dessa classe.
O fluxo básico de execução dessa classe quando recebe uma requisição é:

1. ``dispatch()``
2. ``http_method_not_allowed()``
3. ``options()``

A função ``dispatch()`` verifica se a classe tem um método com o nome do verbo
HTTP usado na requisição. Caso não haja um ``http.HttpResponseNotAllowed`` é
retornado.

Essa classe sempre responde a requisições com o verbo ``OPTIONS`` retornando
nesse caso uma lista com os verbos suportados. A não ser que o método
``options()`` seja sobrescrito.

Um exemplo de implementação:

```python

from django.http import HttpResponse
from django.views.generic import View

class MyView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
```

No exemplo acima a classe só responde a requisições do tipo ``GET`` e
``OPTIONS``, todas as outras requisições retornam
``http.HttpResponseNotAllowed``.

### <a name="template_view"></a>Template View

Renderiza um template. O fluxo básico de execução dessa clase quando recebe
uma requisição é:

1. ``dispatch()``
2. ``http_method_not_allowed()``
3. ``get_context_data()``

Quando você precisa apenas renderizar uma página para o usuário essa com certeza
é a melhor CBV para o caso. Você pode editar o contexto que o template recebe
sobrescrevendo a função ``get_context_data()``

Um exemplo de implementação:

```python

from django.views.generic.base import TemplateView

from articles.models import Article

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context
```

No exemplo acima o template *home.html* será renderizado e vai receber como
contexto uma variável chamada ``lastest_articles``.

Uma coisa interessante é que o contexto da ``TemplateView`` é populado pelo
[ContextMixin](https://docs.djangoproject.com/en/1.8/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin)
esse mixin pega automaticamente os argumentos da URL que serviu a View.

Considere por exemplo:

```python

from django.conf.urls import patterns, url
from .views import HelloView

urlpatterns = patterns(
    '',
    url(r'^say_hello/(?P<name>[\w_-]+)/$', HelloView.as_view(), name='say_hello'),
)
```

No caso do exemplo acima o template renderizado pela ``HelloView`` teria
em seu contexto a variável ``name``.

### <a name="redirect_view"></a>Redirect View

Redireciona o usuário para a url informada.

A URL a ser redirecionada pode conter parâmetros no estilo dicionário-de-strings.
Os parâmetros capturados na URL do ``RedirectView`` serão repassados para a
URL que o usuário está sendo redirecionado.

O fluxo básico de execução dessa clase quando recebe
uma requisição é:

1. ``dispatch()``
2. ``http_method_not_allowed()``
3. ``get_redirect_url()``

Considere a seguinte configuração de URL's para o exemplo de implementação:

```python

from django.conf.urls import url
from django.views.generic.base import RedirectView

from article.views import ArticleCounterRedirectView, ArticleDetail

urlpatterns = [
    url(r'^counter/(?P<pk>[0-9]+)/$', ArticleCounterRedirectView.as_view(), name='article-counter'),
    url(r'^details/(?P<pk>[0-9]+)/$', ArticleDetail.as_view(), name='article-detail'),
]
```

Exemplo de implementação:

```python

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

from articles.models import Article

class ArticleCounterRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        article.update_counter()
        return super(ArticleCounterRedirectView, self).get_redirect_url(*args, **kwargs)

```

Principais atributos:

- ``url``: A URL destino no formato de String
- ``pattern_name``: O nome do padrão de URL. Um ``reverse`` será aplicado
  usando os mesmos
  ``args`` e ``kwargs`` passados para a ``RedirectView``
- ``permanent``: Se for ``True`` retorna o status code como 301 caso contrário
  retorna 302.
- ``query_string``: Se for ``True`` a query_string será enviada para a URL de
  destino.

## <a name="display_views"></a>Display Views

As duas views abaixo foram desenvolvidas para exibir informações. Tipicamente
essas views são as mais usadas na maioria dos projetos.

### <a name="detail_view"></a>DetailView

Renderiza um template contendo em seu contexto **um objeto** obtido pelo
parâmetro enviado na URL.

No fluxo de execução dessa view o objeto que está sendo utilizado está em
``self.object``

O fluxo básico de execução dessa clase quando recebe
uma requisição é:

1. ``dispatch()``
2. ``http_method_not_allowed()``
3. ``get_template_names()``
4. ``get_slug_field()``
5. ``get_queryset()``
6. ``get_object()``
7. ``get_context_object_name()``
8. ``get_context_data()``
9. ``get()``
10. ``render_to_response()``

O fluxo parece grande e complexo mas na verdade é muito simples e facilmente
customizável. Basicamente o que acontece é:

``get_template_names()`` retorna uma lista de templates que devem ser usados para
renderizar a resposta. Caso o primeiro template da lista não seja encontrado o
Django tenta o segundo e assim por diante.

Em seguida o ``get_slug_field()`` entra em ação, essa função deve retornar o
nome do campo que será usado para fazer a busca pelo objeto. Por default o
Django procura pelo campo ``slug``

Agora o ``get_queryset`` deve retornar um queryset que será usado para buscar
um objeto. Aqui é um ótimo lugar para, por exemplo, aplicar um filtro para
exibir somente o Artigo cujo autor é o usuário logado. Considere o exemplo
abaixo:

```python

def ArtigoView(DetailView):
    model = Artigo

    get_queryset(self):
        return self.model.filter(user=request.user)

    # ... o restante do código foi suprimido
```

**IMPORTANTE:** O ``get_queryset()`` é chamado pela implementação default do
método ``get_object()``, se o ``get_object()`` for sobrescrito a chamada ao
``get_queryset()`` pode não ser realizada.

O ``get_object()`` então é o responsável por retornar o objeto que será enviado
para o template. Normalmente essa função não precisa ser sobrescrita.

Depois de obter o objeto que será enviado para o template é necessário saber
qual será o nome desse objeto no contexto do template, isso é feito pela função
``get_context_object_name()``, por default o nome do objeto no template será o
nome do ``Model``, no exemplo acima seria ``artigo``

Depois disso temos o ``get_context_data()`` que já foi comentado acima e então
o ``get()`` que obtém o objeto e coloca no contexto, e em seguida o
``render_to_response`` que renderiza o template.

**IMPORTANTE:** É importante notar que o Django oferece variáveis de
instância para facilitar a customização do comportamento da classe.
Por exemplo a troca do nome do objeto pode ser feita alterando a variável de
instância ``context_object_name`` ao invés de sobrescrever a função
``get_object_name()``.

Abaixo segue um exemplo, onde exibir os detalhes de um *Artigo* somente se o
usuário for o autor dele e vamos pegar esse *Artigo* pelo campo ``titulo`` e
renderizar esse artigo no template ``detalhe_artigo.html`` com o nome
``meu_artigo``.

**views.py**
```python

from django.views.generic.detail import DetailView
from django.utils import timezone

from articles.models import Article

class ArticleDetailView(DetailView):
    slug_field = 'titulo'
    model = Article
    context_object_name = 'meu_artigo'
    template_name = 'detalhe_artigo.html'

    get_queryset(self):
        return self.model.filter(user=self.request.user)

```

**urls.py**
```python
from django.conf.urls import url

from article.views import ArticleDetailView

urlpatterns = [
    url(r'^(?P<titulo>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),
]
```

**detalhe_artigo.html**
```html
<h1>{{ meu_artigo.titulo }}</h1>
<p>{{ meu_artigo.conteudo }}</p>
<p>Reporter: {{ meu_artigo.user.name }}</p>
<p>Published: {{ meu_artigo.data_publicacao|date }}</p>
```

### <a name="list_view"></a>ListView

Uma página que representa uma lista de objetos.
Enquanto essa view está executando a variável ``self.object_list`` vai conter
a lista de objetos que a view está utilizando.

O fluxo básico de execução dessa clase quando recebe
uma requisição é:

1. ``dispatch()``
2. ``http_method_not_allowed()``
3. ``get_template_names()``
5. ``get_queryset()``
6. ``get_object()``
7. ``get_context_object_name()``
8. ``get_context_data()``
9. ``get()``
10. ``render_to_response()``

Nada de novo aqui certo? Podemos exibir apenas uma lista de Artigos que estão
com ``status='publicado'``

```python

from django.views.generic.list import ListView
from django.utils import timezone

from articles.models import Artigo

class ArticleListView(ListView):

    model = Artigo

    def get_queryset(self, **kwargs):
        return Artigo.objects.filter(status='publicado')
```

Outra opção seria:

```python

from django.views.generic.list import ListView
from django.utils import timezone

from articles.models import Artigo

class ArticleListView(ListView):

    model = Artigo
    queryset = Artigo.objects.filter(status='publicado')
```

**artigo_list.html**
```html
<h1>Articles</h1>
<ul>
{% for article in object_list %}
    <li>{{ article.pub_date|date }} - {{ article.headline }}</li>
{% empty %}
    <li>No articles yet.</li>
{% endfor %}
</ul>
```

**DICA:** Normalmente sobrescrevemos as funções quando o retorno depende dos
parâmetros da requisição e utilizamos as variáveis de instância quando não há
essa dependência.

O nome do template que é usado em ambas as views ``DetailView`` e ``ListView``
é determinado da seguinte forma:

* O valor da variável ``template_name`` na View (se definido)
* O valor do campo ``template_name_field`` na instância do objeto que a view
  esta usando.
* ``<app_label>/<model_name><template_name_suffix>.html``


## <a name="editing_views"></a>Editing Views

As views descritas abaixo contém o comportamento básico para edição de conteúdo

### <a name="form_view"></a>FormView

Uma view que mostra um formulário. Se houver erro, mostra o formulário novamente
contendo os erros de validação; Em caso de sucesso redireciona o usuário para
uma nova URL.

**forms.py**
```python

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
```

**views.py**
```python

from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)
```

**contact.html**
```html
<form action="" method="post">{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Send message" />
</form>
```

As funções mais importantes do ``FormView`` são:

- ``form_valid()``: Chamada quando o formulário é validado com sucesso
- ``form_invalid()``: Chamada quando o formuĺário contém erros
- ``get_sucess_url()``: Chamada quando o formulário é validado com sucesso
  e retorna a url para qual o usuário deve ser redirecionado.

### <a name="model_view"></a>Views para lidar com ``models`` (ModelForms)

Grande parte do "poder" das CBV's vem quando precisamos trabalhar com models.

As views listadas abaixo: ``CreateView``, ``UpdateView`` e ``DeleteView`` foram
criadas para facilitar esse trabalho com os models, essas views podem gerar um
``ModelForm`` de maneira automatica, desde que seja possível determinar qual
é o model que a view esta utilizando.

A view vai tentar determinar o model a ser usado das seguintes formas:

- Se houver um atributo ``model`` na classe
- Se o método ``get_object()`` retorna um objeto, a classe desse objeto será
  usada
- Se houver um atributo ``queryset`` o model do ``queryset`` será utilizado

Você não precisa nem mesmo definir um ``success_url`` as views ``CreateView`` e
``UpdateView`` utilizam automaticamente a função ``get_absolute_url()`` do model
se essa função existir.

Você também pode customizar o formulário usado na view se você precisar de algum
tratamento adicional, para fazer isso basta definir a classe de formulários a ser
usada no atributo ``form_class``:

```python

from django.views.generic.edit import CreateView
from myapp.models import Author
from myapp.forms import AuthorForm

class AuthorCreate(CreateView):
    model = Author
    form_class = AuthorForm
```

### <a name="create_update_delete_view"></a>CreateView, UpdateView e DeleteView

Uma view que exibe um form para criar, atualizar ou apagaer um objeto.
Caso existam erros no formulário, este é exibido novamente junto com as
mensagens de erro.

Em caso de sucesso o objeto é salvo.

**models.py**

```python

from django.core.urlresolvers import reverse
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})
```

**views.py**
```python

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from myapp.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['name']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

```

**urls.py**
```python
from django.conf.urls import url
from myapp.views import AuthorCreate, AuthorUpdate, AuthorDelete

urlpatterns = [
    # ...
    url(r'author/add/$', AuthorCreate.as_view(), name='author_add'),
    url(r'author/(?P<pk>[0-9]+)/$', AuthorUpdate.as_view(), name='author_update'),
    url(r'author/(?P<pk>[0-9]+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
]
```

O atributo ``fields`` determina quais campos do model devem estar presentes no
formulário. É obrigatório especificar o atributo ``fields`` ou então o atributo
``form_class``, nunca os dois ao mesmo tempo, pois isso geraria uma exceção
[``ImproperlyConfigured``](https://docs.djangoproject.com/en/1.8/ref/exceptions/#django.core.exceptions.ImproperlyConfigured)

É importante notar também que a ``DeleteView`` exibe as informações do objeto que
será deletado quando é acessada usando o verbo ``GET``, quando usado o verbo
``POST`` o objeto é efetivamente apagado.

**DICA**: O nome dos templates é determinado da seguinte forma:

- ``CreateView`` e UpdateView usam myapp/author_form.html
- ``DeleteView`` usa myapp/author_confirm_delete.html

## <a name="date_views"></a>Date Views

Date-based generic views são views com a função de exibir páginas com dados
filtrados por datas, por exemplo: posts em um blog, notícias, consultas ao médico, etc.

### <a name="archive_view"></a>ArchiveIndexView

Uma página que exibe os "últimas" objetos inseridos, desconsiderando aqueles com uma
data futura a não ser que o atributo ``allow_future`` seja definido como ``True``

É importante notar que:

- O nome default do ``context_object_name`` é ``latest``.
- O sufixo ``_archive`` no nome do template.
- Além da lista de objetos o contexto também contem a variável ``date_list``
  contendo todos os anos que tem objetos em ordem decrescente.
  Isso pode ser alterado para mês ou dia usando o atributo
  ``date_list_period``. Isso se aplica a todas as *Data-based generic views*

Implementação simples:

**urls.py**
```python

from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView

from myapp.models import Article

urlpatterns = [
    url(r'^archive/$',
        ArchiveIndexView.as_view(model=Article, date_field="pub_date"),
        name="article_archive"),
]
```

### <a name="year_view"></a>YearArchiveView

Uma página para exibir um arquivo anual. Retorna todos os objetos de um
determinado ano.

No contexto além da lista de objetos temos ainda:

- ``date_list``: Um objeto QuerySet contendo todos os meses que tenham objetos
    naquele ano representados como objetos datetime.datetime em ordem crescente.
- ``year``: Um objeto datetime.datetime representando o ano atual
- ``next_year``: Um objeto datetime.datetime representando o próximo ano
- ``previous_year``: Um objeto datetime.datetime representando o ano anterior

Exemplo de implementação:

**views.py**
```python
from django.views.generic.dates import YearArchiveView

from myapp.models import Article

class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True
```

**urls.py**
```python
from django.conf.urls import url

from myapp.views import ArticleYearArchiveView

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/$',
        ArticleYearArchiveView.as_view(),
        name="article_year_archive"),
]
```

**article_archive_year.html**
```html
<ul>
    {% for date in date_list %}
        <li>{{ date|date }}</li>
    {% endfor %}
</ul>
```

### <a name="month_view"></a>MonthArchiveView

Uma página para exibir um arquivo mensal. Retorna todos os objetos de um
determinado mês.

No contexto além da lista de objetos temos ainda:

- ``date_list``: Um objeto QuerySet contendo todos os dias que tenham objetos
    naquele mês representados como objetos datetime.datetime em ordem crescente.
- ``month``: Um objeto datetime.datetime representando o mês atual
- ``next_month``: Um objeto datetime.datetime representando o próximo mês
- ``previous_month``: Um objeto datetime.datetime representando o mês anterior

Exemplo de implementação:

**views.py**
```python
from django.views.generic.dates import MonthArchiveView

from myapp.models import Article

class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
```

**urls.py**
```python
from django.conf.urls import url

from myapp.views import ArticleMonthArchiveView

urlpatterns = [
    # Example: /2012/aug/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        ArticleMonthArchiveView.as_view(),
        name="archive_month"),
    # Example: /2012/08/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
        ArticleMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
]
```

**article_archive_month.html**
```html
<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_month %}
        Previous Month: {{ previous_month|date:"F Y" }}
    {% endif %}
    {% if next_month %}
        Next Month: {{ next_month|date:"F Y" }}
    {% endif %}
</p>
```

### <a name="week_view"></a>WeekArchiveView

Uma página para exibir um arquivo semanal. Retorna todos os objetos de uma
determinada semana.

No contexto além da lista de objetos temos ainda:

- ``week``: Um objeto datetime.datetime representando a semana atual
- ``next_week``: Um objeto datetime.datetime representando a próxima semana
- ``previous_week``: Um objeto datetime.datetime representando a semana anterior

Implementação simples:

**views.py**
```python
from django.views.generic.dates import WeekArchiveView

from myapp.models import Article

class ArticleWeekArchiveView(WeekArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    week_format = "%W"
    allow_future = True
```

**urls.py**
```python
from django.conf.urls import url

from myapp.views import ArticleWeekArchiveView

urlpatterns = [
    # Example: /2012/week/23/
    url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
        ArticleWeekArchiveView.as_view(),
        name="archive_week"),
]
```

**article_archive_week.html**
```html
<h1>Week {{ week|date:'W' }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_week %}
        Previous Week: {{ previous_week|date:"F Y" }}
    {% endif %}
    {% if previous_week and next_week %}--{% endif %}
    {% if next_week %}
        Next week: {{ next_week|date:"F Y" }}
    {% endif %}
</p>
```

### <a name="day_view"></a>DayArchiveView

Uma página para exibir um arquivo diário. Retorna todos os objetos de um
determinado dia.

No contexto além da lista de objetos temos ainda:

- ``day``: Um objeto datetime.datetime representando o dia atual
- ``next_day``: Um objeto datetime.datetime representando o próximo dia
- ``previous_day``: Um objeto datetime.datetime representando o dia anterior
- ``next_month``: Um objeto datetime.datetime representando o primeiro dia do
    próximo mês
- ``previous_month``: Um objeto datetime.datetime representando o primeiro dia
    do mês anterior

Implementação simples:

**views.py**
```python
from django.views.generic.dates import DayArchiveView

from myapp.models import Article

class ArticleDayArchiveView(DayArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
```

**urls.py**
```python
from django.conf.urls import url

from myapp.views import ArticleDayArchiveView

urlpatterns = [
    # Example: /2012/nov/10/
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',
        ArticleDayArchiveView.as_view(),
        name="archive_day"),
]
```

**article_archive_day.html**
```html
<h1>{{ day }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_day %}
        Previous Day: {{ previous_day }}
    {% endif %}
    {% if previous_day and next_day %}--{% endif %}
    {% if next_day %}
        Next Day: {{ next_day }}
    {% endif %}
</p>
```

### <a name="today_view"></a>TodayArchiveView

É a mesma coisa do ``DayArchiveView`` mas não usa os parâmetros da URL para
determinar o ano/mês/dia.

O que muda é o urls.py, veja o exemplo abaixo:

```python
from django.conf.urls import url

from myapp.views import ArticleTodayArchiveView

urlpatterns = [
    url(r'^today/$',
        ArticleTodayArchiveView.as_view(),
        name="archive_today"),
]
```

### <a name="date_detail_view"></a>DateDetailView

É a mesma coisa que a ``DetailView`` com a diferença que a data é utilizada
junto com o pk/slug para determinar qual objeto deve ser obtido.

O que muda é o urls.py, veja o exemplo abaixo:

```python
from django.conf.urls import url
from django.views.generic.dates import DateDetailView

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
        DateDetailView.as_view(model=Article, date_field="pub_date"),
        name="archive_date_detail"),
]
```

### <a name="conclusao"></a>Conclusão

Longe de tentar exaurir um assunto de tamanha complexidade e abrangência minha
intenção com esse artigo foi mostrar o funcionamento básico das Class Based Views
e quem sabe incentivar você a utilizar CBV's no seu próximo projeto.

Envie para mim qualquer dúvida, crítica ou sugestão que você tiver em qualquer
uma das minhas redes sociais, posso demorar um pouco a responder mas eu respondo! :)

Ah, se você se interessou pelo assunto e quer se aprofundar mais eu aconselho
começar pela [Documentação oficial](https://docs.djangoproject.com/en/1.8/topics/class-based-views/intro/)

### <a name="ref"></a>Referências

- <https://docs.djangoproject.com/en/1.8/topics/class-based-views/>
- <https://docs.djangoproject.com/en/1.8/ref/class-based-views/>
- <https://github.com/django/django/blob/master/django/views/generic/>
