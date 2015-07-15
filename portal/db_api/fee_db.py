# set_base_fee
# get_base_fee
# add_transaction
# get_transaction (one or all of one student or of any particular type)

from portal.models import *

def set_base_fee(id = None ,amount=None , subject_years_list = None):
	#subject_years is list of subject_year ids eg. {1,2}
	is_none_id = id == None
	is_none_amount = amount == None
	is_none_subject_years = subject_years_list == None
	if is_none_amount and is_none_subject_years_list :
		raise Exception('Minimum two arguments needed')
	if is_none_id:
		print subject_years_list
		base_fee_object = BaseFee.objects.create()
		
		for subject_year_id in subject_years_list :
			subject_year_object = SubjectYear.objects.get(id = subject_year_id)
			
		base_fee_object.subject_years = subject_years_list 
			
		
		return base_fee_object.id











