title: Django Rest Framework - #2 Requests and Responses
Slug: django-rest-framework-requests-responses
Date: 2018-02-14 23:00
Tags: Python, Django, REST
Author: Regis da Silva
Email:  regis.santos.100@gmail.com
Github: rg3915
Twitter: rg3915
Category: Python, Django, REST

* 0 - [Quickstart][10]
* 1 - [Serialization][11]
* 2 - **Requests & Responses**
* 3 - [Class based views][12]

Este post é continuação do post [Django Rest Framework Serialization][11].

O uso de *requests* e *responses* torna nossa api mais flexível. A funcionalidade principal do objeto **Request** é o atributo `request.data`, que é semelhante ao `request.POST`, mas é mais útil para trabalhar com APIs.

## Objeto Response

Introduzimos aqui um objeto `Response`, que é um tipo de `TemplateResponse` que leva conteúdo não renderizado e usa a negociação de conteúdo para determinar o tipo de conteúdo correto para retornar ao cliente.

```python
return Response(data) # Renderiza para o tipo de conteúdo conforme solicitado pelo cliente.
```

Repare também no uso de *status code* pré definidos, exemplo: `status.HTTP_400_BAD_REQUEST`.

E usamos o decorador `@api_view` para trabalhar com funções. Ou `APIView` para classes.

Nosso código ficou assim:

```python
# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Person
from core.serializers import PersonSerializer


@api_view(['GET', 'POST'])
def person_list(request):
    """
    List all persons, or create a new person.
    """
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, pk):
    """
    Retrieve, update or delete a person instance.
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Veja no [GitHub](https://github.com/rg3915/drf/commit/69205da9262415eaf83ff04f22a635e912880a60).


## Usando sufixo opcional

Em `core/urls.py` acrescente

```python
from rest_framework.urlpatterns import format_suffix_patterns

...

urlpatterns = format_suffix_patterns(urlpatterns)
```

E em `views.py` acrescente `format=None` como parâmetro das funções a seguir:

```python
def person_list(request, format=None):

def person_detail(request, pk, format=None):
```

Com isso você pode chamar a api da seguinte forma:

```bash
http http://127.0.0.1:8000/persons.json # ou
http http://127.0.0.1:8000/persons.api
```

Até a próxima.

[10]: http://pythonclub.com.br/django-rest-framework-quickstart.html
[11]: http://pythonclub.com.br/django-rest-framework-serialization.html
[12]: http://pythonclub.com.br/django-rest-framework-class-based-views.html