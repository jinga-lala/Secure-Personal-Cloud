from django.db import models
from django.contrib.auth.models import Permission, User

class File(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000)
    data = models.BinaryField(editable=True)
    timestamp = models.FloatField()
    def __str__(self):
        return self.path



# Create your models here.
