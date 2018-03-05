import socket

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.1.4'
port = 3000

serversocket.bind((host, port))

serversocket.listen(5)

while True:
	clientsocket,addr = serversocket.accept()

	print("Connesso a %s" % str(addr))

	data_rev = clientsocket.recv(24)

	print("Dati ricevuti ---> %s" % str(data_rev.decode()))
	if(data_rev[:4].decode() == "LOGI"):
		msg = 'ALGIqwert12345yuiop5'
		clientsocket.send(msg.encode('ascii'))
		clientsocket.close()
	elif(data_rev[:4].decode() == "LOGO"):
		msg = 'ALGO003'
		clientsocket.send(msg.encode('ascii'))
		clientsocket.close()
	else:
		msg="ADD.001"
		clientsocket.send(msg.encode('ascii'))
		clientsocket.close()