from django.shortcuts import render,redirect
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from portal.db_api.auth_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.staff_db import *
from portal.db_api.branch_db import *
from portal.db_api.batch_db import *
from portal.db_api.fee_db import *
from portal.db_api.student_db import *
from portal.db_api.roles_db import *
from portal.db_api.notice_db import *
from portal.db_api.lecture_db import *
from portal.db_api.standard_db import *


def dashboard(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404
	
	return render(request,'admin/dashboard.html', context)


@csrf_exempt
def view_fees(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict
	branches = get_branch(id=None)
	context['branches'] = branches

	if request.method == 'GET':
	
		
		page_type = 0
		
		
		
		if 'branch' in request.GET:
			page_type = 1
			batches = get_batch(branch_id = int(request.GET.get('branch')))
			context['batches'] = batches
			context['branch_id'] = int(request.GET['branch'])
			#context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
			if 'batch' in request.GET:
				page_type = 2
				context['batch_id'] = int(request.GET['batch'])
				context['branch_id'] = int(request.GET['branch'])
				fee_details = get_batch_fees(batch_id =  int(request.GET['batch']))
				context['fee_details'] = fee_details
				
		context['page_type'] = page_type
		print context

		return render(request,'admin/fees/view-fees.html', context)

@csrf_exempt
def add_staff(request):
	context = {}
	
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		return render(request, 'admin/staff/add_staff.html', context)
	else:
		try:
			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			address = request.POST['address']
			email = request.POST['email']
			phone_number = request.POST['phone_number']
			gender = request.POST['gender']
			username = request.POST['username']
			password = request.POST['password']
			
			set_staff(username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			return redirect('./?message=Added Staff')
		except:
			return redirect('./?message_error=Error Adding Staff')

@csrf_exempt
def view_staff(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		page_type = 1
		if 'staff' in request.GET:
			page_type = 2
			staff = get_staff(id=request.GET['staff'])
			context['staff'] = staff
		context['page_type'] = page_type
		return render(request, 'admin/staff/view_staff.html', context)
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
			set_staff(id=id, username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			return redirect('./?message=Staff Saved')
		except:
			return redirect('./?message_error=Error saving staff')

@csrf_exempt
def set_current_academic_year_view(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		academic_year_list = get_academic_year()
		current_academic_year = get_current_academic_year()

		context['academic_years'] = academic_year_list
		context['current_academic_year'] = current_academic_year

		return render(request, 'admin/set_current_academic_year.html', context)
	elif request.method == 'POST':
		current_academic_year = request.POST['current_academic_year']
		set_current_academic_year(current_academic_year)
		return redirect('./?message=Current academic year changed.')

@csrf_exempt
def assign_roles(request):

	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	if request.method == 'GET':

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		page_type = 1
		if 'staff' in request.GET:
			page_type = 2
			staff_roles = get_staff_role(staff_id=request.GET['staff'])
			branch_permissions = {}
			branches = get_branch()
			branch_dict = {}
			for branch in branches:
				branch_permissions[branch['name']] = []
				branch_dict[branch['name']] = branch['id']
			for staff_role in staff_roles:
				branch_permissions[staff_role['branch_name']].append(staff_role['role'])
			table_display = []
			for index in branch_permissions:
				table_display.append([])
				table_display[-1].append(index)
				table_display[-1].append([[1,False, branch_dict[index]], [2,False, branch_dict[index]], [3,False, branch_dict[index]]])
				for perms in branch_permissions[index]:
					if perms == 'teacher':
						table_display[-1][1][0][1]=True
					if perms == 'accountant':
						table_display[-1][1][1][1]=True
					if perms == 'manager':
						table_display[-1][1][2][1]=True
			context['table_display'] = table_display
			context['staff'] = request.GET['staff']
		context['page_type'] = page_type

		return render(request, 'admin/staff/assign_roles.html', context)

	elif request.method == 'POST':
		try:
			role_name = {}
			role_name[1] = 'teacher'
			role_name[2] = 'accountant'
			role_name[3] = 'manager'
			branches = get_branch()
			for role_index in xrange(1, 4):
				for branch in branches:
					print 'checking for',str(role_index)+'_'+str(branch['id'])
					if str(role_index)+'_'+str(branch['id']) in request.POST:
						set_staff_role(role_id = get_role_by_name(role_name[role_index])['id'], staff_id = request.POST['staff'], branch_id=branch['id'])
			return redirect('./?message=Permissions modified')
		except:
			return redirect('./?message_error=Error modifying permission')



@csrf_exempt
def detailed_progress(request):

	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	branches = get_branch(id=None)
	context['branches'] = branches

	if request.method == 'GET':
		page_type = 0

		if 'branch' in request.GET:
			page_type = 1
			batches = get_batch(branch_id = int(request.GET['branch']))
			context['batches'] = batches
			context['branch_id'] = int(request.GET['branch'])
			if 'batch' in request.GET:
				page_type = 2
				context['batch_id'] = int(request.GET['batch'])
				context['branch_id'] = int(request.GET['branch'])
				lecture_batches = get_lecture_batch(batch_id = int(request.GET['batch']))

				for l_b in lecture_batches:
					if date.today() > l_b['date']:
						l_b['is_past'] = True
						l_b['difference'] = (date.today() - l_b['date']).days
					else:
						l_b['is_past'] = False
						l_b['difference'] = (l_b['date'] - date.today()).days

				context['lecture_batches'] = lecture_batches

		context['page_type'] = page_type


	return render(request, 'admin/track-progress/detailed-progress.html', context)


def graphical_overview(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_admin'] != True:
		return Http404

	context['standards'] = get_standard()
	if request.method == 'GET':
		page_type = 0

		if 'standard' in request.GET:
			page_type = 1
			context['standard_id'] = int(request.GET['standard'])
			batch_list = get_batch(academic_year_id=get_current_academic_year()['id'], standard_id=int(request.GET['standard']))
			context['batch_list'] = batch_list
			lecturebatch_list = []
			count_list = {}
			for batch in batch_list:
				lec_list = {}
				total_counter = 0
				done_counter = 0
				lecture_batch = {}
				lecture_batch['lec_bat'] = get_lecture_batch(batch_id=batch['id'])
				for i in lecture_batch['lec_bat']:
					batch_name = i['batch_name']
					branch_name = i['branch_name']
					
					if not i['lecture_name'] in lec_list:
						lec_list[i['lecture_name']] = {'total_counter':0, 'done_counter':0}
					
					total_counter += 1
					lec_list[i['lecture_name']]['total_counter'] += 1
					
					if i['is_done'] == 1:
						done_counter += 1
						lec_list[i['lecture_name']]['done_counter'] += 1

				lecture_batch['total_counter'] = total_counter
				lecture_batch['done_counter'] = done_counter
				lecture_batch['batch_name'] = batch_name
				lecture_batch['branch_name'] = branch_name
				lecture_batch['lec_list'] = lec_list
				for k,v in lec_list.items():
					if not k in count_list:
						count_list[k] = []

					count_list[k].append(v)

				lecturebatch_list.append(lecture_batch)
			context['lecturebatches'] = lecturebatch_list
			context['count_list'] = count_list
		
		context['page_type'] = page_type


	return render(request, 'admin/track-progress/graphical-overview.html', context)

@csrf_exempt
def add_student_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_admin'] != True:
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

		return render(request,'admin/notices/add-student-notice.html', context)

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
				#print "ddd"
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = None, batch_id = None, student_id = None, staff_id = None)
			elif int(request.POST['branch']) and not int(request.POST['batch']):
				upload_notice(id=None, notice_id = notice_id, for_students = True, for_staff = False, branch_id = int(request.POST['branch']) , batch_id = None, student_id = None, staff_id = None)

			return redirect('./?message=Notice Uploaded')

		except:
			return redirect('./?message_error=Error While Uploading Notice')


@csrf_exempt
def add_staff_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_admin'] != True:
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

		return render(request,'admin/notices/add-staff-notice.html', context)

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
			return redirect('./?message_error=Error While Uploading Notice')
