from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.student_db import *
from portal.db_api.auth_db import *
from portal.db_api.attendance_db import *
from portal.db_api.lecture_db import *
from portal.db_api.attendance_reports_db import *
from portal.db_api.notice_db import *


def dashboard(request):
	auth_dict = get_user(request)
	context ={}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404
	context['auth_dict'] = auth_dict
	parent_object = get_parent(id = auth_dict['id'])
	student_object = StudentParent.objects.get(parent = Parent.objects.get( id = parent_object['id'])).student
	#print student_object
	student_object = get_student_batch(student_id = student_object.id)
	lecture_list = []
	print student_object
	context['lectures'] = get_lecture_batch(batch_id = student_object['student_batch_id'])
	context['notices'] = get_personal_notices(student_id=auth_dict['id'])
	return render(request,'parent/dashboard.html', context)


def view_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	details = get_parent(id = auth_dict['id'])
	context['auth_dict'] = auth_dict
	context['details'] = details
	return render(request,'parent/profile/view-profile.html', context)



def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	details = get_parent(id = auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['staff_details'] = details

	return render(request, 'parent/profile/edit-profile.html', context)

def view_attendance(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	page_type = 1
	parent_object = get_parent(id = auth_dict['id'])
	student_object = StudentParent.objects.get(parent = Parent.objects.get( id = parent_object['id'])).student
	student_batch = get_student_batch(student_id=student_object.id)
	subjects = student_batch['student_subjects']
	context['subjects'] = subjects
	if 'attendance' in request.GET:
		page_type = 2
		subjects_id_list = []
		for subject in subjects:
			if str(subject['id']) in request.GET:
				subjects_id_list.append(subject['id'])
		context['report'] = attendance_report(student_id=student_batch['id'], subjects=subjects_id_list)
	context['page_type'] = page_type

	return render(request, 'parent/attendance/view_attendance.html', context)


@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	set_parent(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])
	
	return redirect('/parent/profile/view-profile')


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	return render(request,'parent/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/parent/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/parent/profile/change-password/?message_error=Password Change Failed')

