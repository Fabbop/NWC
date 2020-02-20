import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024
diff = "4"

def print_msg(data):
	msg = data.split(",")
	for i in msg:
		print(i)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
	TCPClientSocket.connect((HOST, PORT))
	
	while(True):
		print("Choose difficulty: ")
		print("1) 4 x 4: ")
		print("2) 6 x 6: ")
		diff = input()
		TCPClientSocket.sendall(diff.encode("ascii"))
		winner = False

		while(not winner):
			points = input("point 1: ")
			points += ":" + input("point 2: ")
			TCPClientSocket.sendall(points.encode("ascii"))

			data = TCPClientSocket.recv(buffer_size)
			print_msg(data.decode("ascii"))
			
			print("CPU is making a move...")

			data = TCPClientSocket.recv(buffer_size)
			print_msg(data.decode("ascii"))

			data = TCPClientSocket.recv(buffer_size)
			if(data.decode("ascii") != "Waiting players move"):
				winner = True