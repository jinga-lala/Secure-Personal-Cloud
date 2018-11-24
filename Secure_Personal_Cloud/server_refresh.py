#! /usr/bin/python3
import time
from spcv1.models import encryption

while True:
	time.sleep(600)
	for obj in encryption.objects.all():
		if(abs(obj.dead_time_check - time.time()) > 300 ):
			print("Gotcha")
			obj.dead_time_check = time.time()
			obj.locked = 'N'
			obj.save()
