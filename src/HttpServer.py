import usocket as socket
from SpeedMotor import SpeedMotor

motor1 = SpeedMotor(2,0)

def Start():
	
	# Create a socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Bind socket to all of the hosts network addresses
	s.bind(('0.0.0.0', 80))


	s.listen(1)	# just queue up some requests
	while True:
		conn, addr = s.accept()
		print("Got a connection from %s" % str(addr))
		handleRequest(conn)
		# request = str(request)
		# ib = request.find('Val=')
		# if ib > 0 :
		# 	ie = request.find(' ', ib)
		# 	Val = request[ib+4:ie]
		# 	print("Val =", Val)
		# 	conn.send(Val)
			
		# else:
		# 	with open('www/index.htm', 'r') as html:
		# 		conn.send(html.read())
		conn.sendall('\n')
		conn.close()
		print("Connection wth %s closed" % str(addr))


extension2ContentType = {
	"htm" : "text/html",
	"html" : "text/html",
	"css" : "text/css",
	"js" : "text/javascript",
	"ico" : "image/x-icon",
}

def handleRequest(conn):
	request = (conn.recv(1024)).decode("utf-8")
	request_line, headers_alone = request.split('\r\n', 1)
	print("Got Request:\n%s"%str(request_line))

	method, RequestURI, protocolVersion = request_line.split(' ',2)

	print("Method: '%s'"%method)
	print("RequestURI: '%s'"%RequestURI)
	print("protocolVer: '%s'"%protocolVersion)


	if method == "GET":
		# Special case for root, then we should serve index
		if RequestURI == "/":
			conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nServer: Pyro\r\nContent-Type: text/html\r\n\r\n")
			with open("www/index.htm","r") as file:

				conn.sendall(file.read())
				return
		elif "/DATA/" in RequestURI:
			try:
				key, value = RequestURI[6:].split(":")
				print("key: %s"%key)
				print("value: %s"%value)
			except ValueError:
				print("ValueError exception")
				conn.sendall("HTTP/1.1 501 Not Implemented")
				return
				
			if key == "joystick":
				index_xval = value.find("xval=")
				index_sep = value.find("&")
				index_yval = value.find("yval=")
				index_end = len(value) + 1 

				xVal = value[index_xval+5:index_sep]
				motor1Speed = int(xVal) if xVal is not "" else 0
				motor1.SetSpeed(motor1Speed)
				yVal = value[index_yval+5:index_end]
				print(yVal)

				conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nServer: Pyro\r\n\r\n\r\n")
				conn.send(value)
				return
		else:
			contentType = "text/html" # if there is no ending default to html
			temp = ""
			extension = ""
			try:
				temp, extension = RequestURI.split(".")
			except ValueError:
				extension = "html"

			try:
				contentType = extension2ContentType[extension]
			except KeyError:
				conn.sendall("HTTP/1.1 501 Not Implemented")
				return

			file = None
			try:
				file = open("www" + RequestURI,"r")
			except OSError:
				conn.sendall("HTTP/1.1 404 Not Found")
				return
				
			conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nCache-Control: no-cache, no-store, must-revalidate\nServer: Pyro\r\nContent-Type: %s\r\n\r\n"%contentType)
			conn.sendall(file.read())
			return 
	elif method == "POST":
		pass
		

	conn.sendall("HTTP/1.1 404 Not Found")



