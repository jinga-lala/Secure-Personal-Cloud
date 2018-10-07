from django.shortcuts import get_object_or_404
from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import File
from .serializers import FileSerializer

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
