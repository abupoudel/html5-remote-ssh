# encoding=utf8 
import paramiko									# To handle the SSH
import time										# Handling some sleep
import json										# We are relying on JSON object to send/recieve between browser and socket
from thread import start_new_thread				# Handling multiple SSH sessions
from websocket_server import WebsocketServer	# Minimal WebSocket library
import sys										# Forcing system encoding to UTF-8

reload(sys)  
sys.setdefaultencoding('utf8')

# Client lists to handle connections
clients = {}

# We new client connects
def new_client(client, server):
	print("New client connected")
	clients[client["id"]] = {
		'client' : client,
		'in_active_connection' : False,
		'close_me' : False,
		'closed' : False,
		'terminal' : paramiko.SSHClient(),
		'channel' : None
	}
	myClient = clients[client["id"]]['terminal']
	myClient.set_missing_host_key_policy(paramiko.WarningPolicy())

# starting the connection to new SSH Connection
def start_new_shell(client,server, host, port, username, password):
	myClient = clients[client["id"]]['terminal']
	try:
		myClient.connect(host, username=username, password=password, port=port)
		clients[client["id"]]['in_active_connection'] = True
		clients[client["id"]]['closed'] = False
		server.send_message(client,json.dumps({'action':'connection','success':True}))
	except:
		clients[client["id"]]['closed'] = True
		server.send_message(client,json.dumps({'action':'connection','success':False}))
		#bye_client(client,server)
		return
	
	clients[client["id"]]['channel'] = myClient.invoke_shell()
	chan = clients[client["id"]]['channel'] 
	while True:
		if clients[client["id"]]['close_me']:
			break
		if chan.recv_ready():
			server.send_message(client,json.dumps({'action':'message','message':unicode(chan.recv(1024))}))
		time.sleep(0.01)
	chan.close()
	myClient.close()
	clients[client["id"]]['closed'] = True

# When WebSocket client closes
def bye_client(client, server):
	print "Bye," , client
	clients[client['id']]["close_me"] = True
	while not clients[client['id']]["closed"]:
		time.sleep(0.01)
	client["handler"].connection.close()
	del clients[client['id']]
	print len(clients)

# When we recieve thing from WebSocket browser
def message_client(client,server,message):
	json_d = json.loads(message)
	try:
		if json_d["action"] == "connect":
			start_new_thread(start_new_shell,(client,server,json_d["host"],json_d["port"],json_d["username"],json_d["password"],))
		elif json_d["action"] == "key":
			chan = clients[client["id"]]['channel']
			chan.send(json_d["key"])
		elif json_d["action"] == "keySpecial":
			chan = clients[client["id"]]['channel']
			json_d["key"] = "\x1B" + json_d["key"]
			chan.send(json_d["key"])
		elif json_d["action"] == "keyCode":
			chan = clients[client["id"]]['channel']
			chan.send(chr(json_d["keyCode"]))
	except:
		bye_client(client, server)

# Listening to our desired port and setting up the connection
server = WebsocketServer(13254, host='0.0.0.0')
server.set_fn_new_client(new_client)
server.set_fn_client_left(bye_client)
server.set_fn_message_received(message_client)
server.run_forever()
