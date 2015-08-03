from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *
from portal.db_api.lecture_db import *

def dashboard(request):
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
