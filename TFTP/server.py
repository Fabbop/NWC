import socket, threading, queue

class server:

	host = "127.0.0.1"
	port = 65432
	buff_size = 512
	clients = queue.Queue(maxsize=10)
