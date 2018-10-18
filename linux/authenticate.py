import requests
import main

def login(username,password,server):
	'''
	Authenticates user
	'''
	url_login=server+"login/"
	print(url_login)
	client=requests.session()
	client.get(url_login)
	csrftoken = client.cookies['csrftoken']
	login_data = {'username':username,'password':password, 'csrfmiddlewaretoken':csrftoken}
	val=client.post(url_login, data=login_data)
	print(val)
	if(str(val.url)!=url_login):	#Exploiting redirection
		main.USER=username
		return True
	else:
		return False
