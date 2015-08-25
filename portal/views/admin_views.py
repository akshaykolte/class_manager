from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.auth_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.staff_db import *
from portal.db_api.branch_db import *
from portal.db_api.batch_db import *
from portal.db_api.fee_db import *


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
	pass

def view_fees(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict
	branches = get_branch(id=None)
	context['branches'] = branches

	if request.method == 'GET':
	
		
		page_type = 0
		
		
		
		if 'branch' in request.GET:
			page_type = 1
			batches = get_batch(branch_id = int(request.GET['branch']))
			context['batches'] = batches
			context['branch_id'] = int(request.GET['branch'])
			#context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
			if 'batch' in request.GET:
				page_type = 2
				context['batch_id'] = int(request.GET['batch'])
				context['branch_id'] = int(request.GET['branch'])
				fee_details = get_batch_fees(batch_id =  int(request.GET['batch']))

				#print fee_details
				context = {'details':auth_dict, 'fee_details':fee_details, 'batches' : batches, 'branches' : branches}
				
		context['page_type'] = page_type
		print context

		return render(request,'admin/fees/view-fees.html', context)

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

@csrf_exempt
def view_staff(request):
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

		page_type = 1
		if 'staff' in request.GET:
			page_type = 2
			staff = get_staff(id=request.GET['staff'])
			context['staff'] = staff
		context['page_type'] = page_type
		return render(request, 'admin/staff/view_staff.html', context)
	elif request.method == 'POST':
		try:
			id = request.POST['staff']
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			address = request.POST['address']
			email = request.POST['email']
			phone_number = request.POST['phone_number']
			gender = request.POST['gender']
			username = request.POST['username']
			password = request.POST['password']
			set_staff(id=id, username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			return redirect('./?message=Staff Saved')
		except:
			return redirect('./?message_error=Error saving staff')

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
