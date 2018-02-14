title: Django Rest Framework - #3 Class Based Views
Slug: django-rest-framework-class-based-views
Date: 2018-02-15 23:00
Tags: Python, Django, REST
Author: Regis da Silva
Email:  regis.santos.100@gmail.com
Github: rg3915
Twitter: rg3915
Category: Python, Django, REST

* 0 - [Quickstart][10]
* 1 - [Serialization][11]
* 2 - [Requests & Responses][12]
* 3 - **Class based views**

Este post é continuação do post [Django Rest Framework Requests & Responses][12].

Finalmente chegamos as views baseadas em classes. A grande vantagem é que com poucas linhas de código já temos nossa API pronta.

Veja como fica a [views.py](https://github.com/rg3915/drf/blob/b0aa989ffc756e6dc5f65e172dfb43d47127d743/core/views.py):

```python
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Person
from core.serializers import PersonSerializer


class PersonList(APIView):
    """
    List all persons, or create a new person.
    """

    def get(self, request, format=None):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(APIView):
    """
    Retrieve, update or delete a person instance.
    """

    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

E `urls.py`:

```python
urlpatterns = [
    path('persons/', views.PersonList.as_view()),
    path('persons/<int:pk>/', views.PersonDetail.as_view()),
]
```

## Usando Mixins

Repare que no exemplo anterior tivemos que definir os métodos `get()`, `post()`, `put()` e `delete()`. Podemos reduzir ainda mais esse código com o uso de mixins.

```python
from rest_framework import mixins
from rest_framework import generics
from core.models import Person
from core.serializers import PersonSerializer


class PersonList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PersonDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
```

## Usando generic class-based views

E para finalizar usamos `ListCreateAPIView` e `RetrieveUpdateDestroyAPIView` que já tem todos os métodos embutidos.

```python
from rest_framework import generics
from core.models import Person
from core.serializers import PersonSerializer


class PersonList(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
```

Versão final de [views.py](https://github.com/rg3915/drf/blob/263ca63e5c8e2dd2e0f5d6c88c5733fcfdab4f74/core/views.py).

Abraços.

[10]: http://pythonclub.com.br/django-rest-framework-quickstart.html
[11]: http://pythonclub.com.br/django-rest-framework-serialization.html
[12]: http://pythonclub.com.br/django-rest-framework-requests-responses.html