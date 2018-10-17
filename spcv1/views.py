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


# def insertBLOB():
#     # Connect to a DB, e.g., the test DB on your localhost, and get a cursor
#     connection = MySQLdb.connect(db="db.sqlite3")
#     cursor = connection.cursor(  )

#     # Make a new table for experimentation
#     cursor.execute("CREATE TABLE justatest (name TEXT, ablob BLOB)")

#     try:
#         # Prepare some BLOBs to insert in the table
#         names = 'aramis', 'athos', 'porthos'
#         data = {}
#         for name in names:
#             datum = list(name)
#             datum.sort(  )
#             data[name] = cPickle.dumps(datum, 1)

#         # Perform the insertions
#         sql = "INSERT INTO justatest VALUES(%s, %s)"
#         for name in names:
#             cursor.execute(sql, (name, MySQLdb.escape_string(data[name])) )

#         # Recover the data so you can check back
#         sql = "SELECT name, ablob FROM justatest ORDER BY name"
#         cursor.execute(sql)
#         for name, blob in cursor.fetchall(  ):
#             print name, cPickle.loads(blob), cPickle.loads(data[name])
#     finally:
#         # Done. Remove the table and close the connection.
#         cursor.execute("DROP TABLE justatest")
#         connection.close(  )

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
