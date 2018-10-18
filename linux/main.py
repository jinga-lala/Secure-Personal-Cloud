import authenticate
import network_operations
import os
USER=''
SERVER=''
PWD=''

if __name__=="__main__":
	SERVER=input("Enter server IP : ")
	print(SERVER)
	input_user=input("Enter Username : ")
	input_pwd=input("Enter Password : ")
	if(authenticate.login(input_user,input_pwd,SERVER)):
		print("AUTHENTICATED. Hello ",input_user)
		USER=input_user
		# network_operations.get_paths(SERVER,USER)
		
	else:
		print("ACCESS DENIED")
