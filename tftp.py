import socket, struct
from os import path

RRQ, WRQ, DATA, ACK, ERROR, OACK = range(1, 7)
BLOCK_SIZE = 512
DEFAULT_PORT = 69

def default_port(): 
	return socket.getservbyname("tftp", "udp")

def read_chunk(fd, udp_socket, server_addr):
	# block = 1
	# wd = open("copy.txt", "wb")
	# with open(filename, "rb") as fd:
	# 	while(True):
	# 		data = fd.read(512)
	# 		packet = set_data_packet(block, data)
	# 		struct.unpack("!H", packet[:2])[0]
	# 		struct.unpack("!H", packet[2:4])[0]
	# 		print(packet)
	# 		wd.write(packet[4:])
	# 		block += 1
	# 		# print(data)
	# 		if(not data):
	# 			break
	block_num = 1
	while(True):
		data = fd.read(512)
		packet = set_data_packet(block_num, data)
		udp_socket.sendto(packet, server_addr)
		block_num += 1
		if(not data):
			break

def write_chunk():
	pass

def set_data_packet(block_num, data):
	return struct.pack("!HH", DATA, block_num) + data

def set_ack_packet(block_num):
	return struct.pack("!HH", ACK, block_num)

def set_error_packet(errono, msg):
	errmsg = bytes(msg, "utf-8")
	values = (ERROR, errono, msg, 0)
	s = struct.Struct("!HH{}sB".format(len(errmsg)))
	return s.pack(*values)

def set_request_packet(opcode, filename, mode="octet"):
	filen = bytes(filename, "utf-8")
	m = bytes(mode, "utf-8")
	values = (opcode, filen, 0, m, 0)
	s = struct.Struct("!H{}sB{}sB".format(len(filen), len(m)))
	return s.pack(*values)
    
def set_rrq_packet(filename):
	return set_request_packet(RRQ, filename)

def set_wrq_packet(filename):
	return set_request_packet(WRQ, filename)

def get_opcode(packet):
	return struct.unpack("!H", packet[:2])[0]

def get_blocknum(packet):
	return struct.unpack("!H", packet[2:4])[0]

def get_filename(packet):
	filename = packet[2:-7].decode(ascii)
	# return packet[2:-7].decode(ascii)
	return filename

def file_exist(filename):
	return path.exists(filename)


# packet = set_request_packet(WRQ, "hola.txt")
# print(get_filename(packet).decode("ascii"))
# read_chunk("hola.txt")

# datagram = set_request_packet(WRQ, "hola.txt")
# print(get_opcode(datagram))