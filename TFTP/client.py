import socket, logging, errno

logging.basicConfig(level=logging.DEBUG, filename="tftp.log", format='%(asctime)s %(message)s',)

class client:

	server_addr = ("127.0.0.1", 65432)

	def __init__(self):
		self.connect_to()

	def connect_to(self):
		print("Connect to server")
		host = input("Server address: ")
		port = input("Server port: ")	
		self.server_addr = (host, port)


client = client()