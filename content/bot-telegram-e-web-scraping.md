Title: Bot telegram mais web scraping
Slug: Bot telegram mais web scraping
Date: 2016-10-23 20:30
Tags: python,blog,tutorial,aulas
Author: Pedro Souza.
About_author: Just another Programmer and Security Researcher, just a noob., 
Email:  souza.vipedro@gmail.com
Github: Pedro-Souza
Facebook: https://www.facebook.com/DeveloperPS
Category: Python, Bot, Telegram, Scraping


Irei separa o artigo em 2 partes para não ficar extenso. Nessa primeira 
parte irei falar um pouco como criar um bot no telegram e como 
programa-lo para nos responder.

[**Bot simples.**](/bot-telegram-e-web-scraping.md)
**Bot e Web Scraping**

Primeiro de tudo precisamos cria o bot, para isso usamos o próprio bot 
do telegram que faz isso para gente. Para isso bastar iniciar uma 
conversa com o [@BotFather](https://web.telegram.org/#/im?p=@BotFather), ele irá nós da algumas 
opções:

```
/newbot - create a new bot
/token - generate authorization token
/revoke - revoke bot access token
/setname - change a bot's name
/setdescription - change bot description
/setabouttext - change bot about info
/setuserpic - change bot profile photo
/setinline - change inline settings
/setinlinegeo - toggle inline location requests
/setinlinefeedback - change inline feedback settings
/setcommands - change bot commands list
/setjoingroups - can your bot be added to groups?
/setprivacy - what messages does your bot see in groups?
/deletebot - delete a bot
/newgame - create a new game
/listgames - get a list of your games
/editgame - edit a game
/deletegame - delete an existing game
/cancel - cancel the current operation

```

As que nós interessa por enquanto são:

```
/newbot - Cria um novo bot. 
/setdescription - Adiciona uma descrição ao nosso bot.
/setuserpic - Adiciona uma imagem ao nosso bot.
```

Feito isso agora temos um token, que iremos usar para dar funções e vida 
ao bot. Para isso iremos usar a lib telegram-bot, ela irá facilitar a 
nosso vida, assim não iremos precisar mexer diretamente com a API do 
telegram.

### Instalando telegram-bot utilizando o pip

```bash 
pip install python-telegram-bot
```

Agora com a biblioteca instalada iremos programar um mini bot para nós falar as horas.

```python

#!/usr/bin/env python3
# -*- coding:utf-8  -*-

from telegram.ext import Updater, CommandHandler
from time import strftime

up = Updater('Insira o token aqui.')


def Horas(bot, update):

    msg = "Olá {user_name} agora são: "
    msg += strftime('%H:%M:%S')

    bot.send_message(chat_id=update.message.chat_id,
                     text=msg.format(
                         user_name=update.message.from_user.first_name))


up.dispatcher.add_handler(CommandHandler('horas', Horas))
up.start_polling()

```

### Entendendo o código. 

1 - Importamos tudo que iremos utilizar. <br >
2 - Informamos o token do nosso bot. <br >
3 - Criamos uma função que pega a horas com strftime e responde no chat. <br >
4 - Criamos um comando para o nosso bot, no caso o /horas. <br >
5 - Startamos o bot.<br >

Feito isso quando mandar um /horas para o bot ele irá nos responder com: "Olá SeuNome agora são 
Horas."

Caso você queira adicionar mais funções ao bot, 
[aqui](http://python-telegram-bot.readthedocs.io/en/latest/) está a documentação da biblioteca.

Na próxima parte iremos escolher alguns site que fale sobre Python e fazer Scraping nele, assim 
sempre que ele tiver uma nova postagem nosso bot vai nós enviar uma mensagem informando.



