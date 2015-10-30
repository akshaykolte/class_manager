from portal.models import Test, TestBatch, TestStaffRole, Batch, SubjectYear, StaffRole, TestStudentBatch, StudentBatch
from portal.db_api.academic_year_db import get_current_academic_year

def get_test(id=None, subject_year_id=None, academic_year_id=None, batch_id=None, staff_role_id=None, standard_id=None, staff_id=None):
	bit_list = []
	for i in [id, subject_year_id, academic_year_id, batch_id, staff_role_id, standard_id, staff_id]:
		if i == None: bit_list.append('0')
		else: bit_list.append('1')
	if ''.join(bit_list) == '1000000':
		test_obj = Test.objects.get(id=id)
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.name
		test['subject_year_id'] = test_obj.subject_year.id
		test['subject_year_name'] = test_obj.subject_year.subject.name + ' - ' + test_obj.subject_year.subject.standard.name
		test['standard_id'] = test_obj.subject_year.subject.standard.id
		test['standard_name'] = test_obj.subject_year.subject.standard.name
		test['total_marks'] = test_obj.total_marks
		return test
	if academic_year_id == None:
		academic_year_id = get_current_academic_year()['id']
	test_list = []
	if ''.join(bit_list) == '0010010':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, subject_year__subject__standard__id=standard_id)
	elif ''.join(bit_list) == '0010100':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '0010110':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, teststaffrole__staff_role__id=staff_role_id, subject_year__subject__standard__id=standard_id)
	elif ''.join(bit_list) == '0001000':
		test_list = Test.objects.filter(testbatch__batch__id=batch_id)
	elif ''.join(bit_list) == '0001100':
		test_list = Test.objects.filter(testbatch__batch__id=batch_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '0100100':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '0101000':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, testbatch__batch__id=batch_id)
	elif ''.join(bit_list) == '0101100':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, testbatch__batch__id=batch_id, teststaffrole__staff_role__id=staff_role_id)
	elif ''.join(bit_list) == '0100000':
		test_list = Test.objects.filter(subject_year__id = subject_year_id)
	elif ''.join(bit_list) == '0101001':
		test_list = Test.objects.filter(subject_year__id = subject_year_id, testbatch__batch__id=batch_id, teststaffrole__staff_role__staff__id=staff_id)
	elif ''.join(bit_list) == '0000001':
		test_list = Test.objects.filter(subject_year__academic_year__id=academic_year_id, teststaffrole__staff_role__staff__id=staff_id)
	else:
		raise Exception('InvalidArguments')
	test_obj_list = []
	for test_obj in test_list:
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.name
		test['subject_year_id'] = test_obj.subject_year.id
		test['subject_year_name'] = test_obj.subject_year.subject.name + ' - ' + test_obj.subject_year.subject.standard.name
		test['standard_id'] = test_obj.subject_year.subject.standard.id
		test['standard_name'] = test_obj.subject_year.subject.standard.name
		test['total_marks'] = test_obj.total_marks
		test_obj_list.append(test)
	return test_obj_list

def set_test(id=None, name=None, marks=None, subject_year_id=None):
	if id == None and marks != None and subject_year_id != None:
		# 011
		test_obj = Test(name=name,total_marks=marks, subject_year=SubjectYear.objects.get(id=subject_year_id))
		test_obj.save()
		return test_obj.id
	else:
		# 101, 110, 111
		test_obj = Test.objects.get(id=id)
		if name != None:
			test_obj.name = name
		if subject_year_id != None:
			test_obj.subject_year_id = subject_year_id
		if marks != None:
			test_obj.total_marks = marks
		test_obj.save()
		return test_obj.id

def set_test_of_batch(id=None, test_id=None, batch_id=None):
	if id == None:
		# 011
		test_batch_obj = TestBatch(test=Test.objects.get(id=test_id), batch=Batch.objects.get(id=batch_id))
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
	if id == None:
		# 011
		test_staff_role_obj = TestStaffRole(test=Test.objects.get(id=test_id), staff_role = StaffRole.objects.get(id=staff_role_id))
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

def get_batches_of_test(id=None, test_id=None):
	if id != None and test_id == None:
		test_obj = TestBatch.objects.get(id=id)
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.test.name
		test['subject_year_id'] = test_obj.test.subject_year.id
		test['subject_year_name'] = test_obj.test.subject_year.subject.name + ' - ' + test_obj.test.subject_year.subject.standard.name
		test['batch_id'] = test_obj.batch.id
		test['batch_name'] = test_obj.batch.name
		test['branch_id'] = test_obj.batch.branch.id
		test['branch_name'] = test_obj.batch.branch.name
		return test

	test_obj_list = []
	if id == None and test_id != None:
		test_obj_list = TestBatch.objects.filter(test__id=test_id)

	test_list = []
	for test_obj in test_obj_list:
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.test.name
		test['subject_year_id'] = test_obj.test.subject_year.id
		test['subject_year_name'] = test_obj.test.subject_year.subject.name + ' - ' + test_obj.test.subject_year.subject.standard.name
		test['batch_id'] = test_obj.batch.id
		test['batch_name'] = test_obj.batch.name
		test['branch_id'] = test_obj.batch.branch.id
		test['branch_name'] = test_obj.batch.branch.name
		test_list.append(test)

	return test_list

def get_teachers_of_test(id=None, test_id=None):
	if id != None:
		test_obj = TestStaffRole.objects.get(id=id)
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.test.name
		test['subject_year_id'] = test_obj.test.subject_year.id
		test['subject_year_name'] = test_obj.test.subject_year.subject.name + ' - ' + test_obj.test.subject_year.subject.standard.name
		test['staff_role_id'] = test_obj.staff_role.id
		test['staff_name'] = test_obj.staff_role.staff.first_name + ' ' + test_obj.staff_role.staff.last_name
		return test

	test_obj_list = []
	if test_id != None:
		test_obj_list = TestStaffRole.objects.filter(test__id=test_id)

	test_list = []
	for test_obj in test_obj_list:
		test = {}
		test['id'] = test_obj.id
		test['name'] = test_obj.test.name
		test['subject_year_id'] = test_obj.test.subject_year.id
		test['subject_year_name'] = test_obj.test.subject_year.subject.name + ' - ' + test_obj.test.subject_year.subject.standard.name
		test['staff_role_id'] = test_obj.staff_role.id
		test['staff_id'] = test_obj.staff_role.staff.id
		test['staff_name'] = test_obj.staff_role.staff.first_name + ' ' + test_obj.staff_role.staff.last_name
		test_list.append(test)

	return test_list

def delete_test_of_batch(id=None, test_id=None, batch_id=None):
	if id != None:
		# 100
		TestBatch.objects.filter(id=id).delete()
	elif test_id != None and batch_id != None:
		# 011
		TestBatch.objects.filter(test__id=test_id, batch__id=batch_id).delete()

def delete_test_of_staff_role(id=None, test_id=None, staff_id=None):
	if id != None:
		# 100
		TestStaffRole.objects.filter(id=id).delete()
	elif test_id != None and staff_id != None:
		# 011
		TestStaffRole.objects.filter(test__id=test_id, staff_role__staff__id=staff_id).delete()

def set_student_marks(id=None, test_id=None, student_batch_id=None, marks_obtained=None):
	if id == None:
		if TestStudentBatch.objects.filter(test__id=test_id, student_batch__id=student_batch_id).exists():
			test_student_batch_object = TestStudentBatch.objects.get(test__id=test_id, student_batch__id=student_batch_id)
			test_student_batch_object.obtained_marks = marks_obtained
			test_student_batch_object.save()
		else:
			test_student_batch_object = TestStudentBatch(test=Test.objects.get(id=test_id), student_batch=StudentBatch.objects.get(id=student_batch_id), obtained_marks=marks_obtained)
			test_student_batch_object.save()
		return test_student_batch_object.id
	else:
		test_student_batch_object = TestStudentBatch.objects.get(id=id)
		test_student_batch_object.marks_obtained = marks_obtained
		test_student_batch_object.save()
		return test_student_batch_object.id

def get_student_batch_marks(id=None, test_id=None, batch_id=None, student_batch_id=None):
	# valid combinations: 1000, 0101, 0001, 0010, 0110

	if id != None and test_id == None and batch_id == None and student_batch_id == None:
		# 1000
		test_student_batch_object = TestStudentBatch.objects.get(id=id)
		test_student_batch = {}
		test_student_batch['id'] = test_student_batch_object.id
		test_student_batch['student_batch_id'] = test_student_batch_object.student_batch.id
		test_student_batch['student_name'] = test_student_batch_object.student_batch.student.first_name + ' ' + test_student_batch_object.student_batch.student.last_name
		test_student_batch['batch_id'] = test_student_batch_object.student_batch.batch.id
		test_student_batch['batch_name'] = test_student_batch_object.student_batch.batch.name
		test_student_batch['obtained_marks'] = test_student_batch_object.obtained_marks
		return test_student_batch
	elif id == None and test_id != None and batch_id == None and student_batch_id != None:
		# 0101
		test_student_batch_object = TestStudentBatch.objects.get(test__id=test_id, student_batch__id=student_batch_id)
		test_student_batch = {}
		test_student_batch['id'] = test_student_batch_object.id
		test_student_batch['student_batch_id'] = test_student_batch_object.student_batch.id
		test_student_batch['student_name'] = test_student_batch_object.student_batch.student.first_name + ' ' + test_student_batch_object.student_batch.student.last_name
		test_student_batch['batch_id'] = test_student_batch_object.student_batch.batch.id
		test_student_batch['batch_name'] = test_student_batch_object.student_batch.batch.name
		test_student_batch['obtained_marks'] = test_student_batch_object.obtained_marks
		return test_student_batch
	elif id == None and test_id == None and batch_id == None and student_batch_id != None:
		# 0001
		student_batch_object_list = TestStudentBatch.objects.filter(student_batch__id=student_batch_id)
	elif id == None and test_id == None and batch_id != None and student_batch_id == None:
		# 0010
		student_batch_object_list = TestStudentBatch.objects.filter(student_batch__batch__id=batch_id)
	elif id == None and test_id != None and batch_id != None and student_batch_id == None:
		# 0110
		student_batch_object_list = TestStudentBatch.objects.filter(student_batch__batch__id=batch_id, test__id=test_id)
	else:
		raise Exception('InvalidArguments')

	student_batch_list = []
	for test_student_batch_object in student_batch_object_list:
		test_student_batch = {}
		test_student_batch['id'] = test_student_batch_object.id
		test_student_batch['student_batch_id'] = test_student_batch_object.student_batch.id
		test_student_batch['student_name'] = test_student_batch_object.student_batch.student.first_name + ' ' + test_student_batch_object.student_batch.student.last_name
		test_student_batch['batch_id'] = test_student_batch_object.student_batch.batch.id
		test_student_batch['batch_name'] = test_student_batch_object.student_batch.batch.name
		test_student_batch['test_name'] = test_student_batch_object.test.name
		test_student_batch['total_marks'] = test_student_batch_object.test.total_marks
		test_student_batch['subject_name'] = test_student_batch_object.test.subject_year.subject.name
		test_student_batch['obtained_marks'] = test_student_batch_object.obtained_marks
		student_batch_list.append(test_student_batch)
	return student_batch_list

def check_test_staff_permission(staff_id, test_id):
	return TestStaffRole.objects.filter(staff_role__staff__id=staff_id, test__id=test_id).exists()
