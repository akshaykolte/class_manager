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
	# No special dependency
	return True

def validate_student(student_object):
	# No special dependency
	return True

def validate_parent(parent_object):
	# No special dependency
	return True

def validate_student_parent(student_parent_object):
	# No special dependency
	return True

def validate_student_batch(student_batch_object, subject_year_id_list):
	print student_batch_object, subject_year_id_list
	from portal.models import SubjectYear, StudentBatch
	if student_batch_object.standard == None and student_batch_object.academic_year == None and student_batch_object.batch != None:
		for subject_year_id in subject_year_id_list:
			subject_year_object = SubjectYear.objects.get(id=subject_year_id)
			if student_batch_object.batch.academic_year != subject_year_object.academic_year:
				return False
			if student_batch_object.batch.standard != subject_year_object.subject.standard:
				return False
			if student_batch_object.id == None:
				# True when creating new StudentBatch object
				if (StudentBatch.objects.filter(student = student_batch_object.student, academic_year=student_batch_object.batch.academic_year).count() + StudentBatch.objects.filter(student = student_batch_object.student, batch__academic_year=student_batch_object.batch.academic_year).count() ) > 0:
					return False # StudentBatch of academic_year already exists
			else:
				if (StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, academic_year=student_batch_object.batch.academic_year).count() + StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, batch__academic_year=student_batch_object.batch.academic_year).count() ) > 0:
					return False # StudentBatch of academic_year already exists
		return True
	elif student_batch_object.standard != None and student_batch_object.academic_year != None and student_batch_object.batch == None:
		for subject_year_id in subject_year_id_list:
			subject_year_object = SubjectYear.objects.get(id=subject_year_id)
			if student_batch_object.academic_year != subject_year_object.academic_year:
				return False
			if student_batch_object.standard != subject_year_object.subject.standard:
				return False
			if student_batch_object.id == None:
				# True when creating new StudentBatch object
				if (StudentBatch.objects.filter(student = student_batch_object.student, academic_year=student_batch_object.academic_year).count() + StudentBatch.objects.filter(student = student_batch_object.student, batch__academic_year=student_batch_object.academic_year).count() ) > 0:
					return False # StudentBatch of academic_year already exists
			else:
				if (StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, academic_year=student_batch_object.academic_year).count() + StudentBatch.objects.exclude(id=student_batch_object.id).filter(student = student_batch_object.student, batch__academic_year=student_batch_object.academic_year).count() ) > 0:
					return False # StudentBatch of academic_year already exists

		return True
	else:
		return False

def validate_staff(staff_object):
	# No special dependency
	return True

def validate_role(role_object):
	# No special dependency
	return True

def validate_staff_role(staff_role_object):
	# No special dependency
	return True

def validate_subject(subject_object):
	# No special dependency
	return True


def validate_subject_year(subject_year_object):
	# No special dependency
	return True

def validate_lecture(lecture_object):
	# No special dependency
	return True

def validate_lecture_batch(lecture_batch_object):
	if lecture_batch_object.batch.academic_year != lecture_batch_object.lecture.subject_year.academic_year:
		return False
	elif lecture_batch_object.staff_role.role.name != 'teacher' or (lecture_batch_object.staff_role.branch != lecture_batch_object.batch.branch):
		return False
	elif lecture_batch_object.batch.standard != lecture_batch_object.lecture.subject_year.subject.standard:
		return False
	else:
		return True

def validate_attendance(attendance_object):
	subject_year_list = attendance_object.student_batch.subject_years.all()
	for subject_year_object in subject_year_list:
		if subject_year_object == attendance_object.lecture_batch.lecture.subject_year:
			return True
	return False

def validate_base_fee(base_fee_object, subject_year_id_list):
	from portal.models import SubjectYear
	if len(subject_year_id_list) == 0:
		return True
	academic_year = SubjectYear.objects.get(id=subject_year_id_list[0]).academic_year
	standard = SubjectYear.objects.get(id=subject_year_id_list[0]).subject.standard
	for i in subject_year_id_list:
		subject_year_object = SubjectYear.objects.get(id=i)
		if academic_year != subject_year_object.academic_year:
			return False
		if standard != subject_year_object.subject.standard:
			return False
	return True

def validate_fee_type(fee_type_object):
	# No special dependency
	return True

def validate_fee_transaction(fee_transaction_object):
	# No special dependency
	return True
