import sys, struct, tftp, socket, logging, errno
from os import path

logging.basicConfig(level=logging.DEBUG, filename="tftp.log", format='%(asctime)s %(message)s',)

class client():
	
	server_addr = ("127.0.0.1", 69)
    
	def __init__(self, host="127.0.0.1", port=69):
		self.server_addr = (host, port)

	def print_logging(self, msg):
		logging.debug(msg)
	
	def put(self, filename):
		try:
			if(tftp.file_exist(filename)):
				with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_socket:
					wrq_packet = tftp.set_request_packet(tftp.WRQ, filename)
					self.print_logging("Setting request packet")
					udp_socket.sendto(wrq_packet, self.server_addr)
					self.print_logging("Writing request sent")
					ack_packet, addr = udp_socket.recvfrom(516)
					if(tftp.get_opcode(ack_packet) == tftp.ACK and tftp.get_blocknum(ack_packet) == 0):
						self.print_logging("Transfer accepted")
						print("Transfer accepted")
						with open(filename, "rb") as fd:
							block_num = 1
							while(True):
								data = fd.read(512)
								packet = tftp.set_data_packet(block_num, data)
								udp_socket.sendto(packet, self.server_addr)
								# self.print_logging("Block %d sent" % block_num)
								ack_packet, addr = udp_socket.recvfrom(516)
								# if(tftp.get_opcode(ack_packet) == block_num):
								# self.print_logging("Received ACK for %d" % block_num)
								block_num += 1
								if(not data):
									print("Transfer completed")
									self.print_logging("Transfer completed")
									break
						# packet = tftp.set_data_packet(block_num, data)
					
					elif(tftp.get_opcode(ack_packet) == tftp.ERROR):
						self.print_logging("An error has ocurred")
						error_msg = tftp.get_error_msg(ack_packet).decode("ascii")
						self.print_logging(error_msg)
						print("An error has ocurred: " + error_msg)
			else:
				self.print_logging("An error has ocurred, File not found")
				print("An error has ocurred, File not found")
				return
					
		except OSError as e:
			if(e.errno == errno.ENOENT):
				# file not found
				packet = tftp.set_error_packet(1, "File not found")
				# udp_client.sendto(packet, client_addr)
				return 
			elif(e.errno == errno.EPERM or errno.EACCES):
				# acces violation
				packet = tftp.set_error_packet(2, "Access violation")
				# udp_client.sendto(packet, client_addr)
				return
			elif(errno == errno.EFBIG or errno.ENOSPC):
				# disk full
				packet = tftp.set_error_packet(3, "Disk full")
				# udp_client.sendto(packet, client_addr)
				return
			else:
				# unknown
				packet = tftp.set_error_packet(0, "Unknown")
				# udp_client.sendto(packet, client_addr)
				return
		except Exception as e:
			self.print_logging(e)
			return

	def get(self, filename):
		try:
			if(tftp.file_exist(filename)):
				self.print_logging("An error has ocurred")
				print("An error has ocurred")
				self.print_logging("File already exists")
				print("File already exists")
				return
			else:
				with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_socket:
					rrq_packet = tftp.set_request_packet(tftp.RRQ, filename)
					self.print_logging("Setting request packet")
					udp_socket.sendto(rrq_packet, self.server_addr)
					self.print_logging("Reading request sent")
					ack_packet, addr = udp_socket.recvfrom(516)
					if(tftp.get_opcode(ack_packet) == tftp.ACK and tftp.get_blocknum(ack_packet) == 0):
						self.print_logging("Transfer accepted")
						print("Transfer accepted")
						self.print_logging("Ready to receive file {}".format(filename))
						print("Ready to receive file {}".format(filename))
						ack_packet = tftp.set_ack_packet(0)
						udp_socket.sendto(ack_packet, self.server_addr)
						with open(filename, "wb") as fd:
							while(True):
								packet, addr = udp_socket.recvfrom(516)
								data = packet[4:] 
								if(not data):
									ack_no = tftp.get_blocknum(packet)
									ack_packet = tftp.set_ack_packet(ack_no)
									udp_socket.sendto(ack_packet, self.server_addr)
									break
								else:
									fd.write(data)
									ack_no = tftp.get_blocknum(packet)
									ack_packet = tftp.set_ack_packet(ack_no)
									udp_socket.sendto(ack_packet, self.server_addr)
						
						self.print_logging("Transfer completed")
						print("Trasnfer completed")
					
					elif(tftp.get_opcode(ack_packet) == tftp.ERROR):
						self.print_logging("An error has ocurred")
						error_msg = tftp.get_error_msg(ack_packet).decode("ascii")
						self.print_logging(error_msg)
						print("An error has ocurred: " + error_msg)

		except OSError as e:
			if(e.errno == errno.ENOENT):
				# file not found
				packet = tftp.set_error_packet(1, "File not found")
				# udp_client.sendto(packet, client_addr)
				return 
			elif(e.errno == errno.EPERM or errno.EACCES):
				# acces violation
				packet = tftp.set_error_packet(2, "Access violation")
				# udp_client.sendto(packet, client_addr)
				return
			elif(errno == errno.EFBIG or errno.ENOSPC):
				# disk full
				packet = tftp.set_error_packet(3, "Disk full")
				# udp_client.sendto(packet, client_addr)
				return
			else:
				# unknown
				packet = tftp.set_error_packet(0, "Unknown")
				# udp_client.sendto(packet, client_addr)
				return
		except Exception as e:
			self.print_logging(e)
			return


tftp_client = client("192.168.1.78", 65432)

print("TFTP client.")
while True:
	line = input("tftp> ")
	command = line.split(" ")
	if(command[0] == "connect"):
		tftp_client.server_addr = (command[1], int(command[2]))
	elif(command[0] == "get"):
		tftp_client.get(command[1])
	elif(command[0] == "put"):
		tftp_client.put(command[1])
	elif(command[0] == "quit"):
		break