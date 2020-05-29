import sys, struct, tftp, socket, logging, errno, os.path
from os import path

logging.basicConfig(level=logging.DEBUG, filename="tftp.log", format='%(asctime)s %(message)s',)

class client():
	
	server_addr = ("127.0.0.1", 69)
    
	def __init__(self, host="127.0.0.1", port=69):
		self.server_addr = (host, port)

	# def reset(self):
	# 	self.block_num = 1
	# 	self.is_done = False
	# 	# self.status = self.START
	# 	self.port = 69
	# 	# self.setup_file()
	# 	self.setup_connect()

	# def max_packet_size(self):
	# 	return 516

	# def setup_connect(self):
	# 	self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# def send_packet(self, packet):
	# 	self.sock_fd.sendto(packet, self.server_addr)

	# def recv_packet(self):
	# 	(packet, addr) = self.sock_fd.recvfrom(self.max_packet_size)
	# 	return (packet, addr)

	def print_logging(self, msg):
		logging.debug(msg)
	
	def put(self, filename):
		try:
			with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_socket:
				self.print_logging("Ready to send %s" % filename)
				wrq_packet = tftp.set_request_packet(tftp.WRQ, filename)
				self.print_logging("Setting request packet...")
				udp_socket.sendto(wrq_packet, self.server_addr)
				self.print_logging("WRQ sent")
				ack_packet = udp_socket.recvfrom(516)
				if(tftp.get_opcode(ack_packet) == tftp.ACK and tftp.get_blocknum(ack_packet) == 0):
					self.print_logging("Received ACK for %d" % 0)
					with open(filename, "rb") as fd:
						block_num = 1
						while(True):
							data = fd.read(512)
							packet = tftp.set_data_packet(block_num, data)
							udp_socket.sendto(packet, self.server_addr)
							ack_packet = udp_socket.recvfrom(516) 
							# if(tftp.get_opcode(ack_packet) == block_num):
							self.print_logging("Received ACK for %d" % block_num)
							block_num += 1
							if(not data):
								break
					packet = tftp.set_data_packet(block_num, data)
		except Exception as e:
			self.print_logging(e)
		# except OSError as e:
		# 	if(e.errno == errno.ENONET):
		# 		# file not found
		# 	elif(e.errno == errno.EPERM or errno.EACCES):
		# 		# acces violation
		# 	elif(errno == errno.EFBIG or errno.ENOSPC):
		# 		# disk full
		# 	else:
		# 		# unknown
			

	def get(self, filename):
		try:
			pass
		except Exception as e:
			print(e)

	# def handle_packet(self, packet, addr):
	# 	host, port = addr
	# 	if(host != self.server_addr[1]):
	# 		return

	# 	packet_len = len(packet)
	# 	opcode = tftp.get_opcode(packet)

	# 	if(opcode == tftp.ERROR):
	# 		err_code = struct.unpack("!H", packet[2:4])[0]
	# 		err_msg = packet[4:packet_len-1]
	# 		print("Error %s: %s" % (err_code, err_msg))
	# 		sys.exit(err_code)

	# 	elif(opcode == tftp.DATA):
	# 		if(self.port != port):
	# 			self.port = port
	# 		block_num = struct.unpack("!H", packet[2:4])[0]
	# 		if(block_num != self.block_num):
	# 			print("Unexpected block num %d" % block_num)
	# 			return
	# 		data = packet[4:]
	# 		self.fd.write(data)
	# 		if(len(packet) < self.block_size + 2):
	# 			self.is_done = True
	# 			self.fd.close()
	# 			file_len = self.block_size * (self.block_num -1) + len(data)
	# 			print("%d bytes received." % file_len)
	# 		self.block_num += 1
		
	# 	elif(opcode == tftp.ACK):
	# 		if self.port != port:
	# 			self.port = port
	# 		block_num = struct.unpack("!H", packet[2:4])[0]
	# 		self.print_logging("Received ACK for %d" % block_num)
	# 		self.block_num += 1

	# 	else:
	# 		raise Exception("Unrecognized packet: %s", str(opcode))
        
	# def get_next_packet(self):
	# 	if(self.status == self.START):
	# 		opcode = tftp.RRQ if self.action == "get" else tftp.WRQ
	# 		self.print_logging("About to send packet %d" % opcode)
	# 		packet = tftp.set_request_packet(opcode, self.filename)
	# 		self.status = self.DATA
	# 	elif(self.status == self.DATA):
	# 		if(self.action == "get"):
	# 			self.print_logging("About to send ACK for %d" % (self.block_num - 1))
	# 			packet = tftp.set_ack_packet(self.block_num-1)
	# 		elif(self.action == "put"):
	# 			self.print_logging("About to send data for %d" % (self.block_num - 1))
	# 			data = self.fd.read(self.block_size)
	# 			if(len(data) < self.block_size):
	# 				self.is_done = True
	# 			packet = tftp.set_data_packet(self.block_num - 1, data)

	# 	return packet

	# def handle(self):
	# 	while(not self.is_done):
	# 		packet = self.get_next_packet()
	# 		if(packet):
	# 			self.send_packet(packet)
	# 		(packet, addr) = self.recv_packet()
	# 		self.handle_packet(packet, addr)


tftp_client = client()					

# def get(filename):
# 	tftp_client.filename = filename
# 	tftp_client.action = "get"
# 	tftp_client.reset()
# 	tftp_client.handle()



print("TFTP client.")
while True:
	line = input("tftp> ")
	command = line.split(" ")
	if(command[0] == "connect"):
		print(command)
		tftp_client.server_addr = (command[1], int(command[2]))
	elif(command[0] == "get"):
		print(command)
		# tftp_client.get(command[1])
	elif(command[0] == "put"):
		print(command)
		tftp_client.put(command[1])
	elif(command[0] == "quit"):
		break