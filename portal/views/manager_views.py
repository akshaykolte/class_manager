from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *
from portal.db_api.auth_db import *
from portal.db_api.branch_db import *
from portal.db_api.lecture_db import *
from portal.db_api.staff_db import *
from portal.db_api.roles_db import *
from portal.db_api.test_db import *
from portal.db_api.batch_db import *
from portal.db_api.notice_db import *
from portal.db_api.attendance_reports_db import *
from portal.db_api.student_db import *
from django.core.exceptions import *
from django.utils.datastructures import *
from portal.validator.validator import ModelValidateError
from django.http import Http404

import datetime
from datetime import date
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

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
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
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context['details'] = auth_dict;
	context['notices'] = get_personal_notices(staff_id=auth_dict['id'], for_staff =True)

	return render(request,'manager/dashboard.html', context)


def view_profile(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']

	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	staff_details = get_staff(id=auth_dict['id'])

	context['details'] =auth_dict
	context['staff_details'] = staff_details

	return render(request,'manager/profile/view-profile.html', context)

def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])

	context['details'] =auth_dict
	context['staff_details'] = staff_details

	return render(request, 'manager/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	try:
		set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

		return redirect('/manager/profile/view-profile')
	except ModelValidateError, e:
		return redirect('../view-profile?message_error='+str(e))
	except ValueError, e:
		return redirect('../view-profile?message_error='+str(PentaError(1000)))
	except ObjectDoesNotExist, e:
		return redirect('../view-profile/?message_error='+str(PentaError(999)))
	except MultiValueDictKeyError, e:
		return redirect('../view-profile/?message_error='+str(PentaError(998)))
	except Exception, e:
		return redirect('../view-profile/?message_error='+str(PentaError(100)))

def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']

	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']
	context['details'] = auth_dict

	return render(request,'manager/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/manager/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/manager/profile/change-password/?message_error=Password Change Failed')

@csrf_exempt
def add_lectures(request):
	'''
		Page Type					GET  (optional: 'msg')
				0					None
				1					standard
				2					standard, subject

		Post request for adding the lecture: /manager/lectures/add_lectures/
	'''

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context = {}
	if request.method == 'GET':
		try:
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
					context['subject_id'] = int(request.GET['subject'])
			context['page_type'] = page_type
			context['details'] = auth_dict
			return render(request,'manager/lectures/add_lectures.html', context)
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

	elif request.method == 'POST':
		try:
			subject_id = request.POST['subject']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']
			set_lecture(name=lecture_name, description=lecture_description, count=lecture_count, subject_year_id=subject_id)
			context['details'] = auth_dict
			return redirect('./?message=Topic Added')
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

@csrf_exempt
def view_lectures(request):
	'''
		Page Type					GET  (optional: 'message')
				0					None
				1					standard
				2					standard, subject
				3					lecture edit
		Post request for editing the lecture: /manager/lectures/view_lectures/
	'''

	context = {}

	auth_dict = get_user(request)
	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404


	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = 0
			if 'standard' in request.GET:
				page_type += 1
			if 'subject' in request.GET:
				page_type += 2

			standards = get_standard()
			context['standards'] = standards

			if 'standard' in request.GET:
				page_type = 1
				subjects = get_subjects(standard_id=request.GET['standard'])
				context['subjects'] = subjects
				context['standard_id'] = int(request.GET['standard'])
				if 'subject' in request.GET:
					page_type = 2
					context['subject_id'] = int(request.GET['subject'])
					context['lectures'] = get_lecture(subject_year_id=context['subject_id'])
			elif 'lecture' in request.GET:
				page_type = 3
				context['lecture'] = get_lecture(id=request.GET['lecture'])

			context['page_type'] = page_type

			context['details'] = auth_dict

			return render(request,'manager/lectures/view_lectures.html', context)
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


	elif request.method == 'POST':
		try:
			lecture_id = request.POST['lecture']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']

			set_lecture(id=lecture_id, name=lecture_name, description=lecture_description, count=lecture_count)
			context['details'] = auth_dict
			return redirect('./?message=Topic Saved')
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

@csrf_exempt
def add_teacher(request):

	context = {}

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == 'GET':
		try:
			page_type = 0
			context['page_type'] = page_type
			context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])
			context['details'] = auth_dict
			return render(request, 'manager/teacher/add_teacher.html', context)
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

	elif request.method == 'POST':
		try:
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			address = request.POST['address']
			email = request.POST['email']
			phone_number = request.POST['phone_number']
			gender = request.POST['gender']
			username = request.POST['username']
			password = request.POST['password']

			branches = get_branch_of_manager(manager_id=auth_dict['id'])

			branch_list = []
			for branch in branches:
				if str(branch['id']) in request.POST:
					branch_list.append(branch['id'])

			staff_id = set_staff(username = username, password = password, first_name = first_name, last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender)

			for branch in branch_list:
				set_staff_role(role_id=get_role_by_name('teacher')['id'], staff_id=staff_id, branch_id=branch)

			return redirect("./?message=Added Teacher")
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


@csrf_exempt
def view_teacher(request):
	context = {}

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = 0
			if not 'staff' in request.GET:
				page_type = 0
				context['staffs'] = get_staff(role_name='teacher')		# TODO: think about displaying staff of all roles rather than just teacher
			elif 'staff' in request.GET:
				page_type = 1
				context['staff'] = get_staff(id=request.GET['staff'])
				context['branches'] = [[],[]]
				context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])
				staff_teacher_roles = get_staff_role(role_id=get_role_by_name('teacher')['id'], staff_id=request.GET['staff'])
				ids = []
				for i in staff_teacher_roles:
					ids.append(i['branch_id'])
				for i in range(len(context['branches'])):
					if context['branches'][i]['id'] in ids:
						context['branches'][i] = [context['branches'][i], 'T']
					else:
						context['branches'][i] = [context['branches'][i], 'F']

			context['page_type'] = page_type
			context['details'] = auth_dict
			return render(request, 'manager/teacher/view_teacher.html', context)
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

			staff_id = set_staff(id=id, username = username, password = password, first_name = first_name, last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender)

			branches = get_branch_of_manager(manager_id=auth_dict['id'])

			for branch in branches:
				if str(branch['id']) in request.POST:
					# create a branch role for teacher role if doesnt exists
					set_staff_role(role_id = get_role_by_name('teacher')['id'],staff_id = id,branch_id = branch['id'])
				else:
					# delete a branch role for teacher role
					delete_staff_role(staff=id, role=get_role_by_name('teacher')['id'], branch = branch['id'])

			return redirect('./?message=Edited Staff')
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

@csrf_exempt
def add_tests(request):
	context = {}

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = -1
			if not 'standard' in request.GET:
				page_type = 0
				context['standards'] = get_standard()
			elif not 'subject' in request.GET:
				page_type = 1
				context['standards'] = get_standard()
				context['standard_id'] = int(request.GET['standard'])
				context['subjects'] = get_subjects(standard_id=request.GET['standard'])
			else:
				page_type = 2
				context['standards'] = get_standard()
				context['standard_id'] = int(request.GET['standard'])
				context['subjects'] = get_subjects(standard_id=request.GET['standard'])
				context['subject_id'] = int(request.GET['subject'])
				branches = get_branch_of_manager(manager_id=auth_dict['id'])
				batches = []
				for branch in branches:
					batches += get_batch(branch_id=branch['id'], standard_id = request.GET['standard'])
				context['batches'] = batches

				teachers = []
				for branch in branches:
					teachers += get_staff(role_name='teacher', branch_id=branch['id'])

				context['teachers'] = teachers

			context['page_type'] = page_type
			context['details'] = auth_dict
			return render(request,'manager/tests/add_tests.html', context)

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

	elif request.method == 'POST':
		try:
			test_name = request.POST['test_name']
			test_marks = request.POST['test_marks']
			subject_id = request.POST['subject']
			print "here"
			test = set_test(name=test_name, marks=test_marks, subject_year_id=subject_id)
			branches = get_branch_of_manager(manager_id=auth_dict['id'])
			batches = []
			for branch in branches:
				batches += get_batch(branch_id=branch['id'], standard_id=request.POST['standard'])

			print batches
			for batch in batches:
				if 'batch_'+str(batch['id']) in request.POST:
					set_test_of_batch(test_id=test, batch_id=batch['id'])

			teachers = []
			for branch in branches:
				teachers += get_staff(role_name='teacher', branch_id=branch['id'])

			'''
				To make sure the manager doesn't assign test to teacher outside his/her branches
			'''
			for teacher in teachers:
				if 'teacher_'+str(teacher['id']) in request.POST:
					staff_role_id = None
					for branch in branches:
						staff_role_list = get_staff_role(role_id = get_role_by_name('teacher')['id'], staff_id=teacher['id'], branch_id = branch['id'])
						if len(staff_role_list) == 1:
							set_test_of_staff_role(test_id=test, staff_role_id = staff_role_list[0]['id'])
							break


			return redirect('./?message=Test Added')
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

@csrf_exempt
def view_tests(request):
	context = {}

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = -1

			if 'test' in request.GET:
				page_type = 3
				context['test'] = get_test(id=request.GET['test'])
				branches = get_branch_of_manager(manager_id=auth_dict['id'])
				batches = []
				test_batches_list = get_batches_of_test(test_id=request.GET['test'])
				test_batches = []
				for test_i in test_batches_list:
					test_batches.append(test_i['batch_id'])
				for branch in branches:
					batches += get_batch(branch_id=branch['id'], standard_id = context['test']['standard_id'])

				for i in xrange(len(batches)):
					if batches[i]['id'] in test_batches:
						batches[i]['check'] = True
				context['batches'] = batches

				teachers = []
				test_teachers_list = get_teachers_of_test(test_id=request.GET['test'])
				test_teachers = []
				for test_i in test_teachers_list:
					test_teachers.append(test_i['staff_id'])
				for branch in branches:
					teachers += get_staff(role_name='teacher', branch_id=branch['id'])

				for i in xrange(len(teachers)):
					if teachers[i]['id'] in test_teachers:
						teachers[i]['check'] = True

				context['teachers'] = teachers

			elif not 'standard' in request.GET:
				page_type = 0
				context['standards'] = get_standard()
			elif not 'subject' in request.GET:
				page_type = 1
				context['standards'] = get_standard()
				context['standard_id'] = int(request.GET['standard'])
				context['subjects'] = get_subjects(standard_id=request.GET['standard'])
			else:
				page_type = 2
				context['standards'] = get_standard()
				context['standard_id'] = int(request.GET['standard'])
				context['subjects'] = get_subjects(standard_id=request.GET['standard'])
				context['subject_id'] = int(request.GET['subject'])

				context['tests'] = get_test(subject_year_id = request.GET['subject'])

			context['page_type'] = page_type
			context['details'] = auth_dict
			return render(request,'manager/tests/view_tests.html', context)

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


	elif request.method == 'POST':
		try:
			test_name = request.POST['test_name']
			test_id = request.POST['test']

			# save test name
			test = set_test(id=test_id, name=test_name)


			branches = get_branch_of_manager(manager_id=auth_dict['id'])
			batches = []
			for branch in branches:
				batches += get_batch(branch_id=branch['id'], standard_id = get_test(id=test_id)['standard_id'])

			for batch in batches:
				if 'batch_'+str(batch['id']) in request.POST:
					# save test and batch
					try:
						set_test_of_batch(test_id=test_id, batch_id=batch['id'])
					except:
						pass
				else:
					# delete test and batch
					delete_test_of_batch(test_id=test_id, batch_id=batch['id'])

			teachers = []
			for branch in branches:
				teachers += get_staff(role_name='teacher', branch_id=branch['id'])

			'''
				To make sure the manager doesn't assign test to teacher outside his/her branches
			'''
			for teacher in teachers:
				if 'teacher_'+str(teacher['id']) in request.POST:
					staff_role_id = None
					for branch in branches:
						staff_role_list = get_staff_role(role_id = get_role_by_name('teacher')['id'], staff_id=teacher['id'], branch_id = branch['id'])
						if len(staff_role_list) == 1:
							try:
								set_test_of_staff_role(test_id=test, staff_role_id = staff_role_list[0]['id'])
							except:
								pass
							break
				else:
					delete_test_of_staff_role(test_id=test_id, staff_id=teacher['id'])


			return redirect('./?message=Test Saved')
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

def lecturewise_attendance(request):

	# TODO: add checking of permission of branch to manager
	context = {}

	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == "GET":
		try:
			context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])
			page_type = 1
			if 'branch' in request.GET:
				if 'lecture' in request.GET:
					page_type = 5

					# old_table is a magic variable :P
					# change it to True to show a detailed view of the attendance
					# less work, much wow ;)
					old_table = False

					if 'detailed' in request.GET and request.GET['detailed'] == 'True':
						old_table = True

					context['report'] = attendance_report(lecture_id=request.GET['lecture'], branch_id=request.GET['branch'], old_table=old_table)
					print 'len=', len(context['report'][1][0])
					if len(context['report'])<1 or len(context['report'][1])<1 or len(context['report'][1][0]) <= 1:
						page_type = 6
						context['msg'] = 'No lectures added of the topic'
					context['old_table'] = old_table
					context['branch'] = request.GET['branch']
					context['lecture'] = request.GET['lecture']

				else:
					page_type = 2
					context['standards'] = get_standard()
					context['branch_id'] = int(request.GET['branch'])
					if 'standard' in request.GET:
						page_type = 3
						context['standard_id'] = int(request.GET['standard'])
						context['subjects'] = get_subjects(standard_id=request.GET['standard'])
						if 'subject' in request.GET:
							page_type = 4
							context['lectures'] = get_lecture(subject_year_id=request.GET['subject'])

			context['page_type'] = page_type
			return render(request, 'manager/attendance_reports/lecturewise_attendance.html', context)

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

def studentwise_attendance(request):

	'''
			TODO: important: fix the UX for selecting student id and then selecting subjects
	'''
	context = {}

	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == "GET":
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = 1

			if 'student' in request.GET:
				print request.GET
				page_type = 2
				subject_years = get_student_batch(student_id=request.GET['student'])['student_subjects']
				context['student_id'] = request.GET['student']
				context['student_name'] = request.GET['name']
				context['subjects'] = subject_years

				report_list = []
				page_type = 3
				subject_years = get_student_batch(student_id=request.GET['student'])['student_subjects']
				subjects = []
				student_batch_id = get_student_batch(student_id=request.GET['student'])['id']
				for subject_year in subject_years:
					subject_list = []
					subject_list.append(subject_year['id'])
					attendance_dict = {}
					attendance_dict['subject_name'] = subject_year['subject_name']
					attendance_dict['subject_id'] = subject_year['id']
					attendance_dict['attendance_report'] = attendance_report(student_id=student_batch_id, subjects=subject_list)
					report_list.append(attendance_dict)

				context['report'] = report_list
			context['page_type'] = page_type
			return render(request, 'manager/attendance_reports/studentwise_attendance.html', context)

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

def batchwise_attendance(request):

	context = {}

	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if request.method == "GET":
		try:
			page_type = 1
			context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])

			if 'batch' in request.GET:
				page_type = 4
				context['report'] = attendance_report(batch_id=request.GET['batch'])
			elif 'branch' in request.GET:
				page_type = 2
				context['branch_id'] = int(request.GET['branch'])
				context['standards'] = get_standard()

				if 'standard' in request.GET:
					page_type = 3
					context['standard_id'] = int(request.GET['standard'])
					context['batches'] = get_batch(branch_id=request.GET['branch'], standard_id=request.GET['standard'])

			context['page_type'] = page_type
			return render(request, 'manager/attendance_reports/batchwise_attendance.html', context)
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

@csrf_exempt
def add_batch(request):
	context = {}

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context['details'] = auth_dict
	if request.method == 'GET':
		try:
			page_type = 1
			context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])

			if 'branch' in request.GET:
				page_type = 2
				standards = get_standard()
				context['standards'] = standards
				context['branch_id'] = int(request.GET['branch'])

				if 'standard' in request.GET:
					page_type = 3
					context['standard_id'] = int(request.GET['standard'])

			context['page_type'] = page_type
			return render(request, 'manager/batches/add_batch.html', context)
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

	elif request.method == 'POST':
		try:
			# TODO: Check for permission of manager to branch
			set_batch(branch_id=request.POST['branch'], academic_year_id=get_current_academic_year()['id'], standard_id=request.POST['standard'], name=request.POST['batch_name'], description=request.POST['batch_description'])
			return redirect('./?message=Batch Added')
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

@csrf_exempt
def view_batch(request):
	context = {}

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context['details'] = auth_dict
	if request.method == 'GET':
		try:
			page_type = 1
			context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])

			if 'batch' in request.GET:
				page_type = 4
				# TODO check permission of manager to batch
				context['batch'] = get_batch(id=request.GET['batch'])
			elif 'branch' in request.GET:
				page_type = 2
				standards = get_standard()
				context['standards'] = standards
				context['branch_id'] = int(request.GET['branch'])

				if 'standard' in request.GET:
					page_type = 3
					context['standard_id'] = int(request.GET['standard'])
					# TODO check for permission of manager to the branch
					context['batches'] = get_batch(branch_id=request.GET['branch'], standard_id=request.GET['standard'])

			context['page_type'] = page_type
			return render(request, 'manager/batches/view_batch.html', context)
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

	elif request.method == 'POST':
		try:
			# TODO: Check for permission of manager to batch
			set_batch(id=request.POST['batch'], name=request.POST['name'], description=request.POST['description'])
			return redirect('./?message=Batch Saved')
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


@csrf_exempt
def add_student_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict


	if request.method == 'GET':
		try:
			if 'message' in request.GET:
				context['message'] = request.GET['message']
			elif 'message_error' in request.GET:
				context['message_error'] = request.GET['message_error']

			page_type = 0
			branches = get_branch(id=None)
			all_branch={}
			all_branch['name'] = "All Branches"
			all_branch['id'] = 0
			all_branches = []
			all_branches.append(all_branch)
			context['branches'] = all_branches + branches

			if 'branch' in request.GET:



				context['branch_id'] = int(request.GET['branch'])
				if int(request.GET['branch']) :
					page_type = 1
					batches = get_batch(branch_id = int(request.GET['branch']))
					all_batch={}
					all_batch['name'] = "All Batches"
					all_batch['id'] = 0
					all_batch['description'] = "All batches of that branch"
					all_batch['academic_year'] = "current_academic_year"
					all_batch['branch'] = get_branch(id = int(request.GET['branch']))['name']
					all_batch['standard'] = "All standards"
					all_batches = []
					all_batches.append(all_batch)
					context['batches'] = all_batches + batches



					if 'batch' in request.GET:

						context['batch_id'] = int(request.GET['batch'])

						if int(request.GET['batch']) :
							page_type = 2

							students = get_students(id = None,batch_id = int(request.GET['batch']))
							context['students'] = students
						else :
							page_type = 2
							#students = StudentBatch.objects.filter( batch__branch = Branch.objects.get(id = int(request.GET['branch']) ))
							#context['students'] = students
				else:
					page_type = 2

					#students = StudentBatch.objects.filter( batch__academic_year = AcademicYear.objects.get(id = get_current_academic_year()['id'] ))

					#context['students'] = students
					pass

			context['page_type'] = page_type

			return render(request,'manager/notices/add-student-notice.html', context)

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

	elif request.method == 'POST':
		try:

			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1

			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']
			
			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_imp, document = document)

			if int(request.POST['branch']):
				if int(request.POST['batch']):
					students = get_students(id = None,batch_id = int(request.POST['batch']))
					student_list = []

					for student in students:
						#print student
						#print 'student_'+str(student['id']) in request.POST
						if 'student_'+str(student['id']) in request.POST:
							#print subject_year
							upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = None, batch_id = None, student_id = student['id'], staff_id = None)





			if not int(request.POST['branch']) :
				#print "ddd"
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = None, batch_id = None, student_id = None, staff_id = None)
			elif int(request.POST['branch']) and not int(request.POST['batch']):
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = int(request.POST['branch']) , batch_id = None, student_id = None, staff_id = None)

			return redirect('./?message=Notice Uploaded')

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


@csrf_exempt
def add_staff_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict


	if request.method == 'GET':

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = 0
			branches = get_branch(id=None)
			all_branch={}
			all_branch['name'] = "All Branches"
			all_branch['id'] = 0
			all_branches = []
			all_branches.append(all_branch)
			context['branches'] = all_branches + branches

			if 'branch' in request.GET:



				context['branch_id'] = int(request.GET['branch'])
				if int(request.GET['branch']) :
					page_type = 1

					staff = get_staff(branch_id = int(request.GET['branch']))
					context['staff'] = staff

				else:
					page_type = 1

					#students = StudentBatch.objects.filter( batch__academic_year = AcademicYear.objects.get(id = get_current_academic_year()['id'] ))

					#context['students'] = students


			context['page_type'] = page_type

			return render(request,'manager/notices/add-staff-notice.html', context)

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

	elif request.method == 'POST':
		try:

			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1

			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_imp, document = document)
			print int(request.POST['branch'])
			if int(request.POST['branch']):

				staff = get_staff(branch_id = int(request.POST['branch']))
				staff_list = []

				for staff_object in staff:


					if 'staff_'+str(staff_object['id']) in request.POST:
						#print subject_year
						upload_notice(id=None, notice_id = notice_id, for_students = False, for_staff = True, branch_id = None, batch_id = None, student_id = None, staff_id = staff_object['id'])





			if not int(request.POST['branch']) :
				#print "ddd"
				upload_notice(id=None, notice_id = notice_id, for_students = False, for_staff = True, branch_id = None, batch_id = None, student_id = None, staff_id = None)



			return redirect('./?message=Notice Uploaded')

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

@csrf_exempt
def view_my_notices(request):
	context = {}
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	context['details'] = auth_dict
	auth_dict
	notices = Notice.objects.filter(uploader = Staff.objects.get(id=auth_dict['id']))
	context['notices'] = notices



	return render(request,'manager/notices/view-my-notices.html', context)

@csrf_exempt
def edit_my_notice(request):
	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_manager'] != True:
		raise Http404
	#context['notice_id'] = request.GET['notice']

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			notice = get_personal_notices(notice_id =(request.GET.get('notice')))
			context['notice'] = notice
			# date_string = notice['expiry_date'].split('-')
			context['notice_id'] = (request.GET.get('notice'))


			return render(request, 'manager/notices/edit-my-notice.html', context)
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


	elif request.method == 'POST':
		try:
			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None
				
			set_notice(id = request.POST['notice_id'], title = request.POST['title'], description = request.POST['description'], uploader_id = auth_dict['id'] , expiry_date = request.POST['expiry-date'], important = is_imp, document = document)

			return redirect('/manager/notices/view-my-notices/?message=Notice edited')
		except ModelValidateError, e:
			return redirect('../view-my-notices?message_error='+str(e))
		except ValueError, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(100)))
