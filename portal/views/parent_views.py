from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.student_db import *
from portal.db_api.auth_db import *
from portal.db_api.attendance_db import *
from portal.db_api.lecture_db import *
from portal.db_api.attendance_reports_db import *
from portal.db_api.notice_db import *
from portal.db_api.fee_db import *
from portal.db_api.test_db import *
import datetime
from datetime import date
from django.core.exceptions import *
from django.utils.datastructures import *
from portal.validator.validator import ModelValidateError


def dashboard(request):
	auth_dict = get_user(request)
	context ={}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404
	context['auth_dict'] = auth_dict
	parent_object = get_parent(id = auth_dict['id'])
	studentobject = StudentParent.objects.get(parent = Parent.objects.get( id = parent_object['id'])).student
	
	# All Notices
	notices = get_personal_notices(student_id=studentobject.id, for_students =True)
	context['notices'] = notices
	
	# Latest Maximum 10 Notices received in past 1 week. (Min(10, number of notices overall))
	# Only considering expiry date uptil now.
	# Later the expiry date, newer is document.
	# NOTE: This metric is not correct. Need to consider date/time of uploading,
	#       for which we will have to add timestamp of upload.
	notice_list = []
	for notice in notices:
		cur_notice = {}
		cur_notice['title'] = notice['title']
		cur_notice['description'] = notice['description']
		cur_notice['uploader'] = notice['uploader']
		cur_notice['important'] = notice['important']
		cur_notice['document'] = notice['document']
		cur_notice['expiry_date'] = notice['expiry_date']
		notice_list.append(cur_notice)
	
	sorted_notices = sorted(notice_list, reverse=True, key=lambda x: x['expiry_date'])
	context['latest_notices'] = sorted_notices[:min(len(sorted_notices) + 1, 10)]
	
	# All Upcoming lectures
	student_object = get_student_batch(student_id = auth_dict['id'])
	lecture_list = []
	lecturebatch = get_lecture_batch(batch_id = student_object['student_batch_id'])
	upcoming_lectures = []
	for l_b in lecturebatch:
			if date.today() > l_b['date']: # ignore past lectures
				pass
			else: # Adding only upcoming lectures
				l_b['is_past'] = False
				if (l_b['date'] - date.today()).days <= 7:
					upcoming_lectures.append(l_b)
	context['lectures'] = upcoming_lectures
	
	# 10 Latest lectures
	sorted_lectures = sorted(upcoming_lectures, key=lambda x: x['date'])
	latest_lectures = sorted_lectures[:min(len(sorted_lectures) + 1, 10)]
	context['latest_lectures'] = latest_lectures
	
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
	attendance_list = []
	for subject in subjects:
		subject_list = []
		subject_list.append(subject['id'])
		attendance_dict = {}
		attendance_dict['subject_name'] = subject['subject_name']
		attendance_dict['subject_id'] = subject['id']
		attendance_dict['attendance_report'] = attendance_report(student_id=student_batch['id'], subjects=subject_list)
		attendance_list.append(attendance_dict)
	context['report'] = attendance_list
	context['page_type'] = page_type

	return render(request, 'parent/attendance/view_attendance.html', context)



def view_lectures(request):
	auth_dict = get_user(request)
	context ={}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404
	context['auth_dict'] = auth_dict
	parent_object = get_parent(id = auth_dict['id'])
	studentobject = StudentParent.objects.get(parent = Parent.objects.get( id = parent_object['id'])).student
	student_object = get_student_batch(student_id = studentobject.id)
	lecture_list = []
	lecturebatch = get_lecture_batch(batch_id = student_object['student_batch_id'])
	past_lectures = []
	upcoming_lectures = []
	for l_b in lecturebatch:
			if date.today() > l_b['date']:
				l_b['is_past'] = True
				l_b['difference'] = (date.today() - l_b['date']).days
				past_lectures.append(l_b)
			else:
				l_b['is_past'] = False
				l_b['difference'] = (l_b['date'] - date.today()).days
				upcoming_lectures.append(l_b)
	context['past_lectures'] = past_lectures
	context['upcoming_lectures'] = upcoming_lectures
	return render(request,'parent/lecture/view-lectures.html', context)





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



def view_fees(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	student_id = get_student_of_parent(parent_id=auth_dict['id'])['id']

	context = {}
	context['details'] = auth_dict
	if request.method == 'GET':
		# try:
		page_type = 0

		fee_details = get_student_fees( student_id = student_id )
		transaction_details = get_fee_transaction(id = None ,date_start = None, date_end = None, student_id = student_id, fee_type_id = None)
		#print fee_details
		context['fee_details'] = fee_details
		context['transaction_details'] = transaction_details

		context['page_type'] = page_type
		print context

		return render(request,'parent/fees/view-fees.html', context)
		# except ModelValidateError, e:
		# 	return redirect('./?message_error='+str(e))
		# except ValueError, e:
		# 	return redirect('./?message_error='+str(PentaError(1000)))
		# except ObjectDoesNotExist, e:
		# 	return redirect('./?message_error='+str(PentaError(999)))
		# except MultiValueDictKeyError, e:
		# 	return redirect('./?message_error='+str(PentaError(998)))
		# except Exception, e:
		# 	return redirect('./?message_error='+str(PentaError(100)))

def view_marks(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_parent'] != True:
		raise Http404

	student_id = get_student_of_parent(parent_id=auth_dict['id'])['id']

	context = {}
	context['details'] = auth_dict

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		# Useless error handling: redirect loop, commented
		# try:

		page_type = 1
		marks_list = get_student_batch_marks(student_batch_id = get_student_batch(student_id=student_id)['id'])
		context['page_type'] = page_type
		context['marks_list'] = marks_list
		return render(request,'parent/test/view_marks.html', context)

		# except ModelValidateError, e:
		# 	return redirect('./?message_error='+str(e))
		# except ValueError, e:
		# 	return redirect('./?message_error='+str(PentaError(1000)))
		# except ObjectDoesNotExist, e:
		# 	return redirect('./?message_error='+str(PentaError(999)))
		# except MultiValueDictKeyError, e:
		# 	return redirect('./?message_error='+str(PentaError(998)))
		# except Exception, e:
		# 	return redirect('./?message_error='+str(PentaError(100)))
