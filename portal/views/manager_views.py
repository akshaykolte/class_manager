from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *
from portal.db_api.auth_db import *
from portal.db_api.branch_db import *
from portal.db_api.lecture_db import *
from portal.db_api.staff_db import *
from portal.db_api.roles_db import *
from django.http import Http404

def dashboard(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_manager'] != True:
		raise Http404

	return render(request,'manager/dashboard.html')

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

		return render(request,'manager/lectures/add_lectures.html', context)

	elif request.method == 'POST':
		try:
			subject_id = request.POST['subject']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']

			set_lecture(name=lecture_name, description=lecture_description, count=lecture_count, subject_year_id=subject_id)
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


		return render(request,'manager/lectures/view_lectures.html', context)

	elif request.method == 'POST':
		try:
			lecture_id = request.POST['lecture']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_count = request.POST['lecture_count']

			set_lecture(id=lecture_id, name=lecture_name, description=lecture_description, count=lecture_count)
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
			context['staffs'] = get_staff(role_name='teacher')
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
