import usocket as socket
import gc, esp, os
from Util import dPrint


extension2ContentType = {
	"htm" : "text/html",
	"html" : "text/html",
	"css" : "text/css",
	"js" : "text/javascript",
	"ico" : "image/x-icon",
}

class HttpServer():
	def __init__(self, read_timeout):
		# Create a socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# self.s.setblocking(False)
		self.resp = None
		# Bind socket to all of the hosts network addresses
		self.s.bind(('0.0.0.0', 80))

		self.s.listen(1)	# just queue up some requests
		self.timeout = read_timeout

	def acceptConn(self):
		gc.collect()
		try:
			conn, addr = self.s.accept()
		except OSError:
			return
		dPrint (" -------start------- ")
		dPrint("Got a connection from %s" % str(addr))
		resp = self.handleRequest(conn)
		if resp is not None:
			self.resp = resp

		conn.sendall('\n')
		conn.close()
		dPrint("Connection with %s closed" % str(addr))
		dPrint("esp free mem: %s"%str(esp.freemem()))
		dPrint("gc free mem: %s"%str(gc.mem_free()))
		dPrint (" --------end------- ")


	def handleRequest(self,conn):
		# conn.settimeout(self.timeout*100)
		try:
			request = (conn.recv(1024)).decode("utf-8")
			dPrint("full req: '%s'"%str(request))
		except OSError:
			dPrint ("Read Timeout")
			return None

		if len(request) <= 0:
			conn.sendall("HTTP/1.1 400 Bad Request")
			return None
		request_line, headers_alone = request.split('\r\n', 1)
		dPrint("Got Request:\n%s"%str(request_line))

		method, RequestURI, protocolVersion = request_line.split(' ',2)

		dPrint("Method: '%s'"%method)
		dPrint("RequestURI: '%s'"%RequestURI)
		dPrint("protocolVer: '%s'"%protocolVersion)


		if method == "GET":
			# Special case for root, then we should serve index
			if RequestURI == "/":
				conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nServer: Pyro\r\nContent-Type: text/html\r\n\r\n")
				with open("www/index.html","r") as file:

					conn.sendall(file.read())
					return None
			elif "/DATA/" in RequestURI:
				conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nServer: Pyro\r\n\r\n\r\n")
				return RequestURI[6:]

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
					return None

				# file = None
				try:
					os.stat("www" + RequestURI)
					# file = open("www" + RequestURI,"r")
				except OSError:
					conn.sendall("HTTP/1.1 404 Not Found")
					return None
				
				conn.sendall("HTTP/1.1 200 OK\r\nConnection: close\nCache-Control: no-cache, no-store, must-revalidate\nServer: Pyro\r\nContent-Type: %s\r\n\r\n"%contentType)
				with open("www" + RequestURI,"r") as file:
					conn.sendall(file.read())

				return None
		elif method == "POST":
			pass
			
		conn.sendall("HTTP/1.1 404 Not Found")
		return None

	def getResponse(self):
		return self.resp

