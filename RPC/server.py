from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os

class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ("/RPC2",)
	
with SimpleXMLRPCServer(("192.168.1.78", 8000), requestHandler=RequestHandler, allow_none=True, logRequests=True) as server:
  
	server.register_introspection_functions()

	class FileSystem:

		def check_directory(self, directory):
			return os.path.exists(directory)

		def mkdir(self, path, namedir):
			dirpath = path + namedir
			try:
				os.mkdir(dirpath)
			except OSError as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				msg = "Directory %s created" % dirpath
				return msg

		def rmdir(self, path, namedir):
			dirpath = path + namedir
			try:
				os.rmdir(dirpath)
			except OSError as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				msg = "Directory %s deleted" % dirpath
				return msg

		def delete_file(self, path, filename):
			filepath = path + filename
			try:
				os.remove(filepath)
			except OSError as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				msg = "File %s deleted" % filepath
				return msg

		def create_file(self, cwd, filename):
			filepath = cwd + filename + ".txt"
			try:
				f = open(filepath, "wb")
				f.close()
			except Exception as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				msg = "File %s created" % filename
				return msg

		def write_to_file(self, cwd, filename, data):
			filepath = cwd + filename
			try:
				with open(filepath, "a") as fd:
					fd.write(data + "\r\n")
			except Exception as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				msg = "File written"
				return msg

		def read_file(self, cwd, filename):
			filepath = cwd + filename
			try:
				with open(filepath, "r") as fd:
					lines = fd.readlines()
			except Exception as e:
				msg = "An Error has ocurred: %s" % e
				return msg
			else:
				return lines

		def ls(self, path):
			return os.listdir(path)
		
		def change_directory(self, path, cwd, user_dir):
			if(path == ".."):
				if(cwd == user_dir):
					return "You can't change directory"
				else:
					current = cwd.split("/")[:-2]
					cwd = "/".join(current) + "/"
					return cwd
			elif(self.check_directory(cwd + path)):
				cwd = cwd + path + "/"
				return cwd
			elif(path == ""):
				return user_dir
			else:
				return "No such file or directory"


	server.register_instance(FileSystem())

	server.serve_forever()