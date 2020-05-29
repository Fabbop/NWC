import socket, struct

RRQ, WRQ, DATA, ACK, ERROR, OACK = range(1, 7)
BLOCK_SIZE = 512
DEFAULT_PORT = 69

def default_port(): 
	return socket.getservbyname("tftp", "udp")

def read_chunk(filename, sock_fd):
	with open(filename, "rb") as fd:
		while(True):
			data = fd.read(512)
			# print(data)
			if(not data):
				break

def write_chunk(filename):
	pass

def set_data_packet(block_num, data):
	return struct.pack("! H H", DATA, block_num) + data

def set_ack_packet(block_num):
	return struct.pack("!H H", ACK, block_num)

def set_request_packet(opcode, filename, mode="octet"):
	filen = bytes(filename, "utf-8")
	m = bytes(mode, "utf-8")
	values = (opcode, filen, 0, m, 0)
	s = struct.Struct("! H {}s B {}s B".format(len(filen), len(m)))
	return s.pack(*values)
    
def set_rrq_packet(filename):
	return set_request_packet(RRQ, filename)

def set_wrq_packet(filename):
	return set_request_packet(WRQ, filename)

def get_opcode(packet):
	return struct.unpack("!H", packet[:2])[0]

def get_blocknum(packet):
	return struct.unpack("!H", packet[2:4])[0]

read_chunk("hola.txt")