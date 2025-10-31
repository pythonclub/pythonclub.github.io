Title: Testando código que chama serviços da AWS
Slug: testando-codigo-aws
Date: 2025-10-27 21:30
Category: Python
Tags: python, performance
Author: Eduardo Klosowski
Email: eduardo_klosowski@yahoo.com
Github: eduardoklosowski
Twitter: eduklosowski
Site: https://dev.to/eduardoklosowski
About_author: Mestre em computação aplicada, programador backend com conhecimento de DevOps

Eu desenvolvo sistemas que utilizam os serviços da [AWS](https://aws.amazon.com/pt/) faz algum tempo, e ao longo desse tempo houve mudanças na forma como escrevo testes de código que fazem chamadas a seus serviços. Esse texto tem como objetivo apresentar algumas abordagens para escrita de testes que utilizei, e discutir o que motivou suas evoluções, destacando características de cada abordagem. Ao final, pretendo apresentar um padrão que acredito ser uma forma bastante prática de escrever testes de código que interage com serviços da AWS, usando uma biblioteca em [Python](https://www.python.org/) que desenvolvi implementando esse padrão, mas que também poderia ser adaptado para outros contextos (serviços) e linguagens.

## Código a ser testado

Antes de iniciar a discussão sobre os testes, quero apresentar um exemplo de código para ser testado. Ele é uma função que deve consumir mensagens enviadas para uma fila [SQS](https://aws.amazon.com/pt/sqs/), realizar um processamento com a informação contida nas mensagens, e enviar o resultado para outra fila SQS.

```python
import json

def funcao1(cliente_sqs, fila1_url, fila2_url):
    # Recebe até 10 mensagens do SQS
    msgs_recebidas = cliente_sqs.receive_message(
        QueueUrl=fila1_url,
        MaxNumberOfMessages=10,
    )

    # Percorre as mensagens recebidas
    for msg in msgs_recebidas.get('Messages', []):
        # Recupera valor da mensagem
        corpo = json.loads(msg['Body'])
        n = corpo['n']

        # Processa valor
        resultado = n * 2
        resposta = {'resultado': resultado}

        # Envia mensagem com resultado
        cliente_sqs.send_message(
            QueueUrl=fila2_url,
            MessageBody=json.dumps(resposta),
        )

        # Apaga mensagem atual
        cliente_sqs.delete_message(
            QueueUrl=fila1_url,
            ReceiptHandle=msg['ReceiptHandle'],
        )
```

Esse código é uma função que recebe um objeto para interagir com o serviço SQS (`cliente_sqs`) e a URL de duas filas (`fila1_url` e `fila2_url`). Ele busca até 10 mensagens da `fila1_url` (o máximo permitido por chamada), cada mensagem é um [JSON](https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Scripting/JSON) que possui um número no campo `n`. Após recuperar esse valor, um processamento é feito (nesse caso multiplicar o valor por `2`), um novo JSON é gerado e enviado para a `fila2_url`. Se tudo isso ocorrer conforme esperado, a mensagem processada é removida da `fila1_url`, evitando que ela volte para a fila e eventualmente ser feito uma nova tentativa de processá-la. Esse processo é repetido para cada mensagem recebida.

## Teste unitário com *mock*

Uma forma bastante simples de testar é fazer testes unitários (também chamados de [testes de unidade](https://pt.wikipedia.org/wiki/Teste_de_unidade)) e usar [*mocks*](https://pt.wikipedia.org/wiki/Objeto_mock). Para o código de exemplo é possível criar um objeto que simula (*mock*) o `cliente_sqs` passado para a função, e registre as funções chamadas dele. Depois de executar a função a ser testada, basta verificar as chamadas feitas no objeto simulado, e assim validar se a função está se comportando como o esperado.

Na biblioteca padrão do Python existe o [`MagicMock`](https://docs.python.org/pt-br/3.13/library/unittest.mock.html), que facilita a criação de *mocks*. Bastando definir o que deve ser retornando em cada função (se ela tiver retorno), e depois verificar como suas funções foram chamadas (`assert`). Caso espera-se que uma função tenha sido chamada de determinada forma e isso não ocorreu, o teste falhará.

Segue a baixo um exemplo de teste unitário com *mock* para o código apresentado anteriormente:

```python
import json
from exemplo.codigo1 import funcao1
from unittest.mock import MagicMock
from uuid import uuid4

def test_funcao1():
    # Mensagens com valores de entrada e resultados esperados
    msgs = [
        {'n': 0},
        {'n': 1},
        {'n': 2},
    ]
    respostas = [
        {'resultado': 0},
        {'resultado': 2},
        {'resultado': 4},
    ]

    # Define outros valores auxiliares para o teste
    fila1_url = 'http://sqs.aws/fila1'
    fila2_url = 'http://sqs.aws/fila2'
    msgs_mockadas = [
        {
            'ReceiptHandle': uuid4().hex,
            'Body': json.dumps(msg),
        } for msg in msgs
    ]

    # Cria e configura mock do SQS
    mock_cliente_sqs = MagicMock()
    mock_cliente_sqs.receive_message.return_value = {
        'Messages': msgs_mockadas,
    }

    # Chama função a ser testada
    funcao1(mock_cliente_sqs, fila1_url, fila2_url)

    # Verifica se a função buscou as mensagens na fila 1
    mock_cliente_sqs.receive_message.assert_called_once_with(
        QueueUrl=fila1_url,
        MaxNumberOfMessages=10,
    )

    # Verifica se as mensagens da fila 1 foram apagadas
    assert mock_cliente_sqs.delete_message.call_count == len(msgs)
    for msg in msgs_mockadas:
        mock_cliente_sqs.delete_message.assert_any_call(
            QueueUrl=fila1_url,
            ReceiptHandle=msg['ReceiptHandle'],
        )

    # Verifica se as respostas estão corretas na fila 2
    assert mock_cliente_sqs.send_message.call_count == len(respostas)
    for esperado in respostas:
        mock_cliente_sqs.send_message.assert_any_call(
            QueueUrl=fila2_url,
            MessageBody=json.dumps(esperado),
        )
```

Essa abordagem tem algumas vantagens, como: Não precisar configurar e acessar o serviço SQS para rodar os testes, executando tudo localmente; E testa um trecho de código de forma isolada (uma função nesse caso), independente de outras partes do código, como o `cliente_sqs`. Porém esse método também apresenta desvantagens, como: Ao isolar uma parte do código, perde-se a certeza se ele funcionará junto com as demais partes do sistema, uma vez que podem existir diferenças entre uma resposta real e a resposta do *mock* (nesse teste o `msgs_mockadas` possui apenas duas chaves, quando numa resposta verdadeira existiriam várias outras também); Além de ser necessário definir toda vez qual o retorno das funções e validar se elas foram chamadas conforme o esperado; Também é possível fazer um *mock* que aceite uma chamada inválida para o serviço real; E como a mensagem enviada é uma string com JSON, a ordem dos campos pode mudar, assim como sua formatação, o que pode causar un falso negativo no teste. Então qualquer alteração de parâmetros da função ou resposta, pode gerar uma incompatibilidade do *mock* com o comportamento real do sistema.

## Teste de integração com uma reimplementação

Partindo mais para uma abordagem de testes de integração, existe uma reimplementação dos serviços da AWS em Python para ser usada em testes chamada [Moto](https://github.com/getmoto/moto) (que também pode ser utilizada em outras linguagens no seu [modo servidor](http://docs.getmoto.org/en/latest/docs/server_mode.html), semelhante ao [LocalStack](https://www.localstack.cloud/)). Assim também é possível rodar os testes localmente, uma vez que ele simula o comportamento dos serviços da AWS. Um exemplo de teste utilizando essa biblioteca pode ser visto a baixo:

```python
import boto3
import json
from exemplo.codigo1 import funcao1
from moto import mock_aws

@mock_aws
def test_funcao1():
    # Mensagens com valores de entrada e resultados esperados
    msgs = [
        {'n': 0},
        {'n': 1},
        {'n': 2},
    ]
    respostas = [
        {'resultado': 0},
        {'resultado': 2},
        {'resultado': 4},
    ]

    # Conecta no SQS
    cliente_sqs = boto3.client('sqs', region_name='us-east-1')

    # Cria filas de teste
    fila1_url = cliente_sqs.create_queue(QueueName='fila1')['QueueUrl']
    fila2_url = cliente_sqs.create_queue(QueueName='fila2')['QueueUrl']

    # Envia mensagens de teste
    for msg in msgs:
        cliente_sqs.send_message(
            QueueUrl=fila1_url,
            MessageBody=json.dumps(msg),
        )

    # Chama função a ser testada
    funcao1(cliente_sqs, fila1_url, fila2_url)

    # Verifica se a função buscou e apagou as mensagens na fila 1
    assert sum(int(attr) for attr in cliente_sqs.get_queue_attributes(
        QueueUrl=fila1_url,
        AttributeNames=[
            'ApproximateNumberOfMessages',
            'ApproximateNumberOfMessagesNotVisible',
        ],
    )['Attributes'].values()) == 0

    # Verifica se as respostas estão corretas na fila 2
    msgs_de_resposta = cliente_sqs.receive_message(
        QueueUrl=fila2_url,
        MaxNumberOfMessages=10,
    )['Messages']
    for msg in msgs_de_resposta:
        cliente_sqs.delete_message(
            QueueUrl=fila2_url,
            ReceiptHandle=msg['ReceiptHandle'],
        )
    assert [
        json.loads(msg['Body']) for msg in msgs_de_resposta
    ] == respostas

    # Remove filas de teste
    cliente_sqs.delete_queue(QueueUrl=fila1_url)
    cliente_sqs.delete_queue(QueueUrl=fila2_url)
```

Diferente do teste anterior, neste não é necessário se preocupar em montar os retornos dos serviços acessados, porém é necessário conhecer melhor o serviço para criar os recursos utilizados pela função a ser testada. Também não existe uma forma de fazer um `assert` para verificar se uma mensagem foi enviada, é necessário buscá-las da fila, e nesse caso, também chamar a função para removê-las, de forma que elas não voltem para a fila, evitando comportamentos não esperados (embora não seja obrigatório ao usar o Moto como um decorador, mas é bom para evitar problemas). E mesmo que possa existir alguma diferença entre o serviço real e sua reimplementação, espera-se que ele seja confiável, e ao atualizar o Moto, todos os testes já serão validados com os novos comportamentos, terceirizando essa responsabilidade do teste.

## Interagindo com outro serviço (SNS)

Pensando em testar outro serviço da AWS, pode-se trocar a fila SQS para qual a resposta do código é enviada por um tópico [SNS](https://aws.amazon.com/pt/sns/). O código a ser testado então fica:

```python
import json

def funcao2(cliente_sqs, cliente_sns, fila_url, topico_arn):
    # Recebe até 10 mensagens do SQS
    msgs_recebidas = cliente_sqs.receive_message(
        QueueUrl=fila_url,
        MaxNumberOfMessages=10,
    )

    # Percorre as mensagens recebidas
    for msg in msgs_recebidas.get('Messages', []):
        # Recupera valor da mensagem
        corpo = json.loads(msg['Body'])
        n = corpo['n']

        # Processa valor
        resultado = n * 2
        resposta = {'resultado': resultado}

        # Publica mensagem com resultado
        cliente_sns.publish(
            TopicArn=topico_arn,
            Message=json.dumps(resposta),
        )

        # Apaga mensagem atual
        cliente_sqs.delete_message(
            QueueUrl=fila_url,
            ReceiptHandle=msg['ReceiptHandle'],
        )
```

Seu teste pode seguir uma estrutura bastante similar:

```python
import boto3
import json
from exemplo.codigo2 import funcao2
from moto import mock_aws

@mock_aws
def test_funcao2():
    # Mensagens com valores de entrada e resultados esperados
    msgs = [
        {'n': 0},
        {'n': 1},
        {'n': 2},
    ]
    respostas = [
        {'result': 0},
        {'result': 2},
        {'result': 4},
    ]

    # Conecta no SQS e SNS
    cliente_sqs = boto3.client('sqs', region_name='us-east-1')
    cliente_sns = boto3.client('sns', region_name='us-east-1')

    # Cria fila e tópico de teste
    fila_url = cliente_sqs.create_queue(QueueName='fila')['QueueUrl']
    topico_arn = cliente_sns.create_topic(Name='topico')['TopicArn']

    # Envia mensagens de teste
    for msg in msgs:
        cliente_sqs.send_message(
            QueueUrl=fila_url,
            MessageBody=json.dumps(msg),
        )

    # Chama função a ser testada
    funcao2(cliente_sqs, cliente_sns, fila_url, topico_arn)

    # Como fazer um assert das mensagens publicadas no SNS?
    assert ...

    # Remove fila e tópico de teste
    cliente_sqs.delete_queue(QueueUrl=fila_url)
    cliente_sns.delete_topic(TopicArn=topico_arn)
```

Porém como verificar o que foi enviado para o tópico SNS? Como *mocks* não estão sendo utilizados, não tem como fazer um `assert` para verificar se a função foi chamada e com quais parâmetros. O SNS também não tem uma forma direta de recuperar as mensagens publicadas nele. Uma solução possível é criar uma fila SQS, assinar o tópico SNS, de forma que tudo que for enviado para o tópico seja encaminhado para a fila SQS, e validar o tópico SNS a partir da fila SQS (e após a execução do teste, remover a assinatura, fila e tópico). Embora possível, essa solução é bastante trabalhosa e repetitiva, ainda mais se considerar que isso precisará ser refeito em cada teste do projeto que chamar o SNS.

## Simplificando e padronizando (repensando os testes)

Embora a solução apresentada tenha o problema da repetição de código, ela funciona, e para os testes não importa saber criar uma fila ou tópico e removê-los depois (que é uma parte considerável do que é repetido), só importa usá-los. É totalmente plausível (pelo menos na ideia), de na hora de rodar o teste, só perguntar por alguma fila disponível que possa ser utilizada, e depois devolvê-la. Então seria bom se tivesse uma forma de pegar filas e tópicos emprestados para os testes, ou até mesmo criá-los e removê-los, o teste em si não precisa saber o que acontecerá com esses recursos depois de utilizá-los. Na verdade, o teste nem precisaria saber do detalhe de que é necessário primeiro buscar uma mensagem da fila do SQS, e depois deletar essa mensagem, nem de que a mensagem publicada em um tópico SNS precisou passar por uma fila SQS para ser validada.

Pensando dessa forma, só é necessário executar algum código antes do teste para criar os recursos (filas, tópicos...) que serão utilizados, e executar algum código depois dos testes para remover esses recursos criados anteriormente. Além disso, alguma abstração poderia ser criada para simplificar a interação com esses recursos na parte dos testes para facilitar a verificação de sua utilização, que é justamente a parte que importa dos testes.

Para executar algum código antes e depois de algo, no Python pode-se ser usado um [contexto gerenciado](https://docs.python.org/pt-br/3.13/library/stdtypes.html#typecontextmanager) (aquele criado com a estrutura `with ...`), que poderia criar os recursos, passá-lo para o teste, e assim que ele acabar, fazer sua remoção. Porém, o que ele deveria retornar?

Para testar um código que envia mensagens para uma fila SQS, só é necessário saber qual a fila e alguma forma de receber as mensagens enviadas. A identificação de uma fila no SQS se dá através de uma URL, e um [gerador](https://docs.python.org/pt-br/3.13/glossary.html#term-generator) poderia ser criado para abstrair toda a lógica de consumir a fila. Já para testar um código que recebe mensagens de uma fila SQS é necessário saber a URL da fila, e uma função para enviar as mensagens que serão consumidas pelo código a ser testado.

Agora considerando o caso do tópico SNS, toda vez que um tópico for criado, também poderia se criar uma fila SQS que assina esse tópico. A função geradora também poderia buscar nessa fila as mensagens. Isso deixaria o SQS totalmente transparente para os testes (o teste nem saberia que tem uma fila SQS sendo utilizada). Porém para fazer a assinatura, a URL da fila não serve, é necessário seu [ARN](https://docs.aws.amazon.com/pt_br/IAM/latest/UserGuide/reference-arns.html), em outros contextos pode ser necessário o nome e não URL ou ARN.

Para o contexto retornar mais de uma coisa, pode-se utilizar as [tuplas](https://docs.python.org/pt-br/3.13/library/stdtypes.html#tuple) do Python. Porém a questão continua, o que estará nessa tupla? URL da fila? ARN da fila? Nome? Função para enviar mensagens? Gerador para consumir mensagens? Para não ser necessário criar diferentes tuplas para cada caso, pode-se criar uma tupla retornando tudo. Mas pode ser complicado lembrar em que posição está cada coisa, e um código que recebe uma tupla com vários valores e não utiliza a maioria pode gerar confusão. Então em vez de usar tuplas, pode-se criar um objeto seguindo o [modelo de dados do Python](https://docs.python.org/pt-br/3.13/reference/datamodel.html), assim informações (como nome, ARN e URL) podem ir como atributos, a função para enviar mensagens poderia ser um método, e esse objeto também poderia se comportar como um iterador, que é um comportamento do gerador. E por seguir o modelo de dados do Python, isso tudo ainda pareceria algo nativo do Python, onde um objeto abstrairia a fila SQS ou tópico SNS (algo semelhante ao [*page object*](https://www.youtube.com/watch?v=WhZHZ_RYzxw&list=PLOQgLBuj2-3LqnMYKZZgzeC7CKCPF375B&index=18) apresentado no curso de Selenium do [Dunossauro](https://dunossauro.com/)).

E para facilitar ainda mais, esses contextos que criam os recursos podem se tornar [*fixtures*](https://docs.pytest.org/en/stable/explanation/fixtures.html) do [pytest](https://pytest.org/), assim bastaria informar o nome da *fixture* como parâmetro da função de teste que o recurso já seria criado, e assim que o teste terminar, removido.

## Implementando esses padrões nos testes

Os padrões apresentados foram implementados numa biblioteca chamada [pytest-moto-fixtures](https://github.com/eduardoklosowski/pytest-moto-fixtures) (também publicada no [PyPI](https://pypi.org/project/pytest-moto-fixtures/)), assim é possível reutilizá-lo em diferentes testes. Para códigos que utilizam SQS, segue a implementação do [objeto da fila SQS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/services/sqs.py#L17-L107), [contexto para criar fila SQS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/services/sqs.py#L110-L140) e [*fixture* da fila SQS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/fixtures.py#L40-L44) no repositório. Da mesma forma, para códigos que utilizam SNS, segue a implementação do [objeto do tópico SNS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/services/sns.py#L43-L126), [contexto para criar tópico SNS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/services/sns.py#L129-L168) e [*fixture* do tópico SNS](https://github.com/eduardoklosowski/pytest-moto-fixtures/blob/3cdc5b18d6126fca6b78f0f9962bcdbf928ac77f/src/pytest_moto_fixtures/fixtures.py#L60-L64).

Após instalar a biblioteca, o teste da função que recebe mensagens de uma fila SQS e publica a resposta em um tópico SNS fica da seguinte forma:

```python
import json
from exemplo.codigo2 import funcao2

def test_funcao2(sqs_queue, sns_topic):
    # Mensagens com valores de entrada e resultados esperados
    msgs = [
        {'n': 0},
        {'n': 1},
        {'n': 2},
    ]
    respostas = [
        {'resultado': 0},
        {'resultado': 2},
        {'resultado': 4},
    ]

    # Envia mensagens de teste
    for msg in msgs:
        sqs_queue.send_message(body=msg)

    # Chama função a ser testada
    funcao2(sqs_queue.client, sns_topic.client, sqs_queue.url, sns_topic.arn)

    # Verifica se a função buscou e apagou as mensagens na fila do SQS
    assert len(sqs_queue) == 0

    # Verifica se as respostas estão corretas no tópico SNS
    assert len(sns_topic) == len(respostas)
    assert [
        json.loads(msg['Message']) for msg in sns_topic
    ] == respostas
```

Esse teste ficou muito mais simples, focando no que realmente importa para validar se o código está se comportando como deveria, e se aproveita de recursos do Python, como a função [`len`](https://docs.python.org/pt-br/3.13/library/functions.html#len) e [compreensões de lista](https://docs.python.org/pt-br/3.13/tutorial/datastructures.html#list-comprehensions). Toda a criação da fila SQS e tópico SNS se resumiu em adicionar as *fixtures* `sqs_queue` e `sns_topic` como argumentos da função de teste, assim como sua remoção posteriormente.

## Quando precisa de múltiplos recursos do mesmo tipo

O teste anterior foi simples porque precisou de apenas um recurso de cada tipo. Porém se voltar a primeira função, aquela que recebe mensagens de uma fila SQS e envia o resultado para outra fila SQS, é necessário duas filas, mas a biblioteca entrega apenas uma *fixture* que cria uma única fila SQS. Uma opção seria criar outras *fixtures* para criar outras filas, porém quantas? Se criar poucas *fixtures* continuaria faltando filas, se criar muitas elas seriam carregadas sem necessidade.

Outra opção é dar um passo a traz, usando diretamente os contextos gerenciados em vez usá-los através de *fixtures*. O código de teste fica um pouco mais poluído, com comandos para criar as filas, porém possibilita uma maior flexibilidade também, como: Criar mais de uma fila para o teste; Criar filas com nomes específicos (ou que o nome siga um determinado padrão); E controlar quando a fila será criada e removida (ao sair do contexto). Segue um exemplo do teste:

```python
import json
from exemplo.codigo1 import funcao1
from pytest_moto_fixtures.services.sqs import sqs_create_queue

def test_funcao1(sqs_client):
    # Mensagens com valores de entrada e resultados esperados
    msgs = [
        {'n': 0},
        {'n': 1},
        {'n': 2},
    ]
    respostas = [
        {'resultado': 0},
        {'resultado': 2},
        {'resultado': 4},
    ]

    # Cria filas de teste
    with (
        sqs_create_queue(sqs_client=sqs_client) as fila1,
        sqs_create_queue(sqs_client=sqs_client) as fila2,
    ):
        # Envia mensagens de teste
        for msg in msgs:
            fila1.send_message(body=msg)

        # Chama função a ser testada
        funcao1(sqs_client, fila1.url, fila2.url)

        # Verifica se a função buscou e apagou as mensagens na fila1
        assert len(fila1) == 0

        # Verifica se as respostas estão corretas na fila2
        assert len(fila2) == len(respostas)
        assert [
            json.loads(msg['Body']) for msg in fila2
        ] == respostas
```

## Considerações finais

Esse texto apresentou uma sequência de passos e pensamentos que levaram até a criação da biblioteca [pytest-moto-fixtures](https://pypi.org/project/pytest-moto-fixtures/) para auxiliar na escrita de testes de código que utilizam serviços da AWS. Também apresentou como sua arquitetura foi surgindo das necessidades, sempre com o foco em simplificação, e como resolveu essas necessidades.

A biblioteca também possui algumas facilidades que deixaram o código de teste bastante simples, como o uso das *fixtures* para criação de recursos. Junto com o uso das funcionalidades da própria linguagem, isso permitiu um código de teste bastante simples e direto, sem precisar expor detalhes dos serviços utilizados. E para coisas mais complexas ou específicas, a biblioteca também permite utilizar manualmente algumas de suas camadas mais profundas, porém ainda assim de forma simplificada, sem sujar o código tanto quando sua versão sem o uso da biblioteca.

Outra lição que fica é a possibilidade de criarmos bibliotecas para facilitar as coisas repetitivas do dia a dia, e não só usar as feitas por terceiros. Porém isso deve ser feito com estudo para realmente simplificar, caso contrário poderia trazer mais ou outras dificuldades para as atividades. Nessa forma, essa biblioteca seguiu a linha voltada para os testes de integração, outra biblioteca poderia surgir seguindo a ideia de uso de *mocks*, possuindo características diferentes.

Obs: O projeto com os códigos desse artigo pode ser acessado [aqui](https://eduardoklosowski.github.io/blog/testes-aws/testes-aws.tar.gz).

---

Esse artigo foi publicado originalmente no [meu blog](https://eduardoklosowski.github.io/blog/), passe por lá, ou siga-me no [DEV](https://dev.to/eduardoklosowski) para ver mais artigos que eu escrevi.
