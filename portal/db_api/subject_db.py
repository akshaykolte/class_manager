# set_subject
# get_subjects
# assign subjects to student
from portal.models import AcademicYear, Standard, StudentBatch, Subject, SubjectYear
from portal.db_api.academic_year_db import *


def set_subject(subject_id=None, standard_id=None, subject_name=None):

	is_subject_id_none = subject_id == None
	is_standard_id_none = standard_id == None
	is_subject_name_none = subject_name == None

	if is_subject_id_none and not is_standard_id_none and not is_subject_name_none:

		standard_object = Standard.objects.get(id=standard_id)
		subject_object = Subject(name=subject_name, standard=standard_object)

		subject_object.save()
		return subject_object.id

	elif not is_subject_id_none:

		subject_object = Subject.objects.get(id=subject_id)
		
		if not is_standard_id_none:
			subject_object.standard = Standard.objects.get(id=standard_id)

		if not is_subject_name_none:
			subject_object.name = subject_name

		subject_object.save()
		return subject_object.id

	else:
		raise Exception('Wrong parameters passed')

def set_subject_year(subject_id=None, year_id=None):

	is_subject_id_none = subject_id == None
	is_year_id_none = year_id == None

	if is_year_id_none:
		year_id = get_current_academic_year()['id']

	if not is_subject_id_none:

		subject_year_object = SubjectYear(subject=Subject.objects.get(id=subject_id), academic_year=AcademicYear.objects.get(id=year_id))

		subject_year_object.save()
		return subject_year_object.id

	else:
		raise Exception('Wrong parameters passed')


def get_subjects(subject_id=None, student_batch_id=None, batch_id=None, standard_id=None):

	'''
	subject_id 		student_batch_id	batch_id 	standard_id
		1					0				0			0			returns dict of that subject
		0					1				0			0			returns all subjects of that student
		0					0				1			0			returns all subjects of students in that batch
		0					0				0			1			returns all subjects pertaining to that standard
	'''

	is_subject_id_none = subject_id == None
	is_student_batch_id_none = student_batch_id == None
	is_batch_id_none = batch_id == None
	is_standard_id_none = standard_id == None


	if not is_subject_id_none and is_student_batch_id_none and is_batch_id_none and is_standard_id_none:

		subject_object = Subject.objects.get(id=subject_id)

		subject_dict={}
		subject_dict['id'] = subject_object.id
		subject_dict['name'] = subject_object.name
		subject_dict['standard_id'] = subject_object.standard.id
		subject_dict['standard_name'] = subject_object.standard.name

		return subject_dict

	elif is_subject_id_none and not is_student_batch_id_none and is_batch_id_none and is_standard_id_none:

		student_batch_object = StudentBatch.objects.get(id=student_batch_id)

		subject_year_list = [] 
		
		for i in student_batch_object.subject_years.all():
			subject_year_dict={}
			subject_year_dict['id'] = i.id
			subject_year_dict['subject_id'] = i.subject.id
			subject_year_dict['subject_name'] = i.subject.name
			subject_year_dict['standard_id'] = i.subject.standard.id
			subject_year_dict['standard_name'] = i.subject.standard.name
			subject_year_dict['year_id'] = i.academic_year.id
			subject_year_list.append(subject_year_dict)


		student_dict = {}
		student_dict['id'] = student_batch_object.id
		student_dict['name'] = student_batch_object.student.first_name + ' ' + student_batch_object.student.last_name
		student_dict['batch_id'] = student_batch_object.batch.id 
		student_dict['batch_name'] = student_batch_object.batch.name
		student_dict['subjects'] = subject_year_list

		return student_dict

	elif is_subject_id_none and is_student_batch_id_none and not is_batch_id_none and is_standard_id_none:
		pass

	elif is_subject_id_none and is_student_batch_id_none and is_batch_id_none and not is_standard_id_none:
		pass

	else:
		raise Exception('Wrong parameters passed')
