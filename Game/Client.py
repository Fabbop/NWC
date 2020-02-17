import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024
diff = "4"

def print_board(board, diff):
	i = 0
	for y in range(int(diff)):
		row = ""
		for x in range(int(diff)):
			row += board[i] + " "
			i += 1
		
		print(row)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
	TCPClientSocket.connect((HOST, PORT))
	print("Choose difficulty: ")
	print("1) 4 x 4: ")
	print("2) 6 x 6: ")
	diff = input()
	TCPClientSocket.sendall(diff.encode("ascii"))
	while(True):
		point1 = input("point 1: ")
		TCPClientSocket.sendall(point1.encode("ascii"))
		point2 = input("point 2: ")
		TCPClientSocket.sendall(point2.encode("ascii"))

		data = TCPClientSocket.recv(buffer_size)
		board = data.decode("ascii")
		# print(board)
		if(diff == "1"):
			print_board(board, 4)
		elif(diff == "2"):
			print_board(board, 6)
		
		while(True):
			data = TCPClientSocket.recv(buffer_size)
			if not data:
				break
			else:
				msg = data.decode("ascii")
				print(msg)
		
		# print("all data received")
			# data = TCPClientSocket.recv(buffer_size)
			# score = data.decode("ascii")
			# print(score)
		
		# print("CPU is making a move...")

		# data = TCPClientSocket.recv(buffer_size)
		# msg = data.decode("ascii")
		# print("CPU made a " + msg)
		# data = TCPClientSocket.recv(buffer_size)
		# score = data.decode("ascii")
		# print(score)

		# print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())
		# print("Enviando mensaje...")
		# TCPClientSocket.sendall(b"Hello TCP server")