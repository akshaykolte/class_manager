from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.staff_db import *
from portal.db_api.auth_db import *

def dashboard(request):
	return render(request,'accountant/dashboard/dashboard.html')

def view_profile(request):
	auth_dict = get_user(request)
	if auth_dict['permission_accountant'] != True:
		raise Http404

	details = get_staff(id=auth_dict['id'])
	
	context = {'auth_dict':auth_dict, 'details':details}

	return render(request,'accountant/profile/view-profile.html', context)	
	
def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['permission_accountant'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	return render(request,'accountant/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['permission_accountant'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/accountant/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/accountant/profile/change-password/?message_error=Password Change Failed')	