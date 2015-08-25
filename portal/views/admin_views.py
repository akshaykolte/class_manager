from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.auth_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.staff_db import *

def dashboard(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404
	
	return render(request,'admin/dashboard.html', context)

def batchwise_fees(request):
	# TODO: Kolte will complete
	pass

@csrf_exempt
def add_staff(request):
	context = {}
	
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		return render(request, 'admin/staff/add_staff.html', context)
	else:
		try:
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			address = request.POST['address']
			email = request.POST['email']
			phone_number = request.POST['phone_number']
			gender = request.POST['gender']
			username = request.POST['username']
			password = request.POST['password']
			
			set_staff(username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			return redirect('./?message=Added Staff')
		except:
			return redirect('./?message_error=Error Adding Staff')

def view_staff(request):
	pass

@csrf_exempt
def set_current_academic_year_view(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':

		context = {}
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		academic_year_list = get_academic_year()
		current_academic_year = get_current_academic_year()

		context['academic_years'] = academic_year_list
		context['current_academic_year'] = current_academic_year

		return render(request, 'admin/set_current_academic_year.html', context)
	elif request.method == 'POST':
		current_academic_year = request.POST['current_academic_year']
		set_current_academic_year(current_academic_year)
		return redirect('./?message=Current academic year changed.')

def assign_roles(request):
	pass
