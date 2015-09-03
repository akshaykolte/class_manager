from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.staff_db import *
from portal.db_api.student_db import *
from portal.db_api.auth_db import *
from portal.db_api.fee_db import *
from portal.db_api.branch_db import *
from portal.db_api.batch_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.standard_db import *
from portal.db_api.subject_db import *
from portal.db_api.notice_db import *
from portal.models import Notice


def dashboard(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context['details'] = auth_dict;
	context['notices'] = get_personal_notices(staff_id=auth_dict['id'], for_staff =True)

	return render(request,'accountant/dashboard.html', context)

def view_profile(request):
	auth_dict = get_user(request)
	context = {}
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])
	
	context['details'] = auth_dict;
	context['staff_details'] = staff_details

	return render(request,'accountant/profile/view-profile.html', context)	
	
def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	context['details'] = auth_dict;

	return render(request,'accountant/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404


	if auth_dict['permission_accountant'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/accountant/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/accountant/profile/change-password/?message_error=Password Change Failed')	


def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])
	
	context['details'] = auth_dict
	context['staff_details'] = staff_details

	return render(request, 'accountant/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/accountant/profile/view-profile')

def view_fees(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict
	

	if request.method == 'GET':
	
		
		page_type = 0
		
		
		
		if 'student' in request.GET:
			page_type = 1
			
			context['student_id'] = int(request.GET['student'])
			context['student_name'] = request.GET['name']

			fee_details = get_student_fees( student_id = int(request.GET['student']) )
			transaction_details = get_fee_transaction(id = None ,date_start = None, date_end = None, receipt_number = None, student_id = int(request.GET['student']), fee_type_id = None)
		

				
				
			#print fee_details
			context['fee_details'] = fee_details
			context['transaction_details'] = transaction_details
				
		context['page_type'] = page_type
		print context

		return render(request,'accountant/fees/view-fees.html', context)
	

@csrf_exempt
def add_base_fees(request):
	
	
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_accountant'] != True:
		raise Http404
	
	context = {}
	context['details'] = auth_dict
	

	if request.method == 'GET':
		
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		
		page_type = 0
		academic_years = get_academic_year(id=None)
		context['academic_years'] = academic_years

		if 'academic_year' in request.GET:
			page_type = 1
			standards = get_standard(id=None)
			context['standards'] = standards
			context['academic_year_id'] = int(request.GET['academic_year'])
			#context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
			if 'standard' in request.GET:
				page_type = 2
				context['standard_id'] = int(request.GET['standard'])

				subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.GET['standard']), academic_year_id=int(request.GET['academic_year']), subject_year_id=None)
				context['subject_years'] = subject_years
				
			

		context['page_type'] = page_type

		return render(request,'accountant/fees/add-base-fees.html', context)

	elif request.method == 'POST':
		try:
			
			amount = request.POST['amount']
			subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.POST['standard']), academic_year_id=int(request.POST['academic_year']), subject_year_id=None)
			subject_year_list = []
			for subject_year in subject_years:
				if 'subject_year_'+str(subject_year['id']) in request.POST:
					#print subject_year
					subject_year_list.append(subject_year['id'])

			set_base_fee(amount=amount , subject_years_list = subject_year_list)
			return redirect('./?message=Base Fee Set')
		except:
			return redirect('./?message_error=Error. Transaction Failed.')



@csrf_exempt
def view_base_fees(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	context = {}
	context['details'] = auth_dict
	

	
	if request.method == 'GET':
		
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		
		page_type = 0
		academic_years = get_academic_year(id=None)
		context['academic_years'] = academic_years

		if 'academic_year' in request.GET:
			page_type = 1
			standards = get_standard(id=None)
			context['standards'] = standards
			context['academic_year_id'] = int(request.GET['academic_year'])
			#context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
			if 'standard' in request.GET:
				page_type = 2
				context['standard_id'] = int(request.GET['standard'])

				base_fees = get_base_fee(id = None , subject_years_list = None,  academic_year_id=int(request.GET['academic_year']), standard_id=int(request.GET['standard']))
				context['base_fees'] = base_fees
				
			

		context['page_type'] = page_type

		return render(request,'accountant/fees/view-base-fees.html', context)

@csrf_exempt
def edit_base_fees(request):
	auth_dict = get_user(request)
	context = {}


	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	
	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		base_fees = get_base_fee(id = (request.GET.get('base-fee')) , subject_years_list = None,  academic_year_id=None, standard_id=None)
		context['academic_year_id'] = request.GET.get('academic_year')
		context['standard_id'] = request.GET.get('standard')
		context['base_fees'] = base_fees
		context['details'] = auth_dict
		return render(request, 'accountant/fees/edit-base-fee.html', context)

	elif request.method == 'POST':
		try:
			print "dfdsfsdf"
			set_base_fee(id = (request.POST.get('base-fee')), amount=request.POST['amount'] , subject_years_list = None)  
			print "dfdsfsdf"
			return redirect('/accountant/fees/edit-base-fees/?academic_year='+str((request.POST.get('academic_year_id')))+'&standard='+str((request.POST.get('standard_id')))+'&base-fee='+str((request.POST.get('base-fee')))+'&message=Transaction made')
		except:
			return redirect('./?message_error=Error. Transaction Failed.')
				


'''@csrf_exempt
def edit_base_fees_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	set_base_fee(id = request.POST['base-fee'] , amount=request.POST['amount'] , subject_years_list = None)  

	return redirect('/accountant/fees/view-base-fees.html')	'''	

	


@csrf_exempt
def make_transaction(request):
	'''
		Page Type					GET  (optional: 'msg')
				0					None
				1					student
				2					student, fee_type
				
		Post request for making transaction: /accountant/fees/make_transaction/
	'''
	
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_accountant'] != True:
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
		context['branches'] = branches

		if 'student_batch' in request.GET:
			page_type = 1
			context['student_batch_id'] = request.GET['student_batch']
			context['student_name'] = request.GET['student_name']
				
			fee_types = get_fee_types()
			context['fee_types'] = fee_types
			if 'fee_type' in request.GET:
				page_type = 2
				context['fee_type_id'] = int(request.GET['fee_type'])
		context['page_type'] = page_type
		print context
		return render(request,'accountant/fees/make-transaction.html', context)

	elif request.method == 'POST':
		try:
			id = request.POST['student_batch']

			student_batch_object = StudentBatch.objects.get(id = request.POST['student_batch'])
			student_batch_id = student_batch_object.id
			
			print student_batch_id

			fee_type_id = request.POST['fee_type']
			
			print fee_type_id
			receipt_number = request.POST['receipt_number']
			
			amount = request.POST['amount']
			
			date = request.POST['date']
			print date
			print "herera"
			
			time = request.POST['time']
			
			set_fee_transaction(id = None ,amount = amount, date =  date, time = time , receipt_number = receipt_number, student_batch_id = student_batch_id, fee_type_id = fee_type_id)
		
			return redirect('./?message=Transaction made')
		except Exception, e:
			return redirect('./?message_error=' + str(e))



@csrf_exempt
def create_student(request):
	
	
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_accountant'] != True:
		raise Http404
	
	context = {}
	context['details'] = auth_dict
	

	if request.method == 'GET':
		
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		return render(request, 'accountant/student/create-student.html', context)	
	 

	elif request.method == 'POST':

		if request.POST['password'] != request.POST['confirmpassword'] :
			return redirect('./?message_error=Student Passwords Do Not Match')

		if request.POST['ppassword'] != request.POST['pconfirmpassword'] :
		    return redirect('./?message_error=Parent Passwords Do Not Match')    
        
		else:

			username = request.POST['username']
			
			password = request.POST['password']
			
			first_name = request.POST['first_name']
			
			last_name = request.POST['last_name']
			
			address = request.POST['address']

			email = request.POST['email']

			phone_number = int(request.POST['phone_number'])

			gender = request.POST['gender']


			pusername = request.POST['pusername']
			
			ppassword = request.POST['ppassword']
			
			pfirst_name = request.POST['pfirst_name']
			
			plast_name = request.POST['plast_name']
			
			paddress = request.POST['paddress']

			pemail = request.POST['pemail']

			pphone_number = int(request.POST['pphone_number'])

			pgender = request.POST['pgender']
			
		 	parent_id = set_parent(id = None,username = pusername , password = ppassword, student_id = None, first_name = pfirst_name ,last_name = plast_name ,address = paddress, email = pemail, phone_number = pphone_number, gender = pgender )

			set_student(id = None,username = username, password = password, parent_id = parent_id, batch_id = None, first_name = first_name ,last_name = last_name ,address = address, email = email, phone_number = phone_number, gender = gender )				
			
			return redirect('./?message=Entry made')

			'''except:
				return redirect('./?message_error=Error. Entry Failed.')'''


@csrf_exempt
def admit_student(request):
	
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] != True:
		raise Http404
	
	if auth_dict['permission_accountant'] != True:
		raise Http404
	context = {}
	context['details'] = auth_dict
	

	if request.method == 'GET':
		
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		
		page_type = -1
		

		if 'student' in request.GET:
			page_type = 0
			context['student_id'] = request.GET['student']
			context['student_name'] = request.GET['name']
			academic_years = get_academic_year(id=None)
			context['academic_years'] = academic_years	
			if 'academic_year' in request.GET:
				page_type = 1
				standards = get_standard(id=None)
				context['standards'] = standards
				context['academic_year_id'] = int(request.GET['academic_year'])
				#context['student_batch_id'] = StudentBatch.objects.get(student = Student.objects.get(id = int(request.GET['student']))).id
				if 'standard' in request.GET:
					page_type = 2
					context['standard_id'] = int(request.GET['standard'])
					batches = get_batch()
					batches.append({'id' : -1, 'name' : 'Empty Batch'})
					context['batches'] =  batches
				
					if 'batch' in request.GET:
						page_type = 3
						context['batch_id'] = int(request.GET['batch'])
						subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.GET['standard']), academic_year_id=int(request.GET['academic_year']), subject_year_id=None)
						context['subject_years'] = subject_years
							
			
		context['page_type'] = page_type
		return render(request,'accountant/student/admit-student.html', context)

	elif request.method == 'POST':
		'''try:'''
		id = request.POST['student']

		student_object = Student.objects.get(id = request.POST['student'])
		student_id = student_object.id
		
	

		academic_year_id = request.POST['academic_year']
		

		standard_id = request.POST['standard']
		
		batch_id = request.POST['batch']
		print batch_id
		subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.POST['standard']), academic_year_id=int(request.POST['academic_year']), subject_year_id=None)
		subject_year_list = []
		for subject_year in subject_years:
			if 'subject_year_'+str(subject_year['id']) in request.POST:
				print subject_year
				subject_year_list.append(subject_year['id'])
		if batch_id == '-1':
			set_student_batch(id=None,student_id = student_id, batch_id = None, subject_year_id_list= subject_year_list, academic_year_id = academic_year_id, standard_id = standard_id)
		else:
			set_student_batch(id=None,student_id = student_id, batch_id = batch_id, subject_year_id_list= subject_year_list, academic_year_id = None, standard_id = None)	
		return redirect('./?message=Transaction made')
		'''except:
			return redirect('./?message_error=Error. Transaction Failed.')'''


@csrf_exempt
def add_student_notice(request):


	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_accountant'] != True:
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

		return render(request,'accountant/notices/add-student-notice.html', context)

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

	if auth_dict['permission_accountant'] != True:
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

		return render(request,'accountant/notices/add-staff-notice.html', context)

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
			
			
			
			

@csrf_exempt
def view_my_notices(request):
	auth_dict = get_user(request)
	
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	context = {}
	context['details'] = auth_dict
	auth_dict
	notices = Notice.objects.filter(uploader = Staff.objects.get(id=auth_dict['id']))	
	context['notices'] = notices

	

	return render(request,'accountant/notices/view-my-notices.html', context)

@csrf_exempt
def edit_my_notice(request):
	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404
	#context['notice_id'] = request.GET['notice']
	
	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		notice = get_personal_notices(notice_id =(request.GET.get('notice')))	
		context['notice'] = notice
		context['notice_id'] = (request.GET.get('notice'))
		
		
		return render(request, 'accountant/notices/edit-my-notice.html', context)

	elif request.method == 'POST':
		try:
		
			set_notice(id = request.POST['notice_id'], title = request.POST['title'], description = request.POST['description'], uploader_id = auth_dict['id'] , expiry_date = request.POST['expiry-date'], important = request.POST['is_important'])
			
			return redirect('/accountant/notices/view-my-notices/?message=Notice edited')
		except:
			return redirect('./?message_error=Error. Edit Failed.')