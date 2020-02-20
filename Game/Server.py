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
		# while(msg == "Invalid move"):
		# 	msg = self.verify_move((y1, x1), (y2, x2), 1)
		
		move = self.str_board_move((y1, x1), (y2, x2))
		
		return msg, move

	def verify_move(self, point1, point2, player):
		x1 = self.get_position(point1)
		x2 = self.get_position(point2)
		if(x1 < 0 or x2 < 0):
			print("Invalid move")
			msg = "Invalid move"
		else:
			if(self.board[x1] == self.board[x2]):
				print("Point")
				msg = "Point"
				self.set_score(x1, player)
				self.set_score(x2, player)
			else:
				print("Try again!")
				msg = "Try again!"
		
			# self.print_board_move(point1, point2)
		
		return msg

	def set_score(self, x, player):
		self.score[x] = player

	def count_scores(self):
		player1 = int(np.count_nonzero(self.score == 1) / 2)
		player2 = int(np.count_nonzero(self.score == 2) / 2)
		# print("P1: " + str(player1) + " P2: " + str(player2))
		return "CPU: " + str(player1) + " Player: " + str(player2)
	
	def str_board_move(self, point1, point2):
		strboardmove = ""
		i = 0
		for y in range(self.difficulty):
			row = ""
			for x in range(self.difficulty):
				if(i == self.get_position(point1) or i == self.get_position(point2) or self.score[i] != 0):
					row += str(self.board[i]) + " "
				else:
					row += "x "
				i += 1
			
			strboardmove += row
			strboardmove += ","

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

	sock_fd, client_addr = TCPServerSocket.accept()
	with sock_fd:
		print("Client: ", client_addr)
		while True:
			print("Waiting for player to choose difficulty...")
			data = sock_fd.recv(buffer_size)
			dif = data.decode("ascii")
			if(dif == "1"):
				game = memory(4)
				game.print_board()
				while(np.count_nonzero(game.score) < len(game.score)):
					print("Waiting players move...")
					
					data = sock_fd.recv(buffer_size)
					points = data.decode("ascii").split(":")

					point1 = points[0].split(",")
					point2 = points[1].split(",")

					msg = game.verify_move(point1, point2, 2)
					if(msg == "Invalid move"):
						msg += ", "
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					else:
						board = game.str_board_move(point1, point2)
						msg += "," + board
						score = game.count_scores()
						msg += score
						data = msg.encode("ascii")
						sock_fd.sendall(data)

					msg, move = game.random_move()
					if(msg == "Invalid move"):
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					else:
						msg += "," + move
						score = game.count_scores()
						msg += score
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					
					sock_fd.sendall(b"Waiting players move")

				sock_fd.sendall(b"Game ended")
			elif(dif == "2"):
				game = memory(6)
				game.print_board()
				while(np.count_nonzero(game.score) < len(game.score)):
					print("Waiting players move...")
					
					data = sock_fd.recv(buffer_size)
					points = data.decode("ascii").split(":")

					point1 = points[0].split(",")
					point2 = points[1].split(",")

					msg = game.verify_move(point1, point2, 2)
					if(msg == "Invalid move"):
						msg += ", "
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					else:
						board = game.str_board_move(point1, point2)
						msg += "," + board
						score = game.count_scores()
						msg += score
						data = msg.encode("ascii")
						sock_fd.sendall(data)

					msg, move = game.random_move()
					if(msg == "Invalid move"):
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					else:
						msg += "," + move
						score = game.count_scores()
						msg += score
						data = msg.encode("ascii")
						sock_fd.sendall(data)
					
					sock_fd.sendall(b"Waiting players move")

				sock_fd.sendall(b"Game ended")
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