from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File, encryption, shared_files


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
# 	#	fields = ('id', 'username', 'password', 'email','last_login', 'is_superuser', 'first_name', 'last_name','is_staff','is_active','date_joined','groups','user_permissions')


class FileSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = File
        fields = ('user', 'path', 'timestamp', 'data', 'md5sum', 'safe')

    # def create(self, request):
    # 	j = request.data
    # 	u = UserSerializer(read_only=True)
    # 	f = FileSerializer(read_only=True)


class EncryptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = encryption
        fields = "__all__"


class FileSerializerNotData(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('user', 'path', 'md5sum')
        depth = 1


class FileShareSerializerNotData(serializers.ModelSerializer):
    class Meta:
        model = shared_files
        fields = ('sender','reciever', 'path')

class FileShareSerializerData(serializers.ModelSerializer):
    class Meta:
        model = shared_files
        fields = "__all__"
