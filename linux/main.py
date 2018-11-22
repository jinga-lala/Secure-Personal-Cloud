import authenticate
import network_operations
import os
import utils
import argparse
import sys
import json
import getpass
import en_de
from shutil import rmtree
USER = ''
SERVER = ''
PWD = './'
TOKEN= ''
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
j = dict()
if __name__ == "__main__":
    # print(os.getcwd())

    l = open(LOGFILE, "r")
    j = json.load(l)
    l.close()
    SERVER = j["SERVER"]
    USER = j["USER"]
    PWD = j["PWD"]
    AUTHENTICATED = j["AUTHENTICATED"]
    TOKEN = j["TOKEN"]
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
        ans,TOKEN = authenticate.login(input_user, input_pwd, SERVER,True)
        if(ans):
            print("AUTHENTICATED. Hello", input_user)
            l = open(LOGFILE, "w")
            j["SERVER"] = SERVER
            j["USER"] = input_user
            j["PWD"] = PWD
            j["AUTHENTICATED"] = True
            j["TOKEN"] = TOKEN
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
        if(sys.argv[1] == "logout"):
            # if(USER == ""):
            #     print("User not logged in")
            # else:
            l = open(LOGFILE, "w")
            j["USER"] = ""
            j["AUTHENTICATED"] = False
            j["PWD"] = ""
            j["TOKEN"] = ""
            json.dump(j, l)
            l.close()
            os.remove(en_de.PATH)
            print("Logged out successfully")
        if(sys.argv[1] == "status"):
            if(SERVER != "" and USER != "" and PWD != ""):
                utils.status(PWD, SERVER, USER,token=TOKEN)
            # elif USER == "":
            #     print("Login first")
            else:
                print("Observe a folder first")
        if(sys.argv[1] == "observe"):
            PWD = os.getcwd()
            #PWD = "./"
            l = open(LOGFILE, "w")
            j["PWD"] = PWD
            json.dump(j, l)
            l.close()
        if(sys.argv[1] == "sync"):
            input_pwd = getpass.getpass("Enter your Password : ")
            if(authenticate.login(USER, input_pwd, SERVER)):
                print("Authenticated")
                a, b, c, d = utils.get_paths_of_uploads_and_downloads(pwd=PWD, server=SERVER, username=USER, token=TOKEN)
                utils.status(PWD, SERVER, USER, TOKEN)
                if(len(a) or len(b) or len(c)):
                    choice = input("Press y to continue , n to quit : ")
                    if(choice == "y"):
                        utils.create_files(a, PWD, USER, SERVER,TOKEN)
                        utils.upload_files(b, PWD, d, SERVER,TOKEN)
                        utils.resolve_conflicts(c, PWD, USER, d, SERVER,TOKEN)
                # else:
                #     print("Directory already upto date")
            else:
                print("Access Denied")
        if(sys.argv[1]=="en-de"):
            if sys.argv[2] == "update":
                input_pwd = getpass.getpass("Enter your Password : ")
                if(authenticate.login(USER, input_pwd, SERVER)):
                    print("Authenticated")
                    a,d = utils.get_paths_of_uploads_and_downloads(pwd=PWD, server=SERVER, username=USER,update=True,token=TOKEN)
                    # print(a)
                    pwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
                    os.mkdir(pwd)
                    utils.create_files(a, pwd, USER, SERVER,TOKEN)
                    '''
                    TODO - proper UX here
                    '''
                    # utils.resolve_conflicts(c, PWD, USER, d, SERVER)
                    en_de.get_schema()
                    for file in a:
                        network_operations.update_file(file[2:], pwd, USER, SERVER, TOKEN)
                    # utils.update_files(a, pwd, d, SERVER)
                    rmtree(pwd)
                    # utils.upload_files(c, PWD, d, SERVER)

            elif sys.argv[2] == "dump":
                choice = input("The details of the scheme will soon appear on the screen. Do you really want that?\n")
                choice=choice.lower()
                if choice == "y" or choice== "yes":
                    en_de.disp_schema()
                else:
                    print("Well okay then")   
            elif sys.argv[2] == "list":
                en_de.list() 

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
