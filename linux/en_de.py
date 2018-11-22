'''
TODO - Bug where encryption scheme cannot be changed without observe
'''
import network_operations as net_ops
from Crypto.Cipher import AES, Salsa20, ChaCha20
from Crypto import Random
import pickle
import os
import subprocess
DEFAULT_SCHEME = "AES"
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto.dat")
BASH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encrypt_decrypt.sh")
class encryption_data:
	def __init__(self,scheme,key):
		self.scheme = scheme
		self.key = key
	def __str__(self):
		return("Encryption Scheme : "+self.scheme+"\nKey : "+(net_ops.encode(self.key)))

def list():
	index = print("These are the available encryption schemes :\n\t1. AES \n\t2. Salsa20 \n\t3. ChaCha20\n")	
def disp_schema():
	f = open(PATH,"rb")
	enc_data = pickle.load(f)
	print(enc_data)
def generate_schema(scheme="ChaCha20",key="",path=PATH):
	# print("Generating scheme - AES")
	if(key == ""):
		if scheme == "ChaCha20":
			key = Random.get_random_bytes(32)
		else:
			key = Random.get_random_bytes(16)
		print("Your scheme is",scheme)
		print("Your key is",net_ops.encode(key))
		print("As if you will remember your key... Just copy the file 'crypto.dat' in your installation folder for your next login, or change your key")
	else:
		while(len(key)%4):
			key+="y" # = is a specia character in base64 encoding hence a hardoded word is used

		if scheme == "AES" or scheme == "Salsa20":
			'''
			The code handles keys of all lengths
			'''
			print(len(key))
			try:
				if len(net_ops.decode(key))>=16:
					key = net_ops.decode(key)[0:16]
				else:
					print("Key too short, enter a 24 character key.")
					key = input("Enter a longer key : ")
					generate_schema(scheme,key)
					return
			except ValueError as e:			#TODO
				print("Your key is not compliant. Do not use spaces or special characters...")
				key = input("Enter a key : ")
				generate_schema(scheme,key)
				return
		elif scheme == "ChaCha20":
			try:
				if len(net_ops.decode(key)) >= 32:
					key = net_ops.decode(key)[0:32]
				else:
					print("Key too short, enter a 48 character key.")
					key = input("Enter a longer key : ")
					generate_schema(scheme,key)
					return
			except ValueError as e:
				print("Your key is not compliant. Do not use spaces or special characters...")
				key = input("Enter a key : ")
				generate_schema(scheme,key)
				return
	d = encryption_data(scheme,key)
	f = open(path,"wb")
	pickle.dump(d,f)
	f.close()
	print("Generated a scheme")

def load_scheme(path,dump=PATH):
	f = open(path,"rb")
	data = f.read()
	f.close()
	f = open(dump,"wb")
	f.write(data)
	f.close()


def get_schema(path=PATH):
	choice = input("Do you have a config file for the key? (Enter y/n) : \n")
	if choice == "y" or choice == "Y":
		input_path = input("Enter the full path of the file : \n")
		load_scheme(input_path,path)
	else:
		schemes = ['AES','Salsa20','ChaCha20']
		index = input("Enter the number corresponding to your encryption scheme :\n\t1. AES \n\t2. Salsa20 \n\t3. ChaCha20\n")
		scheme = schemes[int(index)-1]
		choice = input("Do you have a key?\n")
		if(choice == "y"):
			key = input("Enter the key as a string : ")
		else:
			key=""
		generate_schema(scheme,key,path)


def encrypt(path,key_path=PATH):
	f = open(key_path,"rb")
	enc_data = pickle.load(f)
	# print(enc_data)
	scheme = enc_data.scheme
	key = enc_data.key.hex()
	print(key)
	f.close()
	bash_command = "bash "+BASH+" en "+scheme+" "+key+" "+path+" "+path+".enc"
	subprocess.run(bash_command,shell=True,check=False)
	# print(type(key))
	# if(scheme == "AES"):
	# 	iv = Random.new().read(AES.block_size)	#TODO
	# 	cipher = AES.new(key, AES.MODE_CFB, iv)
	# 	return [iv + cipher.encrypt(data),16]
	# elif scheme == "Salsa20":
	# 	cipher = Salsa20.new(key=key)
	# 	# nonce = b'1'*8
	# 	# print(len(cipher.nonce))
	# 	return [cipher.nonce + cipher.encrypt(data),8]
	# else:
	# 	cipher = ChaCha20.new(key=key)
	# 	ciphertext = cipher.encrypt(data)
	# 	return [cipher.nonce+ciphertext,8]
	# f.close()
	# if scheme == "Blowfish":
	# 	iv = Random.new().read(bs)
	# 	cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
	# 	bs = Blowfish.block_size
	# 	plen = bs - divmod(len(data),bs)[1]
	# 	padding = [plen]*plen
	# 	padding = pack('b'*plen, *padding)
	# 	return iv + cipher.encrypt(data + padding)
	# if scheme == "CAST":
	return

def decrypt(path,key_path=PATH):
	f = open(key_path,"rb")
	enc_data = pickle.load(f)
	# print(enc_data)
	scheme = enc_data.scheme
	key = enc_data.key.hex()
	# if scheme == "AES":
	# 	iv = data[:AES.block_size]
	# 	cipher = AES.new(key, AES.MODE_CFB, iv)
	# 	return cipher.decrypt(data[AES.block_size:])
	# elif scheme == "Salsa20":
	# 	msg_nonce = data[:8]
	# 	ciphertext = data[8:]
	# 	cipher = Salsa20.new(key=key, nonce=msg_nonce)
	# 	return cipher.decrypt(ciphertext)
	# else:
	# 	msg_nonce = data[:8]
	# 	ciphertext = data[8:]
	# 	cipher = ChaCha20.new(key=key, nonce=msg_nonce)
	# 	return cipher.decrypt(ciphertext)
	f.close()
	print(key)
	bash_command = "bash "+BASH+" de "+scheme+" "+key+" "+path+".enc "+path
	subprocess.run(bash_command,shell=True,check=False)
