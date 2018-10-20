import base64
import os
import requests
import json
def decode(data):
	'''
	Returns bytestream from given string
	'''
	return(base64.b64decode(data))


def encode(data):		
	'''
	Returns string from given bytestream
	'''
	return(base64.b64encode(data).decode('ascii'))

def upload_file(path,user,server):
	'''
	Uploads file given a dict of user, path of file and server
	URL.
	'''
	file=open(path,"rb")
	data=file.read()
	encoded_data=encode(data)
	payload={'user':user,'path':path,'timestamp':os.path.getmtime(path),'data':encoded_data}
	post_data=json.dumps(payload)
	headers={'Content-type':'application/json'}
	api_url=server+"api/"
	client=requests.session()
	p=client.post(api_url,data=post_data,headers=headers)	
	return p	
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
	# print(data.json())
	return [decode(data.json()[0]["data"]),data.json()[0]["timestamp"]]	#fix this	

def get_user_id(username,server):
	api_url=server+"userAPI/"+username+"/"
	client=requests.session()
	data=client.get(api_url)
	return(data.json()[0]["id"])		

def update_file(path,username,server):
	file=open(path,"rb")
	data=file.read()
	encoded_data=encode(data)
	payload={'path':path,'timestamp':os.path.getmtime(path),'data':encoded_data}
	post_data=json.dumps(payload)
	headers={'Content-type':'application/json'}
	api_url=server+"api/"+username+"/"+path
	client=requests.session()
	p=client.post(api_url,data=post_data,headers=headers)	
	return p	
