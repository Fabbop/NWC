import sys, struct, tftp, socket, logging, errno, os.path
from os import path

logging.basicConfig(level=logging.DEBUG, filename="tftp.log", format='%(asctime)s %(message)s',)

class server():

	addr = ("127.0.0.1", 69)

	def __init__(self, host="127.0.0.1", port=69):
		self.addr = (host, port)

		with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as udp_client:
			while True:
				print("Listening...")
				self.print_logging("Listening...")
				rq_packet, client_addr = udp_client.recvfrom(512)
				rq_code = tftp.get_opcode(rq_packet)
				if(rq_code == 1):
					# RRQ
					pass
				elif(rq_code == 2):
					# WRQ
					self.print_logging("Write request received from {}".format(client_addr))
					self.put(rq_packet, udp_client, client_addr)
				else:
					self.print_logging("Unknown request")

	def put(self, rq_packet, udp_client, client_addr):
		try:
			if(tftp.file_exist(tftp.get_filename(rq_packet))):
				packet = tftp.set_error_packet(6, "File already exists")
				udp_client.sendto(packet, client_addr)
				return
			else:
				ack = tftp.set_ack_packet(0)
				udp_client.sendto(ack, client_addr)
				with open(tftp.get_filename(rq_packet), "wb") as fd:
					while(True):
						packet = udp_client.recvfrom(516)
						data = packet[4:]
						if(not data):
							break
						else:
							fd.write(data)
							ack_no = tftp.get_blocknum(packet)
							ack_packet = tftp.set_ack_packet(ack_no)
							udp_client.sendto(ack_packet, client_addr)




		except OSError as e:
			if(e.errno == errno.ENOENT):
				# file not found
				packet = tftp.set_error_packet(1, "File not found")
				udp_client.sendto(packet, client_addr)
				return 
			elif(e.errno == errno.EPERM or errno.EACCES):
				# acces violation
				packet = tftp.set_error_packet(2, "Access violation")
				udp_client.sendto(packet, client_addr)
				return
			elif(errno == errno.EFBIG or errno.ENOSPC):
				# disk full
				packet = tftp.set_error_packet(3, "Disk full")
				udp_client.sendto(packet, client_addr)
				return
			else:
				# unknown
				packet = tftp.set_error_packet(0, "Unknown")
				udp_client.sendto(packet, client_addr)
				return
		except Exception as e:
			self.print_logging(e)
			return

	def print_logging(self, msg):
		logging.debug(msg)
				



# def main():
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	s.bind(("", PORT))
# 	print("listening on {}".format(PORT))

# 	while True:
# 		data, addr = s.recvfrom(MAXSIZE)
# 		print("{} from {}".format(data, addr))
# 		s.sendto("Hello, {}".format(addr), addr)

server("192.168.1.68", 65432)