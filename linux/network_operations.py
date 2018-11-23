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


def upload_file(path, pwd, user, server, token, username, key_path, shared=False):
    '''
    Uploads file given a dict of user, path of file and server
    URL.
    '''
    en_de.encrypt((pwd + path[1:]).replace(' ', '\ '), key_path)
    # try:
    file = open((pwd + path[1:] + ".enc"), "r")
    # file = open((pwd + path[1:]), "rb")
    # print(file)
    '''
    TODO - Currently storing unencrypted md5sum...
    '''
    data = file.read()
    file.close()
    file = open((pwd + path[1:]), "rb")
    check_sum_data = file.read()
    encoded_data = encode(check_sum_data)
    md5sum = get_md5_sum(encoded_data)
    file.close()
    os.remove((pwd + path[1:] + ".enc"))

    if data == "":  # TODO
        print("Rakhta hun mai khulla")
        data = "IAo="  # Base64 for " " character
        md5sum = get_md5_sum(data)
    if shared == False:
        safe = "Y"
    else:
        safe = "N"
    payload = {'user': user, 'path': path, 'timestamp': os.path.getmtime(path), 'data': data, 'md5sum': md5sum, 'safe': safe}
    post_data = json.dumps(payload)
    headers = {'Content-type': 'application/json', "Authorization": "Token " + token}
    api_url = server + "api/" + username + "/"
    client = requests.session()
    p = client.post(api_url, data=post_data, headers=headers)
    return p
    # TODO


def get_paths(server, username, token):
    print("Getting Paths")
    api_url = server + "pathAPI/" + username  # fix this
    # print(api_url)
    client = requests.session()

    header = {"Authorization": "Token " + token}
    paths_and_timestamps = client.get(api_url, headers=header)
    return(paths_and_timestamps.json())


def recieved_shared(user, path, server):
    data = {"path": path}
    api_url = server + "shareAPI/" + user + "/recieve"
    client = requests.session()
    post_data = json.dumps(data)
    # print(api_url,post_data)
    headers = {'Content-type': 'application/json'}
    p = client.post(api_url, data=post_data, headers=headers)
    return p


def download_file(path, pwd, user, server, token, key_path, shared=False, buff=False):
    '''
    Get paths, check whether those paths exist, if they don't, we download,
    if there are extraneous paths, we upload.
    Then diff files/check timestamps, have a THRESHOLD variable for diff tolerance
    '''
    # while True:

    api_url = server + "updateAPI/" + user + "/" + path[2:]  # Fix URL
    header = {"Authorization": "Token " + token}
    client = requests.session()
    data = client.get(api_url, headers=header)
    # print(data.json(), api_url, header)
    d = data.json()[0]["data"]
    # buff_file = open(path+)
    if buff == False:
        file_path = pwd + path[1:]
    else:
        file_path = pwd + "/buff_diff.txt"
    file = open(file_path + ".enc", "w")
    file.write(d)
    file.close()
    file_path = file_path.replace(' ', '\ ')
    en_de.decrypt(file_path, key_path)
    os.remove(file_path.replace('\ ', ' ') + ".enc")
    d = open(file_path.replace('\ ', ' '), "rb")
    file = d.read()
    d.close()

    # os.remove(key_path)
    # print(get_md5_sum(encode(file[8:])),data.json()[0]["md5sum"])
    if(get_md5_sum(encode(file)) == data.json()[0]["md5sum"]):
        print("File recieved okay")  # fix this
        # print(shared)
        return   # fix this
    else:
        print("Error in recieving file", path, "\n Make sure you have the correct key.")
        choice = input("Do you want to try again? (Enter y or n) : ")
        if choice == "y":
            download_file(path,pwd, user, server,token, key_path, shared)
        else:
            file = open(file_path.replace(' ', '\ '), "wb")
            file.write(decode("IAo="))
            file.close()


def get_user_id(username, server, token):
    api_url = server + "userAPI/" + username + "/"
    client = requests.session()
    header = {"Authorization": "Token " + token}
    data = client.get(api_url, headers=header)
    try:
        return(data.json()[0]["id"])
    except:
        return -1


def send_sharing_file(server, data):
    api_url = server + "shareAPI/" + data["sender"] + "/send"
    if(data["path"] in [x["path"] for x in get_paths(server, data["sender"])]):
        client = requests.session()
        post_data = json.dumps(data)
        headers = {'Content-type': 'application/json'}
        p = client.post(api_url, data=post_data, headers=headers)
        return p
    else:
        print("File doesn't exist on the server...")


def check_for_files(reciever, server):
    api_url = server + "shareAPI/" + reciever + "/recieved"
    client = requests.session()
    data = client.get(api_url)
    return(data.json())


def update_file(path, pwd, username, server, token):
    en_de.encrypt((pwd + "/"+ path).replace(' ', '\ '))
    # try:
    file = open((pwd + "/"+path+".enc"), "r")
    # print(file)
    # except FileNotFoundError:
    # print(path," not found")
        # return
    # print(user)
    data = file.read()
    file.close()
    file = open(pwd+"/"+path,"rb")
    check_sum_data = file.read()
    encoded_data = encode(check_sum_data)
    md5sum = get_md5_sum(encoded_data)
    file.close()
    os.remove((pwd +"/"+ path+".enc"))
    # data,length = en_de.encrypt(pwd + path[1:],key_path)
    # encoded_data = encode(data)

    if encoded_data == "":      #TODO
        encoded_data = "IAo="  # Base64 for " " character
    # if shared == False:
    #     safe = "Y"
    # else:
    #     safe = "N"
    payload = {'path': path.replace(pwd, "."), 'timestamp': os.path.getmtime(path), 'data': data,'md5sum':md5sum,'safe':'Y'}
    post_data = json.dumps(payload)
    headers = {'Content-type': 'application/json', "Authorization" : "Token "+ token}
    api_url = server + "updateAPI/" + username + "/" + path
    client = requests.session()
    p = client.post(api_url, data=post_data, headers=headers)
    return p
