#数字交易所


#Get Started

virtualenvs 配置： virtualenv venv

激活 virtualenvs： source venv/bin/activate

退出 virtualenvs： deactivate

```
$ pip install -r requirements.txt
```

$ ./apps/trade/main.py
$ ./apps/ws_gateway/main.py
$ ./apps/mailer/main.py
```

# Applications - Trade
Matching engine and the core of the exchange platform

# Applications - Ws Gateway
The HTTP/WebSocket gateway is based on Tornado.  It relays HTTP or websocket API
requests to the trade engine in order to place orders or fetching market data.

# Applications - Mailer
The mailing application... sends mail. To that end, 
it uses Mailchimp's transaction email solution, Mandrill.

E-mail templates are stored under the templates/ dir,
and which template to use (and the data to fill it out)
are supplied by listening on the zeromq socket.

