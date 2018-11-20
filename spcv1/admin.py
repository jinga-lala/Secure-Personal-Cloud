from django.contrib import admin
from .models import File,encryption,shared_files

admin.site.register(File)
admin.site.register(encryption)
admin.site.register(shared_files)
# Register your models here.
