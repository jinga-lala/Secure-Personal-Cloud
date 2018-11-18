import base64
import os
import requests
import json
import hashlib
import en_de
def decode(data):
    '''
    Returns bytestream from given string
    '''
    try:
        return(base64.b64decode(data))
    except:
        raise ValueError("Pad correctly")


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
    print(file)
    '''
    TODO - Currently storing unencrypted md5sum...
    '''
    data = file.read()
    file.close()
    encoded_data = encode(data)
    md5sum = get_md5_sum(encoded_data)
    data,length = en_de.encrypt(data)
    encoded_data = encode(data)

    if encoded_data == "":      #TODO
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
        file = decode(data.json()[0]["data"])
        file = en_de.decrypt(file)
        # print(get_md5_sum(encode(file[8:])),data.json()[0]["md5sum"])
        if(get_md5_sum(encode(file))==data.json()[0]["md5sum"]):
            print("File recieved okay")         #fix this
                
            return [file, data.json()[0]["timestamp"]]  # fix this
        else:
            print("Error in recieving file, trying again")

def get_user_id(username, server):
    api_url = server + "userAPI/" + username + "/"
    client = requests.session()
    data = client.get(api_url)
    return(data.json()[0]["id"])


def update_file(path, pwd, username, server):
    file = open((pwd +"/"+ path), "rb")
    data = file.read()
    file.close()
    encoded_data = encode(data)
    md5sum = get_md5_sum(encoded_data)
    data,length = en_de.encrypt(data)
    encoded_data = encode(data)
    payload = {'path': path.replace(pwd, "."), 'timestamp': os.path.getmtime(path), 'data': encoded_data,'md5sum':md5sum}
    post_data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    api_url = server + "api/" + username + "/" + path
    client = requests.session()
    p = client.post(api_url, data=post_data, headers=headers)
    return p
