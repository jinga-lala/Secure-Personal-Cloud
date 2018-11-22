from django.contrib import admin
from .models import File,encryption,Token

admin.site.register(File)
admin.site.register(encryption)
admin.site.register(Token)
# Register your models here.
