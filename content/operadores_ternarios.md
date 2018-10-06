Title: Trabalhando com operadores ternários
Date: 2018-10-06 09:21
Tags: Python, tutorial, operadores ternários
Category: Geral
Slug: trabalhando-com-operadores-ternarios
Author: Vitor Hugo de Oliveira Vargas
About_author: Eterno estudante e fã da cultura DevOps
Email:  vitor.hov@gmail.com
Github: otoru
Twitter: vitor_hov
Facebook: Ovitorugo
Linkedin: vitor-hov

Quando estamos escrevendo um código qualquer, possivelmente 
a expressão que mais utilizamos é o `if`. Para qualquer 
tarefas que buscamos automatizar ou problemas que buscamos 
resolver, sempre acabamos caindo em lógicas como "Se isso 
acontecer, então faça aquilo, senão faça aquele outro...".

Quando estamos falando de ações a serem executadas, pessoalmente
gosto da forma com que o código fica organizado em python quando
usamos este tipo de condições, por exemplo:

    :::python

    if vencer_o_thanos:
        restaurar_a_paz()

    else:
        foo()

Vemos claramente onde onde o bloco executado caso `vencer_o_thanos`
seja `True` começa e/ou termina graças a indentação. Quanto mais `if`s
você concatenar, mais bonito seu código fica e em momento algum  o mesmo
se torna mais consfuso (ao menos, não deveria se tornar).
Entretanto, sempre fico extremamente incomodado quando tenho de 
escrever um bloco tão longo para apenas marcar uma variável. Um bloco
de código como o abaixo me da um grande incomodo.

    :::python

    if vencer_o_thanos:
        paz = True

    else:
        paz = False

Por isso, para trabalhar com variáveis que possuem um valor condicional,
gosto sempre de trabalhar com expressões condicionais, ou como costumam
ser chamadas, **operadores ternários**.

Operadores ternários são todos os operadores que podem receber três 
operandos. Como as expressões condicionais costumam ser os operadores 
ternários mais populares nas linguagens em que aparecem, acabamos por 
associar estes nomes e considerar que são a mesma coisa. Cuidado ao tirar
este tipo de conclusão, mesmo que toda vogal esteja no alfabeto, o 
alfabeto não é composto apenas por vogais.

A estrutura de uma expressão condicional é algo bem simples, veja só:

    :::python

    paz = True if vencer_o_thanos else False
    tipo_de_x = "Par" if x % 2 == 0 else "impar"

Resumidamente, teremos **um valor seguido de uma condição e por fim seu 
valor caso a condição seja falsa**. Pessoalmente acredito que apesar de um
pouco diferente, essa forma de escrita para casos como o exemplificado acima
é muito mais clara, mais explicita.

Se você fizer uma tradução literal das booleanas utilizadas no primeiro exemplo,
lerá algo como `paz é verdadeira caso vencer_o_thanos, caso contrário é Falsa.` 
já o segundo exemplo fica mais claro ainda, pois lemos algo como 
`tipo_de_x é par caso o resto da divisão de x por 2 seja 0, se não, tipo_de_x é impar.`.

Interpretar código dessa forma pode ser estranho para um programador. Interpretar
uma abertura de chave ou uma indentação já é algo mas natural. Todavia, para aqueles
que estão começando, o raciocínio ocorre de forma muito mais parecida com a descrita
acima. Espero que tenham gostado do texto e que esse conhecimento lhes seja útil.