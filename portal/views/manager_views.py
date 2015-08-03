from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *
from portal.db_api.auth_db import *
from portal.db_api.lecture_db import *
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