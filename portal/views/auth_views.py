from django.shortcuts import render,redirect
from portal.db_api.auth_db import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
	context = {}
	auth_dict = get_user(request)
	if auth_dict['logged_in']:
		context = {'logged_in':True,'message':'You are logged in'}
	return render(request,'home.html',context)

@csrf_exempt
def login(request):
	auth_dict = get_user(request)
	print auth_dict
	if auth_dict['logged_in']:
		if auth_dict['login_type'] == 'staff':
			if auth_dict['permission_admin'] == True:
				return redirect('/admin/dashboard/')

			elif auth_dict['permission_manager'] == True:
				return redirect('/manager/dashboard/')

			elif auth_dict['permission_teacher'] == True:
				return redirect('/teacher/dashboard/')

			elif auth_dict['permission_accountant'] == True:
				return redirect('/accountant/dashboard/dashboard')

		elif auth_dict['login_type'] == 'student':
			return redirect('/student/dashboard/')
		elif auth_dict['login_type'] == 'parent':
			return redirect('/parent/dashboard/')
	else:
		return render(request,'home.html', {'message':'Incorrect login details'})

def logout(request):
	set_logout(request)
	return redirect('/')

