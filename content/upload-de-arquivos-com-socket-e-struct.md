Title: Upload de Arquivos com Socket e Struct
Slug: upload-de-arquivos-com-socket-e-struct
Date: 2018-05-17 19:24:00
Category: Network
Tags: python,tutorial,network,struct,socket
Author: Silvio Ap Silva
Email: contato@kanazuchi.com
Github: kanazux
Linkedin: SilvioApSilva
Twitter: @kanazux
Site: http://kanazuchi.com

Apesar de termos muitas formas de enviarmos arquivos para servidores hoje em dia, como por exemplo o *scp* e *rsync*, podemos usar o python com seus modulos *built-in* para enviar arquivos a servidores usando struct para serializar os dados e socket para criar uma conexão cliente/servidor.

### *Struct*

O modulo [struct](https://docs.python.org/3/library/struct.html) é usado para converter bytes no python em formatos do struct em C.
Com ele podemos enviar num unico conjunto de dados o nome de um arquivo e os bytes referentes ao seus dados.

Struct também é utilizado para serializar diversos tipos de dados diferentes, como bytes, inteiros, floats além de outros, no nosso caso usaremos apenas bytes.

Vamos criar um arquivo para serializar.

```python
!echo "Upload de arquivos com sockets e struct\nCriando um arquivo para serializar." > arquivo_para_upload
```

Agora em posse de um arquivo vamos criar nossa estrutura de bytes para enviar.

```python
arquivo = "arquivo_para_upload"
```

```python
with open(arquivo, 'rb') as arq:
    dados_arquivo = arq.read()
    serializar = struct.Struct("{}s {}s".format(len(arquivo), len(dados_arquivo)))
    dados_upload = serializar.pack(*[arquivo.encode(), dados_arquivo])
```

Por padrão, struct usa caracteres no inicio da sequencia dos dados para definir a ordem dos bytes, tamanho e alinhamento dos bytes nos dados empacotados.
Esses caracteres podem ser vistos na [seção 7.1.2.1](https://docs.python.org/3/library/struct.html#byte-order-size-and-alignment) da documentação.
Como não definimos, será usado o **@** que é o padrão.

Nessa linha:
```python
serializar = struct.Struct("{}s {}s".format(len(arquivo), len(dados_arquivo)))
```
definimos que nossa estrutura serializada seria de dois conjuntos de caracteres, a primeira com o tamanho do nome do arquivo, e a segunda com o tamanho total dos dados lidos em
```python
dados_arquivo = arq.read()
```

Se desempacotarmos os dados, teremos uma lista com o nome do arquivo e os dados lidos anteriormente.

```python
serializar.unpack(dados_upload)[0]
```

    b'arquivo_para_upload'


```python
serializar.unpack(dados_upload)[1]
```

    b'Upload de arquivos com sockets e struct\\nCriando um arquivo para serializar.\n'


Agora de posse dos nossos dados já serializados, vamos criar um cliente e um servidor com socket para transferirmos nosso arquivo.

### *Socket*

O modulo [socket](https://docs.python.org/3/library/socket.html) prove interfaces de socket BSD, disponiveis em praticamente todos os sistemas operacionais.

#### Familias de sockets

Diversas familias de sockets podem ser usadas para termos acessos a objetos que nos permitam fazer chamadas de sistema.
Mais informações sobre as familias podem ser encontradas na [seção 18.1.1](https://docs.python.org/3/library/socket.html#socket-families) da documentação. No nosso exemplo usaremos a AF_INET.

#### AF_INET

**AF_INET** precisa basicamente de um par de dados, contendo um endereço IPv4 e uma porta para ser instanciada.
Para endereços IPv6 o modulo disponibiliza o **AF_INET6**

#### Constante [SOCK_STREAM]

As constantes representam as familias de sockets, como a constante AF_INET e os protocolos usados como parametros para o modulo socket.
Um dos protocolos mais usados encontrados na maioria dos sistemas é o SOCK_STREAM.

Ele é um protocolo baseado em comunicação que permite que duas partes estabeleçam uma conexão e conversem entre si.

### *Servidor e cliente socket*

Como vamos usar um protocolo baseado em comunicação, iremos construir o servidor e cliente paralelamente para um melhor entendimento.

> Servidor

Para esse exemplo eu vou usar a porta 6124 para o servidor, ela esta fora da range reservada pela IANA para sistemas conhecidos, que vai de 0-1023.

Vamos importar a bilioteca socket e definir um host e porta para passarmos como parametro para a constante AF_INET.

```python
import socket
host = "127.0.0.1"
porta = 6124
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Agora usaremos o metodo bind para criarmos um ponto de conexão para nosso cliente. Esse metodo espera por uma tupla contento o host e porta como parametros.

```python
sock.bind((host, porta))
```

Agora vamos colocar nosso servidor socket em modo escuta com o metodo listen. Esse metodo recebe como parametro um numero inteiro (**backlog**) definindo qual o tamanho da fila que será usada para receber pacotes SYN até dropar a conexão. Usaremos um valor baixo o que evita SYN flood na rede. Mais informações sobre *backlog* podem ser encontradas na [RFC 7413](https://tools.ietf.org/html/rfc7413).

```python
sock.listen(5)
```

Agora vamos colocar o nosso socket em um loop esperando por uma conexão e um inicio de conversa. Pra isso vamos usar o metodo *accept* que nos devolve uma tupla, onde o primeiro elemento é um novo objeto socket para enviarmos e recebermos informações, e o segundo contendo informações sobre o endereço de origem e porta usada pelo cliente.

**Vamos criar um diretório para salvar nosso novo arquivo.**

```python
!mkdir arquivos_recebidos
```

*Os dados são enviados sempre em bytes*. **Leia os comentários**

```python
while True:
    novo_sock, cliente = sock.accept()
    with novo_sock:  # Caso haja uma nova conexão
        ouvir = novo_sock.recv(1024)  # Colocamos nosso novo objeto socket para ouvir
        if ouvir != b"":  # Se houver uma mensagem...
            """
            Aqui usaremos os dados enviados na mensagem para criar nosso serielizador.

            Com ele criado poderemos desempacotar os dados assim que recebermos.
            Veja no cliente mais abaixo qual a primeira mensagem enviada.
            """
            mensagem, nome, dados = ouvir.decode().split(":")
            serializar = struct.Struct("{}s {}s".format(len(nome.split()[0]), int(dados.split()[0])))
            novo_sock.send("Pode enviar!".encode())  # Enviaremos uma mensagem para o cliente enviar os dados.
            dados = novo_sock.recv(1024)  # Agora iremos esperar por eles.
            nome, arquivo = serializar.unpack(dados)  # Vamos desempacotar os dados
            """
            Agora enviamos uma mensagem dizendo que o arquivo foi recebido.

            E iremos salva-lo no novo diretório criado.
            """
            novo_sock.send("Os dados do arquivo {} foram enviados.".format(nome.decode()).encode())
            with open("arquivos_recebidos/{}".format(nome.decode()), 'wb') as novo_arquivo:
                novo_arquivo.write(arquivo)
                print("Arquivo {} salvo em arquivos_recebidos.".format(nome.decode()))

    Arquivo arquivo_para_upload salvo em arquivos_recebidos.

```

> Cliente

Nosso cliente irá usar o metodo *connect* para se connectar no servidor e a partir dai começar enviar e receber mensagens. Ele também recebe como parametros uma tupla com o host e porta de conexão do servidor.

```python
host = '127.0.0.1'
porta = 6124
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria nosso objeto socket
sock.connect((host, porta))
sock.send("Enviarei um arquivo chamado: {} contendo: {} bytes".format(
    arquivo, len(dados_arquivo)).encode())  # Enviamos a mensagem com o nome e tamanho do arquivo.
ouvir = sock.recv(1024)  # Aguardamos uma mensagem de confirmação do servidor.
if ouvir.decode() == "Pode enviar!":
    sock.send(dados_upload)  # Enviamos os dados empacotados.
    resposta = sock.recv(1024)  # Aguardamos a confirmação de que os dados foram enviados.
    print(resposta.decode())

    Os dados do arquivo arquivo_para_upload foram enviados.

```

Agora podemos checar nossos arquivos e ver se eles foram salvos corretamente.

```python
!md5sum arquivo_para_upload; md5sum arquivos_recebidos/arquivos_para_upload

    605e99b3d873df0b91d8834ff292d320  arquivo_para_upload
    605e99b3d873df0b91d8834ff292d320  arquivos_recebidos/arquivo_para_upload

```

Com base nesse exemplo, podem ser enviados diversos arquivos, sendo eles texto, arquivos compactados ou binários.

Sem mais delongas, fiquem com Cher e até a próxima!

Abraços.
