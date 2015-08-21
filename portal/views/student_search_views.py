# TODO Remove unnecessary imports

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


def home(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_manager'] == False and auth_dict['permission_accountant'] == False:
		raise Http404

	context['details'] = auth_dict
	page_type = 1

	if 'search' in request.GET:
		students = search_students(first_name=request.GET['first_name'], last_name=request.GET['last_name'], username=request.GET['username'], email=request.GET['email'], phone_number=request.GET['phone_number'])
		page_type = 0
		context['students'] = students

	elif 'student' in request.GET:
		students = get_student_batch_of_student(student_id=request.GET['student'])
		context['students'] = students
		page_type = 2

	context['page_type'] = page_type
	return render(request,'student_search/home.html', context)
