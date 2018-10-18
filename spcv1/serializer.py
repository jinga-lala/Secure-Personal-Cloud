from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  File

class FileSerializer(serializers.ModelSerializer):

	class Meta:
		model = File
		fields = ('user', 'path', 'timestamp','data')
		depth = 1

class FileSerializerNotData(serializers.ModelSerializer):

	class Meta:
		model = File
		fields = ('user' , 'path', 'timestamp')
		depth = 1

