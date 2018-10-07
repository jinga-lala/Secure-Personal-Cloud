from django.shortcuts import get_object_or_404
from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializer import FileSerializer
from django.shortcuts import render
from .forms import UserForm

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                files = File.objects.filter(user=request.user)
                return render(request, 'spcv1/index.html', {'file': files})
    context = {
        "form": form,
    }
    return render(request, 'spcv1/register.html', context)



#List all users, with their file paths and time-stamp
#user/filename
class FileList(APIView):

	def get(self, request):
		files = File.objects.all() #get all file objects
		serializer = FileSerializer(file, many=True)
		return Response(serializer.data)

	def post(self):
		pass

# Create your views here.
