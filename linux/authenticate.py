import requests
import main
import en_de
import json
def login(username,password,server,first=False):
	'''
	Authenticates user
	'''
	url_login=server+"login/"
	print(url_login)
	client=requests.session()
	client.get(url_login)
	csrftoken = client.cookies['csrftoken']
	login_data = {'username':username,'password':password, 'csrfmiddlewaretoken':csrftoken}
	# val=client.post(url_login, data=login_data)
	# client.close()
	
	login_data2 = {'username':username,'password':password}
	first_response = client.post(url_login,data=login_data, headers={'csrfmiddlewaretoken': csrftoken})
	print(first_response)
	client.close()

	get_token={'username':username, 'password':password}
	TOKEN =""

	# print(val)
	if(str(first_response.url)!=url_login):	#Exploiting redirection
		main.USER = username
		if(first):
			client = requests.session()
			APIurl = server+"encAPI/"+username+"/"
			l = client.get(APIurl)
			if(len(l.json())):
				en_de.get_schema()
			else:
				en_de.generate_schema()
				client = requests.session()
				APIurl = server+"encAPI/"+username+"/"
				l = client.post(APIurl)
		if (first):
			second_call = requests.post(server + "token-auth/", json=get_token)
			tok = second_call.json()
			TOKEN = tok['token']

			client2=requests.session()
			client2.get(server+"spc/token")
			csrftoken2 = client2.cookies['csrftoken']
			payload = {'user': username, 'token' : TOKEN , 'csrfmiddlewaretoken':csrftoken2}
			client2.post(server+"spc/token", data=payload)
		return True,TOKEN
	else:
		return False,TOKEN
