import xmlrpc.client, datetime

class client:
	
	server = xmlrpc.client.ServerProxy("http://localhost:8000")
	user_dir = ""
	cwd = ""

while(True):
	client = client()
	user = input("User: ")
	if(client.server.check_directory(user)):
		client.user_dir = user + "/"
		client.cwd = user + "/"
		break
	else:
		print("User not found")

while(True):
	line = input(">")
	command = line.split(" ")