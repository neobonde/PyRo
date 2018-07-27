from SpeedMotor import SpeedMotor

def Start():
	m = SpeedMotor(2,0)
	m.SetSpeed(0)
	# minimal Ajax in Control Webserver
	import socket	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0', 80))
	s.listen(0)	# just queue up some requests
	Val = 0
	while True:
		m.SetSpeed(int(Val))
		conn, addr = s.accept()
		print("Got a connection from %s" % str(addr))
		request = conn.recv(1024)
		conn.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: Pyro serv\nContent-Type: text/html\n\n')
		request = str(request)
		ib = request.find('Val=')
		if ib > 0 :
			ie = request.find(' ', ib)
			Val = request[ib+4:ie]
			print("Val =", Val)
			conn.send(Val)
			
		else:
			with open('index.htm', 'r') as html:
				conn.send(html.read())
		conn.sendall('\n')
		conn.close()
		print("Connection wth %s closed" % str(addr))