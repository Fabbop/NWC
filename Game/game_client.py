import socket

class client:
	
	server_addr = ("127.0.0.1", 65432)
	buffer_size = 1024

	def __init__(self, host="127.0.0.1", port=65432):
		self.server_addr = (host, port)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
			tcp_socket.connect(self.server_addr)

			self.playing(tcp_socket)

	def playing(self, tcp_socket):
		winner = False

		while(not winner):
			data = tcp_socket.recv(self.buffer_size)
			if(data.decode("ascii") == "Game ended"):
				winner = True
			points = input("point 1: ")
			points += ":" + input("point 2: ")
			tcp_socket.sendall(points.encode("ascii"))

			data = tcp_socket.recv(self.buffer_size)
			self.print_msg(data.decode("ascii"))	

			# data = tcp_socket.recv(self.buffer_size)
			# self.print_msg(data.decode("ascii"))
	
	def print_msg(self, data):
		msg = data.split(",")
		for i in msg:
			print(i)

game_client = client()