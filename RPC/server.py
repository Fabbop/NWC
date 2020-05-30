import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ("/RPC2",)
	
# Create server
with SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler) as server:
  
	server.register_introspection_functions()

	# Register a function under a different name
	# def adder_function(x, y):
	# 	return x + y

	# server.register_function(adder_function, 'add')

	# Register an instance; all the methods of the instance are
	# published as XML-RPC methods (in this case, just 'mul').
	class FileSystem:

		def check_directory(self, directory):
			return os.path.exists(directory)

		def create_file(self, filename, fnext):
			pass

		def mul(self, x, y):
			return x * y

	server.register_instance(FileSystem())

	# Run the server's main loop
	server.serve_forever()