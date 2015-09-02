from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.staff_db import *
from portal.db_api.auth_db import *
from portal.db_api.subject_db import *
from portal.db_api.standard_db import *
from portal.db_api.batch_db import *
from portal.db_api.lecture_db import *
from portal.db_api.branch_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.student_db import *
from portal.db_api.attendance_db import *
from portal.models import *
import datetime
from datetime import date
def view_profile(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	details = get_staff(id=auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['details'] = details

	return render(request,'teacher/profile/view-profile.html', context)

def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	details = get_staff(id=auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['details'] = details

	return render(request, 'teacher/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/teacher/profile/view-profile')


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	return render(request,'teacher/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/teacher/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/teacher/profile/change-password/?message_error=Password Change Failed')

def logout(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	set_logout(request)
	return redirect('/')


def dashboard(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	context['details'] = auth_dict	



	# TODO Notices model yet to implement
	






	return render(request,'teacher/dashboard.html', context)


# Lectures Tab
@csrf_exempt
def add_lectures(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
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
				print "hehrheheheheheh"
				page_type = 2
				subject_year_dict = get_subject_year(subject_id=request.GET['subject'])
				print subject_year_dict

				lectures = get_lecture(subject_year_id = subject_year_dict['id'])

				context['subject_id'] = int(request.GET['subject'])
				context['lectures'] = lectures
				
				if 'lecture' in request.GET:
					page_type = 3
					context['lecture_id'] = int(request.GET['lecture'])
					context['expected_count'] = get_lecture(id=context['lecture_id'])[0]['count']
					branches =  get_branch_of_teacher(teacher_id = auth_dict['id'])
					context['branches'] = branches
					academic_year_id = get_current_academic_year()['id']
					batch_list=[]
					for branch in branches:
						batch = get_batch(academic_year_id = academic_year_id,standard_id = request.GET['standard'],branch_id = branch['id'])
						for i in batch:
							batch_list.append(i)
					print batch_list
					context['batches'] = batch_list
		
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/lectures/add-lectures.html', context)


	elif request.method == 'POST':
		try:
			lecture_id = request.POST['lecture']
			lecture_name = request.POST['lecture_name']
			lecture_description = request.POST['lecture_description']
			lecture_date = request.POST['lecture_date']
			lecture_duration = request.POST['lecture_duration']
			batch = request.POST['batch']
			branch = get_batch(id = batch)
			staff_role_dict = get_staff_role(staff_id = auth_dict['id'], branch_id = branch['branch_id'], role_name='teacher')
			print staff_role_dict
			set_lecture_batch(name=lecture_name, description=lecture_description, date=datetime.datetime.strptime(lecture_date, "%Y-%m-%d").date() , duration = lecture_duration,lecture_id = lecture_id,staff_role_id = staff_role_dict['id'],batch_id = batch)
			context['details'] = auth_dict


			return redirect('./?message=Lecture Added')
		except Exception as e:
			print e
			return redirect('./?message_error=Error Adding Lecture')

@csrf_exempt


def view_lecture(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	if request.method == 'GET':
		context = {}

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		page_type = 0
		staff_role_list = get_staff_role(staff_id = auth_dict['id'])
		staff_role_id_list = []
		
		for staff_role in staff_role_list:
			staff_role_id = staff_role['id']
			staff_role_id_list.append(staff_role_id)
		lecturebatches = []
		for staff_role_id in staff_role_id_list:
			lecturebatch = get_lecture_batch(staff_role_id = staff_role_id)
			for l_b in lecturebatch:
					if date.today() > l_b['date']:
						l_b['is_past'] = True
						l_b['difference'] = (date.today() - l_b['date']).days
					else:
						l_b['is_past'] = False
						l_b['difference'] = (l_b['date'] - date.today()).days
			for i in lecturebatch:
				lecturebatches.append(i)
		context['lecturebatches'] = lecturebatches	
		if 'lecturebatch' in request.GET:
			page_type = 1
			lecturebatch = get_lecture_batch(id = request.GET['lecturebatch'])
			context['lecturebatch'] = lecturebatch
			context['cur_batch_id'] = lecturebatch['batch_id']
			context['is_done'] = lecturebatch['is_done']
			lecture_id = lecturebatch['lecture_id']
			lecture = get_lecture(id = lecture_id)
			standard_id = lecture[0]['standard_id']
			subject_year_id = lecture[0]['subject_year_id']
			lectures = get_lecture(subject_year_id = subject_year_id)
			context['lectures'] = lectures
			context['cur_lecture_id'] = lecturebatch['lecture_id']


			branches =  get_branch_of_teacher(teacher_id = auth_dict['id'])
			context['branches'] = branches
			academic_year_id = get_current_academic_year()['id']
			batch_list=[]
			for branch in branches:
				batch = get_batch(academic_year_id = academic_year_id,standard_id = standard_id,branch_id = branch['id'])
				for i in batch:
					batch_list.append(i)
					print batch_list
				context['batches'] = batch_list
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/lectures/view-lecture.html', context)
	elif request.method == 'POST':
		try:
		
			id = request.POST['lecturebatch']
			lecturebatch_name = request.POST['lecturebatch_name']
			lecturebatch_description = request.POST['lecturebatch_description']
			lecturebatch_date = request.POST['lecturebatch_date']
			lecturebatch_duration = request.POST['lecturebatch_duration']
			lecturebatch_batch = request.POST['batch']
			lecturebatch_lecture = request.POST['lecture']
			lecturebatch_is_done = request.POST['is_done']
			if lecturebatch_is_done == "True":
				lecturebatch_is_done = 1
			elif lecturebatch_is_done == "False":
				lecturebatch_is_done = 0

			set_lecture_batch(id=id, name = lecturebatch_name, description = lecturebatch_description, date = lecturebatch_date , duration = lecturebatch_duration,batch_id = lecturebatch_batch,lecture_id = lecturebatch_lecture, is_done=lecturebatch_is_done)
		
			print 'Hererere'
			return redirect('./?message=Edited Lecture batch')	
		except Exception as e:
			print 'sd', e
			return redirect('./?message_error=Error Editing Lecture')

@csrf_exempt
def add_attendance(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
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
				subject_year_dict = get_subject_year(subject_id=request.GET['subject'])

				lectures = get_lecture(subject_year_id = subject_year_dict['id'])

				context['subject_id'] = int(request.GET['subject'])
				context['lectures'] = lectures
				
				if 'lecture' in request.GET:
					page_type = 3
					context['lecture_id'] = int(request.GET['lecture'])
					context['expected_count'] = get_lecture(id=context['lecture_id'])[0]['count']
					branches =  get_branch_of_teacher(teacher_id = auth_dict['id'])
					context['branches'] = branches
					academic_year_id = get_current_academic_year()['id']
					batches=[]
					for branch in branches:
						batch = get_batch(academic_year_id = academic_year_id,standard_id = request.GET['standard'],branch_id = branch['id'])
						for i in batch:
							batches.append(i)
					context['batches'] = batches
					lecturebatches = []

					for batch in batches:
						lecturebatch = get_lecture_batch(batch_id = batch['id'],lecture_id = context['lecture_id'])
						for i in lecturebatch:
					 		lecturebatches.append(i)
					
					context['lecturebatches'] = lecturebatches
					
					batch_list = []
					for batch in batches:
						batch_dict={}
						batch_id = batch['id']
						students = get_students(batch_id = batch_id)
						batch_dict['batch'] = batch
						batch_dict['students'] = students
						batch_list.append(batch_dict)
						context['batch_list'] = batch_list
						
					'''if not batch_list:
						page_type = 2'''
					print "here123"
					if 'lecturebatch' in request.GET:
						print 'HERERE'
						print  request.GET['lecturebatch']
						page_type=4
						context['lecturebatch_id'] = int(request.GET['lecturebatch'])

						



		
		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/attendance/add-attendance.html', context)

	elif request.method == 'POST':
		
		try:
			standard = request.POST['standard']
			lecture = request.POST['lecture']
			lecturebatch = request.POST['lecturebatch']
			print lecturebatch
			print 'her234'
			academic_year_id = get_current_academic_year()['id']
			batches = get_batch(academic_year_id = academic_year_id,standard_id = standard)
			for batch in batches:
				students = get_students(batch_id = batch['id'])
				print 'heres'
				for student in students:
					if 'batch_'+str(batch['id'])+'student_'+str(student['id']) in request.POST:
						print '00here123'
						student_batch = get_student_batch(student_id = student['id'])
						print lecturebatch
						set_attendance(count = 1,student_batch_id = student_batch['id'],lecture_batch_id = lecturebatch)
						print 'here1'


			
			
					


			return redirect('./?message=Attendance Marked')
		except Exception as e:
			print 'sd', e
			return redirect('./?message_error=Error Marking Attendance')

