import os
import network_operations
import difflib
import en_de
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crypto.dat")

def get_paths_of_uploads_and_downloads(pwd, server, username,token,update=False):
    paths_and_timestamps = network_operations.get_paths(server, username,token)
    user = network_operations.get_user_id(username, server,token)
    os.chdir(pwd)
    all_files = []
    for path, subdir, files in os.walk(pwd):
        for name in files:
            all_files.append(os.path.join(path, name))
    all_files = [x.replace(pwd, ".") for x in all_files]
    all_files = set(all_files)
    all_cloud_files = set([x["path"] for x in paths_and_timestamps])  # Compare with replace with ./, download with full path
    upload_paths = list(all_files - all_cloud_files)
    # upload_paths=[(x[1:]+pwd) for x in upload_paths]
    if update == True:
        return [list(all_cloud_files),user]
    download_paths = []
    conflicts = []
    for i in paths_and_timestamps:
        if(os.path.isfile(i["path"]) == False):
            download_paths.append(i["path"])
        else:
            p=pwd+i["path"][1:]
            f=open(p,"rb")
            # f,length=en_de.encrypt(f.read())
            '''
            TODO - ditch the first 8/16 bytes, then calc md5sum
            '''
            md5=network_operations.get_md5_sum(network_operations.encode(f.read()))
            # print(i["md5sum"],md5)
            # print(md5,i["md5stok = request.META['HEADERS']
        # print(tok)um"])
            if(i["md5sum"] != md5):
                conflicts.append(i["path"])
      
    return([download_paths, upload_paths, conflicts, user])


def create_file(path, pwd, user, server, token,key_path=KEY_PATH,shared=False):
    # data, timestamp = network_operations.download_file(path[2:], user, server, token)
    # path = pwd + path[1:]
    directory = "/".join(path.split("/")[:-1]) + "/"
    directory = pwd + directory[1:]
    directory.replace("%20"," ")
    print(directory)
    try:
        os.makedirs(directory)
    except FileExistsError:
        a = 1
    network_operations.download_file(path,pwd,user, server,key_path,shared)

    # file = open(path, "wb")
    # file.write(data)
    # # print(timestamp)
    # file.close()
    # os.utime(path, (timestamp, timestamp))


def create_files(paths, pwd, user, server,token,key_path=KEY_PATH,shared=False):
    '''
    Downloads files from given list of paths, creates directories and saves them
    Use on download_paths[]
    '''
    printProgressBar(0, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
    i=0
    for path in paths:
        print("Downloading ", path)
        create_file(path, pwd, user, server,token,key_path,shared)
        printProgressBar(i + 1, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
        i+=1


def upload_files(paths, pwd, user, server,token,username):
    '''
    Uploads files on given paths
    '''
    printProgressBar(0, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
    i=0
    for path in paths:
        print("Uploading ", path)
        network_operations.upload_file(path, pwd, user, server,token,username,KEY_PATH)
        printProgressBar(i + 1, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
        i+=1


def status(pwd, server, username,token):
    to_be_downloaded, to_be_uploaded, conflicted, _ = get_paths_of_uploads_and_downloads(pwd, server, username,token)
    f=0
    if(len(to_be_uploaded)):
        print("\n", "Files not on server : ", "\n")
        f=1
        for path in to_be_uploaded:
            print("\t", path)
    if(len(to_be_downloaded)):
        print("\n", "Files not available locally : ", "\n")
        f=1
        for path in to_be_downloaded:
            print("\t", path)
    if(len(conflicted)):
        f=1
        print("\n", "Conflicted files : ", "\n")
        for path in conflicted:
            print("\t", path)
    if(f == 0):
        print("Up to date, no syncing required")

def resolve_conflicts(paths, pwd, username, user_id, server,token):
    '''
    Call on conflicts array, downloads files, compares them, asks user, then maybe downloads
    '''
    # TODO
    allowed = ["txt", "py", "cpp", "c", ]
    printProgressBar(0, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
    i=0
    for file in paths:
        printProgressBar(i + 1, len(paths), prefix = 'Progress:', suffix = 'Complete', length = 50)
        i +=1
        if(len(file[2:].split(".")) > 1):
            extension = file.split(".")[-1]
            if(extension not in allowed):
                print(file, " differs on the cloud, resolve conflict manually.")
                choice = input("Enter 'u' to upload file, 'd' to download : ")
                if(choice == 'u'):
                    network_operations.update_file(file[2:], pwd, username, server,token)
                if(choice == 'd'):
                    create_file(file, pwd, username, server)
            else:
                network_operations.download_file(file, pwd,username, server,token,KEY_PATH,buff=True)
                # fileb = open("./buff_diff.txt", "wb")
                # fileb.write(contents)
                # fileb.close()
                f1 = open(pwd+"./buff_diff.txt", "r")
                f2 = open(file, "r")
                diff1 = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file, tofile=pwd+"./buff_diff.txt")
                diff2 = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file, tofile=pwd+"./buff_diff.txt")
                f2.close()
                f1.close()

                os.remove(pwd+"./buff_diff.txt")
                # if(1.0 * len([_ for _ in diff1]) < (0.15) * len([_ for _ in f2.readlines()])):  # Threshold=15%
                #     print("Fast forwarding ", file)
                #     create_file(file, pwd, username, server)
                # else:
                print("For file", file, "Here are the conflicts")
                for line in diff1:
                    print(line)
                choice = input("Enter 'u' to upload file, 'd' to download : ")
                if(choice == 'u'):
                    network_operations.update_file(file[2:], pwd, username, server, token)
                if(choice == 'd'):
                    create_file(file, pwd, username, server, token)

        else:

            '''
            Diff here
            '''
            network_operations.download_file(file[2:], username, server, token,key_path=KEY_PATH,buff=True)
            # fileb = open("./buff_diff.txt", "wb")
            # fileb.write(contents)
            # fileb.close()
            f1 = open(pwd+"./buff_diff.txt", "r")
            f2 = open(file, "r")
            diff1 = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file, tofile=pwd+"./buff_diff.txt")
            diff2 = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file, tofile=pwd+"./buff_diff.txt")
            f2.close()
            f1.close()

            os.remove(pwd+"./buff_diff.txt")
            # if(1.0 * len([_ for _ in diff1]) < (0.15) * len([_ for _ in f2.readlines()])):  # Threshold=15%
            #     print("Fast forwarding ", file)
            #     create_file(file, pwd, username, server)
            # else:
            print("For file", file, "Here are the conflicts")
            for line in diff1:
                print(line)
            choice = input("Enter 'u' to upload file, 'd' to download : ")
            if(choice == 'u'):
                network_operations.update_file(file[2:], pwd, username, server, token)
            if(choice == 'd'):
                create_file(file, pwd, username, server, token)


def send_file(user,reciever,path,pwd,server,token):
    '''
    '''
    if(network_operations.get_user_id(reciever,server,token) != -1):
        data = {"sender":user,"reciever":reciever,"path":path}
        network_operations.send_sharing_file(server,data)
        create_file(path, pwd, user, server,token)
        print("Generating a shared key for ",path)
        temp_key_path = "temp_key.dat"
        en_de.get_schema(path=temp_key_path)
        reciever_uploader = network_operations.get_user_id(reciever,server,token)
        network_operations.upload_file(path, pwd, reciever_uploader, server,token, temp_key_path,shared=True)
        print("The key for the file can be found in your home folder under the name 'temp_key.dat', if you wish to share it")

    else:
        print("Enter a valid user")

def recieve_files(reciever,pwd,server,token):
    files = network_operations.check_for_files(reciever,server)
    if(len(files)):
        shared_with_me = {}
        for x in files:
            try:
                shared_with_me[x["sender"]].append(x["path"])
            except:
                shared_with_me.update({x["sender"]:[x["path"]]})
        for x in shared_with_me:
            print("User ",x," has sent you",len(shared_with_me[x])," file(s)")
            choice = input("Do you want to download them? (Make sure you have the key...)")
            if(choice.lower() == "y" or choice.lower() == "yes"):
                key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_key.dat")
                en_de.get_schema(path=key_path)
                for file in shared_with_me[x]:
                    print("Downloading ",file)
                    create_file(file,pwd,reciever,server,token,key_path,True)
                    network_operations.recieved_shared(reciever,file,server)
                    print("Backing file up...")
                    # reciever_uploader = network_operations.get_user_id(reciever,server)
                    # if (file in [x["path"] for x in get_paths(server,data["sender"])]):
                        # print("There is a conflict in ",file,". \nResolve and resync with the server")
                    # else:
                    network_operations.update_file(file[2:], pwd, reciever, server,token)


def die_with_usage():
    print("Enter a couple of args please")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    if(total==0):
        print()
    else:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()