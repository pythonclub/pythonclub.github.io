Title: Extraindo Texto de Imagens com Python
Date: 2015-11-22 17:00
Tags: imagens,ocr,pytesseract,extrair texto
Category: Manipulação de imagens
Slug: extraindo-texto-de-imagens-com-python
Author: André Ramos
Email:  andrel.ramos97@gmail.com
Github: andrelramos
About_author: Programador web/desktop/mobile. Apaixonado por tecnologia, programação e python.

Introdução
-----------

Já precisou extrair texto de imagens mas não sabia como? aprenda como fazer isso com apenas 3 linhas de código (Por isso amo python!). Antes de começarmos, vamos ver um pouco de teoria.

### O que é OCR?

Segundo o Wikipedia, OCR é um acrónimo para o inglês Optical Character Recognition, é uma tecnologia para reconhecer caracteres a partir de um arquivo de imagem ou mapa de bits sejam eles escaneados, escritos a mão, datilografados ou impressos. Dessa forma, através do OCR é possível obter um arquivo de texto editável por um computador. A engine OCR que vamos utilizar é a **Tesseract**, a mesma foi inicialmente desenvolvida nos laboratórios da HP e tem seu projeto hospedado em: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract). Texto adaptado de: [https://pt.wikipedia.org/wiki/Reconhecimento_ótico_de_caracteres](https://pt.wikipedia.org/wiki/Reconhecimento_%C3%B3tico_de_caracteres)

Como descrito acima, já existe uma tecnologia para realizar essa função, então apenas precisamos utilizá-la em nosso script python e assim desenvolvermos o que a imaginação permitir.

### Instalando Dependências (Ubuntu)

Primeiro vamos começar pela instalação do Tesseract OCR. Abra o terminal e digite o seguinte comando:
	
	:::bash
	$ sudo apt-get install tesseract-ocr tesseract-ocr-por

Também precisamos instalar a biblioteca Pillow e suas dependências. Ela será necessária para carregar a imagem para nosso script:

Ubuntu 12.04/14.04:
    
    :::bash
	$ sudo apt-get install python-dev python3-dev build-essential liblcms1-dev zlib1g-dev libtiff4-dev libjpeg8-dev libfreetype6-dev libwebp-dev
	$ sudo -H pip install Pillow

Ubuntu 15.04/15.10/16.04:
	
	:::bash
	$ sudo apt-get install python-dev python3-dev build-essential liblcms2-dev zlib1g-dev libtiff5-dev libjpeg8-dev libfreetype6-dev libwebp-dev
	$ sudo -H pip install Pillow


Agora partiremos para a instalação do wrapper que irá permitir a utilização do Tesseract através do python:

    :::bash
	$ sudo -H pip install pytesseract


### Mão Na Massa!

Finalmente chegamos a parte prática desse artigo. Como dito anteriormente, são apenas 3 linhas de código, mas antes de começar baixe a seguinte imagem para realizar seus testes:

![imagem para teste](images/andrelramos/ocr2.png "Imagem Para Teste")

Agora vamos ao código:

	:::python
	
	from PIL import Image # Importando o módulo Pillow para abrir a imagem no script
	
	import pytesseract # Módulo para a utilização da tecnologia OCR

	print( pytesseract.image_to_string( Image.open('nome_da_imagem.jpg') ) ) # Extraindo o texto da imagem

Simples né? Mas nem sempre o texto sai 100% correto, depende muito da qualidade da imagem e da quantidade de detalhes que a mesma possui, porem existe algumas técnicas usadas para fazer melhorias na imagem diminuindo a chance de erros na hora da extração.

**Alguns links que podem te ajudar a aproveitar ao maximo da tecnologia OCR:**

* [http://pt.scribd.com/doc/88203318/Como-escanear-livros-com-qualidade-e-produzir-textos-por-OCR#scribd](http://pt.scribd.com/doc/88203318/Como-escanear-livros-com-qualidade-e-produzir-textos-por-OCR#scribd)

* [http://profs.if.uff.br/tjpp/blog/entradas/ocr-de-qualidade-no-linux](http://profs.if.uff.br/tjpp/blog/entradas/ocr-de-qualidade-no-linux)

