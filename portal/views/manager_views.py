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
from portal.db_api.attendance_reports_db import *
from portal.db_api.student_db import *
from django.http import Http404

def dashboard(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_manager'] != True:
		raise Http404
	context['details'] = auth_dict
	return render(request,'manager/dashboard.html', context)

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
				context['subject_id'] = int(request.GET['subject'])
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request,'manager/lectures/add_lectures.html', context)

	elif request.method == 'POST':
		try:
			subject_id = request.POST['subject']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']

			set_lecture(name=lecture_name, description=lecture_description, count=lecture_count, subject_year_id=subject_id)
			context['details'] = auth_dict
			return redirect('./?message=Lecture Added')
		except:
			return redirect('./?message_error=Error Adding Lecture')

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

	auth_dict = get_user(request)
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_manager'] != True:
		raise Http404

	
	if request.method == 'GET':
		context = {}
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		
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

	elif request.method == 'POST':
		try:
			lecture_id = request.POST['lecture']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']

			set_lecture(id=lecture_id, name=lecture_name, description=lecture_description, count=lecture_count)
			context['details'] = auth_dict
			return redirect('./?message=Lecture Edited')
		except:
			return redirect('./?message_error=Error Editing Lecture')

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
		page_type = 0
		context['page_type'] = page_type
		context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])
		context['details'] = auth_dict
		return render(request, 'manager/teacher/add_teacher.html', context)
	elif request.method == 'POST':
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
	elif request.method == 'POST':
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

	elif request.method == 'POST':
		try:
			test_name = request.POST['test_name']
			subject_id = request.POST['subject']
			test = set_test(name=test_name, subject_year_id=subject_id)

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
		except Exception as e:
			print 'sd', e
			return redirect('./?message_error=Error Adding Test')

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
		except:
			return redirect('./?message_error=Error Saving Test')

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
		context['branches'] = get_branch_of_manager(manager_id=auth_dict['id'])
		page_type = 1
		if 'branch' in request.GET:
			if 'lecture' in request.GET:
				page_type = 5
				context['report'] = attendance_report(lecture_id=request.GET['lecture'], branch_id=request.GET['branch'])
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
		page_type = 1

		if 'student' in request.GET:
			page_type = 2
			subject_years = get_student_batch(student_id=request.GET['student'])['student_subjects']
			context['student_id'] = request.GET['student']
			context['subjects'] = subject_years

			if 'report' in request.GET:
				page_type = 3
				subject_years = get_student_batch(student_id=request.GET['student'])['student_subjects']
				subjects = []
				for subject_year in subject_years:
					if str(subject_year['id']) in request.GET:
						subjects.append(subject_year['id'])
				context['report'] = attendance_report(student_id=request.GET['student'], subjects=subjects)

		context['page_type'] = page_type
		return render(request, 'manager/attendance_reports/studentwise_attendance.html', context)