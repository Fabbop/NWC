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
	try:
		line = input(client.cwd + " : ")
		command = line.split(" ")

		if(command[0] == "cd"):
			msg = client.server.change_directory(command[1], client.cwd, client.user_dir)
			if(msg == "You can't change directory" or msg == "No such file or directory"):
				print(msg)
			else:
				if(command[1] == ""):
					client.cwd = client.user_dir
				else:
					client.cwd = client.server.change_directory(command[1], client.cwd, client.user_dir)

		elif(command[0] == "mkdir"):
			print(client.server.mkdir(client.cwd, command[1]))

		elif(command[0] == "rmdir"):
			print(client.server.rmdir(client.cwd, command[1]))

		elif(command[0] == "ls"):
			for x in client.server.ls(client.cwd):
				print(x)

		elif(command[0] == "remove"):
			print(client.server.delete_file(client.cwd, command[1]))

		elif(command[0] == "create"):
			print(client.server.create_file(client.cwd, command[1]))

		elif(command[0] == "write"):
			data = " ".join(command[2:])
			print(client.server.write_to_file(client.cwd, command[1], data))
		
		elif(command[0] == "read"):
			lines = client.server.read_file(client.cwd, command[1])
			for i in lines:
				print(i)

		elif(command[0] == "quit"):
			break

		else:
			print("Command not found")
		
	except Exception as e:
		print(e)