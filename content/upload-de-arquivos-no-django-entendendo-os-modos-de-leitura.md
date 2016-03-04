Title: Upload de arquivos no Django: entendendo os modos de leitura
Date: 2016-02-26 18:39
Tags: django, csv, upload, HttpRequest, UploadedFile
Category: Django
Slug: upload-de-arquivos-no-django-entendendo-os-modos-de-leitura
Author: Eduardo Cuducos
About_author: Sociólogo, geek, cozinheiro e fã de esportes.
Email:  cuducos@gmail.com
Github: cuducos
Site: http://cuducos.me
Twitter: cuducos
Linkedin: cuducos
Alias: /upload-de-arquivos-no-django-entendo-os-modos-de-leitura

Em uma conversa com a galera do [Welcome to the Django](http://welcometothedjango.com.br) acabei experimentando e aprendendo – na prática — sobre _csv_, _strings_, _bytes_, _file object_ e a maneira como uploads funcionam. Registrei minha exploração e espero que mais gente possa encontrar uma ou outra coisa nova aqui!

## O problema

Fui alterar um projeto feito com [Django](http://djangoproject.com), atualizando do Python 2 para o Python 3, e me deparei com um pedaço de uma _view_ que, como o [Henrique Bastos](http://henriquebastos.net) falou, funcionava “por acaso” no Python 2:


```python
def foobar(request):
    …    
    lines = csv.reader(request.FILES['file.csv'])
    for line in lines:
        …
```

Essa _view_ recebe um arquivo `CSV` (upload do usuáio) e só processa as linhas do arquivo, sem salvá-lo em disco. No Python 3, esse trecho da _view_ passou a dar erro:

```
_csv.Error: iterator should return strings, not bytes (did you open the file in text mode?)
```

O Henrique, além de falar que o código funcionava “por acaso”, me lembrou que o `csv.reader(…)` já recebe um arquivo aberto. Assim fui explorar a maneira que o Django estava me entregando os arquivos no `HttpRequest` (no caso da minha _view_, o que eu tinha em mãos no `request.FILES['file.csv']`).

## Simulando o ambiente da _view_

Para explorar isso, eu precisava simular o ambiente da minha _view_. Comecei criando um arquivo simples, `teste.txt`:

```
Linha 1, foo
Linha 2, bar
Linha 3, acentuação
```

Depois fui ler a [documentação do `HttpRequest.FILES`](https://docs.djangoproject.com/en/1.9/ref/request-response/#django.http.HttpRequest.FILES) e descobri que os arquivos ali disponíveis são instâncias de [`UploadedFile`](https://docs.djangoproject.com/en/1.9/ref/files/uploads/#django.core.files.uploadedfile.UploadedFile).

Logo, se eu criar uma instância da classe `UploadedFile`, posso acessar um objeto do mesmo tipo que eu acessava na _view_ pelo `request.FILES['file.csv']`. Para criar essa instância, preciso de um arquivo aberto, algo como `open(file_path, modo)`. Para continuar a simulação, eu precisava saber de que forma o Django abre o arquivo do upload quando instancia ele no `HttpRequest.FILES`.

Eu desconfiava que não era em texto (`r`), que era em binário (`rb`). A documentação do [curl](https://curl.haxx.se/docs/manpage.html#-F), por exemplo, indicava que os arquivos eram enviados como binários. A documentação da [Requests](http://docs.python-requests.org/en/master/user/advanced/#streaming-uploads) tem um aviso grande, em vermelho, desencorajando qualquer um usar outro modo que não o binário.

Lendo mais sobre o `UploadedFile` descobri que esse objeto tem um atributo `file` que, é uma referência ao `file object` nativo do Python que a classe `UploadFile` envolve. E esse atributo `file`, por sua vez, tem o atributo `mode` que me diz qual o modo foi utilizado na abertura do arquivo. Fui lá na minha _view_ e dei um `print(request.FILES['file.csv'].file.mode)` e obtive `rb` como resposta.

Pronto! Finalmente eu tinha tudo para simular o ambiente da _view_ no meu [IPython](http://ipython.org):


```python
import csv
from django.core.files.uploadedfile import UploadedFile
uploaded = UploadedFile(open('teste.txt', 'rb'), 'teste.txt')
```

Assim testei o trecho que dava problema…


```python
for line in csv.reader(uploaded.file):
    print(line)
```

… e obtive o mesmo erro.

## Solução

Como já tinha ficado claro, o arquivo estava aberto como binário. Isso dá erro na hora de usar o `csv.reader(…)`, pois o `csv.reader(…)` espera um texto, _string_ como argumento. Aqui nem precisei ler a documentação, só lembrei da mensagem de erro: _did you open the file in text mode?_ – ou seja, _você abriu o arquivo no modo texto?_

Lendo a documentação do `UploadedFile` e do `File` do Django (já que a primeira herda da segunda), achei dois métodos úteis: o `close()` e o `open()`. Com eles fechei o arquivo que estava aberto no modo `rb` e (re)abri o mesmo arquivo como `r`:


```python
uploaded.close()
uploaded.open('r')
```

Agora sim o arquivo está pronto para o `csv.reader(…)`:


```python
for line in csv.reader(uploaded.file):
    print(line)
```

    ['Linha 1', ' foo']
    ['Linha 2', ' bar']
    ['Linha 3', ' acentuação']


Enfim, esse métodos `UploadedFile.close()` e `UploadedFile.open(mode=mode)` podem ser muito úteis quando queremos fazer algo diferente de gravar os arquivos recebidos em disco.

> Quem aprendeu alguma coisa nova?
>
> — Raymond Hettinger
