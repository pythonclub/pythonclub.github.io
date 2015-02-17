Microframework contra "Baterias Incluídas"
##########################################

:date: 2015-02-17 12:35
:tags: django, flask, python
:category: python
:slug: microframework_contra_baterias_incluidas
:author: Eduardo Klosowski
:email: eduardo_klosowski@yahoo.com
:github: eduardoklosowski
:site: https://eduardoklosowski.wordpress.com/

.. _Django: https://www.djangoproject.com/
.. _Flask: http://flask.pocoo.org/
.. _PHP: https://php.net/
.. _Python: https://www.python.org/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _WTForms: https://wtforms.readthedocs.org/en/latest/

Python_ é uma linguagem de programação que tem a fama existir mais frameworks web que palavras reservadas, isso se reflete em uma diversidade de opções para os mais diversos gostos. Talvez isso seja um reflexo da diversidade de pessoas que utilizam o Python para as mais diversas finalidades.

Quando iniciei no desenvolvimento web, comecei com PHP_, da forma mais simples possível, montando cada página em arquivos separados com alguns includes para não repetir muito o código. Quando migrei para Python, o primeiro impacto foi ter que utilizar algum framework e não seguir a forma de cada página num arquivo, até poderia manter os arquivos utilizando CGI, mas não teria desempenho, ou escrever o WSGI diretamente, mas acabaria criando outro framework para facilitar o processo.

Comecei a aprender o Django_, achei legal, porém foi complicado por ser muito diferente do que eu estava acostumado e passava mais tempo consultando a documentação que programando efetivamente. Com a filosofia de “baterias incluídas”, o Django tem incorporado bibliotecas para as funcionalidades mais comuns de uma página ou aplicação web pode precisar, como formulário, acesso a banco de dados relacionais, paginação, internacionalização…

Outra opção que temos é utilizar um microframework, que auxilie apenas no WSGI e utilizar outras bibliotecas para montar a base da aplicação, como no caso do Flask_. Ele vem por padrão com outras bibliotecas, como o Jinja 2 para auxiliar a escrever o html das páginas e caso precise de banco de dados ou formulários, basta instalar alguma biblioteca como o SQLAlchemy_ e o WTForms_.

A primeira coisa que pode ser notada ao comparar esses dois modelos é a complexidade, com certeza um microframework é mais simples e fácil de aprender, uma vez que você está focado apenas em como interagir com o servidor ou protocolo HTTP, não tem que se preocupar com banco de dados por exemplo.

O primeiro ponto contra o microframework é a necessidade do programador conheçer ou procurar outras bibliotecas para partes específicas da aplicação, como persistência de dados. Muitas vezes isso pode levar ao desenvolvimento de algo que já está pronto e disponível por desconhecimento. Porém o programador não fica restrito ao que o framework suporta, podendo adotar qualquer tipo de biblioteca, diferente do Django que por exemplo não suporta oficialmente nenhum banco NoSQL, é possível utilizá-los, porém você não conseguirá integrá-los nativamente com os models e forms. Além de que utilizar algum framework específico pode aproveitar melhor as funcionalidades de um banco de dados, em vez de funções genéricas suportada por todos.

Por outro lado, uma vantagem de você ter um framework que define as bibliotecas é a possibilidade de integração das mesmas, como no caso do Django, com um model escrito, é extremamente fácil criar um form baseado no mesmo, com validação, ou fazer a migração do esquema da tabela no banco sem precisar escrever tudo na mão ou duplicar o código e lógicas. Também não é necessário sair procurando bibliotecas na internet, e você terá tudo em apenas uma documentação, que na hora de buscar ajuda evita respostas do tipo com a biblioteca tal funciona ou ter que conhecer mais de uma biblioteca que fazem a mesma tarefa para decidir qual das duas utilizar.

Microframeworks e “baterias incluídas” são abordagens opostas, cada uma pode se sair melhor que a outra de acordo com o caso. Se você tiver que desenvolver um sistema que necessite de bibliotecas que o Django oferece e se encaixe na forma dele de resolver os problemas, com certeza é uma ótima opção, uma vez que você terá as bibliotecas integradas e tudo pronto para utilizar. Caso o sistema seja mais simples, não necessitando de todas as bibliotecas oferecidas pelo Django, ou tenha necessidades mais específicas, o Flask começa a ganhar vantagens, uma vez que o fato de ser reduzido pode deixá-lo mais leve ou até ter uma configuração inicial mais rápida.

Com certeza tem o conhecimento das duas abordagens é importante na hora da decisão do framework, nada pior que durante o desenvolvimento o framework ficar atrapalhando, por ele não ter foco para um determinado fim, ou ser tornar burocrático demais para coisas simples. Para quem estiver conhecendo um framework como o Django e acha que algumas coisas seriam mais práticas fazer na mão, tente visualizar todo o processo, que em algum ponto será facilitado por ser desta forma ou mais prático, porém vai necessitar de algum tempo para acostumar.

----

Texto publicado originalmente no meu blog. Acesse https://eduardoklosowski.wordpress.com/ para mais textos como este.
