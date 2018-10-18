import base64
import os

def encode(data):		#TODO- EnDe
	'''
	Returns string from given bytestream
	'''
	# file=open(path,"rb")
	data=file.read()
	return(base64.b64encode(data).decode('ascii'))

def decode(data):
	'''
	Returns bytestream from given string
	'''
	return(base64.b64decode(data))

def upload_file(path,user,server):
	file=open(path,"rb")
	data=file.read()
	'''
	Put crypto here
	'''
	encoded_data=encode(data)

def download_file():
	'''
	Get paths, check whether those paths exist, if they don't, we download, 
	if there are extraneous paths, we upload.
	Then diff files/check timestamps, have a THRESHOLD variable for diff tolerance
	'''
	