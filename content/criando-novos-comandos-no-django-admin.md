title: Criando novos comandos no django-admin
Slug: criando-novos-comandos-no-django-admin
Date: 2015-11-29 22:00
Tags: Python, Django
Author: Regis da Silva
Email:  regis.santos.100@gmail.com
Github: rg3915
Twitter: rg3915
Category: Python, Django

Veja aqui como criar o seu próprio comando para ser usado com o django-admin ou manage.py do Django.

O [django-admin ou manage.py][1] já tem um bocado de comandos interessantes, os mais utilizados são:

* [startproject][4] - cria novos projetos.
* [startapp][5] - cria novas apps.
* [makemigrations][6] - cria novas migrações baseadas nas mudanças detectadas nos modelos Django.
* [migrate][7] - sincroniza o banco de dados com as novas migrações.
* [createsuperuser][8] - cria novos usuários.
* [test][9] - roda os testes da aplicação.
* [loaddata][14] - carrega dados iniciais a partir de um json, por exemplo, `./manage.py loaddata fixtures.json`
* [shell][15] - inicializa um interpretador Python interativo.
* [dbshell][18] - acessa o banco de dados através da linha de comando, ou seja, você pode executar comandos sql do banco, por exemplo, diretamente no terminal.
* [inspectdb][16] - retorna todos os modelos Django que geraram as tabelas do banco de dados.
* [runserver][17] - roda o servidor local do projeto Django.

Mas de repente você precisa criar um comando personalizado conforme a sua necessidade. A palavra chave é `BaseCommand` ou [Writing custom django-admin commands][2].

## Começando do começo

> Importante: estamos usando Django 1.8 e Python 3.

### Criando o projeto

Eu usei este [Makefile][13] para criar o projeto.

```bash
wget --output-document=Makefile https://goo.gl/UMTpZ1
make setup
```

Ele vai criar um virtualenv e pedir pra você executar os seguintes comandos:

```bash
source venv/bin/activate
cd djangoproject
make install
```

Pronto! Agora nós já temos um projetinho Django funcionando. Note que o nome da app é **core**.

### Criando as pastas

Para criarmos um novo comando precisamos das seguintes pastas:

    core
    ├── management
    │   ├── __init__.py
    │   ├── commands
    │   │   ├── __init__.py
    │   │   ├── novocomando.py

No nosso caso, teremos 3 novos comandos, então digite, estando na pasta `djangoproject`

```bash
mkdir -p core/management/commands
touch core/management/__init__.py
touch core/management/commands/{__init__.py,hello.py,initdata.py,search.py}
```


## Sintaxe do novo comando

> Importante: estamos usando Django 1.8 e Python 3.

O Django 1.8 usa o `argparse` como parser de argumentos do `command`, mais informações em [module-argparse][19].

```python
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    help = 'Texto de ajuda aqui.'
    option_list = BaseCommand.option_list + (
        make_option('--awards', '-a',
                    action="store_true",
                    help='Ajuda da opção aqui.'),
    )

    def handle(self, **options):
        print('Hello world.')
        if options['awards']:
            print('Awards')
```

Entendeu? Basicamente o `handle` é a função que executa o comando principal, no caso o `print('Hello world.')`, ou seja, se você digitar o comando a seguir ele imprime a mensagem na tela.

```bash
$ ./manage.py hello
Hello World
```

`--awards` é um argumento opcional, você também pode digitar `-a`.

```bash
$ ./manage.py hello -a
Hello World
Awards
```

`action="store_true"` significa que o comando é opcional.

**Obs**: A partir do Django 1.8 os comandos de argumentos opcionais são baseados em `**options`.


Veja uma outra forma de escrever

```python
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Argumento nomeado (opcional)
        parser.add_argument('--awards', '-a',
                            action='store_true',
                            help='Ajuda da opção aqui.')

    def handle(self, *args, **options):
        print('Hello world.')
        if options['awards']:
            print('Awards')
```

A diferença é que aqui usamos `parser.add_argument` ao invés de `make_option`.

### hello.py

```python
from django.core.management.base import BaseCommand, CommandError
# minimalista
class Command(BaseCommand):
    help = 'Print hello world'

    def handle(self, **options):
        print('Hello World')
```

**Uso**

```bash
$ ./manage.py hello
```

### initdata.py

**Objetivo**: Obter alguns filmes de uma api e salvar os dados no banco.

**api**: [omdbapi.com][3]

**models.py**

```python
from django.db import models

class Movie(models.Model):
    title = models.CharField(u'título', max_length=100)
    year = models.PositiveIntegerField('ano', null=True, blank=True)
    released = models.CharField(u'lançamento', max_length=100, default='', blank=True)
    director = models.CharField('diretor', max_length=100, default='', blank=True)
    actors = models.CharField('atores', max_length=100, default='', blank=True)
    poster = models.URLField('poster', null=True, blank=True)
    imdbRating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    imdbID = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'filme'
        verbose_name_plural = 'filmes'

    def __str__(self):
        return self.title
```

Não se esqueça de fazer

```bash
./manage.py makemigrations
./manage.py migrate
```

**admin.py**

Vamos visualizar pelo admin.

```python
from django.contrib import admin
from core.models import Movie

admin.site.register(Movie)
```

Instale o `requests`

```bash
pip install requests
```

**initdata.py**

O código a seguir é longo, mas basicamente temos

* `print_red(name)` função que imprime um texto em vermelho (opcional)
* `get_html(year)` função que lê os dados da api usando [requests][20], e depois escolhe um filme randomicamente a partir de 2 letras
* `get_movie(year)` se o dicionário conter `{'Response': 'True', ...}` então retorna um dicionário do filme localizado
* `save()` salva os dados no banco
* `handle(movies, year)` este é o comando principal. Busca os filmes várias vezes, conforme definido pela variável `movies`, e salva os n filmes.


```python
import random
import string
import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from optparse import make_option
from core.models import Movie


class Command(BaseCommand):
    help = 'Faz o crawler numa api de filmes e retorna os dados.\n \
    Uso: ./manage.py initdata\n \
    ou: ./manage.py initdata -m 20\n \
    ou: ./manage.py initdata -m 20 -y 2015'
    option_list = BaseCommand.option_list + (
        make_option('--movies', '-m',
                    dest='movies',
                    default=10,
                    help='Define a quantidade de filmes a ser inserido.'),
        make_option('--year', '-y',
                    dest='year',
                    action='store',
                    default=None,
                    help='Define o ano de lançamento do filme.'),
    )

    def print_red(self, name):
        ''' imprime em vermelho '''
        print("\033[91m {}\033[00m".format(name))

    def get_html(self, year):
        '''
        Le os dados na api http://www.omdbapi.com/ de forma aleatoria
        e escolhe um filme buscando por 2 letras
        '''

        ''' Escolhe duas letras aleatoriamente '''
        letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
        ''' Se não for definido o ano, então escolhe um randomicamente '''
        if year is None:
            year = str(random.randint(1950, 2015))
        url = 'http://www.omdbapi.com/?t=' + letters + \
            '*&y=' + str(year) + '&plot=short&r=json'
        return requests.get(url).json()

    def get_movie(self, year, **kwargs):
        ''' Retorna um dicionário do filme '''
        movie = self.get_html(year)
        j = 1  # contador
        ''' Faz a validação de Response. Se a resposta for falsa, então busca outro filme. '''
        while movie['Response'] == 'False' and j < 100:
            movie = self.get_html(year)
            self.print_red('Tentanto %d vezes\n' % j)
            j += 1
        return movie

    def save(self, **kwargs):
        try:
            ''' SALVA os dados '''
            Movie.objects.create(**kwargs)
        except ValidationError as e:
            self.print_red(e.messages)
            self.print_red('O objeto não foi salvo.\n')

    def handle(self, movies, year, **options):
        ''' se "movies" não for nulo, transforma em inteiro '''
        if movies is not None:
            movies = int(movies)
        ''' busca os filmes n vezes, a partir da variavel "movies" '''
        for i in range(movies):
            ''' verifica as validações '''
            m = self.get_movie(year)
            if m['imdbRating'] == "N/A":
                m['imdbRating'] = 0.0
            ''' Transforma "year" em inteiro '''
            if "–" in m['Year']:
                m['Year'] = year
            data = {
                "title": m['Title'],
                "year": m['Year'],
                "released": m['Released'],
                "director": m['Director'],
                "actors": m['Actors'],
                "poster": m['Poster'],
                "imdbRating": m['imdbRating'],
                "imdbID": m['imdbID'],
            }
            self.save(**data)
            print('\n', i + 1, data['year'], data['title'])

        print('\nForam salvos %d filmes' % movies)
```

**Uso**

```bash
Usage: ./manage.py initdata [options] 

Faz o crawler numa api de filmes e retorna os dados.
     Uso: ./manage.py initdata
     ou: ./manage.py initdata -m 20
     ou: ./manage.py initdata -m 20 -y 2015
```


### search.py

**Objetivo**: Localizar o filme pelo título ou ano de lançamento.

```python
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from core.models import Movie


class Command(BaseCommand):
    help = "Localiza um filme pelo título ou ano de lançamento.\n \
    Uso: ./manage.py search -t 'Ted 2'\n \
    ou: ./manage.py search -y 2015\n \
    ou: ./manage.py search -t 'a' -y 2015"
    option_list = BaseCommand.option_list + (
        make_option('--title', '-t',
                    dest='title',
                    default=None,
                    help='Localiza um filme pelo título.'),
        make_option('--year', '-y',
                    dest='year',
                    default=None,
                    help='Localiza um filme pelo ano de lançamento.'),
    )

    def handle(self, title=None, year=None, **options):
        ''' dicionário de filtros '''
        filters = {
            'title__istartswith': title,
            'year': year
        }

        filter_by = {key: value for key, value in filters.items() if value is not None}
        queryset = Movie.objects.filter(**filter_by)

        for movie in queryset:
            print(movie.year, movie.title)
        print('\n%s filmes localizados.' % queryset.count())
```

**Uso**

```bash
Usage: ./manage.py search [options] 

Localiza um filme pelo título ou ano de lançamento.
     Uso: ./manage.py search -t 'Ted 2'
     ou: ./manage.py search -y 2015
     ou: ./manage.py search -t 'a' -y 2015
```


[Aqui][10] tem um exemplo legal que eu usei como ideia pra fazer este post.

Mais algumas referências:

[Writing custom django-admin commands][2]

[Zachary Voase: Fixing Django Management Commands][11]

[Adding Custom Commands to manage.py and django-admin.py by dave][12]

[1]: https://docs.djangoproject.com/en/1.8/ref/django-admin/
[2]: https://docs.djangoproject.com/en/1.8/howto/custom-management-commands/
[3]: http://www.omdbapi.com/
[4]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#startproject-projectname-destination
[5]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#startapp-app-label-destination
[6]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#makemigrations-app-label
[7]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#migrate-app-label-migrationname
[8]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#createsuperuser
[9]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#test-app-or-test-identifier
[10]: https://github.com/rhblind/django-gcharts/blob/master/demosite/management/commands/initdata.py
[11]: http://zacharyvoase.com/2009/12/09/django-boss/
[12]: http://thingsilearned.com/2009/03/13/adding-custom-commands-to-managepy-and-django-adminpy/
[13]: https://gist.github.com/rg3915/a26a2daef369b729e2ed
[14]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#loaddata-fixture-fixture
[15]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#shell
[16]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#inspectdb
[17]: https://docs.djangoproject.com/en/1.8/ref/django-admin/#runserver-port-or-address-port
