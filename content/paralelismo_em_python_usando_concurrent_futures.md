Title: Paralelismo em Python usando concurrent.futures
Slug: concorrencia-e-paralelismo-em-python-parte1
Date: 2016-02-11 20:30
Tags: python, concorrencia, paralelismo
Author: José Cordeiro de Oliveira Junior
Email:  cordjr@gmail.com
Github: cordjr
Site: http://evaldojunior.com.br
Twitter: cordjr
Category: Python

Paralelismo em Python usando concurrent.futures
----------------------------------------
Esse artigo tem por objétivo abordadr o uso da bliblioteca concurrent.futures para realizar operções paralelas em python, dito isto, gostaria de conceituar de de forma simples a diferença entre paralelismo e concorrência:

 - **Concorrência** é quando um computador de apenas um core parece de estar realizando varias operações ao mesmo tempo quando na verdade está alternando a execução destas operações de forma tão rapida que temos a ilusão de que o tudo está sendo executado simultaneamente.

 - **Paralelismo** é quando um computador de dois ou mais cores executa operações realmente de forma paralela utilizando para isso os cores disponíves, ou seja, se um determinado computador tem 2 cores posso ter duas operações sendo executas paralelamente cada uma em um core diferente.

 Infelizmente o GIL (Python's global interpreter lock) inpede que se faça paraleleismo usando threads em python , porêm, o modulo multiprocessing (bateria inclusa) facilmente acessível via cuncurrent.futures permite que possámos utilizar multiplos cores de cpu. Para isso, esta modulo 'engana' o GIL cirando novos interpretadores como subprcoessos do processo do interpretador principal sendo que cada subprocesso tem um ligação com o processo principal de forma que recebem instruções para realizar operações e retornar resultados.





