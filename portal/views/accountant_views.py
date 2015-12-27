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
from portal.db_api.sms_db import *
from portal.db_api.notice_db import *
from portal.db_api.cheque_db import *
from portal.db_api.emi_db import *
from portal.models import Notice
from django.core.exceptions import *
from django.utils.datastructures import *
from portal.validator.validator import ModelValidateError
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import time
from portal.models import *
import datetime
from datetime import date
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
import mimetypes
import os
import urllib

def respond_as_attachment(request):

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

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context['details'] = auth_dict

	# All notices
	notices = get_personal_notices(staff_id=auth_dict['id'], for_staff =True)
	context['notices'] = notices

	# Latest Maximum 10 Notices received in past 1 week. (Min(10, number of notices overall))
	# Only considering expiry date uptil now.
	# Later the expiry date, newer is document.
	# NOTE: This metric is not correct. Need to consider date/time of uploading,
	#       for which we will have to add timestamp of upload.
	notice_list = []
	for notice in notices:
		cur_notice = {}
		cur_notice['title'] = notice['title']
		cur_notice['description'] = notice['description']
		cur_notice['uploader'] = notice['uploader']
		cur_notice['important'] = notice['important']
		cur_notice['document'] = notice['document']
		cur_notice['expiry_date'] = notice['expiry_date']
		notice_list.append(cur_notice)

	sorted_notices = sorted(notice_list, reverse=True, key=lambda x: x['expiry_date'])
	context['latest_notices'] = sorted_notices[:min(len(sorted_notices) + 1, 10)]

	# All transactions that accountant is responsible for
	branches_of_accountant = get_branch_of_accountant(accountant_id=auth_dict['id'])
	batches_of_accountant = []
	for branch in branches_of_accountant:
		branch_id = branch['id']
		batches = get_batch(branch_id = branch_id)
		for batch in batches:
			batches_of_accountant.append(batch)

	transactions = []

	for batch in batches_of_accountant:
		fees = get_batch_fees(batch_id = batch['id'])
		for fee in fees:
			transactions.append(fee)

	print transactions

	# 10 Latest Transactions
	sorted_transactions = sorted(transactions, reverse=True, key=lambda x: x['date'])
	latest_transactions = sorted_transactions[:min(len(sorted_transactions) + 1, 10)]
	context['latest_transactions'] = latest_transactions

	# Pending Fee transactions
	pending_transactions = []
	for transaction in transactions:
		if transaction['total_fees_remaining'] > 0:
			pending_transactions.append(transaction)
	context['pending_transactions'] = pending_transactions

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

	try:
		set_staff(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])
		return redirect('/accountant/profile/view-profile')
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

def view_fees(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context = {}
	context['details'] = auth_dict
	if request.method == 'GET':
		try:
			page_type = 0
			if 'student' in request.GET:
				page_type = 1
				context['student_id'] = int(request.GET['student'])
				context['student_name'] = request.GET['name']
				fee_details = get_student_fees( student_id = int(request.GET['student']) )
				transaction_details = get_fee_transaction(id = None ,date_start = None, date_end = None, student_id = int(request.GET['student']), fee_type_id = None)
				#print fee_details
				context['fee_details'] = fee_details
				context['transaction_details'] = transaction_details

			context['page_type'] = page_type
			print context

			return render(request,'accountant/fees/view-fees.html', context)
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
		try:
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
			amount = request.POST['amount']
			subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.POST['standard']), academic_year_id=int(request.POST['academic_year']), subject_year_id=None)
			subject_year_list = []
			for subject_year in subject_years:
				if 'subject_year_'+str(subject_year['id']) in request.POST:
					#print subject_year
					subject_year_list.append(subject_year['id'])

			set_base_fee(amount=amount , subject_years_list = subject_year_list)
			return redirect('./?message=Base Fee Set')
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

		try:
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
		try:
			base_fees = get_base_fee(id = (request.GET.get('base-fee')) , subject_years_list = None,  academic_year_id=None, standard_id=None)
			context['academic_year_id'] = request.GET.get('academic_year')
			context['standard_id'] = request.GET.get('standard')
			context['base_fees'] = base_fees
			context['details'] = auth_dict
			return render(request, 'accountant/fees/edit-base-fee.html', context)
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
			set_base_fee(id = (request.POST.get('base-fee')), amount=request.POST['amount'] , subject_years_list = None)
			return redirect('/accountant/fees/edit-base-fees/?academic_year='+str((request.POST.get('academic_year_id')))+'&standard='+str((request.POST.get('standard_id')))+'&base-fee='+str((request.POST.get('base-fee')))+'&message=Base fees modified')
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
				3					cheque/cash if transaction=payment
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
	page_type = 0

	if request.method == 'GET':

		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']

		try:
			page_type = 0
			branches = get_branch(id=None)
			context['branches'] = branches

			if 'student' in request.GET:
				page_type = 1
				context['student_id'] = request.GET['student']
				context['student_name'] = request.GET['student_name']

				fee_types = get_fee_types()
				context['fee_types'] = fee_types
				if 'fee_type' in request.GET:
					page_type = 2
					context['fee_type_id'] = int(request.GET['fee_type'])
					# 1 represents fee type payment
					if int(request.GET['fee_type']) == 1:
						page_type = 3
						if 'payment_method' in request.GET:
							context['payment_method'] = request.GET['payment_method']

							if request.GET['payment_method'] == 'cash':
								page_type = 2
							else:
								page_type = 4
			context['page_type'] = page_type
			print context
			return render(request,'accountant/fees/make-transaction.html', context)
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

			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))


	elif request.method == 'POST':
		try:
			id = request.POST['student']

			'''student_batch_object = StudentBatch.objects.get(id = request.POST['student_batch'])
			student_batch_id = student_batch_object.id'''

			#print student_batch_id



			fee_type_id = request.POST['fee_type']

			if request.POST['payment_method'] == 'cheque':
				#print fee_type_id
				#receipt_number = request.POST['receipt_number']

				amount = request.POST['amount']
				cheque_date = request.POST['cheque_date']
				cheque_number = request.POST['cheque_number']
				bank_name = request.POST['bank_name']
				bank_branch_name = request.POST['bank_branch_name']
				description = request.POST['description']
				date = request.POST['date']

				cheque_id = set_cheque(id = None, student_id = id, amount = amount, cheque_date = cheque_date, cleared = False, clearance_date = None, description = description, cheque_number = cheque_number, bank_name = bank_name, bank_branch_name = bank_branch_name)
				#print date
				#print "herera"

				#time = request.POST['time']

				transaction_id = set_fee_transaction(id = None ,amount = amount, date =  date, student_id = request.POST['student'], fee_type_id = fee_type_id, cheque_id = cheque_id)
			if request.POST['payment_method'] == 'cash':
				#print fee_type_id
				#receipt_number = request.POST['receipt_number']

				amount = request.POST['amount']

				date = request.POST['date']
				#print date
				#print "herera"

				#time = request.POST['time']

				transaction_id = set_fee_transaction(id = None ,amount = amount, date =  date, student_id = request.POST['student'], fee_type_id = fee_type_id)


			return redirect('/accountant/fees/view-transaction/?transaction='+str(transaction_id)+'&cheque_number='+str(request.POST['cheque_number']))





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

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def view_transaction(request):
	context = {}

	auth_dict = get_user(request)
	context['details'] = auth_dict


	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	if 'transaction' in request.GET:
		context['transaction_id'] = request.GET['transaction']
		context['payment_method'] = 'Cash'
		if 'cheque_number' in request.GET:
			context['payment_method'] = 'Cheque'
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']
	context['transaction_details'] = get_fee_transaction(id = request.GET['transaction'])
	return render_to_pdf(
           'accountant/fees/view-transaction.html',
            context
        )




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
			try:
				username = request.POST['username']
				password = request.POST['password']
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				address = request.POST['address']
				email = request.POST['email']
				phone_number = request.POST['phone_number']
				gender = request.POST['gender']
				pusername = request.POST['pusername']
				ppassword = request.POST['ppassword']
				pfirst_name = request.POST['pfirst_name']
				plast_name = request.POST['plast_name']
				paddress = request.POST['paddress']
				pemail = request.POST['pemail']
				pphone_number = request.POST['pphone_number']
				pgender = request.POST['pgender']
			 	parent_id = set_parent(id = None,username = pusername , password = ppassword, student_id = None, first_name = pfirst_name ,last_name = plast_name ,address = paddress, email = pemail, phone_number = pphone_number, gender = pgender )
				set_student(id = None,username = username, password = password, parent_id = parent_id, batch_id = None, first_name = first_name ,last_name = last_name ,address = address, email = email, phone_number = phone_number, gender = gender )
				return redirect('./?message=Entry made')

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
def admit_student_old(request):
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
		try:
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
					if 'standard' in request.GET:
						page_type = 2
						context['standard_id'] = int(request.GET['standard'])
						batches = get_batch(academic_year_id=request.GET['academic_year'], standard_id=request.GET['standard'])
						batches.append({'id' : -1, 'name' : 'Empty Batch'})
						context['batches'] =  batches
						if 'batch' in request.GET:
							page_type = 3
							context['batch_id'] = int(request.GET['batch'])
							subject_years = get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=int(request.GET['standard']), academic_year_id=int(request.GET['academic_year']), subject_year_id=None)
							context['subject_years'] = subject_years

			context['page_type'] = page_type
			return render(request,'accountant/student/admit-student-old.html', context)
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

				student_batch_id = set_student_batch(id=None,student_id = student_id, batch_id = None, subject_year_id_list= subject_year_list, academic_year_id = academic_year_id, standard_id = standard_id)
				#Creating base fee transaction after admission
				subject_years = StudentBatch.objects.get(id = student_batch_id).subject_years.all()
				basefees = get_base_fee(id = None , subject_years_list = subject_years)
				total = {}
				total['base_fees'] = 0
				for basefee in basefees :
					#print basefee
					total['base_fees'] = total['base_fees'] + basefee.amount

				date = (time.strftime("%Y-%m-%d"))
				transaction_id = set_fee_transaction(id = None ,amount = total['base_fees'], date =  date, student_id = student_id, fee_type_id = FeeType.objects.get(name = 'base fee').id)
			else:
				student_batch_id = set_student_batch(id=None,student_id = student_id, batch_id = batch_id, subject_year_id_list= subject_year_list, academic_year_id = None, standard_id = None)
				#Creating base fee transaction after admission
				subject_years = StudentBatch.objects.get(id = student_batch_id).subject_years.all()
				basefees = get_base_fee(id = None , subject_years_list = subject_years)
				total = {}
				total['base_fees'] = 0
				for basefee in basefees :
					#print basefee
					total['base_fees'] = total['base_fees'] + basefee.amount

				date = (time.strftime("%Y-%m-%d"))
				transaction_id = set_fee_transaction(id = None ,amount = total['base_fees'], date =  date, student_id = student_id, fee_type_id = FeeType.objects.get(name = 'base fee').id )


			return redirect('./?message=Student Admitted')


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
		try:
			page_type = -1
			if 'student' in request.GET:
				page_type = 0
				context['student_id'] = request.GET['student']
				context['student_name'] = request.GET['name']
				academic_years = get_academic_year(id=None)
				context['academic_years'] = academic_years
				standards = get_standard(id=None)
				context['standards'] = standards
				if 'base_fee' in request.GET:
					page_type = 2
					context['fee'] = request.GET['fee']
				elif 'academic_year' in request.GET:
					page_type = 1
					count = 0
					acs_list = []
					academic_year_set = set()
					standard_set = set()
					for get_params in request.GET.keys():
						if get_params[:4] == 'acs_':
							acs_dict = {}
							acs_dict['academic_year'] = int(get_params[4:].split('_')[0])
							if acs_dict['academic_year'] in academic_year_set:
								return redirect('./?message_error=Academic Year should be unique')
							academic_year_set.add(acs_dict['academic_year'])
							acs_dict['academic_year_name'] = get_academic_year(id=acs_dict['academic_year'])['name']
							acs_dict['standard'] = int(get_params[4:].split('_')[1])
							if acs_dict['standard'] in standard_set:
								return redirect('./?message_error=Standard should be unique')
							standard_set.add(acs_dict['standard'])
							acs_dict['standard_name'] = get_standard(id=acs_dict['standard'])['name']
							acs_dict['batches'] = get_batch(academic_year_id=acs_dict['academic_year'], standard_id=acs_dict['standard'])
							acs_dict['batches'].append({'id' : -1, 'name' : 'Assign batch later'})
							acs_dict['subject_years'] = get_subjects(standard_id=acs_dict['standard'], academic_year_id=acs_dict['academic_year'])
							acs_list.append(acs_dict)
							count += 1
					context['acs_list'] = acs_list

			context['page_type'] = page_type
			return render(request,'accountant/student/admit-student.html', context)
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
			id = request.POST['student']

			student_object = Student.objects.get(id = request.POST['student'])
			student_id = student_object.id
			total_cost = 0
			if 'fee_amount' in request.POST:
				date = (time.strftime("%Y-%m-%d"))
				transaction_id = set_fee_transaction(amount = request.POST['fee_amount'], date =  date, student_id = student_id, fee_type_id = FeeType.objects.get(name = 'base fee').id)
				if 'emi' in request.POST:
					return redirect('../add-emi/?name='+request.POST['name']+'&student='+str(student_id)+'&message=Fee set for Student - Please enter EMI details')
				else:
					return redirect('./?message=Fee set for Student')
			else:
				for post_params in request.POST.keys():
					if post_params[:4] == 'acs_':
						academic_year_id = int(post_params[4:].split('_')[0])
						standard_id = int(post_params[4:].split('_')[1])
						batch_id = request.POST['batch_'+str(academic_year_id)+'_'+str(standard_id)]
						subject_years = get_subjects(standard_id=standard_id, academic_year_id=academic_year_id)
						subject_year_list = []
						for subject_year in subject_years:
							if 'subject_year_'+str(academic_year_id)+'_'+str(standard_id)+'_'+str(subject_year['id']) in request.POST:
								subject_year_list.append(subject_year['id'])
						if batch_id == '-1':

							student_batch_id = set_student_batch(student_id = student_id, batch_id = None, subject_year_id_list= subject_year_list, academic_year_id = academic_year_id, standard_id = standard_id)
							#Creating base fee transaction after admission
							subject_years = StudentBatch.objects.get(id = student_batch_id).subject_years.all()
							basefees = get_base_fee(subject_years_list = subject_years)
							total = {}
							total['base_fees'] = 0
							for basefee in basefees :
								#print basefee
								total['base_fees'] = total['base_fees'] + basefee.amount
								total_cost += basefee.amount

							date = (time.strftime("%Y-%m-%d"))
							# Commenting transaction as user can edit at a further stage
							# transaction_id = set_fee_transaction(id = None ,amount = total['base_fees'], date =  date, student_id = student_id, fee_type_id = FeeType.objects.get(name = 'base fee').id)
						else:
							student_batch_id = set_student_batch(id=None,student_id = student_id, batch_id = batch_id, subject_year_id_list= subject_year_list, academic_year_id = None, standard_id = None)
							#Creating base fee transaction after admission
							subject_years = StudentBatch.objects.get(id = student_batch_id).subject_years.all()
							basefees = get_base_fee(id = None , subject_years_list = subject_years)
							total = {}
							total['base_fees'] = 0
							for basefee in basefees :
								#print basefee
								total['base_fees'] = total['base_fees'] + basefee.amount
								total_cost += basefee.amount

							date = (time.strftime("%Y-%m-%d"))
							# Commenting transaction as user can edit at a further stage
							# transaction_id = set_fee_transaction(id = None ,amount = total['base_fees'], date =  date, student_id = student_id, fee_type_id = FeeType.objects.get(name = 'base fee').id )


				return redirect('./?message=Student Admitted&base_fee=True&fee='+str(total_cost)+'&student='+str(student_id)+'&name='+request.POST['name'])


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
	if auth_dict['permission_accountant'] != True:
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
						return redirect('/accountant/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&batch_id='+str(request.POST['batch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))
					else:
						return redirect('/accountant/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&batch_id='+str(request.POST['batch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))
				else:
					return redirect('/accountant/notices/send-sms-notice/?branch_id='+str(request.POST['branch'])+'&title='+title+'&description='+description+'&notice='+str(notice_id))


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

	if auth_dict['permission_accountant'] != True:
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


	return render(request, 'accountant/notices/send-sms-notice.html', context)

@csrf_exempt
def send_sms_notice_submit(request):
	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404


	print 'here'
	print request.POST



	student_id_list = []
	students = get_students()
	for student in students:
		if "student_"+str(student['id']) in request.POST:
			student_id_list.append(student['id'])
	sms_for_notices(student_id_list = student_id_list, notice_title = request.POST['title'],notice_description = request.POST['description'],staff_id = auth_dict['id'])

	return redirect ('/accountant/sms-status/')

def sms_status(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	context['not_sent_sms'] = get_pending_sms(auth_dict['id'])
	context['details'] = auth_dict

	return render(request, "accountant/sms-status.html", context)


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

			return render(request,'accountant/notices/add-staff-notice.html', context)
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

	if auth_dict['permission_accountant'] != True:
		raise Http404

	if 'message' in request.GET:
		context['message'] = request.GET['message']
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

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

		try:
			notice = get_personal_notices(notice_id =(request.GET.get('notice')))
			context['notice'] = notice
			# date_string = notice['expiry_date'].split('-')
			context['notice_id'] = (request.GET.get('notice'))
			return render(request, 'accountant/notices/edit-my-notice.html', context)
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

			if len(request.FILES) > 0:
				document = request.FILES['myfile']
			else:
				document = None

			set_notice(id = request.POST['notice_id'], title = request.POST['title'], description = request.POST['description'], uploader_id = auth_dict['id'] , expiry_date = request.POST['expiry-date'], important = is_imp, document = document)

			return redirect('/accountant/notices/view-my-notices/?message=Notice edited')
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

def add_emi(request):
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
		try:
			page_type = -1
			if 'student' in request.GET:
				page_type = 0
				context['student_id'] = request.GET['student']
				context['student_name'] = request.GET['name']
				fee_details = get_student_fees( student_id = int(request.GET['student']) )
				context['fee_details'] = fee_details
				if 'number_emi' in request.GET:
					page_type = 1
					context['number_emi'] = int(request.GET['number_emi'])
					context['down_payment_amount'] = int(request.GET['down_payment_amount'])
					list_emi = []
					list_emi.append([1, context['down_payment_amount'], "Down Payment"])
					remaining_amount = (float(fee_details[0]['total_fees'])-context['down_payment_amount'])/context['number_emi']
					for i in range(context['number_emi']):
						list_emi.append([i+2, int(remaining_amount), "EMI "+str(i+1)])
					context['emis'] = list_emi
					if 'emi1' in request.GET and 'emi_deadline1' in request.GET:
						index = 1
						while 'emi'+str(index) in request.GET and 'emi_deadline'+str(index) in request.GET:
							print 'Creating EMI ', request.GET['emi'+str(index)], request.GET['emi_deadline'+str(index)]
							set_emi(
								student_id = context['student_id'],
								amount_due = int(request.GET['emi'+str(index)]),
								time_deadline = datetime.datetime.strptime(request.GET['emi_deadline'+str(index)], '%Y-%m-%d'),
								description = request.GET['description'+str(index)]
							)
							index += 1
						return redirect('./?message=Added EMIs')
			context['page_type'] = page_type
			return render(request,'accountant/student/add-emi.html', context)
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
def view_cheques(request):
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

		try:
			page_type = 0
			cheques = get_cheque(id = None, student_id = None, start_date = None, end_date = None, cleared = None, cheque_number = None)
			upcoming_cheques = []
			cleared_cheques = []
			deadline_cheques = []
			for cheque in cheques :
				if cheque['cheque_date'] > datetime.date.today() and  not cheque['cleared']:
					print "upcoming"
					upcoming_cheques.append(cheque)
				if cheque['cheque_date'] <= datetime.date.today() and  not cheque['cleared']:
					deadline_cheques.append(cheque)
				if cheque['cleared']:
					cleared_cheques.append(cheque)


			context['upcoming_cheques'] = upcoming_cheques
			context['cleared_cheques'] = cleared_cheques
			context['deadline_cheques'] = deadline_cheques

			context['page_type'] = page_type
			return render(request,'accountant/cheques/view-cheques.html', context)
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
def edit_cheque(request):
	auth_dict = get_user(request)
	context = {}
	context['details'] = auth_dict

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_accountant'] != True:
		raise Http404

	if request.method == 'GET':
		if 'message' in request.GET:
			context['message'] = request.GET['message']
		elif 'message_error' in request.GET:
			context['message_error'] = request.GET['message_error']
		try:
			cheque = get_cheque(id = int(request.GET['cheque']))

			context['cheque'] = cheque
			return render(request, 'accountant/cheques/edit-cheque.html', context)
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
		#try:
		set_cheque(id = int(request.POST['cheque_id']), student_id = None, amount = None, cheque_date = None, cleared = request.POST['cleared'], clearance_date = request.POST['clearance_date'], description = request.POST['description'], cheque_number = None, bank_name = request.POST['bank_name'], bank_branch_name = request.POST['bank_branch_name'])
		return redirect('/accountant/cheques/edit-cheque/?cheque='+str((request.POST.get('cheque_id')))+'&message=Cheque Details Updated')
		'''except ModelValidateError, e:
			return redirect('./?message_error='+str(e))
		except ValueError, e:
			return redirect('./?message_error='+str(PentaError(1000)))
		except ObjectDoesNotExist, e:
			return redirect('./?message_error='+str(PentaError(999)))
		except MultiValueDictKeyError, e:
			return redirect('./?message_error='+str(PentaError(998)))
		except Exception, e:
			return redirect('./?message_error='+str(PentaError(100)))'''

def view_emis(request):
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

		try:
			context['page_type'] = 0
			context['pending_emis'] = get_pending_emi()
			context['upcoming_emis'] = get_next_week_emi()
			return render(request,'accountant/emis/view-emis.html', context)
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
