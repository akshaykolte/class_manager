from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.student_db import *
from portal.db_api.auth_db import *
from portal.db_api.attendance_db import *
from portal.db_api.lecture_db import *
from portal.db_api.fee_db import *
from portal.db_api.attendance_reports_db import *
from portal.db_api.notice_db import *
from portal.db_api.test_db import *
import datetime
from datetime import date
from django.core.exceptions import *
from django.utils.datastructures import *
from portal.validator.validator import ModelValidateError
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.http import HttpResponse
import mimetypes
import os
import urllib


def respond_as_attachment(request):

	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404
	#context['notice_id'] = request.GET['notice']

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		file_path = 'media/' + request.GET.get('doc')
		print file_path

		fp = open(file_path, 'rb')
		response = HttpResponse(fp.read())
		fp.close()
		print os.path.basename(file_path)
		original_filename = os.path.basename(file_path)
		type, encoding = mimetypes.guess_type(original_filename)
		if type is None:
		    type = 'application/octet-stream'
		response['Content-Type'] = type
		response['Content-Length'] = str(os.stat(file_path).st_size)
		if encoding is not None:
		    response['Content-Encoding'] = encoding

		# To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
		if u'WebKit' in request.META['HTTP_USER_AGENT']:
		    # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
		    filename_header = 'filename=%s' % original_filename.encode('utf-8')
		elif u'MSIE' in request.META['HTTP_USER_AGENT']:
		    # IE does not support internationalized filename at all.
		    # It can only recognize internationalized URL, so we do the trick via routing rules.
		    filename_header = ''
		else:
		    # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
		    filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
		response['Content-Disposition'] = 'attachment; ' + filename_header
		return response


def dashboard(request):
	auth_dict = get_user(request)
	context ={}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404


	context['auth_dict'] = auth_dict

	# All Notices
	notices = get_personal_notices(student_id=auth_dict['id'], for_students =True)
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


	marks_list = get_student_batch_marks(student_batch_id = get_student_batch(student_id=auth_dict['id'])['id'])
	context['marks_list'] = marks_list

	return render(request,'student/dashboard.html', context)

def view_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404


	details = get_students(id = auth_dict['id'])
	context['auth_dict'] = auth_dict
	context['details'] = details
	return render(request,'student/profile/view-profile.html', context)



def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404


	details = get_students(id=auth_dict['id'])

	context['auth_dict'] =auth_dict
	context['staff_details'] = details

	return render(request, 'student/profile/edit-profile.html', context)

def view_attendance(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404


	page_type = 1
	student_batch = get_student_batch(student_id=auth_dict['id'])
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
	context['auth_dict'] = auth_dict
	return render(request, 'student/attendance/view_attendance.html', context)



def view_lectures(request):
	auth_dict = get_user(request)
	context ={}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404

	context['auth_dict'] = auth_dict
	student_object = get_student_batch(student_id = auth_dict['id'])
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
	return render(request,'student/lecture/view-lectures.html', context)





@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404


	set_student(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/student/profile/view-profile')


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']

	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']
	context['auth_dict'] = auth_dict

	return render(request,'student/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404

	if change_password_db(request):
		return redirect('/student/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/student/profile/change-password/?message_error=Password Change Failed')



#Fees-------------------------------------------------------------

def view_fees(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404

	context = {}
	context['details'] = auth_dict
	context['auth_dict'] = auth_dict
	if request.method == 'GET':
		try:
			page_type = 0

			fee_details = get_student_fees( student_id = auth_dict['id'] )
			transaction_details = get_fee_transaction(id = None ,date_start = None, date_end = None, student_id = auth_dict['id'], fee_type_id = None)
			#print fee_details
			context['fee_details'] = fee_details
			context['transaction_details'] = transaction_details

			context['page_type'] = page_type
			print context

			return render(request,'student/fees/view-fees.html', context)
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

def view_marks(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False or auth_dict['permission_student'] == False:
		raise Http404

	context = {}
	context['details'] = auth_dict
	context['auth_dict'] = auth_dict
	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		# Useless error handling: redirect loop, commented
		# try:

		page_type = 1
		marks_list = get_student_batch_marks(student_batch_id = get_student_batch(student_id=auth_dict['id'])['id'])
		context['page_type'] = page_type
		context['marks_list'] = marks_list
		return render(request,'student/test/view_marks.html', context)

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
