from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.staff_db import *
from portal.db_api.auth_db import *
from portal.db_api.subject_db import *
from portal.db_api.standard_db import *
from portal.db_api.batch_db import *
from portal.db_api.lecture_db import *
from portal.db_api.academic_year_db import *
from portal.models import *
def view_profile(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	details = get_staff(id=auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['details'] = details

	return render(request,'teacher/profile/view-profile.html', context)

def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	details = get_staff(id=auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['details'] = details

	return render(request, 'teacher/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/teacher/profile/view-profile')


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	return render(request,'teacher/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/teacher/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/teacher/profile/change-password/?message_error=Password Change Failed')

def logout(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	set_logout(request)
	return redirect('/')


def dashboard(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	context['details'] = auth_dict	



	# TODO Notices model yet to implement
	






	return render(request,'teacher/dashboard.html', context)


# Lectures Tab
@csrf_exempt
def add_lectures(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	if request.method == 'GET':
		context = {}
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		page_type = 0

		standards = get_standard()
		context['standards'] = standards

		if 'standard' in request.GET:
			page_type = 1
			subjects = get_subjects(standard_id=request.GET['standard'])
			context['subjects'] = subjects
			context['standard_id'] = int(request.GET['standard'])
			
			
			if 'subject' in request.GET:
				page_type = 2
				subject_year_object = SubjectYear.objects.get(subject = Subject.objects.get(id = request.GET['subject']))

				lectures = get_lecture(subject_year_id = subject_year_object.id)

				context['subject_id'] = int(request.GET['subject'])
				context['lectures'] = lectures
				
				if 'lecture' in request.GET:
					page_type = 3
					context['lecture_id'] = int(request.GET['lecture'])
					academic_year_id = get_current_academic_year()['id']
					context['batches']  = get_batch(academic_year_id = academic_year_id,standard_id = request.GET['standard'])
					
		
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/lectures/add-lectures.html', context)


	elif request.method == 'POST':
		try:
			lecture_id = request.POST['lecture']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_date = request.POST['lecture_date']
			lecture_duration = request.POST['lecture_duration']
			batch = request.POST['batch']
			staff_role_list = get_staff_role(staff_id = auth_dict['id'])
			staff_role_id_list = []
			for staff_role in staff_role_list:
				staff_role_id = staff_role['id']
				staff_role_id_list.append(staff_role_id)

			for staff_role_id in staff_role_id_list:
				set_lecture_batch(name=lecture_name, description=lecture_description, date = lecture_date, duration = lecture_duration,lecture_id = lecture_id,staff_role_id = staff_role_id,batch_id = batch)
			context['details'] = auth_dict
			return redirect('./?message=Lecture Added')
		except:
			return redirect('./?message_error=Error Adding Lecture')

@csrf_exempt


def view_lecture(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	if request.method == 'GET':
		context = {}

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		page_type = 0
		staff_role_list = get_staff_role(staff_id = auth_dict['id'])
		staff_role_id_list = []
		
		for staff_role in staff_role_list:
			staff_role_id = staff_role['id']
			staff_role_id_list.append(staff_role_id)
		lecturebatches = []
		for staff_role_id in staff_role_id_list:
			lecturebatch = get_lecture_batch(staff_role_id = staff_role_id)
			for i in lecturebatch:
				lecturebatches.append(i)
		context['lecturebatches'] = lecturebatches	
		if 'lecturebatch' in request.GET:
			page_type = 1
			context['lecturebatch'] = get_lecture_batch(id = request.GET['lecturebatch'])	
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/lectures/view-lecture.html', context)
	elif request.method == 'POST':
		
		id = request.POST['lecturebatch']
		lecturebatch_name = request.POST['lecturebatch_name']
		lecturebatch_description = request.POST['lecturebatch_description']
		lecturebatch_date = request.POST['lecturebatch_date']
		lecturebatch_duration = request.POST['lecturebatch_duration']

		set_lecture_batch(id=id, name = lecturebatch_name, description = lecturebatch_description, date = lecturebatch_date , duration = lecturebatch_duration)
		

		return redirect('./?message=Edited Lecture batch')	
