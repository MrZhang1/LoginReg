from django.shortcuts import render, redirect, HttpResponse
from . import models
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request, 'loginreg/loginpage.html')

def login(request):
	if request.method == 'POST':

		#Register
		if request.POST['action'] == 'Register':

			# Validate user info. If everything is okay register user.
			user = models.LoginReg.LoginMgr.register(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], confirmpassword=request.POST['confirmpassword'])

			#If there are errors passed them to root page, else check if redirect to success page
			if user[0]:
				if 'errors' in user[1]:		#In case of KeyError	
					#print user[1]['errors']
					messages.error(request, user[1]['errors'])
			else:
				request.session['id'] = user[1]['user']
				messages.info(request, 'Successfully registered!')
				return redirect('/process/login/{}'.format(user[1]['user']))
			return redirect('/')


		#Login
		if request.POST['action'] == 'Login':

			#Validate user info. If everything is okay login user
			user = models.LoginReg.LoginMgr.login(email=request.POST['email'],password=request.POST['password'])

			# If there are errors pass them to root page, else redirect to success page
			print user

			if user[0]:
				if 'errors' in user[1]:		#In case of KeyError
					#print user[1]['errors']
					messages.error(request, user[1]['errors'])
				return redirect('/')
			else:
				request.session['id'] = user[1]['user']
				print user[1]['user']
				print type(user[1]['user'])
				messages.info(request, 'Successfully logged in!')
				return redirect('/process/login/{}'.format(user[1]['user']))

	else:
		return redirect('/')



def loginsuccess(request, id):
	if 'id' in request.session:
		if int(request.session['id']) == int(id):
			user = models.LoginReg.LoginMgr.get(id=id)
			return render(request, 'loginreg/loginsuccess.html', context={'user': user})
		else:
			pass
	else:
		return redirect('/')


def logout(request):
	request.session.flush()
	return redirect('/')


