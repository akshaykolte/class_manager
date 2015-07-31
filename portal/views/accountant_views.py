from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.staff_db import *
from portal.db_api.auth_db import *

def dashboard(request):
	return render(request,'accountant/dashboard.html')

def view_profile(request):
	auth_dict = get_user(request)
	staff_dict = get_staff(id = auth_dict['id'])
	
	if auth_dict['logged_in'] and auth_dict['login_type'] == 'staff':
		context = {'staff_dict' : staff_dict,}
		print context
		return render(request,'accountant/view-profile.html', context)
	
	else:
		return render(request,'home.html',{'message':'Login failed'})	
	