from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

# Create your models here.
class LoginManager(models.Manager):

	errors = False

	def register(self,**kwargs):
		Email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

		for entries in kwargs.values():
			if len(entries) < 1:
				errors = True
			else:
				errors = False
				pass
		if errors:
			context ={'errors': 'Fields Cannot Be Empty'}


		elif len(kwargs['first_name']) < 2:
			errors = True
			context ={'errors':'First Name Is Too Short'}

		elif len(kwargs['last_name']) < 2:
			errors = True
			context ={'errors':'Last Name Is Too Short'}

		elif not Email_regex.match(kwargs['email']):
			errors = True
			context ={'errors':'Invalid Email Address'}

		elif len(kwargs['password']) < 8:
			errors = True
			context ={'errors':'Password Is Too Short'}

		elif kwargs['password'] != kwargs['confirmpassword']:
			errors = True
			context ={'errors':'Passwords Must Match'}

		else:
			errors = False
			pw_hash = bcrypt.hashpw(str(kwargs['password']), bcrypt.gensalt(12))
			user = LoginReg.LoginMgr.create(first_name=kwargs['first_name'],last_name=kwargs['last_name'],emailaddress=kwargs['email'].lower(),password=pw_hash)
			user.save()
			context ={'user':user.id}

		return (errors, context)

		# Things to add:
		# 1. if user is already registered, do not allow registeration again. Check if email exists already.
		# 2. define a function to verify empty fields. Then function register and function login can call that function to check if entries are empty. If it returns True, then return to root page and display error message
		# 3. Why can't I define Email_regex globally in the class?
		# 4. Implement flash messages, but only show error messages on root page
		# 5. Add in birth. Check to make sure the date enter is before current entered date
		# 6. Develop a good 'break' test for this app



	def login(self, **kwargs):
		Email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

		for entries in kwargs.values():
			if len(entries) < 1:
				errors = True
			else:
				errors = False
				pass
		if errors:
			context ={'errors': 'Fields Cannot Be Empty'}


		elif not Email_regex.match(kwargs['email']):
			errors = True
			context ={'errors':'Email is invalid'}

		else:
			try:
				useremail = LoginReg.LoginMgr.get(emailaddress=kwargs['email'].lower())
				useremail.save()
			except:
				errors=True
				context ={'errors':'Email and/or Password is invalid'}
				return (errors, context)

			if useremail.id:
				#If email entry exists, check password
				if bcrypt.hashpw(str(kwargs['password']), str(useremail.password)) == useremail.password:
					errors=False
					context = {'user': useremail.id}
				else:
					errors = True
					context ={'errors':'Email and/or Password is invalid'}
				return (errors, context)
			else:
				errors=True
				context ={'errors':'Email and/or Password is invalid'}
			return (errors, context)


		return (errors, context)





class LoginReg(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	emailaddress = models.CharField(max_length=255)
	password = models.CharField(max_length=400)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	LoginMgr = LoginManager()

	class Meta:
		managed=False
		db_table ='users'



