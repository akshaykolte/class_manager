'''

set_test(id=None, name=None, subject_year_id=None):
	# 011, 101, 110, 111

get_test(id=None, subject_year_id=None, academic_year_id=get_current_academic_year()['id'], batch_id=None, staff_role_id=None, standard_id=None):
	# 001001, 001010, 001011, 000100, 000110, 010010, 010100, 010110, 100000

set_test_of_batch(id=None, test_id=None, batch_id=None):
	# 011, 101, 110, 111
	
set_test_of_staff_role(id=None, test_id=None, staff_role_id=None):
	# 011, 101, 110, 111
'''