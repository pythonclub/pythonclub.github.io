pythonclub.github.io
====================

Blog colaborativo sobre tecnologias que envolvam a linguagem Python


Como Contribuir
---------------

* Faça um fork desse repositório
* Clone seu fork ``git clone git@github.com:USUARIO/pythonclub.github.io.git``
* Todas as publicações ficam na pasta ``content``, os textos podem ser escritos
  no formato **Markdown** ou **reStructuredText**, fique a vontade para usar o
  que você sentir mais afinidade.
* Após criar ou editar seu artigo faça um pull-request para que ele seja
  adicionado ao site.


Informações Técnicas
--------------------

O site está sendo hospedado usando o Github Pages que hospeda arquivos HTML sem
qualquer tipo de custo, bastando para isso que existe uma repositório chamado
``seu-usuario.github.io`` o que faz com que qualquer arquivo HTML existente na
branch master seja servido numa web, para gerar esses arquivos HTML usamos o 
**Pelican** que é um projeto feito em Python.


Visualizando sua publicação antes de enviar
-------------------------------------------

O **Pelican** conta com um micro-servidor de desenvolvimento para que você possa
acompanhar em "tempo-real" as mudanças que você efetua nos seus artigos, para
usa-lo basta usando o comando:

``pelican -r content -o output -s pelicanconf.py``


Futuras Publicações
-------------------

| Autor                   | Assunto                                                                       | Data       |
|-------------------------|-------------------------------------------------------------------------------|------------|
| Renato Oliveira         | Introdução ao django.contrib.auth                                             | 03/05/2014 |
| Régis da Silva          | As 20 principais dúvidas que atormentam um iniciante em Django                | ?          |
| Gilmar Soares           | Parseando sites com BeaultifulSoup                                            | 16/05/2014 |
| Fábio Barrionuevo       | Limpando automaticamente o cache do Django ao fazer deploy do Heroku          | 17/05/2014 |
| Igor Santos             | 5 Django Apps que não vivo sem                                                | 06/05/2014 |
| Guilherme Rezende       | Criando uma ferramenta de pentest com Python, Nmap e Scapy                    | 12/05/2014 |
| Fabiano Góes            | Seu primeiro projeto Django com Sublime Text no Linux                         | 12/05/2014 | 
| Rômulo Collopy          | Deploy de projetos com Django-Fagungis                                        | 05/05/2014 |
| Rafael Trevisan         | Entendendo versionamento com Git                                              | 10/05/2014 |
| Artur Felipe Sousa      | O que é six e como ele te ajuda a escrever código compatível com python 2 e 3 | 29/04/2014 |
| Francisco André         | Configurando um servidor de repositórios Git                                  | 15/05/2014 |
