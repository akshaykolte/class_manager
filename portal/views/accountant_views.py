from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.staff_db import *
from portal.db_api.student_db import *
from portal.db_api.auth_db import *
from portal.db_api.fee_db import *

def dashboard(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context['details'] = auth_dict;


	return render(request,'accountant/dashboard.html', context)

def view_profile(request):
	auth_dict = get_user(request)
	context = {}
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])
	
	context['details'] = auth_dict;
	context['staff_details'] = staff_details

	return render(request,'accountant/profile/view-profile.html', context)	
	
def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	context['details'] = auth_dict;

	return render(request,'accountant/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404


	if auth_dict['permission_accountant'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/accountant/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/accountant/profile/change-password/?message_error=Password Change Failed')	


def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])
	
	context['details'] = auth_dict
	context['staff_details'] = staff_details

	return render(request, 'accountant/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/accountant/profile/view-profile')

def view_fees(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	fee_details = get_batch_fees(fee_type_name = 'payment')


	for i in fee_details:
		subject_years = StudentBatch.objects.get(id = i['student_id']).subject_years.all()
		basefees = get_base_fee(id = None , subject_years_list = subject_years)
		for basefee in basefees :
			i['base_fee'] = basefee.amount
	#print details
	context = {'details':auth_dict, 'fee_details':fee_details}

	return render(request,'accountant/fees/view-fees.html', context)	




@csrf_exempt
def make_transaction(request):
	'''
		Page Type					GET  (optional: 'msg')
				0					None
				1					student
				2					student, fee_type
				
		Post request for making transaction: /accountant/fees/make_transaction/
	'''
	
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_accountant'] != True:
		raise Http404
	context = {}
	context['details'] = auth_dict
	
	if request.method == 'GET':
		
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		
		page_type = 0
		
		students = get_students(id = None,batch_id = None,branch_id = None)
		context['students'] = students
		
		if 'student' in request.GET:
			page_type = 1
			fee_types = get_fee_types()
			context['fee_types'] = fee_types
			context['student_id'] = int(request.GET['student'])
			context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
			if 'fee_type' in request.GET:
				page_type = 2
				context['fee_type_id'] = int(request.GET['fee_type'])
		context['page_type'] = page_type

		return render(request,'accountant/fees/make-transaction.html', context)

	elif request.method == 'POST':
		try:
			student_batch = StudentBatch.objects.get(student = Student.objects.get(id = int(request.POST['student'])))
			student_batch_id = request.POST['student']
			
			fee_type_id = request.POST['fee_type']
			
			receipt_number = request.POST['receipt_number']
			
			amount = request.POST['amount']
			
			date = request.POST['date']
			
			time = request.POST['time']
			
			set_fee_transaction(id = None ,amount = amount, date = '2015-8-5', time = '19:45:07', receipt_number = receipt_number, student_batch_id = student_batch_id, fee_type_id = fee_type_id)
			
			return redirect('./?message=Transaction made')
		except:
			return redirect('./?message_error=Error. Transaction Failed.')



