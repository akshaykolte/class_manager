from portal.models import Test, TestBatch, TestStaffRole
from portal.db_api import academic_year_db

def get_test(id=None, subject_year_id=None, academic_year_id=get_current_academic_year()['id'], batch_id=None, staff_role_id=None, standard_id=None):
	bit_list = []
	for i in [id, subject_year_id, academic_year_id, batch_id, staff_role_id, staff_role_id]:
		if i == None: bit_list.append('0')
		else: bit_list.append('1')
	if ''.join(bit_list) == '100000':
		test_obj = Test.objects.get(id=id)
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.name
		test['subject_year_id'] = test_obj.subject_year__id
		test['subject_year_name'] = test_obj.subject_year__name
		return test
	test_list = []
	if ''.join(bit_list) == '001001':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, subject_year__subject__standard__id=standard_id)
	elif ''.join(bit_list) == '001010':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '001011':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, teststaffrole__staff_role__id=staff_role_id, subject_year__subject__standard__id=standard_id)
	elif ''.join(bit_list) == '000100':
		test_list = Test.objects.filter(testbatch__batch__id=batch_id)
	elif ''.join(bit_list) == '000110':
		test_list = Test.objects.filter(testbatch__batch__id=batch_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '010010':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '010100':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, testbatch__batch__id=batch_id)
	elif ''.join(bit_list) == '010110':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, testbatch__batch__id=batch_id, teststaffrole__staff_role__id=staff_role_id)
	else:
		raise Exception('InvalidArguments')
	test_obj_list = []
	for test_obj in test_list:
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.name
		test['subject_year_id'] = test_obj.subject_year__id
		test['subject_year_name'] = test_obj.subject_year__name
		test_obj_list.append(test)
	return test_obj_list

def set_test(id=None, name=None, subject_year_id=None):
	if id!=None:
		# 011
		test_obj = Test(name=name, subject_year__id=subject_year_id)
		test_obj.save()
		return test_obj.id
	else:
		# 101, 110, 111
		test_obj = Test.objects.get(id=id)
		if name != None:
			test_obj.name = name
		if subject_year_id != None:
			test_obj.subject_year_id = subject_year_id
		test_obj.save()
		return test_obj.id

def set_test_of_batch(id=None, test_id=None, batch_id=None):
	if id!=None:
		# 011
		test_batch_obj = TestBatch(test__id=test_id, batch__id=batch_id)
		test_batch_obj.save()
		return test_batch_obj.id
	else:
		# 101, 110, 111
		test_batch_obj = Test.objects.get(id=id)
		if test_id != None:
			test_batch_obj.test = Test.objects.get(id=test_id)
		if batch_id != None:
			test_batch_obj.batch = Batch.objects.get(id=batch_id)
		test_batch_obj.save()
		return test_batch_obj.id

def set_test_of_staff_role(id=None, test_id=None, staff_role_id=None):
	if id!=None:
		# 011
		test_staff_role_obj = TestBatch(test__id=test_id, staff_role__id=batch_id)
		test_staff_role_obj.save()
		return test_staff_role_obj.id
	else:
		# 101, 110, 111
		test_staff_role_obj = TestStaffRole.objects.get(id=id)
		if test_id != None:
			test_staff_role_obj.test = Test.objects.get(id=test_id)
		if staff_role_id != None:
			test_staff_role_obj.staff_role = StaffRole.objects.get(id=staff_role_id)
		test_staff_role_obj.save()
		return test_staff_role_obj.id