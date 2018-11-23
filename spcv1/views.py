from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .models import File, encryption, Token, shared_files
from .serializer import FileSerializer
from .serializer import FileSerializerNotData
from .serializer import UserSerializer
from .serializer import EncryptionSerializer
from .serializer import FileShareSerializerNotData,FileShareSerializerData
from django.shortcuts import render
from .forms import UserForm, TokenForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
#import MySQLdb, cPickle


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/spc')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def FileTree(request):
    files = File.objects.all()
    paths = []
    for file in files:
        filepath = file.path[2:]
        paths.append(filepath)
    return render(request, 'files.html', {'paths': paths})


# List all users, with their file paths and time-stamp
# user/filename
class FileList(APIView):

    def get(self, request, user_id):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        files = File.objects.all()  # get all file objects
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        # aTTENTION NEED TO BE SECURED
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        j = request.data
        serializer = FileSerializer(data=j)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.

# class FileListNotData(APIView):
#     # authentication_classes = (SessionAuthentication, BasicAuthentication)
#     # permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         files = File.objects.all() #get all file objects
#         serializer = FileSerializerNotData(files, many=True)
#         return Response(serializer.data)

#     def post(self):
#         pass


class FileListNotDataUser(APIView):

    def get(self, request, user_id):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user_id)
        files = File.objects.filter(user=user[0], safe='Y')
        serializer = FileSerializerNotData(files, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class FileListUserData(APIView):

    def get(self, request, user_id, path):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_path = "./" + path  # ASSUMPTION: ALL PATHS WILL BEGIN WITH "./"
        # print(new_path)
        user = User.objects.filter(username=user_id)
        files = File.objects.filter(user=user[0], path=new_path)
        serializer = FileSerializer(files, many=True)
        # print(serializer)
        return Response(serializer.data)

    def post(self, request, user_id, path):
        '''
            to resove conflicts and update file data
        '''
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        # print("AAH OOPS")
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_path = "./" + path
        user = User.objects.filter(username=user_id)
        files = File.objects.filter(user=user[0], path=new_path).update(data=request.data["data"], timestamp=request.data["timestamp"], md5sum=request.data["md5sum"], safe=request.data["safe"])
        return Response(request.data, status=status.HTTP_201_CREATED)


class UserId(APIView):

    def get(self, request, user_id):
        # tok = request.META['HTTP_AUTHORIZATION']
        # tok = tok[6:]
        # gettok = Token.objects.filter(user=user_id)
        # if(gettok[0].token) != tok:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user_id)
        # files = File.objects.filter(user=user[0])
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self):
        pass


class getEnc(APIView):

    def get(self, request, user_id):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        # print("fgmfkmsdm")
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user_id)
        # files = File.objects.filter(user=user[0])
        enc = encryption.objects.filter(user=user[0])
        serializer = EncryptionSerializer(enc, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        if(gettok[0].token) != tok:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=user_id)
        # files = File.objects.filter(user=user[0])
        data = {"user": user[0].id, "encrypted": "T","locked":request.data["locked"],"last_enc_update":request.data["last_enc_update"],"dead_time_check":request.data["dead_time_check"]}
        enc = EncryptionSerializer(data=data)
        if enc.is_valid():
            enc.save()
            enc = encryption.objects.filter(user=user[0].id).update(**data)
            # enc.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        enc = encryption.objects.filter(user=user[0].id).update(**data)
        # enc.save()

        return Response(status=status.HTTP_201_CREATED)


class FileShareAPI(APIView):
    def get(self, request, user_id, mode):
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        # print("fgmfkmsdm")
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if mode == "path":

            files = shared_files.objects.filter(reciever=user_id)
            # files = File.objects.filter(user=user[0])
            # enc = encryption.objects.filter(user=user[0])
            serializer = FileShareSerializerNotData(files, many=True)
            return Response(serializer.data)  # TODO deletion
        else:
            files = shared_files.objects.filter(reciever=user_id)
            # files = File.objects.filter(user=user[0])
            # enc = encryption.objects.filter(user=user[0])
            serializer = FileShareSerializerData(files, many=True)
            return Response(serializer.data)  # TODO deletion

    def post(self, request, user_id, mode):
        '''
        Mode tells whether sending or recieving
        '''
        tok = request.META['HTTP_AUTHORIZATION']
        tok = tok[6:]
        gettok = Token.objects.filter(user=user_id)
        # print("fgmfkmsdm")
        if(gettok[0].token) != tok:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if(mode == "send"):
            j = request.data
            # files = File.objects.filter(user=user[0])
            # data={"user":user[0].id,"encrypted":"T"}
            enc = FileShareSerializerData(data=j)
            if enc.is_valid():
                enc.save()
                return Response(request.data, status=status.HTTP_201_CREATED)
            return Response(enc.errors, status=status.HTTP_400_BAD_REQUEST)
        elif mode == "done":
            j = request.data
            file = shared_files.objects.filter(reciever=user_id, path=j["path"],sender=j["sender"]).delete()
            return Response(request.data, status=status.HTTP_201_CREATED)
            # return Response(enc.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            j = request.data
            file = shared_files.objects.filter(reciever=user_id, path=j["path"],sender=j["sender"])
            print(file[0])
            serializer = FileShareSerializerData(file, many=True)
            return Response(serializer.data)

def getToken(request):
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            print("OOHLALALAL")
            entry = Token(user=form.cleaned_data.get('user'), token=form.cleaned_data.get('token'))
            entry.save()
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('/spc')
    else:
        form = TokenForm()
    return render(request, 'signup.html', {'form': form})

