import socket, time, random, threading
import numpy as np

class server:

	# host = "127.0.0.1"
	# port = 65432
	server_addr = ("127.0.0.1", 65432)
	buffer_size = 1024
	clients = []
	threads = []

	def __init__(self, host, port):
		self.server_addr = (host, port)
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
				thread_read = threading.Thread(target=self.recibir_datos, args=[client_conn, client_addr])
				self.threads.append(thread_read)
				thread_read.start()
				self.gestion_conexiones()
		except Exception as e:
			print(e)

	def gestion_conexiones(self):
		for connection in self.clients:
			if(connection.fileno() == -1):
				self.clients.remove(connection)

		print("hilos activos: ", threading.active_count())
		print("enum: ", threading.enumerate())
		print("conexiones: ", len(self.clients))
		print(self.clients)


	def recibir_datos(self, conn, addr):
		try:
			cur_thread = threading.current_thread()
			print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
			while True:
				data = conn.recv(1024)
				response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
				if not data:
					print("Fin")
					break
			conn.sendall(response)
		except Exception as e:
			print(e)
		finally:
			conn.close()