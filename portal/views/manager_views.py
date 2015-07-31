from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *

def dashboard(request):
	return render(request,'manager/dashboard.html')

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
		if 'msg' in request.GET:
			context['msg'] = request.GET['msg']
		
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