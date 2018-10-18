from django.shortcuts import get_object_or_404
from  rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .models import File
from .serializer import FileSerializer
from .serializer import FileSerializerNotData
from django.shortcuts import render
from .forms import UserForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
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



#List all users, with their file paths and time-stamp
#user/filename
class FileList(APIView):

	def get(self, request):
		files = File.objects.all() #get all file objects
		serializer = FileSerializer(files, many=True)
		return Response(serializer.data)

	def post(self):
		pass

# Create your views here.

class FileListNotData(APIView):

    def get(self, request):
        files = File.objects.all() #get all file objects
        serializer = FileSerializerNotData(files, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class FileListNotDataUser(APIView):

    def get(self,request,user_id):
        user = User.objects.filter(username=user_id)
        files = File.objects.filter(user=user[0])
        serializer = FileSerializerNotData(files, many=True)
        return Response(serializer.data)

    def  post(self):
        pass

class FileListUserData(APIView):

    def get(self,request,user_id,path):
        new_path = "./"+path ## ASSUMPTION: ALL PATHS WILL BEGIN WITH "./"
        user = User.objects.filter(username=user_id)
        files = File.objects.filter(user=user[0], path=new_path)
        serializer = FileSerializer(files, many=True )
        return Response(serializer.data)

    def post(self):
        pass

 