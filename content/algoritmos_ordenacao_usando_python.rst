Algoritmos de Ordenação
########################

:date: 2018-11-29 13:10
:tags: python, algoritmos
:category: Python
:slug: algoritmos-ordenacao
:author: Lucas Magnum
:email:  lucasmagnumlopes@gmail.com
:github: lucasmagnum
:linkedin: lucasmagnum

Fala pessoal, tudo bom?

Nos vídeos abaixo, vamos aprender como implementar alguns dos algoritmos de ordenação usando Python.


Bubble Sort
===========

Como o algoritmo funciona: Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=Doy64STkwlI <https://www.youtube.com/watch?v=Doy64STkwlI&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r&t=0s&index=3>`_.


.. youtube::  Doy64STkwlI

Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=B0DFF0fE4rk <https://www.youtube.com/watch?v=B0DFF0fE4rk&index=3&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r>`_.

.. youtube::  B0DFF0fE4rk

Código do algoritmo

.. code-block:: python

    def sort(array):

        for final in range(len(array), 0, -1):
            exchanging = False

            for current in range(0, final - 1):
                if array[current] > array[current + 1]:
                    array[current + 1], array[current] = array[current], array[current + 1]
                    exchanging = True

            if not exchanging:
                break


Selection Sort
==============

Como o algoritmo funciona: Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=vHxtP9BC-AA <https://www.youtube.com/watch?v=vHxtP9BC-AA&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r&index=4>`_.

.. youtube::  vHxtP9BC-AA

Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=0ORfCwwhF_I <https://www.youtube.com/watch?v=0ORfCwwhF_I&index=5&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r&index=5>`_.

.. youtube::  0ORfCwwhF_I

Código do algoritmo

.. code-block:: python

    def sort(array):
        for index in range(0, len(array)):
            min_index = index

            for right in range(index + 1, len(array)):
                if array[right] < array[min_index]:
                    min_index = right

            array[index], array[min_index] = array[min_index], array[index]


Insertion Sort
==============

Como o algoritmo funciona: Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=O_E-Lj5HuRU <https://www.youtube.com/watch?v=O_E-Lj5HuRU&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r&t=0s&index=6>`_.

.. youtube::  O_E-Lj5HuRU

Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=Sy_Z1pqMgko <https://www.youtube.com/watch?v=Sy_Z1pqMgko&index=7&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r>`_.

.. youtube::  Sy_Z1pqMgko

Código do algoritmo

.. code-block:: python

    def sort(array):
        for p in range(0, len(array)):
            current_element = array[p]

            while p > 0 and array[p - 1] > current_element:
                array[p] = array[p - 1]
                p -= 1

            array[p] = current_element


Merge Sort
==============

Como o algoritmo funciona: Como implementar o algoritmo usando Python: `https://www.youtube.com/watch?v=Lnww0ibU0XM <https://www.youtube.com/watch?v=Lnww0ibU0XM&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r&t=0s&index=8>`_.

.. youtube::  Lnww0ibU0XM


Como implementar o algoritmo usando Python - Parte I: `https://www.youtube.com/watch?v=cXJHETlYyVk <https://www.youtube.com/watch?v=cXJHETlYyVk&index=9&list=PLvo_Yb_myrNBhIdq8qqtNSDFtnBfsKL2r>`_.

.. youtube::  cXJHETlYyVk

Código do algoritmo

.. code-block:: python

    def sort(array):
        sort_half(array, 0, len(array) - 1)


    def sort_half(array, start, end):
        if start >= end:
            return

        middle = (start + end) // 2

        sort_half(array, start, middle)
        sort_half(array, middle + 1, end)

        merge(array, start, end)


    def merge(array, start, end):
        array[start: end + 1] = sorted(array[start: end + 1])

