from django.db import models
from django.contrib.auth.models import Permission, User

class File(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
   # username=models.CharField(max_length=1000)
    path = models.CharField(max_length=1000)
    data = models.CharField(max_length=10000000000)
    md5sum = models.CharField(max_length=100)
    timestamp = models.FloatField()
    safe = models.CharField(max_length=1,default='Y')
    class Meta:
    	unique_together = (('user','path'),)
    # def __init__(self):
    # 	username = user.username
    def __str__(self):
        return self.path

class encryption(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    encrypted = models.CharField(max_length=1)

class shared_files(models.Model):
    sender = models.CharField(max_length=100)   #TODO
    reciever = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
# Create your models here.
