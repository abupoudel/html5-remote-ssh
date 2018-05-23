# HTML5 Remote SSH
HTML5 based Remote SSH with Python backend

# Table of Content
  * [Requirements](#requirements)
  * [Python setup](#python-setup)
  * [WebsocketServer](#websocketserver)
  * [HTML Setup](#html-setup)

# Requirements
  - Python 2.7 (Tested), may work with other version of Python
  - HTML5 browser supporting WebSocket and JSON(you can replace JSON with other library if you donot have support of it)

# Python setup
## Paramiko
[Paramiko](https://github.com/paramiko/paramiko/) is a python based SSH client with good documentation. You can easily install it using following command
```
pip install paramiko
```

## WebsocketServer
I wanted a simplest of the WebSocket server so I selected [this](https://github.com/Pithikos/python-websocket-server). As state [here](https://github.com/Pithikos/python-websocket-server#installation) about the installation, you can easily install it by:
  1. `pip install git+https://github.com/Pithikos/python-websocket-server` (latest code)
  2. `pip install websocket-server` (might not be up-to-date)

# HTML Setup
You can just copy [shell.html](html/shell.html) and edit few things up depending on your requirements. The main connection line looks like below and can be edited to set the host/username/password you required
```
mainSocket.send(JSON.stringify({action: 'connect', host:"localhost",port:22,username:'user',password:'password'}));
```
## Parameters
  - action:		'connect' (default to connect for connection)
  - host:		the host you would like to connect to. localhost, www.google.com, 192.168.1.5(this will connect to the server's local network and not your own)
  - port:		default is 22, you can send the port you want
  - username:	the username you want to connect to
  - password:	the password you connect to server for the username


Please feel free to modifiy code on you end, the application still needs upgrade since I only required few basics for my personal project and I wanted to share the code.
