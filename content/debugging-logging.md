Title: Debugging - logging
Date: 2016-11-27 17:48
Tags: python, debugging, logging
Category: Python
Slug: debugging-logging
Author: Bruno Santana
Email:  santanasta@gmail.com
Github: BrunoLSA


Achei algo interessante no livro que estou lendo (Automatize tarefas maçantes com Python) e resolvi compartilhar.

Trata-se do Logging, que ajuda no debug do programa.

Vejam o exemplo nesse programa, com falha:

	:::python
	import logging
	logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


	logging.debug('Start of program')

	def factorial(n):
	    logging.debug('Start of factorial(%s%%)' % (n))
	    total = 1
	    for i in range(n+1):
		    total *= i
		    logging.debug('i is ' + str(i) + ', total is ' + str(total))
	    logging.debug('End of factorial(%s%%)' % (n))
	    return total

	print(factorial(5))
	logging.debug('End of program')


O programa retorna:

	:::python
	 2016-11-15 16:17:30,339 - DEBUG - Start of program
	 2016-11-15 16:17:30,340 - DEBUG - Start of factorial(5%)
	 2016-11-15 16:17:30,340 - DEBUG - i is 0, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - i is 1, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - i is 2, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - i is 3, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - i is 4, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - i is 5, total is 0
	 2016-11-15 16:17:30,340 - DEBUG - End of factorial(5%)
	 2016-11-15 16:17:30,340 - DEBUG - End of program
	0

Dessa forma, podemos ver o passo a passo que o programa está realizando e identificar onde está o erro. No caso, vemos que para corrigir o problema, devemos alterar o **for i in range(n+1):** para **for i in range(1, n+1):**.
Quando o desenvolvedor não quiser mais visualizar as mensagens de logging, basta chamar **logging.disable(logging.CRITICAL)** logo embaixo do **import logging**. Essa função faz com que não seja necessário alterar o programa removendo todas as chamadas de logging manualmente.

Também é possível gravar as mensagens de log num arquivo, ao invés de mostrá-las na tela. A função aceita o argumento **filename**.

	:::python
	import logging
	logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


Lado negativo do uso dessa função: a leitura do código fica difícil, por causa desse monte de logging.debug no meio do código. Para evitar isso, pode-se usar um decorator.




