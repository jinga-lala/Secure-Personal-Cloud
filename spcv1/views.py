from django.shortcuts import get_object_or_404
from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializer import FileSerializer
from django.shortcuts import render
from .forms import UserForm
from django.http import HttpResponse
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
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
