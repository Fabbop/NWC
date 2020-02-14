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



# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
# buffer_size = 1024

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
#     TCPServerSocket.bind((HOST, PORT))
#     TCPServerSocket.listen()
#     print("El servidor TCP está disponible y en espera de solicitudes")

#     Client_conn, Client_addr = TCPServerSocket.accept()
#     with Client_conn:
#         print("Conectado a", Client_addr)
#         while True:
#             print("Esperando a recibir datos... ")
#             data = Client_conn.recv(buffer_size)
#             print ("Recibido,", data,"   de ", Client_addr)
#             if not data:
#                 break
#             print("Enviando respuesta a", Client_addr)
#             Client_conn.sendall(data)

board = memory(4)
print(board.board)