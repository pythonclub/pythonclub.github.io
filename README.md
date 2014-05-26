[pythonclub.com.br][0]
======================

Blog colaborativo sobre tecnologias que envolvam a linguagem Python


Como Contribuir
---------------

* Faça um fork desse repositório, clicando no botão [![Fork][14]][15], na parte superior direita da pagina do Github
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

Não entendeu nada? Veja o video que explica o processo de fork, clone, push e pull-request : http://pythonclub.com.br/como-fazer-fork-clone-push-pull-request-no-github.html
 

Sincronizando seu fork
----------------------

Caso você já tenha feito fork a algum tempo você tem duas opções para garantir que
estará trabalhando com as ultimas alterações, que pode ser simplesmente deletar
seu fork e fazer um novo ou sincronizar seu fork com o repositório de origem
usando as [instruções contidas na wiki][11]



Informações Técnicas
--------------------

O site pythonclub.com.br está sendo hospedado usando o **[Github Pages][1]**.

O **[Github Pages][1]** hospeda arquivos HTML sem qualquer tipo de custo, bastando 
que exista um repositório chamado ``seu-usuario.github.io`` 
(Perceba que deve ser incluido o ``.github.io``).
Os arquivos HTML devem ser incluidos no branch ``master`` para que o Github automaticamente
publique aqueles arquivos HTML na web no endereço: ``http://seu-usuario.github.io``


Para gerar os arquivos HTML, e visando a facilidade de escrever textos utilizando
a linguagem de marcação [Markdown][11] e [reStructuredText][12], 
utilizamos o **[Pelican][2]**, que é um projeto feito em Python.

Como a branch ``master`` é usada internamente pelo Github para servir os
arquivos HTML, criamos uma branch chamado ``pelican`` para armazenar os arquivos
de configuração e as publicação em seu "estado-bruto".

Essa branch está definida
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

Alguns dos contribuidores criaram o compromisso de publicar alguns artigos.

Foi estabelecido um prazo maximo para a entrega dos artigos com o intuito de que o contribuidor realmente publique o artigo com o conteudo que ele mesmo definiu.

Você pode ver a lista contendo os nomes dos artigos nesta planilha no [Google Drive][7].

Quando tiver um assunto e uma data de entrega, adicione na planinha, ao finalizar o seu artigo, envie o pull request e atualize a planilha marcando que sua publicação já foi entregue.


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
[11]: https://github.com/pythonclub/pythonclub.github.io/wiki/Sincronizando-seu-fork-com-o-reposit%C3%B3rio-principal
[12]: http://br-mac.org/2013/09/o-que-e-markdown.html
[13]: http://pt.wikipedia.org/wiki/Restructuredtext
[14]: https://github.com/pythonclub/pythonclub.github.io/raw/pelican/content/images/pythonclub_geral/fork_git_hub0_o.png
[15]: https://github.com/pythonclub/pythonclub.github.io/fork
