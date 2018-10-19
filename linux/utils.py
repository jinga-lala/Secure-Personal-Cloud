import os
import network_operations
def get_paths_of_uploads_and_downloads(pwd,server,username):
	paths_and_timestamps=network_operations.get_paths(server,username)
	user=paths_and_timestamps[0]["user"]["id"]
	os.chdir(pwd)
	all_files=[]
	for path,subdir,files in os.walk(pwd):
		for name in files:
			all_files.append(os.path.join(path,name))
	all_files=set(all_files)
	all_cloud_files=set([x["path"] for x in paths_and_timestamps])
	upload_paths=list(all_files-all_cloud_files)
	download_paths=[]
	conflicts=[]
	for i in paths_and_timestamps:
		if(os.path.isfile(i["path"])==False):
			download_paths.append(i["path"])
		else:
			if(i["timestamp"]!=os.path.getmtime(i["path"])):
				conflicts.append(i["path"])
	return([download_paths,upload_paths,conflicts,user])

def create_files(paths,pwd,user,server):
	'''
	Downloads files from given list of paths, creates directories and saves them
	Use on download_paths[]
	''' 
	for path in paths:
		data,__=network_operations.download_file(path[2:],user,server)
		directory="/".join(path.split("/")[:-1])+"/"
		try:
			os.makedirs(directory)
		except FileExistsError:
			a=1
		file=open(path,"wb")
		file.write(data)
		file.close()

def upload_files(paths,user,server):
	'''
	Uploads files on given paths
	'''
	for path in paths:
		network_operations.upload_file(path,user,server)

def status(pwd,server,username):
	to_be_downloaded,to_be_uploaded,conflicted,_=get_paths_of_uploads_and_downloads(pwd,server,username)
	print("\n","Files not on server : ","\n")
	for path in to_be_uploaded:
		print("\t",path)
	print("\n","Files not available locally : ","\n")
	for path in to_be_downloaded:
		print("\t",path)
	print("\n","Conflicted files : ","\n")
	for path in conflicted:
		print("\t",path)

def resolve_conflicts(paths,user,server):
	'''
	Call on conflicts array, downloads files, compares them, asks user, then maybe downloads
	'''
	# TODO
