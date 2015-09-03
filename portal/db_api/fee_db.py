# set_base_fee
# get_base_fee
# add_transaction
# get_transaction (one or all of one student or of any particular type)
from django.db.models import Count
from portal.models import *

def set_base_fee(id = None ,amount=None , subject_years_list = None):
	#subject_years is list of subject_year ids eg. [1,2]
	#if id=none create new base fee object
	#else if id!=none specify amount to change and dont provide subjectyearlist
	is_none_id = id == None
	is_none_amount = amount == None
	is_none_subject_years_list = subject_years_list == None

	if is_none_amount  :
		raise Exception('Amount needed')

	if is_none_subject_years_list and is_none_id :
		raise Exception('Minimum two arguments needed')

	if is_none_id:

		base_fee_object = BaseFee(amount=amount)
		base_fee_object.save()
		for subject_year_id in subject_years_list :
			subject_year_object = SubjectYear.objects.get(id = subject_year_id)
			print subject_year_object
			base_fee_object.subject_years.add(subject_year_object)

		return base_fee_object.id

	else :

		base_fee_object = BaseFee.objects.get(id=id)
		base_fee_object.amount =amount
		base_fee_object.save()
		return base_fee_object.id

def get_base_fee(id = None , subject_years_list = None, academic_year_id=None, standard_id=None):
	#subject_years is list of subject_year ids eg. [1,2]

	#if 0 args return all base fee object DONE
	#else if id=none and subjectyearlist!=none specify return that object TODO
	is_none_id = id == None
	is_none_subject_years_list = subject_years_list == None
	is_none_academic_year_id = academic_year_id == None
	is_none_standard_id = standard_id == None

	if not is_none_academic_year_id and not is_none_standard_id:
		base_fee_list=[]
		base_fee_objects = BaseFee.objects.filter(subject_years__academic_year__id=academic_year_id, subject_years__subject__standard__id=standard_id).distinct()
		#print base_fee_objects
		for base_fee in base_fee_objects :
			base_fee_object = {}
			base_fee_object['id']=base_fee.id
			base_fee_object['amount']=base_fee.amount
			subject_year_list=[]

			#print base_fee.subject_years

			for subject in base_fee.subject_years.all():
				subject_year_object = {}
				subject_year_object['id'] = subject.id
				subject_year_object['subject'] = subject.subject
				subject_year_object['academic_year'] = subject.academic_year
				subject_year_list.append(subject_year_object)
			base_fee_object['subject_years']=subject_year_list
			base_fee_list.append(base_fee_object)

		return base_fee_list

	if not is_none_id and not is_none_subject_years_list:
		raise Exception('Less than two arguments needed')

	if is_none_id and is_none_subject_years_list :

		base_fee_list=[]
		base_fee_objects = BaseFee.objects.all()
		#print base_fee_objects
		for base_fee in base_fee_objects :
			base_fee_object = {}
			base_fee_object['id']=base_fee.id
			base_fee_object['amount']=base_fee.amount
			subject_year_list=[]

			#print base_fee.subject_years

			for subject in base_fee.subject_years.all():
				subject_year_object = {}
				subject_year_object['id'] = subject.id
				subject_year_object['subject'] = subject.subject
				subject_year_object['academic_year'] = subject.academic_year
				subject_year_list.append(subject_year_object)
			base_fee_object['subject_years']=subject_year_list
			base_fee_list.append(base_fee_object)

		return base_fee_list

	if not is_none_id and is_none_subject_years_list :


		base_fee = BaseFee.objects.get(id = id)


		base_fee_object = {}
		base_fee_object['id']=base_fee.id
		base_fee_object['amount']=base_fee.amount
		subject_year_list=[]
		#print base_fee.subject_years

		for subject in base_fee.subject_years.all():
			subject_year_object = {}
			subject_year_object['id'] = subject.id
			subject_year_object['subject'] = subject.subject
			subject_year_object['academic_year'] = subject.academic_year
			subject_year_list.append(subject_year_object)
		base_fee_object['subject_years']=subject_year_list


		return base_fee_object

	if is_none_id and not is_none_subject_years_list :

		'''subject_year_combo = []
								for subject in subject_years_list:
									subject_year_object = SubjectYear.objects.get(id = subject)
									subject_year_combo.append(subject_year_object)'''

		base_fee = BaseFee.objects.annotate(count=Count('subject_years')).filter(subject_years=subject_years_list[0])

		for subject_year in subject_years_list[1:]:
			base_fee = base_fee.filter(subject_years = subject_year)

		base_fee = base_fee.filter(count=len(subject_years_list))
		#print "========================================================================================================================================"
		#print base_fee
		return base_fee

		'''base_fee_object = {}


		base_fee = BaseFee.objects.filter(subject_years__id = subject_years_list[0]).filter(subject_years__id = subject_years_list[1])

		print base_fee

		return True

		base_fee_object['id']=base_fee.id
		base_fee_object['amount']=base_fee.amount
		subject_year_list=[]


		for subject in base_fee.subject_years.all():
			subject_year_object = {}
			subject_year_object['id'] = subject.id
			subject_year_object['subject'] = subject.subject
			subject_year_object['academic_year'] = subject.academic_year
			subject_year_list.append(subject_year_object)
		base_fee_object['subject_years']=subject_year_list


		return base_fee_object'''

def set_fee_transaction(id = None ,amount=None ,date = None, time = None, receipt_number = None, student_batch_id = None, fee_type_id = None):
	is_none_id = id == None
	is_none_amount = amount == None
	is_none_date = date == None
	is_none_time = time == None
	is_none_receipt_number = receipt_number == None
	is_none_student_batch_id = student_batch_id == None
	is_none_fee_type_id = fee_type_id == None

	if is_none_id:
		student_batch_object = StudentBatch.objects.get(id = student_batch_id)
		fee_type_object = FeeType.objects.get(id = fee_type_id)
		fee_transaction_object = FeeTransaction(amount = amount, date = date, time = time, receipt_number = receipt_number, student_batch = student_batch_object, fee_type = fee_type_object)
		fee_transaction_object.save()

		return True

	else :
		raise Exception('You cannot edit a fee transaction')

def get_fee_transaction(id = None ,date_start = None, date_end = None, receipt_number = None, student_id = None, fee_type_id = None):
	is_none_id = id == None
	is_none_date_start = date_start == None
	is_none_date_end = date_end == None
	is_none_receipt_number = receipt_number == None
	is_none_fee_type_id = fee_type_id == None
	is_none_student_id = student_id == None

	# if student batch id given return transactions for that student
	'''if not is_none_student_id:
		student_object = Student.objects.get(id = student_id)
		fee_transaction = FeeTransaction.objects.filter(student_batch = StudentBatch.objects.get(student=student_object))
		fee_list = []

		for i in fee_transaction:
			fee_dict = {}
			fee_dict['id'] = i.id
			fee_dict['amount'] = i.amount
			fee_dict['date'] = i.date
			fee_dict['time'] = i.time
			fee_dict['timestamp'] = i.timestamp
			fee_dict['student_batch'] = i.student_batch
			fee_dict['fee_type'] = i.fee_type

			fee_list.append(fee_dict)

		return fee_list'''

	# if student batch id given return transactions for that student
	if not is_none_student_id:
		fee_transaction = FeeTransaction.objects.filter(student_batch__student__id = student_id)
		fee_list = []

		fee_academic_year_list = []
		for i in fee_transaction:
			fee_dict = {}
			fee_dict['id'] = i.id
			fee_dict['receipt_number'] = i.receipt_number
			fee_dict['amount'] = i.amount
			fee_dict['date'] = i.date
			fee_dict['time'] = i.time
			fee_dict['timestamp'] = i.timestamp
			fee_dict['student_batch'] = i.student_batch
			fee_dict['fee_type'] = i.fee_type

			fee_list.append(fee_dict)

			if i.student_batch.batch != None:
				if not i.student_batch.batch.academic_year.id in fee_academic_year_list:
					fee_dict['academic_year'] = i.student_batch.batch.academic_year
				fee_academic_year_list.append(fee_dict)
			else:
				if not i.student_batch.academic_year.id in fee_academic_year_list:
					fee_dict['academic_year'] = i.student_batch.academic_year
				fee_academic_year_list.append(fee_dict)

		return fee_academic_year_list

	if not is_none_fee_type_id:
		fee_type_object = FeeType.objects.get(id = fee_type_id)
		fee_transaction = FeeTransaction.objects.filter(fee_type = fee_type_object)
		fee_list = []

		for i in fee_transaction:
			fee_dict = {}
			fee_dict['id'] = i.id
			fee_dict['amount'] = i.amount
			fee_dict['date'] = i.date
			fee_dict['time'] = i.time
			fee_dict['timestamp'] = i.timestamp
			fee_dict['student'] = i.student
			fee_dict['fee_type'] = i.fee_type
			fee_list.append(fee_dict)

		return fee_list


	if not is_none_id:

		i = FeeTransaction.objects.get(id =id)

		fee_dict = {}
		fee_dict['id'] = i.id
		fee_dict['amount'] = i.amount
		fee_dict['date'] = i.date
		fee_dict['time'] = i.time
		fee_dict['timestamp'] = i.timestamp
		fee_dict['student'] = i.student
		fee_dict['fee_type'] = i.fee_type

		return fee_dict

	else :
		raise Exception('Wrong set of arguments')




#================================function not being used===================
'''def get_fee_balance(student_batch_id = None, fee_type_name = None):

	is_none_student_batch_id = student_batch_id == None
	is_none_fee_type = fee_type_name == None

	# if student batch id given return transactions for that student
	if not is_none_student_batch_id:
		student_batch_object = StudentBatch.objects.get(id = student_batch_id)
		fee_type_object = FeeType.objects.get(name = fee_type_name)

		fee_transaction = FeeTransaction.objects.filter(student = student_batch_object, fee_type = fee_type_object)
		fee_list = []


		total = {}
		total['total_fees_paid'] =0
		for i in fee_transaction:


			total['student'] = i.student_batch.student.first_name + ' ' + i.student_batch.student.last_name
			total['total_fees_paid'] = total['total_fees_paid'] + i.amount



		fee_list.append(total)
		print fee_list
		return fee_list

	else :
		raise Exception('Wrong set of arguments')
'''

def get_student_fees(student_id = None):

	is_none_student_id = student_id == None

	if not is_none_student_id :
		student_batch_objects = StudentBatch.objects.filter(student__id = student_id)
	#fee_type_object = FeeType.objects.get(name = fee_type_name)
	fee_list = []
	total = {}
	total['total_fees_paid'] =0
	total['discount'] = 0
	total['base_fees'] = 0
	total['total_fees'] = 0
	total['fees_remaining'] = 0
	for  student_batch_object in student_batch_objects:


		subject_years = student_batch_object.subject_years.all()
		if student_batch_object.batch != None:
			print 'subjects_years', subject_years, ' for student batch', student_batch_object, student_batch_object.academic_year, student_batch_object.batch.academic_year
		else:
			print 'subjects_years', subject_years, ' for student batch', student_batch_object, student_batch_object.academic_year, None
		print '\n\n\n\n\n'
		basefees = get_base_fee(id = None , subject_years_list = subject_years)

		for basefee in basefees :
			#print basefee
			total['base_fees'] = total['base_fees'] + basefee.amount


	fee_transaction = FeeTransaction.objects.filter(student_batch__student__id = student_id)
	#print fee_transaction
	for i in fee_transaction:


		total['student'] = i.student_batch.student.first_name + ' ' + i.student_batch.student.last_name
		total['student_id'] = student_id
		if(i.fee_type.name == 'payment'):
			total['total_fees_paid'] = total['total_fees_paid'] + i.amount

		if(i.fee_type.name == 'discount'):
			total['discount'] = total['discount'] + i.amount

	total['total_fees'] = total['base_fees'] - total['discount']
	total['fees_remaining'] = total['total_fees'] - total['total_fees_paid']
	fee_list.append(total)
	return fee_list

	#else :
	#	raise Exception('Wrong set of arguments')


def get_fee_types(id = None):

	is_none_fee_id = id == None

	if is_none_fee_id :
		fee_types = FeeType.objects.all()

		fee_list = []

		for i in fee_types:
			fee_dict = {}
			fee_dict['id'] = i.id
			fee_dict['name'] = i.name

			fee_list.append(fee_dict)

		return fee_list

def get_batch_fees(batch_id = None):

	is_none_batch_id = batch_id == None

	if not is_none_batch_id :
		student_batch_objects = StudentBatch.objects.filter(batch = Batch.objects.get(id = batch_id))
	else :
		student_batch_objects = StudentBatch.objects.all()
	#fee_type_object = FeeType.objects.get(name = fee_type_name)
	fee_list = []
	for object in student_batch_objects:

		fee_transaction = FeeTransaction.objects.filter(student_batch__student = object.student)

		total = {}
		total['total_fees_paid'] =0
		total['total_fees_remaining'] =0
		total['discount'] = 0
		total['base_fees'] = 0
		total['total_fees'] = 0

		studentbatches = StudentBatch.objects.filter(student = object.student)

		for studentbatch in studentbatches:
			subject_years = studentbatch.subject_years.all()
			basefees = get_base_fee(id = None , subject_years_list = subject_years)
			print basefees
			for basefee in basefees :
				total['base_fees'] = total['base_fees'] + basefee.amount



		for i in fee_transaction:



			total['student'] = i.student_batch.student.first_name + ' ' + i.student_batch.student.last_name
			total['student_id'] = i.student_batch.student.id
			if(i.fee_type.name == 'payment'):
				total['total_fees_paid'] = total['total_fees_paid'] + i.amount

			if(i.fee_type.name == 'discount'):
				total['discount'] = total['discount'] + i.amount

		total['total_fees'] = total['base_fees'] - total['discount']
		total['total_fees_remaining'] = total['total_fees'] - total['total_fees_paid']
		fee_list.append(total)

	return fee_list

	#else :
	#	raise Exception('Wrong set of arguments')
