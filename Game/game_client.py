import socket, threading

class client:
	
	server_addr = ("127.0.0.1", 65432)
	buffer_size = 1024
	threads = []
	winner = False
	board = ""
	score = ""
	last = ""

	def __init__(self, host="127.0.0.1", port=65432):
		self.server_addr = (host, port)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
			tcp_socket.connect(self.server_addr)

			thr = threading.Thread(target=self.receive_data, args=(tcp_socket,))
			self.threads.append(thr)
			thr.start()

			thr = threading.Thread(target=self.play, args=(tcp_socket,))
			self.threads.append(thr)
			thr.start()
			# self.play(tcp_socket)

	def receive_data(self, tcp_socket):
		try:
			print("receiving data...")
			while True:
				data = tcp_socket.recv(self.buffer_size)
				msg = data.decode("ascii").split("=")
				print(msg)
				if(msg[1] == "Game finished"):
					self.winner = True
					break
				elif(msg[0] == "score"):
					self.score = msg[1]
				elif(msg[0] == "board"):
					self.board == msg[1]
				elif(msg[0] == "last"):
					self.last == msg[1]
		except Exception as e:
			print("Error while receiving")
			print(e)

	def play(self, tcp_socket):
		try:
			print("playing...")
			while(not self.winner):
				print("1) make move")
				print("2) view board")
				print("3) view score")
				print("4) view last")
				opt = int(input())
				if(opt == 1):
					points = input("point 1: ")
					points += ":" + input("point 2: ")
					print("sending...")
					tcp_socket.sendall(points.encode("ascii"))
					print("points sended")
				elif(opt == 2):
					self.print_msg(self.board)
				elif(opt == 3):
					self.print_msg(self.score)
				elif(opt == 4):
					self.print_msg(self.last)

				# data = tcp_socket.recv(self.buffer_size)
				# self.print_msg(data.decode("ascii"))
		except Exception as e:
			print("Game error")
			print(e)
	
	def print_msg(self, data):
		msg = data.split(",")
		for i in msg:
			print(i)

game_client = client()