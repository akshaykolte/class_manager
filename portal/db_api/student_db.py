# get_students (individual, of batch, of branch, all) return: all details, batch details, branch details and subject details
# set_student (add or modify if already exists, if batch_id is present then assign student to that batch) return: id
# get_parent(from student) return: parent details
# set_parent(student_id as a parameter) return: id
# get_previous_students (pass batch_id as parameter)

# !!!!!!!!!!!!!!!!!!!!!!!!
	# 1. set_student_batch(student_batch_id,student_id,batch_id,subject_year_id_list)

	# 2. get_student_batch(student_batch_id,batch_id,standard_id,academic_year_id,student_id)
		# if academic_year_id is None then academic_year_id = get_current_academic_year()['id']
		# possible combinations: 00001,00011,00110,01000,10000


# !!!!!!!!!!!!!!!!!!!!!!!!

from portal.models import Student,Parent,StudentParent,Batch,StudentBatch,SubjectYear,Standard, Branch
from portal.db_api.academic_year_db import *
from django.db.models import Q
from portal.validator.validator import PentaError

def get_students(id = None,batch_id = None, subject_year_id = None):
	is_none_id = id == None
	is_none_batch_id = batch_id == None
	is_none_subject_year_id = subject_year_id == None

	if not is_none_id and is_none_batch_id and is_none_subject_year_id:
		student_object = {}
		student = Student.objects.get(id=id)
		student_object['id'] = student.id
		student_object['username'] = student.username
		student_object['password'] = student.password
		student_object['first_name'] = student.first_name
		student_object['last_name'] = student.last_name
		student_object['address'] = student.address
		student_object['email'] = student.email
		student_object['phone_number'] = student.phone_number
		student_object['gender'] = student.gender
		return student_object

	elif not is_none_batch_id  and is_none_subject_year_id:
		student_list = []
		student_batch = StudentBatch.objects.filter(batch = Batch.objects.get(id = batch_id))
		for i in student_batch:
			student_dict = {}
			student_dict['id'] = i.student.id
			student_dict['username'] = i.student.username
			student_dict['password'] = i.student.password
			student_dict['first_name'] = i.student.first_name
			student_dict['last_name'] = i.student.last_name
			student_dict['address'] = i.student.address
			student_dict['email'] = i.student.email
			student_dict['phone_number'] = i.student.phone_number
			student_dict['gender'] = i.student.gender
			student_dict['batch'] = i.batch
			subject_year_list = []
			for j in i.subject_years.all():
				subject_year_dict={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
			student_dict['subjects'] = subject_year_list
			student_list.append(student_dict)
		return student_list
	elif is_none_id and is_none_batch_id and is_none_subject_year_id:
		student_list = []
		student = Student.objects.all()
		for i in student:
			student_dict = {}
			student_dict['id'] = i.id
			student_dict['username'] = i.username
			student_dict['password'] = i.password
			student_dict['first_name'] = i.first_name
			student_dict['last_name'] = i.last_name
			student_dict['address'] = i.address
			student_dict['email'] = i.email
			student_dict['phone_number'] = i.phone_number
			student_dict['gender'] = i.gender
		return student_list
	elif is_none_id and not is_none_batch_id and not is_none_subject_year_id:
		student_list = []
		student_batch = StudentBatch.objects.filter(batch = Batch.objects.get(id = batch_id), subject_years__id=subject_year_id)
		for i in student_batch:
			student_dict = {}
			student_dict['id'] = i.student.id
			student_dict['username'] = i.student.username
			student_dict['password'] = i.student.password
			student_dict['first_name'] = i.student.first_name
			student_dict['last_name'] = i.student.last_name
			student_dict['address'] = i.student.address
			student_dict['email'] = i.student.email
			student_dict['phone_number'] = i.student.phone_number
			student_dict['gender'] = i.student.gender
			student_dict['batch'] = i.batch
			subject_year_list = []
			for j in i.subject_years.all():
				subject_year_dict={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
			student_dict['subjects'] = subject_year_list
			student_list.append(student_dict)
		return student_list


def get_parent(id = None,student_id = None):
	is_none_id = id == None
	is_none_student_id = student_id == None

	if not is_none_id:
		parent_object = {}
		parent = Parent.objects.get(id=id)
		parent_object['id'] = parent.id
		parent_object['username'] = parent.username
		parent_object['password'] = parent.password
		parent_object['first_name'] = parent.first_name
		parent_object['last_name'] = parent.last_name
		parent_object['address'] = parent.address
		parent_object['email'] = parent.email
		parent_object['phone_number'] = parent.phone_number
		parent_object['gender'] = parent.gender
		return parent_object

	if not is_none_student_id:
		parent_object = {}

		if not StudentParent.objects.filter(student = Student.objects.get(id = student_id)).exists():
			return parent_object
		student_parent_object = StudentParent.objects.get(student = Student.objects.get(id = student_id))
		parent = student_parent_object.parent
		parent_object['id'] = parent.id
		parent_object['username'] = parent.username
		parent_object['password'] = parent.password
		parent_object['first_name'] = parent.first_name
		parent_object['last_name'] = parent.last_name
		parent_object['address'] = parent.address
		parent_object['email'] = parent.email
		parent_object['phone_number'] = parent.phone_number
		parent_object['gender'] = parent.gender
		return parent_object




def set_student(id=None,username=None,password=None, parent_id = None,batch_id= None, first_name=None ,last_name=None ,address=None, email=None, phone_number=None, gender=None ):

	is_none_id = id == None
	is_none_username = username == None
	is_none_password = password == None
	is_none_parent_id = parent_id == None
	is_none_batch_id = batch_id == None
	is_none_first_name = first_name == None
	is_none_last_name = last_name == None
	is_none_address = address == None
	is_none_email = email == None
	is_none_phone_number = phone_number == None
	is_none_gender = gender == None

	if is_none_id:
		student_object = Student(username = username,password = password,first_name = first_name,last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender)
		student_object.save()
		if not is_none_batch_id:
			student_batch_object = Student_batch(student = student_object,batch = Batch.objects.get(id = batch_id))
			student_batch_object.save()
			return student_batch_object.id
		if not is_none_parent_id:
			parent_object = Parent.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		return student_object.id

	elif not is_none_id:
		student_object = Student.objects.get(id=id)
		if not is_none_batch_id:
			student_batch_object = StudentBatch(student = student_object,batch = Batch.objects.get(id = batch_id))
			student_batch_object.save()

		if not is_none_parent_id:
			parent_object = Parent.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		if not is_none_username:
			student_object.username = username
		if not is_none_password:
			student_object.password = password
		if not is_none_first_name:
			student_object.first_name = first_name
		if not is_none_last_name:
			student_object.last_name = last_name
		if not is_none_address:
			student_object.address = address
		if not is_none_email:
			student_object.email = email
		if not is_none_phone_number:
			student_object.phone_number = phone_number
		if not is_none_gender:
			student_object.gender = gender
		student_object.save()
		return student_object.id
	else:
		raise Exception ('Enter all fields')

def set_parent(id=None,username = None,password = None, student_id = None, first_name=None ,last_name=None ,address=None, email=None, phone_number=None, gender=None ):

	is_none_id = id == None
	is_none_username = username == None
	is_none_password = password == None
	is_none_student_id = student_id == None
	is_none_first_name = first_name == None
	is_none_last_name = last_name == None
	is_none_address = address == None
	is_none_email = email == None
	is_none_phone_number = phone_number == None
	is_none_gender = gender == None

	if is_none_id:
		parent_object = Parent(first_name = first_name,last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender, username=username, password=password)
		parent_object.save()
		if not is_none_student_id:
			student_object = Student.objects.get(id=student_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		return parent_object.id

	elif not is_none_id:
		parent_object = Parent.objects.get(id=id)
		if not is_none_username:
			parent_object.username = username
		if not is_none_password:
			parent_object.password = password
		if not is_none_student_id:
			student_object = Student.objects.get(id=student_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()

		if not is_none_first_name:
			parent_object.first_name = first_name
		if not is_none_last_name:
			parent_object.last_name = last_name
		if not is_none_address:
			parent_object.address = address
		if not is_none_email:
			parent_object.email = email
		if not is_none_phone_number:
			parent_object.phone_number = phone_number
		if not is_none_gender:
			parent_object.gender = gender
		parent_object.save()
		return parent_object.id
	else:
		raise Exception ('Enter all fields')

def set_student_batch(id=None,student_id=None,batch_id=None,subject_year_id_list=None, academic_year_id=None, standard_id=None):
	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_batch_id = batch_id == None
	is_none_subject_year_id_list = subject_year_id_list == None

	if is_none_id:
		if batch_id != None and academic_year_id == None and standard_id == None:
			student_batch_object = StudentBatch(student = Student.objects.get(id = student_id),batch = Batch.objects.get(id = batch_id))
		elif batch_id == None and academic_year_id != None and standard_id != None:
			student_batch_object = StudentBatch(student = Student.objects.get(id = student_id),academic_year = AcademicYear.objects.get(id=academic_year_id), standard=Standard.objects.get(id=standard_id))
		else:
			return None
		# if not is_none_subject_year_id_list and len(subject_year_id_list)==0:
		# 	# TODO: Bad design, consider overriding .save() to accomodate
		# 	# subject_year_list (and other similar multi-fields) to save
		# 	# data in the overriden functions
		# 	PentaError(1051).raise_error()
		student_batch_object.save(validate = True, subject_year_id_list = subject_year_id_list)
		if not is_none_subject_year_id_list:
			for subject_year_id in subject_year_id_list:
				subject_year_object = SubjectYear.objects.get(id = subject_year_id)
				student_batch_object.subject_years.add(subject_year_object)
		student_batch_object.save()
		return student_batch_object.id

	else:
		student_batch_object = StudentBatch.objects.get(id = id)
		if not is_none_student_id:
			student_batch_object.student = Student.objects.get(id = student_id)
		if not is_none_batch_id:
			student_batch_object.batch = Batch.objects.get(id = batch_id)
		if not is_none_subject_year_id_list:
			for subject_year_id in subject_year_id_list:
				subject_year_object = SubjectYear.objects.get(id = subject_year_id)
				student_batch_object.subject_years.add(subject_year_object)
		student_batch_object.save()
		return student_batch_object.id


def get_student_batch(id=None,batch_id=None,standard_id=None,academic_year_id=None,student_id=None, batch_assigned=True):
	# if academic_year_id is None then academic_year_id = get_current_academic_year()['id']
	# possible combinations: 000010,000110,001101,010000,100000
	is_none_id = id == None
	is_none_batch_id = batch_id == None
	is_none_standard_id = standard_id == None
	is_none_academic_year_id = academic_year_id == None
	is_none_student_id = student_id == None

	#000010
	if not is_none_student_id and is_none_id and is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(student = Student.objects.get(id = student_id),batch__academic_year = AcademicYear.objects.get(id =get_current_academic_year()['id']))
		student_batch = {}
		student_batch['id'] = student_batch_object.id
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
		student_batch['student_batch_id'] = student_batch_object.batch.id
		student_batch['student_batch_name'] = student_batch_object.batch.name
		student_batch['student_batch_description'] = student_batch_object.batch.description
		subject_year_list = []
		for j in student_batch_object.subject_years.all():
			subject_year_dict ={}
			subject_year_dict['id'] = j.id
			subject_year_dict['subject_id'] = j.subject.id
			subject_year_dict['subject_name'] = j.subject.name
			subject_year_dict['standard_id'] = j.subject.standard.id
			subject_year_dict['standard_name'] = j.subject.standard.name
			subject_year_dict['year_id'] = j.academic_year.id
			subject_year_list.append(subject_year_dict)
		student_batch['student_subjects'] = subject_year_list
		return student_batch

	#000110
	if not is_none_student_id and is_none_id and is_none_batch_id and is_none_standard_id and not is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(student = Student.objects.get(id = student_id),batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id = academic_year_id)))
		student_batch = {}
		student_batch['id'] = student_batch_object.id
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
		student_batch['student_batch_id'] = student_batch_object.batch.id
		student_batch['student_batch_name'] = student_batch_object.batch.name
		student_batch['student_batch_description'] = student_batch_object.batch.description
		subject_year_list = []
		for j in student_batch_object.subject_years.all():
			subject_year_dict ={}
			subject_year_dict['id'] = j.id
			subject_year_dict['subject_id'] = j.subject.id
			subject_year_dict['subject_name'] = j.subject.name
			subject_year_dict['standard_id'] = j.subject.standard.id
			subject_year_dict['standard_name'] = j.subject.standard.name
			subject_year_dict['year_id'] = j.academic_year.id
			subject_year_list.append(subject_year_dict)
		student_batch['student_subjects'] = subject_year_list
		return student_batch

	#001101
	if is_none_student_id and is_none_id and is_none_batch_id and not is_none_standard_id and not is_none_academic_year_id:
		if batch_assigned == True:
			student_batch_object_list = StudentBatch.objects.filter(batch__standard__id = standard_id,batch__academic_year__id = academic_year_id)
		else:
			student_batch_object_list = StudentBatch.objects.filter(standard__id = standard_id, academic_year__id = academic_year__id)

		student_batch_list = []
		for student_batch_object in student_batch_object_list:
			student_batch = {}
			student_batch['id'] = student_batch_object.id
			student_batch['student_username'] = student_batch_object.student.username
			student_batch['student_password'] = student_batch_object.student.password
			student_batch['student_first_name'] = student_batch_object.student.first_name
			student_batch['student_last_name'] = student_batch_object.student.last_name
			student_batch['student_address'] = student_batch_object.student.address
			student_batch['student_email'] = student_batch_object.student.email
			student_batch['student_phone_number'] = student_batch_object.student.phone_number
			student_batch['student_gender'] = student_batch_object.student.gender
			student_batch['student_batch_id'] = student_batch_object.batch.id
			student_batch['student_batch_name'] = student_batch_object.batch.name
			student_batch['student_batch_description'] = student_batch_object.batch.description
			subject_year_list = []
			for j in student_batch_object.subject_years.all():
				subject_year_dict ={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
			student_batch['student_subjects'] = subject_year_list
			student_batch_list.append(student_batch)
		return student_batch_list

	#010000
	if is_none_student_id and is_none_id and not is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object_list = StudentBatch.objects.filter(batch = Batch.objects.get(id=batch_id,academic_year = AcademicYear.objects.get(id = get_current_academic_year()['id'])))
		student_batch_list = []
		for student_batch_object in student_batch_object_list:
			student_batch = {}
			student_batch['id'] = student_batch_object.id
			student_batch['student_username'] = student_batch_object.student.username
			student_batch['student_password'] = student_batch_object.student.password
			student_batch['student_first_name'] = student_batch_object.student.first_name
			student_batch['student_last_name'] = student_batch_object.student.last_name
			student_batch['student_address'] = student_batch_object.student.address
			student_batch['student_email'] = student_batch_object.student.email
			student_batch['student_phone_number'] = student_batch_object.student.phone_number
			student_batch['student_gender'] = student_batch_object.student.gender
			student_batch['student_batch_id'] = student_batch_object.batch.id
			student_batch['student_batch_name'] = student_batch_object.batch.name
			student_batch['student_batch_description'] = student_batch_object.batch.description
			subject_year_list = []
			for j in student_batch_object.subject_years.all():
				subject_year_dict ={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
			student_batch['student_subjects'] = subject_year_list
			student_batch_list.append(student_batch)
		return student_batch_list

	#100000
	if is_none_student_id and not is_none_id and is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(id=id,batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id =get_current_academic_year()['id'])))
		student_batch = {}
		student_batch['id'] = student_batch_object.id
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
		student_batch['student_batch_id'] = student_batch_object.batch.id
		student_batch['student_batch_name'] = student_batch_object.batch.name
		student_batch['student_batch_description'] = student_batch_object.batch.description
		subject_year_list = []
		for j in student_batch_object.subject_years.all():
			subject_year_dict ={}
			subject_year_dict['id'] = j.id
			subject_year_dict['subject_id'] = j.subject.id
			subject_year_dict['subject_name'] = j.subject.name
			subject_year_dict['standard_id'] = j.subject.standard.id
			subject_year_dict['standard_name'] = j.subject.standard.name
			subject_year_dict['year_id'] = j.academic_year.id
			subject_year_list.append(subject_year_dict)
		student_batch['student_subjects'] = subject_year_list
		return student_batch







def get_previous_students(batch_id = None):
	is_none_batch_id = batch_id == None
	if not is_none_batch_id:
		student_batch_object = StudentBatch.objects.filter(batch = Batch.objects.get(id = batch_id))
		student_list= []
		for i in student_batch_object:
			student_dict = {}
			student_dict['username'] = i.student.username
			student_dict['password'] = i.student.password
			student_dict['first_name'] = i.student.first_name
			student_dict['last_name'] = i.student.last_name
			student_dict['address'] = i.student.address
			student_dict['email'] = i.student.email
			student_dict['phone_number'] = i.student.phone_number
			student_dict['gender'] = i.student.gender
			student_list.append(student_dict)
		return student_list
	else:
		raise Exception('batch_id required')

def search_students(first_name='', last_name='', username='', email='', phone_number=''):
	# TODO Think of optimisation (probably using indexes
	students = Student.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name, username__icontains=username, email__icontains=email, phone_number__icontains=phone_number)
	student_list = []
	for i in students:
		student_dict = {}
		student_dict['id'] = i.id
		student_dict['username'] = i.username
		student_dict['first_name'] = i.first_name
		student_dict['last_name'] = i.last_name
		student_dict['email'] = i.email
		student_dict['phone_number'] = i.phone_number
		student_list.append(student_dict)

	return student_list

def get_student_batch_of_student(student_id, staff_id=None):
	# TODO (maybe?) merge with get_student_batch()
	if staff_id == None:
		student_batch = StudentBatch.objects.filter(student__id=student_id)
	else:
		student_batch = StudentBatch.objects.filter(Q(student__id=student_id, batch__branch = Branch.objects.filter(staffrole__role__name__in=['manager','accountant'], staffrole__staff__id=staff_id).distinct()) | (Q(student__id=student_id, batch = None)))
	student_batch_list = []
	for student_batch_object in student_batch:
		student_batch = {}
		student_batch['id'] = student_batch_object.id
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
		if student_batch_object.batch != None :
			student_batch['student_batch_name'] = student_batch_object.batch.name
			student_batch['student_batch_description'] = student_batch_object.batch.description
		subject_year_list = []
		for j in student_batch_object.subject_years.all():
			subject_year_dict ={}
			subject_year_dict['id'] = j.id
			subject_year_dict['subject_id'] = j.subject.id
			subject_year_dict['subject_name'] = j.subject.name
			subject_year_dict['standard_id'] = j.subject.standard.id
			subject_year_dict['standard_name'] = j.subject.standard.name
			subject_year_dict['academic_year_id'] = j.academic_year.id
			subject_year_dict['academic_year_name'] = str(j.academic_year.year_start)+'-'+str(j.academic_year.year_end)
			subject_year_dict['year_id'] = j.academic_year.id
			subject_year_list.append(subject_year_dict)
		student_batch['student_subjects'] = subject_year_list
		student_batch_list.append(student_batch)
	return student_batch_list

def get_student_of_parent(parent_id=None):
	if parent_id != None:
		student = StudentParent.objects.get(parent = Parent.objects.get( id = parent_id)).student
	student_dict = {}
	student_dict['id'] = student.id
	student_dict['username'] = student.username
	student_dict['password'] = student.password
	student_dict['first_name'] = student.first_name
	student_dict['last_name'] = student.last_name
	student_dict['address'] = student.address
	student_dict['email'] = student.email
	student_dict['phone_number'] = student.phone_number
	student_dict['gender'] = student.gender
	return student_dict
