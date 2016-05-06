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
from portal.db_api.sms_db import *
from portal.db_api.notice_db import *
from portal.db_api.lecture_db import *
from portal.db_api.standard_db import *
from django.core.exceptions import *
from django.utils.datastructures import *
from portal.validator.validator import ModelValidateError

import datetime
from datetime import date
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.http import HttpResponse
import mimetypes
import os
import urllib

def respond_as_attachment(request):

	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404
	#context['notice_id'] = request.GET['notice']

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		file_path = 'media/' + request.GET.get('doc')
		print file_path

		fp = open(file_path, 'rb')
		response = HttpResponse(fp.read())
		fp.close()
		print os.path.basename(file_path)
		original_filename = os.path.basename(file_path)
		type, encoding = mimetypes.guess_type(original_filename)
		if type is None:
		    type = 'application/octet-stream'
		response['Content-Type'] = type
		response['Content-Length'] = str(os.stat(file_path).st_size)
		if encoding is not None:
		    response['Content-Encoding'] = encoding

		# To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
		if u'WebKit' in request.META['HTTP_USER_AGENT']:
		    # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
		    filename_header = 'filename=%s' % original_filename.encode('utf-8')
		elif u'MSIE' in request.META['HTTP_USER_AGENT']:
		    # IE does not support internationalized filename at all.
		    # It can only recognize internationalized URL, so we do the trick via routing rules.
		    filename_header = ''
		else:
		    # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
		    filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
		response['Content-Disposition'] = 'attachment; ' + filename_header
		return response

def dashboard(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	context['details'] = auth_dict;
	context['notices'] = get_personal_notices(staff_id=auth_dict['id'], for_staff =True)

	return render(request,'admin/dashboard.html', context)

def view_profile(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])

	context['details'] =auth_dict
	context['staff_details'] = staff_details

	return render(request,'admin/profile/view-profile.html', context)

def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	staff_details = get_staff(id=auth_dict['id'])

	context['details'] =auth_dict
	context['staff_details'] = staff_details

	return render(request, 'admin/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	try:
		set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

		return redirect('/admin/profile/view-profile')
	except ModelValidateError, e:
		return redirect('../view-profile?message_error='+str(e))
	except ValueError, e:
		return redirect('../view-profile?message_error='+str(PentaError(1000)))
	except ObjectDoesNotExist, e:
		return redirect('../view-profile/?message_error='+str(PentaError(999)))
	except MultiValueDictKeyError, e:
		return redirect('../view-profile/?message_error='+str(PentaError(998)))
	except Exception, e:
		return redirect('../view-profile/?message_error='+str(PentaError(100)))


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']

	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']
	context['details'] = auth_dict

	return render(request,'admin/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/admin/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/admin/profile/change-password/?message_error=Password Change Failed')


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
				fee_details = get_batch_fees(batch_id = int(request.GET['batch']))
				context['fee_details'] = fee_details

		context['page_type'] = page_type

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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

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
		try:
			current_academic_year = request.POST['current_academic_year']
			set_current_academic_year(current_academic_year)
			return redirect('./?message=Current academic year changed.')
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

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

		try:
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

		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

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
		try:
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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))


def graphical_overview(request):
	context = {}
	auth_dict = get_user(request)
	context['details'] = auth_dict

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_admin'] != True:
		return Http404

	try:
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
				batch_number = 0
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
							lec_list[i['lecture_name']] = {'total_counter':0, 'done_counter':0, 'batch_number':batch_number}

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
					batch_number += 1

				for k,v in count_list.items():
					for num,i in enumerate(v):
						if i['batch_number'] != num:
							temp_counter = num
							while temp_counter != i['batch_number']:
								v.insert(temp_counter, {'total_counter':0, 'done_counter':0, 'batch_number':temp_counter})
								temp_counter += 1

				for k,v in count_list.items():
					if len(v) != 0:
						if v[-1]['batch_number'] != batch_number:
							temp_counter = v[-1]['batch_number'] + 1
							while temp_counter < batch_number:
								v.insert(temp_counter, {'total_counter':0, 'done_counter':0, 'batch_number':temp_counter})
								temp_counter += 1

				context['lecturebatches'] = lecturebatch_list
				context['count_list'] = count_list

			context['page_type'] = page_type


		return render(request, 'admin/track-progress/graphical-overview.html', context)
	except ModelValidateError, e:
		return redirect('./?message_error='+str(e))
	except ValueError, e:
		return redirect('./?message_error='+str(PentaError(1000)))
	except ObjectDoesNotExist, e:
		return redirect('./?message_error='+str(PentaError(999)))
	except MultiValueDictKeyError, e:
		return redirect('./?message_error='+str(PentaError(998)))
	except Exception, e:
		return redirect('./?message_error='+str(PentaError(100)))


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
		try:
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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

	elif request.method == 'POST':
		try:

			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1

			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_imp, document = document)

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
			if is_important:
				if int(request.POST['branch']):
					if int(request.POST['batch']):
						return redirect('/admin/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&batch_id='+str(request.POST['batch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))
					else:
						return redirect('/admin/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&batch_id='+str(request.POST['batch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))
				else:
					return redirect('/admin/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))

			else:
				return redirect('./?message=Notice Uploaded')
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

def send_sms_notice(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] != True:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404



	context = {}

	print 'GET:'
	print request.GET
	context['details'] = auth_dict
	branch_id = request.GET['branch_id']
	notice_id = request.GET['notice']
	student_list = []
	if int(request.GET['branch_id']):
		if int(request.GET['batch_id']):
			batch_id = request.GET['batch_id']
			context['batch_id'] = batch_id
			notice_viewers = NoticeViewer.objects.filter(notice_id = notice_id)
			print 'notice::'
			print notice_viewers
			for notice_viewer in notice_viewers:
				if notice_viewer.student:
					student_list.append(notice_viewer.student)

		else:
			batch_id = request.GET['batch_id']
			context['batch_id'] = batch_id
			notice_viewers = NoticeViewer.objects.filter(notice_id = notice_id)
			for notice_viewer in notice_viewers:
				if notice_viewer.student:
					student_list.append(notice_viewer.student)


	else:

		student_list = get_students()



	context['students'] = student_list
	context['notice_id'] = notice_id
	context['branch_id'] = branch_id
	context['title'] = request.GET['title']
	context['description'] = request.GET['description']


	return render(request, 'admin/notices/send-sms-notice.html', context)

@csrf_exempt
def send_sms_notice_submit(request):
	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404


	print 'here'
	print request.POST



	student_id_list = []
	students = get_students()
	for student in students:
		if "student_"+str(student['id']) in request.POST:
			student_id_list.append(student['id'])
	sms_for_notices(student_id_list = student_id_list, notice_title = request.POST['title'],notice_description = request.POST['description'],staff_id = auth_dict['id'])

	return redirect ('/admin/sms-status/')

def sms_status(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	context['not_sent_sms'] = get_pending_sms(auth_dict['id'])
	context['details'] = auth_dict

	return render(request, "admin/sms-status.html", context)

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

		try:
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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

	elif request.method == 'POST':
		try:
			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1
			title = request.POST['title']
			description = request.POST['description']
			expiry_date = request.POST['expiry-date']
			is_important = request.POST['is_important']

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			notice_id = set_notice(id=None, title=title, description= description, uploader_id= auth_dict['id'], expiry_date = expiry_date , important= is_imp, document = document)
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
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))

@csrf_exempt
def view_my_notices(request):
	context = {}

	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	context['details'] = auth_dict
	auth_dict
	notices = Notice.objects.filter(uploader = Staff.objects.get(id=auth_dict['id']))
	context['notices'] = notices



	return render(request,'admin/notices/view-my-notices.html', context)

@csrf_exempt
def edit_my_notice(request):
	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_admin'] != True:
		raise Http404
	#context['notice_id'] = request.GET['notice']

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		notice = get_personal_notices(notice_id =(request.GET.get('notice')))
		context['notice'] = notice
		# date_string = notice['expiry_date'].split('-')
		context['notice_id'] = (request.GET.get('notice'))


		return render(request, 'admin/notices/edit-my-notice.html', context)

	elif request.method == 'POST':
		try:
			if request.POST['is_important'] == "False":
				is_imp = 0
			else:
				is_imp = 1

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			set_notice(id = request.POST['notice_id'], title = request.POST['title'], description = request.POST['description'], uploader_id = auth_dict['id'] , expiry_date = request.POST['expiry-date'], important = is_imp, document = document)

			return redirect('/admin/notices/view-my-notices/?message=Notice edited')
		except ModelValidateError, e:
			return redirect('../view-my-notices?message_error='+str(e))
		except ValueError, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('../view-my-notices?message_error='+str(PentaError(100)))



@csrf_exempt
def delete_staff(request):
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

		branches = get_branch(id=None)
		context['branches'] = branches


		staff_list = search_staffs(first_name='', last_name='', username='', email='', phone_number='')
		print staff_list, len(staff_list)

		batch_list = {}

		context['staff_list'] = staff_list

		context['page_type'] = page_type
		context['details'] = auth_dict
		return render(request, 'admin/staff/delete-staff.html', context)

	elif request.method == 'POST':

		try:
			standard = request.POST['standard']
			batch_id = request.POST['batch']
			print 'her234'
			academic_year_id = get_current_academic_year()['id']
			#batches = get_batch(academic_year_id = academic_year_id,standard_id = standard)
			#for batch in batches:
			students = get_students(batch_id = batch_id)

			print 'heres'
			for student in students:
				if 'batch_'+str(batch_id)+'student_'+str(student['id']) in request.POST:
					print '00here123'
					print student
					student_batch = get_student_batch(id = None,batch_id=batch_id,standard_id=None,academic_year_id=None,student_id = student['id'], batch_assigned=True)
					set_attendance_daywise(id = None ,attended = True, student_batch_id = student['id'], date = request.POST['date'])

					print 'here1'
				else:
					student_batch = get_student_batch(id = None,batch_id=batch_id,standard_id=None,academic_year_id=None,student_id = student['id'], batch_assigned=True)
					set_attendance_daywise(id = None ,attended = False, student_batch_id = student['id'], date = request.POST['date'])
			return redirect('/teacher/attendance/send-sms/?batch_id='+str(batch_id)+'&date='+str(request.POST['date']))
		except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))
