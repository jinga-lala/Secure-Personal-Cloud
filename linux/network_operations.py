import base64
import os
import requests
import json
import hashlib

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

def get_md5_sum(file):
    '''
    Returns the MD5sum (hexdigest) as a string for a base64 encoded file
    '''
    return hashlib.md5(file.encode('utf-8')).hexdigest()


def upload_file(path, pwd, user, server):
    '''
    Uploads file given a dict of user, path of file and server
    URL.
    '''
    file = open((pwd + path[1:]), "rb")
    data = file.read()
    encoded_data = encode(data)
    md5sum = get_md5_sum(encoded_data)
    if encoded_data == "":
        encoded_data = "IAo="  # Base64 for " " character
    payload = {'user': user, 'path': path, 'timestamp': os.path.getmtime(path), 'data': encoded_data,'md5sum':md5sum}
    post_data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    api_url = server + "api/"
    client = requests.session()
    p = client.post(api_url, data=post_data, headers=headers)
    return p
    # TODO


def get_paths(server, username):
    print("Getting Paths")
    api_url = server + "pathAPI/" + username  # fix this
    # print(api_url)
    client = requests.session()
    paths_and_timestamps = client.get(api_url)
    return(paths_and_timestamps.json())


def download_file(path, user, server):
    '''
    Get paths, check whether those paths exist, if they don't, we download,
    if there are extraneous paths, we upload.
    Then diff files/check timestamps, have a THRESHOLD variable for diff tolerance
    '''
    while True:
    
        api_url = server + "api/" + user + "/" + path  # Fix URL
        client = requests.session()
        data = client.get(api_url)
        # print(data.json())
        
        if(get_md5_sum(data.json()[0]["data"])==data.json()[0]["md5sum"]):
            print("File recieved okay")         #fix this
            file=decode(data.json()[0]["data"])
            return [decode(data.json()[0]["data"]), data.json()[0]["timestamp"]]  # fix this
        else:
            print("Error in recieving file, tryin again")

def get_user_id(username, server):
    api_url = server + "userAPI/" + username + "/"
    client = requests.session()
    data = client.get(api_url)
    return(data.json()[0]["id"])


def update_file(path, pwd, username, server):
    file = open((pwd + path), "rb")
    data = file.read()
    encoded_data = encode(data)
    md5sum=get_md5_sum(encoded_data)
    payload = {'path': path.replace(pwd, "."), 'timestamp': os.path.getmtime(path), 'data': encoded_data,'md5sum':md5sum}
    post_data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    api_url = server + "api/" + username + "/" + path
    client = requests.session()
    p = client.post(api_url, data=post_data, headers=headers)
    return p
