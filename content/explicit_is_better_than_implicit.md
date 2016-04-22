Explicit is better than implicit
===================

Esse post não é diretamente relacionado a desenvolvimento com Python, mas conta a história de uma das muitas experiências que passamos desenvolvendo e mostra como a filosofia e o _mindset_ __Python__ podem nos influenciar a tomar decisões melhores.

## Contexto geral

Atualmente trabalho remotamente pela Toptal, uma empresa de consultoria em _software_ com foco em trabalho remoto e que tem um processo seletivo bastante rígido para garantir uma qualidade acima da média para seus clientes ([saiba mais sobre a Toptal aqui](https://www.toptal.com/#book-tested-programmers)).

No time em que faço parte os papéis são bem definidos entre desenvolvedores _front-end_ e _back-end_ e faço parte da equipe de _back-end_, que usa principalmente __Django__ nas aplicações. À medida que evoluímos e nos tornamos mais maduros como time, buscamos soluções que pudessem otimizar nosso processo de desenvolvimento.

Atualmente utilizamos _CircleCI_ -- uma plataforma para integração e entrega contínuas -- para tarefas como rodar nossa suíte de testes, fazer a integração de nosso código, instanciar uma nova versão de nossos sistemas em um ambiente de _staging_ e criar imagens __Docker__ posteriormente colocadas em produção.

## Melhorias

Nosso time constantemente reavalia processos, ferramentas e o resultado são discussões interessantes sobre como tornar nosso trabalho mais rápido e produtivo.

Recentemente começamos a utilizar um servidor __NPM__ -- um dos mais usados gerenciadores de pacotes para __Javascript__ -- privado para uma melhor separação de pacotes _front-end_, otimizando o tempo de _build_ de _assets_ de 47 para 25 segundos.

Na raiz do nosso projeto temos um _package.json_ com o seguinte conteúdo:

``` json
{
  // [ ... ]
  "dependencies": {
    "cat": "^1.0.0",
    "front": "^1.0.0",
    "core": "^1.0.0",
  },
  // [ ... ]
}
```

Sendo que __cat__, __front__ e __core__ (renomeados para exemplificar) são pacotes mantidos por nós mesmos no __NPM__ privado. Por padrão, se você lista o pacote com `“^”` (como por exemplo acima `“^1.0.0”`), o _npm_ considera apenas o número que representa a _major version_, no caso o número 1, e fará o _download_ da última versão que começa com 1.

Essa abordagem tem quatro pontos fracos:

 1. Ela pode quebrar seu código. Se pacote de terceiro atualizar, seu código pode não estar preparado para lidar com as novas funcionalidades adicionadas, principalmente porque _libs_ evoluem tão rapidamente que se torna fácil acontecer uma atualização sem _backwards compatibility_.
 2. Você não sabe exatamente qual versão do pacote seu sistema está usando em produção. Para saber, você teria que acessar os servidores remotamente e executar o comando `npm list`, por exemplo (poderia fazer localmente também mas existe a possibilidade de que no momento em que ocorreu o _deploy_, aquele pacote estava em uma versão anterior à sua versão local).
 3. Você perde o controle de quando quer que seu sistema utilize a nova versão do pacote.
 4. Se você precisar fazer um _rollback_ ou usar uma imagem antiga de seu sistema em produção, ainda assim ela vai utilizar a última versão do pacote, o que pode levar a mais dores de cabeça.

# Problema

Recentemente tivemos um _bug_ em produção, e uma mudança no pacote _core_ resolveria. __O que fazer com o sistema principal?__ Nada, não era necessária nenhuma alteração. Só precisaríamos gerar uma nova imagem _Docker_ que ela seria montada do zero e no momento de instalar os pacotes _npm_, baixaria a última versão.

Bastava realizar _rebuild_ na branch _master_ no __CircleCI__, que assim que terminado ele trataria de enviar um _webhook_ para o nossa ferramenta que cria imagens _Docker_. Nós utilizamos o seguinte padrão de nomenclatura dessas imagens:
```
myapp-production-<branch>-<sha[:7]>
```
Como não fizemos nenhuma alteração no sistema principal, o _branch_ e o _sha_ continuaram os mesmos.

Resumindo, nosso _Docker_ recebeu um pedido de _build_ para aquela _branch_ e _sha_ e, por padrão, primeiro procurou em seu _cache_ de imagens se já existia alguma imagem pronta com aquele nome. O resultado foi que a mesma imagem, sem o _hotfix_, foi para produção (pois ela havia sido criada antes e no momento em que baixou os pacotes _npm_ ainda não havia alterações no _core_).

Demoramos um pouco para perceber o problema, mas o suficiente para resolvê-lo sem que _stakeholders_ percebessem.

## Solução

Algum tempo depois discutimos e nós desenvolvedores _back-end_ sugerimos a seguinte solução:

``` json
{
  // [ ... ]
  "dependencies": {
    "cat": "1.0.5",
    "front": "1.0.7",
    "core": "1.0.10",
  },
  // [ ... ]
}
```

Com essa abordagem:

1. Você pode fazer _rollback_ do seu código sem problemas pois o código antigo vai usar a versão antiga do pacote.
2. Você tem controle sobre quando quer que seu sistema utilize a nova versão do pacote.
3. Você sabe exatamente quais versões de pacotes seu sistema está utilizando, bastando abrir o _packages.json_.
4. Caso uma nova versão quebre seu código, você pode voltar uma versão rapidamente até que o problema seja resolvido.

O problema que tivemos em produção não aconteceria caso tivéssemos utilizado a abordagem acima. Assim que os pacotes fossem atualizados, criaríamos uma _pull request_ no repositório do sistema principal com as seguintes alterações:

``` diff
diff --git i/package.json w/package.json
index eaae10d..5aa773b 100644
--- i/package.json
+++ w/package.json
@@ -9,7 +9,7 @@
   "dependencies": {
     "cat": "1.0.5",
     "front": "1.0.7",
-    "core": "1.0.10",
+    "core": "1.0.11",
   },
```
Após o _merge_, um novo _build_ aconteceria no __CircleCI__, e um novo _sha_ seria enviado via _webhook_. O _Docker_ não encontraria nenhuma imagem com essa combinação de _branch_ e _sha_ e criaria uma nova do zero. Produção teria o _hotfix_ e não haveria constrangimento.

Os desenvolvedores _front-end_ não gostaram da ideia de ter que atualizar o arquivo toda vez que alguma dependência subisse de versão. Discutimos bastante e a última coisa que eu disse foi: __“from the Zen of Python: explicit is better than implicit”__.

Lição aprendida.
