import socket, logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s',)

class client:

	server_addr = ("127.0.0.1", 65432)
	buff_size = 512

	def __init__(self, host="127.0.0.1", port=65432):
		self.server_addr = (host, port)
		print("Connect to server")
		host = input("Server address: ")
		port = input("Server port: ")
		

	


client = client()