import socket, time, random, threading, copy, queue
import numpy as np
from game import memory

class threadpool():

	active = []
	lock = threading.Lock()

	def __init__(self):
        super(threadpool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

	def activate(self, name):
		with self.lock:
			self.active.append(name)
			# logging.debug('Ejecutando: %s', self.active)

	def deactivate(self, name):
		with self.lock:
			self.active.remove(name)
			# logging.debug('Ejecutando: %s', self.active)

class server:

	server_addr = ("127.0.0.1", 65432)
	buffer_size = 1024
	clients = []
	threads = []
	game = memory()
	player_slots = 2
	barrier = threading.Barrier(2)
	q = queue.Queue(maxsize=2)
	pool = threadpool()
	sem = threading.Semaphore(2)

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
			tcp_socket.listen(10)
			print("Waiting for " + str(self.player_slots))

			self.client_connection(tcp_socket)
		
	def client_connection(self, tcp_socket):
		try:
			while True:
				client_conn, client_addr = tcp_socket.accept()
				print("Connection established with: ", client_addr)
				self.clients.append(client_conn)
				self.game.add_player(client_addr[1])
				print(self.game.players)
				thread_read = threading.Thread(target=self.playing, args=[client_conn, client_addr])
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

	def playing(self, conn, addr):
		try:
			self.player_slots -= 1
			print("Waiting for " + str(self.player_slots))
			self.barrier.wait()
			cur_thread = threading.current_thread()
			print("{} playing from {}".format(addr, cur_thread.name))
			while(np.count_nonzero(self.game.score) < len(self.game.score)):
				conn.sendall(b"Waiting player move")
				print("Waiting players move...")
				
				data = conn.recv(self.buffer_size)
				points = data.decode("ascii")
				point1, point2 = get_points(points)
				
				data = make_move(self.game, point1, point2, addr[1])
				conn.sendall(data)
			
			conn.sendall(b"Game ended")
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
		msg += ", "
		data = msg.encode("ascii")
	else:
		board = game.str_board_move(point1, point2)
		msg += "," + board
		score = game.count_scores()
		msg += score
		data = msg.encode("ascii")
		
	return data

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
