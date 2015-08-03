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

from portal.models import Student,Parent,StudentParent,Batch,StudentBatch,SubjectYear,Standard
from portal.db_api.academic_year_db import *

def get_students(id = None,batch_id = None,branch_id = None):
	is_none_id = id == None
	is_none_batch_id = batch_id == None
	is_none_branch_id = branch_id == None

	if not is_none_id and is_none_batch_id:
		student_object = {}
		student = Student.objects.get(id=id)
		student_batch = StudentBatch.objects.get(student = Student.objects.get(id=id))
		student_object['username'] = student.username
		student_object['password'] = student.password
		student_object['first_name'] = student.first_name
		student_object['last_name'] = student.last_name
		student_object['address'] = student.address
		student_object['email'] = student.email
		student_object['phone_number'] = student.phone_number
		student_object['gender'] = student.gender
		subject_year_list = []
		for j in student_batch.subject_years.all():
				subject_year_dict={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
		student_object['subjects'] = subject_year_list
		return student_object

	if not is_none_id and not is_none_batch_id:
		student_batch = StudentBatch.objects.get(student = Student.objects.get(id=id))

		student_object = {}
		student = Student.objects.get(id=id)
		student_object['username'] = student.username
		student_object['password'] = student.password
		student_object['first_name'] = student.first_name
		student_object['last_name'] = student.last_name
		student_object['address'] = student.address
		student_object['email'] = student.email
		student_object['phone_number'] = student.phone_number
		student_object['gender'] = student.gender
		student_object['batch'] = student_batch.batch
		subject_year_list = []
		for j in student_batch.subject_years.all():
				subject_year_dict={}
				subject_year_dict['id'] = j.id
				subject_year_dict['subject_id'] = j.subject.id
				subject_year_dict['subject_name'] = j.subject.name
				subject_year_dict['standard_id'] = j.subject.standard.id
				subject_year_dict['standard_name'] = j.subject.standard.name
				subject_year_dict['year_id'] = j.academic_year.id
				subject_year_list.append(subject_year_dict)
		student_object['subjects'] = subject_year_list
		return student_object

	elif not is_none_batch_id:
		student_list = []
		student_batch = StudentBatch.objects.filter(batch = Batch.objects.get(id = batch_id))
		for i in student_batch:
			student_dict = {}
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
	else:
		student_list = []
		student = Student.objects.all()
		for i in student:
			student_batch = StudentBatch.objects.get(student = i)
			student_dict = {}
			student_dict['username'] = i.username
			student_dict['password'] = i.password
			student_dict['first_name'] = i.first_name
			student_dict['last_name'] = i.last_name
			student_dict['address'] = i.address
			student_dict['email'] = i.email
			student_dict['phone_number'] = i.phone_number
			student_dict['gender'] = i.gender
			subject_year_list = []
			for j in student_batch.subject_years.all():
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
		parent_object = Parent(first_name = first_name,last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender)
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

def set_student_batch(id=None,student_id=None,batch_id=None,subject_year_id_list=None):
	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_batch_id = batch_id == None
	is_none_subject_year_id_list = subject_year_id_list == None

	if is_none_id:

		student_batch_object = StudentBatch(student = Student.objects.get(id = student_id),batch = Batch.objects.get(id = batch_id))
		student_batch_object.save()
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
				

def get_student_batch(id=None,batch_id=None,standard_id=None,academic_year_id=None,student_id=None):
	# if academic_year_id is None then academic_year_id = get_current_academic_year()['id']
	# possible combinations: 00001,00011,00110,01000,10000
	is_none_id = id == None
	is_none_batch_id = batch_id == None
	is_none_standard_id = standard_id == None
	is_none_academic_year_id = academic_year_id == None
	is_none_student_id = student_id == None

	#00001
	if not is_none_student_id and is_none_id and is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(student = Student.objects.get(id = student_id),batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id =get_current_academic_year()['id'])))
		student_batch = {}
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
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

	#00011
	if not is_none_student_id and is_none_id and is_none_batch_id and is_none_standard_id and not is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(student = Student.objects.get(id = student_id),batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id = academic_year_id)))
		student_batch = {}
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
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

	#00110
	if is_none_student_id and is_none_id and is_none_batch_id and not is_none_standard_id and not is_none_academic_year_id:
		student_batch_object_list = StudentBatch.objects.filter(standard = Standard.objects.get(id = standard_id),batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id = academic_year_id)))
		student_batch_list = []
		for student_batch_object in student_batch_object_list:
			student_batch = {}
			student_batch['student_username'] = student_batch_object.student.username
			student_batch['student_password'] = student_batch_object.student.password
			student_batch['student_first_name'] = student_batch_object.student.first_name
			student_batch['student_last_name'] = student_batch_object.student.last_name
			student_batch['student_address'] = student_batch_object.student.address
			student_batch['student_email'] = student_batch_object.student.email
			student_batch['student_phone_number'] = student_batch_object.student.phone_number
			student_batch['student_gender'] = student_batch_object.student.gender
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

	#01000
	if is_none_student_id and is_none_id and not is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object_list = StudentBatch.objects.filter(batch = Batch.objects.get(id=batch_id,academic_year = AcademicYear.objects.get(id = get_current_academic_year()['id'])))
		student_batch_list = []
		for student_batch_object in student_batch_object_list:
			student_batch = {}
			student_batch['student_username'] = student_batch_object.student.username
			student_batch['student_password'] = student_batch_object.student.password
			student_batch['student_first_name'] = student_batch_object.student.first_name
			student_batch['student_last_name'] = student_batch_object.student.last_name
			student_batch['student_address'] = student_batch_object.student.address
			student_batch['student_email'] = student_batch_object.student.email
			student_batch['student_phone_number'] = student_batch_object.student.phone_number
			student_batch['student_gender'] = student_batch_object.student.gender
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

	#10000
	if is_none_student_id and not is_none_id and is_none_batch_id and is_none_standard_id and is_none_academic_year_id:
		student_batch_object = StudentBatch.objects.get(id=id,batch = Batch.objects.get(academic_year = AcademicYear.objects.get(id =get_current_academic_year()['id'])))
		student_batch = {}
		student_batch['student_username'] = student_batch_object.student.username
		student_batch['student_password'] = student_batch_object.student.password
		student_batch['student_first_name'] = student_batch_object.student.first_name
		student_batch['student_last_name'] = student_batch_object.student.last_name
		student_batch['student_address'] = student_batch_object.student.address
		student_batch['student_email'] = student_batch_object.student.email
		student_batch['student_phone_number'] = student_batch_object.student.phone_number
		student_batch['student_gender'] = student_batch_object.student.gender
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



