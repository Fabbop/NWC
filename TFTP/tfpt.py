import socket, logging, errno

logging.basicConfig(level=logging.DEBUG, filename="tftp.log", format='%(asctime)s %(message)s',)

class tftp:

	timeout = 0.5
	block_size = 512
	buff_size = 65536
