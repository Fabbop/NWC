import socket, time, random, threading, copy
import numpy as np
from game import memory

class server:

	server_addr = ("127.0.0.1", 65432)
	buffer_size = 1024
	clients = []
	threads = []
	game = memory()

	def __init__(self, host="127.0.0.1", port=65432):
		self.server_addr = (host, port)
		print("Choose difficulty: ")
		print("1) 4 x 4: ")
		print("2) 6 x 6: ")
		diff = int(input())
		self.game.set_board(diff)
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
			tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			tcp_socket.bind(self.server_addr)
			tcp_socket.listen(5)
			print("Listening...")
			self.client_connection(tcp_socket)
		
	def client_connection(self, tcp_socket):
		try:
			while True:
				client_conn, client_addr = tcp_socket.accept()
				print("Connection established with: ", client_addr)
				self.clients.append(client_conn)
				self.game.add_player(client_addr[1])
				print(self.game.players)

				thread_read = threading.Thread(target=self.play, args=(client_conn, client_addr))
				self.threads.append(thread_read)
				thread_read.start()
				self.connection_management()
		except Exception as e:
			print(e)

	def connection_management(self):
		for connection in self.clients:
			if(connection.fileno() == -1):
				self.clients.remove(connection)

		# print("Active threads: ", threading.active_count())
		# print("Enum: ", threading.enumerate())
		# print("Connections: ", len(self.clients))
		# print(self.clients)

	def receive_data(self, conn):
		while True:
			data = conn.recv(self.buffer_size)
			if(data):
				points = data.decode("ascii")
				point1, point2 = get_points(points)
				return point1, point2


	def play(self, conn, addr):
		try:
			cur_thread = threading.current_thread()
			print("{} playing from {}".format(addr, cur_thread.name))
			while(np.count_nonzero(self.game.score) < len(self.game.score)):
				conn.sendall(b"msg=Waiting player move")
				print("Waiting players move...")

				point1, point2 = self.receive_data(conn)
				
				# data = conn.recv(self.buffer_size)
				# points = data.decode("ascii")
				# point1, point2 = get_points(points)
				
				last, score, board = make_move(self.game, point1, point2, addr[1])
				for i in self.clients:
					i.sendall(last)
					i.sendall(score)
					i.sendall(board)
			
			for i in self.clients:
				i.sendall(b"msg=Game finished")
		except Exception as e:
			print(e)
		finally:
			conn.close()

def get_points(p):
	points = p.split(":")
	point1 = points[0].split(",")
	point2 = points[1].split(",")

	return point1, point2

def make_move(game, point1, point2, player):
	msg = game.verify_move(point1, point2, player)

	if(msg == "Invalid move"):
		board = game.str_board()
		msg += ", " + board
		last = msg.encode("ascii")
	else:
		board = game.str_board_move(point1, point2)
		msg += "," + board
		last = msg.encode("ascii")
		
	msg = game.count_scores()
	score = msg.encode("ascii")

	msg = game.str_board()
	board = msg.encode("ascii")
	
	return last, score, board

def make_random_move(game):
	msg, move = game.random_move()
	if(msg == "Invalid move"):
		data = msg.encode("ascii")
	else:
		msg += "," + move
		score = game.count_scores()
		msg += score
		data = msg.encode("ascii")

	return data

serv = server()
