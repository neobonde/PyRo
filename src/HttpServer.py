import ure as re
import picoweb
from parser import parseJoystick

class HttpServer():
	def __init__(self, ip, port=80, debug = False):
		self.ip = ip
		self.port = port
		self.debug = debug
		
		self.joystickX = 0
		self.joystickY = 0

		self.app = picoweb.WebApp("PyRo Webserver")

		@self.app.route("/")
		def index(req, resp):
			print(req)
			yield from picoweb.start_response(resp, content_type = "text/html")  
			openFile = open('www/index.html', 'r')
		
			for line in openFile:
				yield from resp.awrite(line)

		@self.app.route("/favicon.ico")
		def favico(req, resp):
			yield from picoweb.start_response(resp, content_type = "image/x-icon") 

			openFile = open("www/favicon.ico") 
			
			for line in openFile:
				yield from resp.awrite(line)


		@self.app.route(re.compile('^\/(.+\.html)$'))
		def hyperText(req, resp):
			file_path = req.url_match.group(1)
			print(file_path)

			yield from picoweb.start_response(resp, content_type = "text/html")  
			openFile = open('www/'+file_path, 'r')
		
			for line in openFile:
				yield from resp.awrite(line)


		@self.app.route(re.compile('^\/(.+\.css)$'))
		def styleSheet(req, resp):
			file_path = req.url_match.group(1)
			print(file_path)

			yield from picoweb.start_response(resp, content_type = "text/css")  
			openFile = open('www/'+file_path, 'r')
		
			for line in openFile:
				yield from resp.awrite(line)

		@self.app.route(re.compile('^\/(.+\.min.js)$'))
		def minJavascript(req, resp):
			file_path = req.url_match.group(1)
			print(file_path)

			yield from picoweb.start_response(resp, content_type = "application/javascript")  
			openFile = open('www/'+ file_path, 'r')

			for line in openFile:
				yield from resp.awrite(line)


		@self.app.route(re.compile('^\/(DATA\/joystick:.+)$'))
		def joystick(req, resp):
			joystick = req.url_match.group(1).split('/')[1]

			self.joystickX, self.joystickY = parseJoystick(joystick)
			
			yield from picoweb.start_response(resp)



	def start(self):
		self.app.run(debug=self.debug, host=self.ip, port=self.port)

	def getJoystick(self):
		return self.joystickX, self.joystickY