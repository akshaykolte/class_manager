from portal.models import *

def validate_academic_year(academic_year_object):
	# No special dependency
	return True

def validate_branch(branch_object):
	# No special dependency
	return True

def validate_standard(standard_object):
	# No special dependency
	return True

def validate_batch(batch_object):
	return True

def validate_student(student_object):
	return True

def validate_parent(parent_object):
	return True

def validate_student_parent(student_parent_object):
	return True

def validate_staff(staff_object):
	return True

def validate_role(role_object):
	return True

def validate_staff_role(staff_role_object):
	return True

def validate_subject(subject_object):
	return True

def validate_subject_year(subject_year_object):
	return True

def validate_lecture(lecture_object):
	return True

def validate_lecture_batch(lecture_batch_object):

	if lecture_batch_object.batch.academic_year.id == lecture_batch_object.lecture.subject_year.academic_year.id:
		return True
	else:
		return False

def validate_attendance(attendance_object):
	return True

def validate_base_fee(base_fee_object):
	return True

def validate_fee_type(fee_type_object):
	return True

def validate_fee_transaction(fee_transaction_object):
	return True