import base64
import os
import requests
import json
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
	# TODO

def get_paths(server,username):
	print("Getting Path")
	api_url=server+"pathAPI/"+username	#fix this
	print(api_url)
	client=requests.session()
	paths_and_timestamps=client.get(api_url)
	return(paths_and_timestamps.json())

def download_file(path,user,server):
	'''
	Get paths, check whether those paths exist, if they don't, we download, 
	if there are extraneous paths, we upload.
	Then diff files/check timestamps, have a THRESHOLD variable for diff tolerance
	'''
	api_url=server+"api/"+user+"/"+path #Fix URL
	client=requests.session()
	data=client.get(api_url)
	return [decode(data.json()[0]["data"]),data.json()[0]["timestamp"]]	#fix this	

	