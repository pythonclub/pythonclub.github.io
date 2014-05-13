[pythonclub.com.br][0]
======================

Blog colaborativo sobre tecnologias que envolvam a linguagem Python


Como Contribuir
---------------

* Faça um fork desse repositório
* Clone seu fork:

    ``git clone --recursive https://github.com/SEU_USUARIO_DO_GITHUB/pythonclub.github.io.git``

* Instale os requirements ``pip install -r requirements.txt``
* Todas as publicações ficam na pasta ``content``, os textos podem ser escritos
  no formato **[Markdown][4]** ou **[reStructuredText][5]**, fique a vontade
  para usar o que você sentir mais afinidade, veja alguns **[exemplos][6]**.
* Após criar ou editar seu artigo faça um pull-request para que ele seja
  adicionado ao site.
* Caso tenha dificuldades para escrever Markdown ou reStructuredText, veja esses editores online que auxiliam sua escrita: 
  * [StackEdit][8]
  * [Dillinger][9]
  * [Prose][10]


Informações Técnicas
--------------------

O site está sendo hospedado usando o **[Github Pages][1]**. Ele hospeda arquivos
HTML sem qualquer tipo de custo, bastando que exista um repositório
chamado ``seu-usuario.github.io`` o que faz com que qualquer arquivo HTML
existente na branch ``master`` seja servido numa web.

Para gerar esses arquivos
HTML utilizamos o **[Pelican][2]**, que é um projeto feito em Python.

Como a branch ``master`` é usada internamente pelo Github para servir os
arquivos HTML. Criamos uma branch chamado ``pelican`` para armazenar os arquivos
de configuração e as publicação em seu "estado-bruto". Essa branch está definida
como padrão para o repositório e você possivelmente não precisará se preocupar
com isso.


Visualizando sua publicação antes de enviar
-------------------------------------------

O **Pelican** conta com algumas facilidades que permitem que você teste o site
localmente na medida que você vai escrevendo o texto e antes de enviar para o
servidor, inclusive vem com um script para facilitar isso.

Para utilizar o script para iniciar basta
executar o comando:

``./develop_server.sh start``

Então basta visitar o endereço [http://localhost:8000/][3]

Para finalizar o servidor use:

``./develop_server.sh stop``

Futuras Publicações
-------------------

As publicações estão no [Google Drive][7], sendo mais fácil e interativo manipular uma planilha Excel.
Quando tiver um assunto e uma data de entrega, adicione na planinha, ao finalizar o seu artigo, envie o pull request e atualiza a planilha marcando que sua publicação já foi entregue.


[0]: http://pythonclub.com.br/
[1]: https://pages.github.com/
[2]: http://docs.getpelican.com/en/3.3.0/
[3]: http://localhost:8000/
[4]: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
[5]: http://docutils.sourceforge.net/docs/user/rst/quickref.html
[6]: https://github.com/pythonclub/pythonclub.github.io/tree/pelican/exemplos
[7]: https://docs.google.com/spreadsheets/d/1sddA5pa5LcssPvibBYOHUujyfRpmL1zKw_-MSn784Tg/edit#gid=0
[8]: https://stackedit-beta.herokuapp.com/ 
[9]: http://dillinger.io/
[10]: http://prose.io/
