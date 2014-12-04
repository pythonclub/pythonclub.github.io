Title: Desenvolvendo com Bottle - Parte 1
Slug: desenvolvendo-com-bottle-parte-1
Date: 2014-12-03 19:40
Tags: bottle,python
Author: Eric Hideki
Email:  eric8197@gmail.com
Github: erichideki
Site: http://ericstk.wordpress.com
Twitter: erichideki
Linkedin: erichideki
Category: begginers, bottle, tutorial

# Bottle, framework full-stack sem Django
-------

#Esse artigo foi originalmente traduzido de:

[http://www.avelino.xxx/2014/12/bottle-full-stack-without-django]

Este artigo é baseado em uma palestra que apresentei aqui no Brasil, seguem os [slides](https://speakerdeck.com/avelino/bottle-o-full-stack-sem-django)!

![Bottle micro framework web](/images/bottle.png)

Bottle é um micro framework web compatível com WSGI, depende apenas da biblioteca padrão do Python, sendo compatível com Python 2.6, 2.7, 3.2, 3.3 e 3.4, [sendo um arquivo único](https://github.com/defnull/bottle/blob/master/bottle.py). Ele foi criado pelo Marcel Hellkamp ([@defnull](https://github.com/defnull)) e mantido pela [comunidade](https://github.com/orgs/bottlepy/people) que mantém esse framework.

[Django](https://www.djangoproject.com/) é um framework para rápido desenvolvimento na web, escrito em Python, no qual usa o padrão MTV(model-template-view), sendo pragmático. Foi originalmente criado como um sistema de gerenciamento de um site jornalístico na cidade de Lawrence, Kansas. Se tornou um projeto open-source e foi publicado sobre a licença BSD em 2005. O nome Django foi inspirado pelo músido de jazz Django Reinhardt. Django se tornou muito conhecido pelas suas baterias inclusas, i.e diversas bibliotecas distribuídas que se juntaram ao centro do framework para simplificar o trabalho (chamado "Full stack").

Pragmatismo é o que contém a prática, considerações realistas, com objetivos bem definidos. Ser pragmático é ser prático tendo objetivos definidos. Em outras palavras, o time que desenvolve o Django toma algumas modelagens de arquitetura e quem usa Django segue essa arquitetura sem ser capaz de mudá-la facilmente.

Isto é bom para um framework web que tem baterias inclusas? Depente, se você usa tudo o que o framework oferece, sim, mas nem todos os designs de aplicações são iguais.

Muitos projetos não usam 80% do que Django oferece, nesses casos em que não usam mais que 50%, o custo que pagamos ao oferecer o Django a alguém é alto, já que temos definido a arquitetura, ou seja, perde-se a performance porque o Django tem diversos módulos que não serão usados e obrigatoriamente subirá alguns módulos que não iremos usar. Quando nós usamos um micro framework, fazemos toda a arquitetura da aplicação, então não temos previamente preparado a arquitetura para desenvolver o necessário, dedicando o tempo do time para definir a arquitetura da aplicação.

Todos os pacotes que nós temos na biblioteca padrão do Python/Django podem ser substituídas usando um micro framework!

* ORM - [SQLAlchemy](http://www.sqlalchemy.org/) to [bottle-sqlalchemy](https://github.com/iurisilvio/bottle-sqlalchemy)
* Forms - [WTForms](https://wtforms.readthedocs.org/en/latest/)
* Template Engine - [Jinja2](http://jinja.pocoo.org/docs/dev/), [mako](http://www.makotemplates.org/), etc
* Migration - [Alembic](http://alembic.readthedocs.org/en/latest/)


## SQLAlchemy

O SQLAlchemy existe antes do Django, [sim, antes do Django](https://github.com/zzzeek/sqlalchemy/commit/ec052c6a1f1fb0236bd367c510d82f076cb67bc9) e desde 2005 temos um time focado no desenvolvimento da ORM, ao contrário do Django que dispṍe tempo cuidando do framework web + ORM (Eu acredito que eu não preciso falar com um desenvolvedor focado render mais do que um desenvolvedor não focado).

Estrutura de um modelo:

```python
class Entity(Base):
    __tablename__ = 'entity'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Entity('%d', '%s')>" % (self.id, self.name)
```

## WTForms

A solução alternativa para aqueles que não usam Django e precisam trabalhar com formulários, nós temos o WTForms, que foi criado em [2008](https://github.com/wtforms/wtforms/commit/c0998bac1a4d5cd5fdf43a825529a64e24dea9a5) e atualizado ainda hoje!

Estrutura de um formulário:

```python
class UserForm(Form):
    name = TextField(validators=[DataRequired(), Length(max=100)])
    email = TextField(validators=[DataRequired(), Length(max=255)])
```

## Mecanismo de template

Jinja2 é um moderno e contém um design de template amigável para Python, modelado após os templates do Django. É rápido, amplamente usado e seguro com a opcional área restrita de template no ambiente de desenvolvimento.

Estrutura de um template:

```html
<title>{% block title %}{% endblock %}</title>
<ul>
{% for user in users %}
  <li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
</ul>
```

## Migrações

A utilização do Alembic começa com a criação do ambiente de migração. Este é o diretório de arquivos que especificam para uma particular aplicação. O ambiente de migração é criado apenas uma vez, e é mantido ao longo do desenvolvimento do código da aplicação.

Estrutura de uma migração:

```python
revision = '1975ea83b712'
down_revision = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    pass

def downgrade():
    pass
```

Como criar a evolução e o rebaixamento:

```python
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
```

Estrutura de alteração de tabela:

```python
"""
$ alembic revision -m "Add a column"
"""

revision = 'ae1027a6acf'
down_revision = '1975ea83b712'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
```


## Conclusão

Exatamente o que você vê, tudo o que o Django contém temos fora do conjunto do Django. Eu não escreveria esse artigo para falar mal do Django, e sim mostrar que existem outras soluções para desenvolvimento full stack. Muitas pessoas usam o Django mas não entendem o ambiente Python, hoje o Django traz muitas coisas preparadas que fazem alguns desenvolvedores serem preguiçosos e não adquirir experiência em arquitetura de software.

Venha ajudar o Bottle, somos uma comunidade em crescimento, para contribuir com o código do Bottle, olhe essa issue que nós abrimos. Em caso de dúvidas, nós temos uma lista de e-mail e um canal IRC.

[Se envolva!](http://bottlepy.org/docs/dev/development.html#get-involved)
[http://www.avelino.xxx/2014/12/bottle-full-stack-without-django]:http://www.avelino.xxx/2014/12/bottle-full-stack-without-django
