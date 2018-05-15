Title: Monitorando Ips Duplicados na Rede
Slug: monitorando-ips-duplicados-na-rede
Date: 2018-05-15 10:24:00
Category: Network
Tags: python,tutorial,network,scapy,defaultdict
Author: Silvio Ap Silva
Email: contato@kanazuchi.com
Github: kanazux
Linkedin: SilvioApSilva
Twitter: @kanazux
Site: http://kanazuchi.com

Muitos administradores de redes e sysadmins encontram problemas de conectividade nos ambientes que administram e por muitas vezes o problema é um simples IP duplicado causando todo mal estar. Agora veremos como usar o scapy e defaultdict da lib collections para monitorar esses IPs.

### Scapy

O Scapy é uma poderosa biblioteca de manipulação de pacotes interativa, com abrangencia a uma enorme quantidade de protocolos provenientes da suite TCP/IP.
Mais informações sobre o scpay pode ser encontrada na [**documentação oficial**](http://scapy.readthedocs.io/en/latest/index.html).
Nesse caso em especifico iremos utilizar do scapy a metaclasse *ARP* e a função *sniff*.

```python
from scapy.all import ARP, sniff
```

#### sniff

Vamos usar a função sniff para monitorar os pacotes que trafegam na rede usando o protocolo ARP.
Pra isso vamos utilizar dela quatro parametros basicos:

```python
sniff(prn=pacotes, filter="arp", iface=interface, timeout=10)
```

* prn, chama uma função para ser aplicada a cada pacote capturado pelo sniff.

* filter, irá filtrar todos os pacotes que contiverem o protocolo ARP.

* iface, determina a interface de rede que será monitorada.

* timeout, irá determinar que nosso monitoramento da rede se dara por 60 segundos.

#### ARP

ARP é uma metaclasse de pacotes com dados sobre o protocolo arp pertencente a camada de enlace de dados.
Iremos utilizar essa metaclasse para filtrar os pacotes com informações de pacotes com respostas a requisições arp. (opcode == 2 [is at])
As informações sobre o protocolo ARP podem serm encontradas na [rfc826](https://tools.ietf.org/html/rfc826) no site do IETF.

### collections.defaultdict

defaultdict é uma subclasse de dict que prove uma instancia de variavel para a chamada de uma chave inexistente.

```python
from collections import defaultdict
list_ips = defaultdict(set)
```

Basicamente nossa função irá monitorar por um certo tempo o trafego de pacotes pela rede adicionar a nossa variavel *list_ips* o endereço ou endereços MAC encontrados.

### Definindo a função que será passada como parametro para o sniff.

Para cada pacote capturado pela função sniff, será checado se o opcode corresponde a um response do protocolo arp.
Caso seja, sera adicionado a nossa defaultdict.

```python
def pacotes(pacote):
    """Checa se o valor do opcode dentro do protocolo arp é igual a 2."""
    if pacote[ARP].op == 2:
        # Se for adiciona o ip de origem e seu mac à dict list_ips
        list_ips[pacote[ARP].psrc].add(pacote[ARP].hwsrc)
```

### Limpando a tabela arp

Para que seja feita novas requisições arp, iremos limpar nossa tabela arp e iniciar o monitoramento da rede.
Pra isso iremos usar o comando arp, dentro do shell do sistema. *(Como uso [FreeBSD](https://www.freebsd.org) vou definir uma função chamando um comando pelo csh)*

```python
import os
os.system('which arp')
/usr/sbin/arp
```

Com posse do caminho do comando arp, irei definir uma função que limpe a tabela e inicie o monitore a rede por 60 segundos.

```python
def monitorar(interface):
    """
    O comando arp no FreeBSD usa os parametros:

    -d para deletar as entradas
    -i para declarar a interface
    -a para representar todas entradas a serem deletas.
    """
    cmd = "/usr/sbin/arp -d -i {} -a".format(interface)
    os.system(cmd)
    sniff(prn=pacotes, filter="arp", iface=interface, timeout=10)
```

E por ultimo chamar a função de monitoramento.
No meu caso eu vou monitorar a interface **em0**.

```python
monitorar("em0")
```

Agora só conferir as entradas em nossa dict.

```python
for ip in list_ips:
    print "IP: {} -> MACs: {}".format(ip, ", ".join(list(list_ips[ip])))

IP: 192.168.213.1 -> MACs: 00:90:0b:49:3d:0a
IP: 192.168.213.10 -> MACs: 08:00:27:bf:52:6d, a0:f3:c1:03:74:6a
```

Eu uso um script rodando nos switchs e gateway da rede que me enviam mensagens assim que ips duplicados são encontrados na rede.
Também da pra usar o **arping** do scpay para fazer as requisições arp e coletar os responses.

Abraços.
