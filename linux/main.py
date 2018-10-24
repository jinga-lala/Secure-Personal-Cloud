import authenticate
import network_operations
import os
import utils
import argparse
import sys
import json
import getpass
USER = ''
SERVER = ''
PWD = './'
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
if __name__ == "__main__":
    # print(os.getcwd())

    l = open(LOGFILE, "r")
    j = json.load(l)
    l.close()
    SERVER = j["SERVER"]
    USER = j["USER"]
    PWD = j["PWD"]
    AUTHENTICATED = j["AUTHENTICATED"]
    # print((AUTHENTICATED=="False"),len(sys.argv))
    if(len(sys.argv) == 1 and AUTHENTICATED == True):
        l = open(LOGFILE, "r")
        j = json.load(l)
        user = j["USER"]
        print('You are already logged in as ' + user)
        l.close()
    elif(len(sys.argv) == 1 and AUTHENTICATED == False):
        input_user = input("Enter Username : ")
        input_pwd = getpass.getpass("Enter Password : ")
        SERVER = input("Enter server : ")
        if(authenticate.login(input_user, input_pwd, SERVER)):
            print("AUTHENTICATED. Hello", input_user)
            l = open(LOGFILE, "w")
            j["SERVER"] = SERVER
            j["USER"] = input_user
            j["PWD"] = PWD
            j["AUTHENTICATED"] = True
            json.dump(j, l)
            l.close()
        else:
            print("ACCESS DENIED")
            l = open(LOGFILE, "w")
            j["USER"] = ""
            json.dump(j, l)
            l.close()
    elif(AUTHENTICATED == True):
        if(sys.argv[1] == "set-url"):
            if(len(sys.argv) < 3):
                utils.die_with_usage()
            else:
                SERVER = sys.argv[2]
                l = open(LOGFILE, "w")
                j["SERVER"] = SERVER
                json.dump(j, l)
                l.close()
        if(sys.argv[1] == "status"):
            if(SERVER != "" and USER != "" and PWD != ""):
                utils.status(PWD, SERVER, USER)
            else:
                utils.die_with_usage()
        if(sys.argv[1] == "observe"):
            # PWD=os.getcwd()
            PWD = "./"
            l = open(LOGFILE, "w")
            j["PWD"] = PWD
            json.dump(j, l)
            l.close()
        if(sys.argv[1] == "sync"):
            # input_pwd = getpass.getpass("Enter your Password : ")
            a, b, c, d = utils.get_paths_of_uploads_and_downloads(pwd=PWD, server=SERVER, username=USER)
            utils.status(PWD, SERVER, USER)
            choice = input("Press y to continue , n to quit")
            if(choice == "y"):
                utils.create_files(a, PWD, USER, SERVER)
                utils.upload_files(b, PWD, d, SERVER)
                utils.resolve_conflicts(c, PWD, USER, d, SERVER)

    # SERVER=input("Enter server IP : ")
    # print(SERVER)
    # input_user=input("Enter Username : ")
    # input_pwd=input("Enter Password : ")
    # if(authenticate.login(input_user,input_pwd,SERVER)):
    #   print("AUTHENTICATED. Hello ",input_user)
    #   USER=input_user
    #   a,b,c,d=utils.get_paths_of_uploads_and_downloads(pwd="./",server=SERVER,username=USER)
    #   utils.status(PWD,SERVER,USER)
    #   # utils.create_files(a,PWD,USER,SERVER)
    #   utils.upload_files(b,d,SERVER)
    #   utils.resolve_conflicts(c,PWD,USER,d,SERVER)
        # print(a,c)
        # utils.create_files(a,"./",USER,SERVER)
    # print(a)
    # print(b)
    # print(c)
    # path=input("Enter path of file : ")
    # u=network_operations.get_paths(SERVER,USER)
    # u=u[0]["user"]
    # p=network_operations.upload_file(path,u,SERVER)
    # network_operations.get_paths(SERVER,USER)

    else:
        print("ACCESS DENIED")
