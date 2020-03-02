import socket, time, random
import numpy as np

class memory:

	difficulty = 4
	board = np.zeros(16, dtype=np.uint8)
	score = np.zeros(16, dtype=np.uint8)
	pairs = 8
	players = []

	def __init__(self, difficulty=4):
		self.difficulty = difficulty
		self.board = np.zeros((difficulty ** 2), dtype=np.uint8)
		self.pairs = int((self.difficulty ** 2) / 2)
		self.scramble()

	def add_player(self, client):
		self.players.append(client)
		player_id = self.players.index(client)
		
		return player_id

	def get_player(self, client):
		index = self.players.index(client) + 1

		return index

	def set_board(self, diff):
		if(diff == "1"):
			self.difficulty = 4
			self.board = np.zeros(16, dtype=np.uint8)
			self.score = np.zeros(16, dtype=np.uint8)
			self.pairs = 8
		elif(diff == 2):
			self.difficulty = 6
			self.board = np.zeros(36, dtype=np.uint8)
			self.score = np.zeros(36, dtype=np.uint8)
			self.pairs = 18

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
		move = self.str_board_move((y1, x1), (y2, x2))
		
		return msg, move

	def verify_move(self, point1, point2, player):
		x1 = self.get_position(point1)
		x2 = self.get_position(point2)
		if(x1 < 0 or x2 < 0 or x1 == x2):
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
		
		return msg

	def set_score(self, x, player):
		i = self.get_player(player)
		# i = self.players.index(player)
		self.score[x] = i

	def count_scores(self):
		score = ""
		for i in (self.players):
			points = int(np.count_nonzero(self.score == self.get_player(i)) / 2)
			score += "p" + str(self.get_player(i)) + ": " + str(points) + " "
		# player1 = int(np.count_nonzero(self.score == 1) / 2)
		# player2 = int(np.count_nonzero(self.score == 2) / 2)
		
		return score
	
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