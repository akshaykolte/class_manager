# set_base_fee
# get_base_fee
# add_transaction
# get_transaction (one or all of one student or of any particular type)

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
		
def get_base_fee(id = None , subject_years_list = None):
	#subject_years is list of subject_year ids eg. [1,2]
	
	#if 0 args return all base fee object DONE
	#else if id=none and subjectyearlist!=none specify return that object TODO
	is_none_id = id == None
	is_none_subject_years_list = subject_years_list == None
	
	if not is_none_id and not is_none_subject_years_list :
		raise Exception('Less than two arguments needed')
		
	if is_none_id and is_none_subject_years_list :
	
		base_fee_list=[]
		base_fee_objects = BaseFee.objects.all()
		print base_fee_objects
		for base_fee in base_fee_objects :
			base_fee_object = {}
			base_fee_object['id']=base_fee.id
			base_fee_object['amount']=base_fee.amount
			subject_year_list=[]
			
			print base_fee.subject_years
			
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
		print base_fee.subject_years
		
		for subject in base_fee.subject_years.all():
			subject_year_object = {}
			subject_year_object['id'] = subject.id
			subject_year_object['subject'] = subject.subject
			subject_year_object['academic_year'] = subject.academic_year
			subject_year_list.append(subject_year_object)
		base_fee_object['subject_years']=subject_year_list
		
		
		return base_fee_object
		
	'''if is_none_id and not is_none_subject_years_list :
		
		base_fee_object = {}
		
			
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

	
	
	
