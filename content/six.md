Title: Sobre o six e como ele ajuda a escrever código compatível com python 2 e 3
Date: 2014-05-04 22:21
Tags: python, six, compatibility
Category: Python
Slug: sobre-o-six-e-como-ele-ajuda-a-escrever-codigo-compativel-com-python-2-e-3
Author: Artur Felipe de Sousa
Email:  arturfelipe.sousa@gmail.com
Github: arturfelipe
Bitbucket: arturfsousa
Site: http://artursousa.com.br
Twitter: arturfsousa
Facebook: ArturFelipe
Linkedin: arturfsousa


### Python 2.x ou python 3.x?

Quem de nós já não se deparou com a seguinte dúvida: Qual versão do
python devo usar para começar meu projeto?

Há 6 anos, em dezembro de 2008 foi lançada a versão 3.0 do python. Uma versão
polêmica, a primeira incopatível com suas anteriores (2.x). A intenção era de
corrigir antigas "chatices" que vinham incomodando o Guido van Rossum e a
comunidade, e remover coisas desnecessárias. Alguns exemplos mais comuns:

* Todas as strings são unicode **str()**
* O comando print virou a built-in **print()**
* Iterators ao invés de listas: **map(), filter(), zip()** e **range()**
* Tipo long passou a ser somente int
* Todas as classes são new-style

Para mais detalhes [https://docs.python.org/3.0/whatsnew/3.0.html](https://docs
.python.org/3.0/whatsnew/3.0.html).

O python 3 já está na versão 3.4 e vem sendo cada vez mais suportado por
bibliotecas e frameworks mais populares tais como:

* Django (1.5+)
* Pyramid (1.3a1+)
* Flask
* SqlAlchemy

Todas essas ferramentas tiveram a mesma preocupação que deve estar passando
pela sua cabeça agora: Como migrar ou criar código compatível o máximo possível
entre essas versões?

É aí que entra a biblioteca six.

### Six?

O six é uma biblioteca de compatibilidade entre o python 2 e 3. O nome "six"
surgiu da grande sacada do Benjamin Petersons, 2 * 3 == 6, muita imaginação
não? Todo o código do six está contido em apenas um arquivo python
[six.py](https://bitbucket.org/gutworth/six/src/a497bee85dd833681574672b5a2ec29
6e33c525c/six.py?at=default "Repositório do six").

Para instalar o six, basta usar o pip:

    :::python
    pip install six

Vamos começar com um exemplo de código que funciona somente na versão 2.7.5:

    :::python
    if isinstance(u'Python 2 compatible', unicode):
        print 'is unicode'

O primeiro erro observado é o comando print que gera um erro de sintaxe, o
seguinte é o identificador unicode que não existe mais no python 3 (passou a
ser str somente).

Uma versão deste código que funciona no python 3.4.0 seria:

    :::python
    if isinstance(u'Python 3 compatible', str):
        print('is unicode')

Utilizando o six para compatibilizar o código, teríamos:

    :::python
    import six
    if isinstance(u'Python 2 and 3 compatible', six.string_types):
        six.print_('is unicode')

No exemplo acima foi utilizada a constante **six.string_types**. Essas
constantes são normalmente utilizadas como segundo argumento da função
**isinstance()**. [Veja mais delas](https://pythonhosted.org/six/#constants).

No python 3 alguns atributos e metódos foram substituídos ou removidos de
alguns tipos de estrutura de dados. Os métodos **iterkeys(), itervalues(),
iteritems()** e **iterlists()**, por exemplo, foram renomeados dos dicionários
por **keys(), values(), items()** e **lists()** respectivamente.

    :::python
    # Python 2.7.5
    > my_info = dict(name='Artur Sousa', age=29)
    > my_info.itervalues()
    <dictionary-valueiterator object at 0x10738e680>
    > my_info.values()
    [29, 'Artur Sousa']

    # Python 3.4.0
    > my_info = dict(name='Artur Sousa', age=29)
    > my_info.values()
    dict_values([29, 'Artur Sousa'])

Versões compatíveis destes métodos podem ser encontradas no six:

    :::python
    # Python 2.x 3.x
    > import six
    > my_info = dict(name='Artur Sousa', age=29)
    > six.itervalues(my_info)
    <dictionary-valueiterator object at 0x10738e680>
    > six.iterkeys()
    <dict_keyiterator object at 0x10b2f4638>

[Dentre outras...](https://pythonhosted.org/six/#object-model-compatibility)

No python 3 algumas libs foram reorganizadas da biblioteca padrão. O
**HTMLParser** por exemplo virou **html.parser**. Para isso o six oferece o
módulo moves.

    :::python
    from six.moves import html_parser # 2.x: HTMLParser 3.x: html.parser
    from six.moves import cPickle  # 2.x: cPickle 3.x: pickle

Uma tabela de compatibilidade de métodos e atributos pode ser vista
[aqui](https://pythonhosted.org/six/#module-six.moves).

Esta foi apenas uma parte das funcionalidades que o six oferece para garantir
o funcionamento de códigos escritos nas versões 2 e 3 do python.

O Django utiliza o six a partir da versão 1.5. Veja um exemplo de uso:

    :::python
    # django.contrib.admin.helpers.py - Django 1.7b3
    class AdminErrorList(forms.utils.ErrorList):
        """
        Stores all errors for the form/formsets in an add/change stage view.
        """
        def __init__(self, form, inline_formsets):
            super(AdminErrorList, self).__init__()

            if form.is_bound:
                self.extend(list(six.itervalues(form.errors)))
                for inline_formset in inline_formsets:
                    self.extend(inline_formset.non_form_errors())
                    for errors_in_inline_form in inline_formset.errors:
                        self.extend(list(six.itervalues(errors_in_inline_form)))

Então galera, esse foi um artigo introdutório sobre o six, mostrando alguns
casos de uso e um pouco das diferenças entre o python 2 e 3. Espero que vocês
tenham gostado. Fiquem à vontade para enviar dúvidas, sugestões ou críticas.

Até mais...
