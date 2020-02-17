import socket, time, random
import numpy as np

class memory:

	difficulty = 4
	board = np.zeros(16, dtype=np.uint8)
	score = np.zeros(16, dtype=np.uint8)
	pairs = 8
	img = []

	def __init__(self, difficulty=4):
		self.difficulty = difficulty
		self.board = np.zeros((difficulty ** 2), dtype=np.uint8)
		self.pairs = int((self.difficulty ** 2) / 2)
		self.scramble()

	def scramble(self):
		for i in range(0, self.pairs):
			self.board[i] = i + 1
			self.board[i + self.pairs] = i + 1
		for i in range(0, self.pairs):
			x = random.randint(self.pairs, (len(self.board) - 1))
			n = self.board[x]
			self.board[x] = self.board[i]
			self.board[i] = n

	def get_position(self, point):
		x = 0
		if((int(point[0]) - 1) == 0):
			x = 0
		elif((int(point[0]) - 1) == 1):
			x = 4
		elif((int(point[0]) - 1) == 2):
			x = 8
		elif((int(point[0]) - 1) == 3):
			x = 12
		
		x += (int(point[1]) - 1)

		if(self.score[x] != 0):
			return -1 
		else:
			return x

	def random_move(self):
		y1 = random.randint(1, self.difficulty)
		x1 = random.randint(1, self.difficulty)
		y2 = random.randint(1, self.difficulty)
		x2 = random.randint(1, self.difficulty)
		msg = self.verify_move((y1, x1), (y2, x2), 1)
		return msg

	def verify_move(self, point1, point2, player):
		x1 = self.get_position(point1)
		x2 = self.get_position(point2)
		if(x1 < 0 or x2 < 0):
			print("Invalid move \n")
		else:
			if(self.board[x1] == self.board[x2]):
				print("Point")
				msg = "Point \n"
				self.set_score(x1, player)
				self.set_score(x2, player)
			else:
				print("Incorrect move")
				msg = "Incorrect move \n"
		
			self.print_board_move(point1, point2)
		
		return msg

	def set_score(self, x, player):
		self.score[x] = player

	def count_scores(self):
		player1 = int(np.count_nonzero(self.score == 1) / 2)
		player2 = int(np.count_nonzero(self.score == 2) / 2)
		# print("P1: " + str(player1) + " P2: " + str(player2))
		return "P1: " + str(player1) + " P2: " + str(player2) + " \n"
	
	def str_board_move(self):
		strboardmove = ""
		i = 0
		for y in range(self.difficulty):
			row = ""
			for x in range(self.difficulty):
				if(i == self.get_position(point1) or i == self.get_position(point2) or self.score[i] != 0):
					row += str(self.board[i])
				else:
					row += "x"
				i += 1
			
			strboardmove += row

		return strboardmove

	def print_board(self):
		i = 0
		for y in range(self.difficulty):
			row = ""
			for x in range(self.difficulty):
				if(self.score[i] != 0):
					row += str(self.board[i]) + " "
				else:
					row += "x "
				i += 1
			
			print(row)

	def print_board_move(self, point1, point2):
		i = 0
		for y in range(self.difficulty):
			row = ""
			for x in range(self.difficulty):
				if(i == self.get_position(point1) or i == self.get_position(point2) or self.score[i] != 0):
					row += str(self.board[i]) + " "
				else:
					row += "x "
				i += 1
			
			print(row)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
	TCPServerSocket.bind((HOST, PORT))
	TCPServerSocket.listen()
	print("Listening...")

	Client_conn, Client_addr = TCPServerSocket.accept()
	with Client_conn:
		print("Client: ", Client_addr)
		while True:
			data = Client_conn.recv(buffer_size)
			dif = data.decode("ascii")
			if(dif == "1"):
				game = memory(4)
				game.print_board()
				while(np.count_nonzero(game.score) < len(game.score)):
					print("Waiting player's move")
					data = Client_conn.recv(buffer_size)
					p = data.decode("ascii")
					point1 = p.split(",")
					data = Client_conn.recv(buffer_size)
					p = data.decode("ascii")
					point2 = p.split(",")
					print(point1)
					print(point2)
					msg = game.verify_move(point1, point2, 2)
					board = game.str_board_move().encode("ascii")
					print(Client_conn.sendall(board))
					data = msg.encode("ascii")
					print(Client_conn.sendall(data))
					score = game.count_scores()
					print(Client_conn.sendall(score.encode("ascii")))
					# msg = game.random_move()
					# data = game.str_board_move().encode("ascii")
					# Client_conn.sendall(data)
					# data = msg.encode("ascii")
					# Client_conn.sendall(data)
					# data = game.count_scores()
					# Client_conn.sendall(data.encode("ascii"))
			elif(dif == "2"):
				game = memory(6)
				game.print_board()
			else:
				print("Invalid option")


# board = memory(4)
# board.print_board()
# while(np.count_nonzero(board.score) < len(board.score)):
# 	# board.print_board()
# 	p = input()
# 	point1 = p.split(",")
# 	p = input()
# 	point2 = p.split(",")
# 	# y1 = int(input())
# 	# x1 = int(input())
# 	# y2 = int(input())
# 	# x2 = int(input())
# 	# board.verify_move((y1, x1), (y2, x2), 2)
# 	board.verify_move(point1, point2, 2)
# 	board.count_scores()