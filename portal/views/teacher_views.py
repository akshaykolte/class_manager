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
from portal.db_api.notice_db import *
from portal.db_api.test_db import *
from portal.models import *
from portal.db_api.attendance_reports_db import *
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
						lecturebatch = get_lecture_batch(staff_id=auth_dict['id'],batch_id = batch['id'],lecture_id = context['lecture_id'])
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

def view_attendance(request):
	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	if request.method == 'GET':
		context = {}

		context['branches'] = get_branch_of_teacher(teacher_id=auth_dict['id'])
		page_type = 1
		if 'branch' in request.GET:
			if 'lecture' in request.GET:
				page_type = 5
				context['report'] = attendance_report(lecture_id=request.GET['lecture'], branch_id=request.GET['branch'])
				print 'len=', len(context['report'][1][0])
				if len(context['report'])<1 or len(context['report'][1])<1 or len(context['report'][1][0]) <= 1:
					page_type = 6
					context['msg'] = 'No lectures added of the topic'
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
		context['details'] = auth_dict
		context['page_type'] = page_type
		return render(request, 'teacher/attendance/view_attendance.html', context)

@csrf_exempt
def add_student_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict


	if request.method == 'GET':

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

		return render(request,'teacher/notices/add-student-notice.html', context)

	elif request.method == 'POST':
		try:

			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_important)

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
				print "ddd"
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = None, batch_id = None, student_id = None, staff_id = None)
			elif int(request.POST['branch']) and not int(request.POST['batch']):
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = int(request.POST['branch']) , batch_id = None, student_id = None, staff_id = None)

			return redirect('./?message=Notice Uploaded')

		except:
			return redirect('./?message_error=Error While Uploading Notice')

'''
Not needed for teacher
@csrf_exempt
def add_staff_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict


	if request.method == 'GET':

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

				staff = get_staff(branch_id = int(request.GET['branch']))
				context['staff'] = staff

			else:
				page_type = 1

				#students = StudentBatch.objects.filter( batch__academic_year = AcademicYear.objects.get(id = get_current_academic_year()['id'] ))

				#context['students'] = students


		context['page_type'] = page_type

		return render(request,'teacher/notices/add-staff-notice.html', context)

	elif request.method == 'POST':
		try:

			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_important)
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

		except:
			return redirect('./?message_error=Error While Uploading Notice')'''

@csrf_exempt
def add_test_marks(request):
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
				print subject_year_dict

				branches = get_branch_of_teacher(auth_dict['id'])

				context['subject_id'] = int(request.GET['subject'])
				context['branches'] = branches

				if 'branch' in request.GET:
					page_type = 3
					context['branch_id'] = int(request.GET['branch'])
					batches =  get_batch(branch_id=request.GET['branch'], standard_id=request.GET['standard'])
					context['batches'] = batches

					if 'batch' in request.GET:
						page_type = 4
						context['batch_id'] = int(request.GET['batch'])
						context['tests'] = get_test(subject_year_id=request.GET['subject'], batch_id=request.GET['batch'], staff_id=auth_dict['id'])

						if 'test' in request.GET:
							if check_test_staff_permission(staff_id=auth_dict['id'], test_id=request.GET['test']):
								page_type = 5
								students = get_student_batch(batch_id=request.GET['batch'])
								context['test_id'] = request.GET['test']
								student_marks = get_student_batch_marks(test_id=request.GET['test'], batch_id=request.GET['batch'])
								student_marks_dict = {}
								for student_mark in student_marks:
									student_marks_dict[student_mark['student_batch_id']] = student_mark['obtained_marks']
								students_detailed = []
								for student in students:
									students_detailed.append(student)
									if student['id'] in student_marks_dict:
										students_detailed[-1]['marks'] = student_marks_dict[student['id']]
								context['students'] = students_detailed
							else:
								return Http404

		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'teacher/test/add_test_marks.html', context)

	elif request.method == 'POST':
		try:
			test_id = request.POST['test']
			batch_id = request.POST['batch']
			students = get_student_batch(batch_id=request.POST['batch'])
			for student in students:
				if str(student['id']) in request.POST:
					try:
						int(request.POST[str(student['id'])])
					except:
						continue
					set_student_marks(test_id=test_id, student_batch_id=student['id'], marks_obtained=request.POST[str(student['id'])])
			return redirect('./?message=Student marks added')
		except Exception as e:
			return redirect('./?message_error='+str(e))

def view_test_marks(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_teacher'] != True:
		raise Http404

	tests = get_test(staff_id=auth_dict['id'])
	context['tests'] = tests
	page_type = 0
	if 'test' in request.GET:
		page_type = 1
		branches = get_branch_of_teacher(auth_dict['id'])
		context['branches'] = branches
		context['standard'] = request.GET['standard']
		context['subject'] = request.GET['subject']
		context['test'] = request.GET['test']
		if 'branch' in request.GET:
			page_type = 2
			context['branch_id'] = int(request.GET['branch'])
			context['branch'] = request.GET['branch']
			batches =  get_batch(branch_id=request.GET['branch'], standard_id=request.GET['standard'])
			context['batches'] = batches
	context['page_type'] = page_type
	return render(request, 'teacher/test/view_test_marks.html', context)
