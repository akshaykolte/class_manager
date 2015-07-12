# get_students (individual, of batch, of branch, all) return: all details, batch details, branch details and subject details
# set_student (add or modify if already exists, if batch_id is present then assign student to that batch) return: id
# get_parent(from student) return: parent details
# set_parent(student_id as a parameter) return: id
# get_previous_students (pass batch_id as parameter)
from portal.models import Student,Parent,StudentParent

def set_student(id=None, parent_id = None, first_name=None ,last_name=None ,address=None, email=None, phone_number=None, gender=None ):

	is_none_id = id == None
	is_none_parent_id = parent_id == None
	is_none_batch_id = batch_id == None
	is_none_first_name = first_name == None
	is_none_last_name = last_name == None
	is_none_address = address == None
	is_none_email = email == None
	is_none_phone_number = phone_number == None
	is_none_gender = gender == None

	if is_none_id:
		student_object = Student(first_name = first_name,last_name = last_name, address = address, email = email, phone_number = phone_number, gender = gender)
		student_object.save()
		if not is_none_parent_id:
			parent_object = Parent.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		return student_object.id

	elif not is_none_id:
		student_object = Student.objects.get(id=id)
		if not is_none_parent_id:
			parent_object = Parent.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
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

def set_parent(id=None, student_id = None, first_name=None ,last_name=None ,address=None, email=None, phone_number=None, gender=None ):

	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_batch_id = batch_id == None
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
			student_object = Student.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		return parent_object.id

	elif not is_none_id:
		parent_object = Parent.objects.get(id=id)
		if not is_none_student_id:
			student_object = Student.objects.get(id=parent_id)
			studentparent_object = StudentParent(student = student_object, parent = parent_object)
			studentparent_object.save()
		
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
		parent_object.save()
		return parent_object.id
	else:
		raise Exception ('Enter all fields')



