from error_codes import ErrorCode

error_object = ErrorCode()

class ModelValidateError(Exception):
	pass

class PentaError:
	error_string = ''
	def __init__(self, error=None):
		if error != None:
			self.error_string = error_object[int(error)]
	def __nonzero__(self):
		if self.error_string == '':
			return True
		else:
			return False
	def __str__(self):
		return self.error_string

	def raise_error(self):
		raise ModelValidateError(self.error_string)

def validate_academic_year(academic_year_object):
	# No special dependency
	from portal.models import AcademicYear
	if academic_year_object.is_current == True and AcademicYear.objects.filter(is_current=True).count() > 0:
		return PentaError(1016)
	return PentaError()

def validate_branch(branch_object):
	# No special dependency
	return PentaError()

def validate_standard(standard_object):
	# No special dependency
	return PentaError()

def validate_batch(batch_object):
	# No special dependency
	return PentaError()

def validate_student(student_object):
	# No special dependency
	return PentaError()

def validate_parent(parent_object):
	# No special dependency
	return PentaError()

def validate_student_parent(student_parent_object):
	# No special dependency
	return PentaError()

def validate_student_batch(student_batch_object, subject_year_id_list):
	# print student_batch_object, subject_year_id_list
	from portal.models import SubjectYear, StudentBatch
	if student_batch_object.standard == None and student_batch_object.academic_year == None and student_batch_object.batch != None:
		for subject_year_id in subject_year_id_list:
			subject_year_object = SubjectYear.objects.get(id=subject_year_id)
			if student_batch_object.batch.academic_year != subject_year_object.academic_year:
				return PentaError(1001)
			if student_batch_object.batch.standard != subject_year_object.subject.standard:
				return PentaError(1002)
			if student_batch_object.id == None:
				# True when creating new StudentBatch object
				if (StudentBatch.objects.filter(student = student_batch_object.student, academic_year=student_batch_object.batch.academic_year).count() + StudentBatch.objects.filter(student = student_batch_object.student, batch__academic_year=student_batch_object.batch.academic_year).count() ) > 0:
					return PentaError(1003) # StudentBatch of academic_year already exists
			else:
				if (StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, academic_year=student_batch_object.batch.academic_year).count() + StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, batch__academic_year=student_batch_object.batch.academic_year).count() ) > 0:
					return PentaError(1004) # StudentBatch of academic_year already exists
		return PentaError()
	elif student_batch_object.standard != None and student_batch_object.academic_year != None and student_batch_object.batch == None:
		for subject_year_id in subject_year_id_list:
			subject_year_object = SubjectYear.objects.get(id=subject_year_id)
			if student_batch_object.academic_year != subject_year_object.academic_year:
				return PentaError(1005)
			if student_batch_object.standard != subject_year_object.subject.standard:
				return PentaError(1006)
			if student_batch_object.id == None:
				# True when creating new StudentBatch object
				if (StudentBatch.objects.filter(student = student_batch_object.student, academic_year=student_batch_object.academic_year).count() + StudentBatch.objects.filter(student = student_batch_object.student, batch__academic_year=student_batch_object.academic_year).count() ) > 0:
					return PentaError(1007) # StudentBatch of academic_year already exists
			else:
				if (StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, academic_year=student_batch_object.academic_year).count() + StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, batch__academic_year=student_batch_object.academic_year).count() ) > 0:
					return PentaError(1008) # StudentBatch of academic_year already exists

		return PentaError()
	else:
		return PentaError(1009)

def validate_staff(staff_object):
	# No special dependency
	return PentaError()

def validate_role(role_object):
	# No special dependency
	return PentaError()

def validate_staff_role(staff_role_object):
	# No special dependency
	return PentaError()

def validate_subject(subject_object):
	# No special dependency
	return PentaError()


def validate_subject_year(subject_year_object):
	# No special dependency
	return PentaError()

def validate_lecture(lecture_object):
	# No special dependency
	return PentaError()

def validate_lecture_batch(lecture_batch_object):
	if lecture_batch_object.batch.academic_year != lecture_batch_object.lecture.subject_year.academic_year:
		return PentaError(1010)
	elif lecture_batch_object.staff_role.role.name != 'teacher' or (lecture_batch_object.staff_role.branch != lecture_batch_object.batch.branch):
		return PentaError(1011)
	elif lecture_batch_object.batch.standard != lecture_batch_object.lecture.subject_year.subject.standard:
		return PentaError(1012)
	else:
		return PentaError()

def validate_attendance(attendance_object):
	subject_year_list = attendance_object.student_batch.subject_years.all()
	for subject_year_object in subject_year_list:
		if subject_year_object == attendance_object.lecture_batch.lecture.subject_year:
			return PentaError()
	return PentaError(1013)

def validate_base_fee(base_fee_object, subject_year_id_list):
	from portal.models import SubjectYear, BaseFee
	from django.db.models import Count
	if len(subject_year_id_list) == 0:
		return PentaError()
	academic_year = SubjectYear.objects.get(id=subject_year_id_list[0]).academic_year
	standard = SubjectYear.objects.get(id=subject_year_id_list[0]).subject.standard
	base_fees = BaseFee.objects.annotate(count=Count('subject_years')).filter(subject_years=subject_year_id_list[0])
	for i in subject_year_id_list:
		base_fees = base_fees.filter(subject_years=i)
		subject_year_object = SubjectYear.objects.get(id=i)
		if academic_year != subject_year_object.academic_year:
			return PentaError(1014)
		if standard != subject_year_object.subject.standard:
			return PentaError(1015)
	base_fees = base_fees.filter(count=len(subject_year_id_list))
	if len(base_fees) > 0:
		return PentaError(1048)
	return PentaError()

def validate_fee_type(fee_type_object):
	# No special dependency
	return PentaError()

def validate_fee_transaction(fee_transaction_object):
	# No special dependency
	return PentaError()

def validate_notice_viewer(notice_viewer_object):
	if notice_viewer_object.for_staff == True and notice_viewer_object.for_students == True:
		return PentaError(1036)
	if notice_viewer_object.for_staff == False and notice_viewer_object.for_students == False:
		return PentaError(1037)
	if notice_viewer_object.for_students == True:
		count = 0
		if notice_viewer_object.batch != None:
			count += 1
		if notice_viewer_object.student != None:
			count += 1
		if notice_viewer_object.branch != None:
			count += 1
		if count > 1:
			return PentaError(1038)
	if notice_viewer_object.for_staff == True:
		if notice_viewer_object.batch != None:
			return PentaError(1039)
		if notice_viewer_object.staff != None:
			pass
		if notice_viewer_object.branch != None:
			return PentaError(1039)
	return PentaError()

def validate_test_batch(test_batch_object):
	if test_batch_object.batch.academic_year != test_batch_object.test.subject_year.academic_year:
		return PentaError(1045)
	if test_batch_object.batch.standard != test_batch_object.test.subject_year.subject.standard:
		return PentaError(1046)
	return PentaError()

def validate_test_student_batch(test_student_batch_object):
	from portal.models import TestBatch
	if TestBatch.objects.filter(test=test_student_batch_object.test, batch=test_student_batch_object.student_batch.batch).count() == 0:
		return PentaError(1047)
	return PentaError()
