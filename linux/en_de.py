import network_operations as net_ops
from Crypto.Cipher import AES, Salsa20, ChaCha20
from Crypto import Random
import pickle
import os

DEFAULT_SCHEME = "AES"
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto.dat")

class encryption_data:
	def __init__(self,scheme,key):
		self.scheme = scheme
		self.key = key

def generate_schema(scheme="ChaCha20",key=""):
	# print("Generating scheme - AES")
	if(key == ""):
		key = Random.get_random_bytes(32)
		print("Your scheme is AES")
		print("Your key is",net_ops.encode(key))
		print("As if you will remember your key... Just copy the file 'crypto.dat' in your installation folder for your next login, or change your key")
	else:
		if len(key) >= 16:
			'''
			Key is uniformly 16 bytes, TODO
			'''
			key = net_ops.decode(key[0:16])
		else:
			print("Key too short, enter a 16 character key.")
	d = encryption_data(scheme,key)
	f = open(PATH,"wb")
	pickle.dump(d,f)
	print("Generated a scheme")

def load_scheme(path):
	f = open(path,"rb")
	data = file.read()
	f.close()
	f = open(PATH,"wb")
	f.write(data)
	f.close()


def get_schema():
	choice = input("Do you have a config file for the key? (Enter y/n) : \n")
	if choice == "y" or choice == "Y":
		input_path = input("Enter the full path of the file : \n")
		load_scheme(path)
	else:
		schemes = ['AES','Salsa20','CAST']
		index = input("Enter the number corresponding to your encryption scheme :\n\t1. AES \n\t2. Salsa20 \n\t3. ChaCha20\n")
		scheme = schemes[int(index)-1]
		key = input("Enter the key as a string : ")
		generate_schema(scheme,key)


def encrypt(data):
	f = open(PATH,"rb")
	enc_data = pickle.load(f)
	scheme = enc_data.scheme
	key = enc_data.key
	if(scheme == "AES"):
		iv = b'1'*(AES.block_size)		#TODO
		cipher = AES.new(key, AES.MODE_CFB, iv)
		return [iv + cipher.encrypt(data),16]
	elif scheme == "Salsa20":
		cipher = Salsa20.new(key=key)
		# nonce = b'1'*8
		# print(len(cipher.nonce))
		return [cipher.nonce + cipher.encrypt(data),8]
	else:
		cipher = ChaCha20.new(key=key)
		ciphertext = cipher.encrypt(data)
		return [cipher.nonce+ciphertext,8]
	# if scheme == "Blowfish":
	# 	iv = Random.new().read(bs)
	# 	cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
	# 	bs = Blowfish.block_size
	# 	plen = bs - divmod(len(data),bs)[1]
	# 	padding = [plen]*plen
	# 	padding = pack('b'*plen, *padding)
	# 	return iv + cipher.encrypt(data + padding)
	# if scheme == "CAST":

def decrypt(data):
	f = open(PATH,"rb")
	enc_data = pickle.load(f)
	scheme = enc_data.scheme
	key = enc_data.key
	if scheme == "AES":
		iv = data[:AES.block_size]
		cipher = AES.new(key, AES.MODE_CFB, iv)
		return cipher.decrypt(data[AES.block_size:])
	elif scheme == "Salsa20":
		msg_nonce = data[:8]
		ciphertext = data[8:]
		cipher = Salsa20.new(key=key, nonce=msg_nonce)
		return cipher.decrypt(ciphertext)
	else:
		msg_nonce = data[:8]
		ciphertext = data[8:]
		cipher = ChaCha20.new(key=key, nonce=msg_nonce)
		return cipher.decrypt(ciphertext)


