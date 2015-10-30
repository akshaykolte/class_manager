#get_lecture(individual,all)
#set_lecture((add or modify if already exists)
#get_lecture_batch(of batch,of date, of staffrole,of duration)
#set_lecture_batch(add or modify if already exists)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#get_lecture_batch(of batch,of date, of staffrole,of duration ****and also of a lecture****)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


from portal.models import Lecture,LectureBatch,SubjectYear,StaffRole,Batch

def get_lecture(id = None, subject_year_id = None):
	is_none_id = id == None
	is_none_subject_year_id = subject_year_id == None
	lecture_list = []
	if not is_none_id and is_none_subject_year_id:
		lecture = Lecture.objects.get(id = id)
		# lecture_batch_object = LectureBatch.objects.get(lecture = lecture)
		lecture_obj = {}
		lecture_obj['id'] = lecture.id
		lecture_obj['name'] = lecture.name
		lecture_obj['description'] = lecture.description
		lecture_obj['count'] = lecture.count
		lecture_obj['subject_year_id'] = lecture.subject_year.id
		lecture_obj['subject_id'] = lecture.subject_year.subject.id
		lecture_obj['subject_name'] = lecture.subject_year.subject.name
		lecture_obj['standard_id'] = lecture.subject_year.subject.standard.id
		lecture_obj['standard_name'] = lecture.subject_year.subject.standard.name
		lecture_list.append(lecture_obj)
		return lecture_list

	elif is_none_id and not is_none_subject_year_id:

		lecture_object = Lecture.objects.filter(subject_year=(SubjectYear.objects.get(id=subject_year_id)))


		for i in lecture_object:
			# Commented because of error
			#lecture_batch_object = LectureBatch.objects.get(lecture = i)
			lecture_dict = {}
			lecture_dict['id'] = i.id
			lecture_dict['name'] = i.name
			lecture_dict['description'] = i.description
			lecture_dict['count'] = i.count
			lecture_dict['subject_year_id'] = i.subject_year.id
			lecture_dict['subject_id'] = i.subject_year.subject.id
			lecture_dict['subject_name'] = i.subject_year.subject.name
			lecture_dict['date'] = '-' # TODO
			lecture_list.append(lecture_dict)

		return lecture_list

	else:
		lecture = Lecture.objects.all()
		for i in lecture:
			lecture_batch_object = LectureBatch.objects.get(lecture = i)
			lecture_dict = {}
			lecture_dict['id'] = i.id
			lecture_dict['name'] = i.name
			lecture_dict['description'] = i.description
			lecture_dict['count'] = i.count
			lecture_dict['subject_year_id'] = i.subject_year.id
			lecture_dict['subject_id'] = i.subject_year.subject.id
			lecture_dict['subject_name'] = i.subject_year.subject.name
			lecture_dict['date'] = lecture_batch_object.date
			lecture_list.append(lecture_dict)
		return lecture_list

def set_lecture(id = None,name = None,description = None,count = None,subject_year_id = None):
	is_none_id = id == None
	is_none_name = name == None
	is_none_description = description == None
	is_none_count = count == None
	is_none_subject_year_id = subject_year_id == None

	if is_none_id:
		lecture_object = Lecture(name = name, description = description, count = count, subject_year = SubjectYear.objects.get(id = subject_year_id))
		lecture_object.save()
		return lecture_object.id

	elif not is_none_id:
		lecture_object = Lecture.objects.get(id=id)
		if not is_none_name:
			lecture_object.name = name
		if not is_none_description:
			lecture_object.description = description
		if not is_none_count:
			lecture_object.count = count
		if not is_none_subject_year_id:
			lecture_object.subject_year = SubjectYear.objects.get(id = subject_year_id)
		lecture_object.save()
		return lecture_object.id


def get_lecture_batch(id = None,date = None,lecture_id = None,staff_role_id = None,batch_id = None, staff_id = None):


	is_none_id = id == None
	is_none_date = date == None
	is_none_lecture_id = lecture_id == None
	is_none_staff_role_id = staff_role_id == None
	is_none_staff_id = staff_id == None
	is_none_batch_id = batch_id == None

	if not is_none_id and is_none_date and is_none_lecture_id and is_none_staff_role_id and is_none_batch_id and is_none_staff_id:
		lecture_batch_dict = {}
		lecture_batch_object = LectureBatch.objects.get(id=id)
		lecture_batch_dict['id'] = lecture_batch_object.id
		lecture_batch_dict['name'] = lecture_batch_object.name
		lecture_batch_dict['description'] = lecture_batch_object.description
		lecture_batch_dict['date'] = lecture_batch_object.date
		lecture_batch_dict['duration'] = lecture_batch_object.duration
		lecture_batch_dict['lecture_id'] = lecture_batch_object.lecture.id
		lecture_batch_dict['lecture_name'] = lecture_batch_object.lecture.name
		lecture_batch_dict['lecture_batch_name'] = lecture_batch_object.name
		lecture_batch_dict['staff_role_id'] = lecture_batch_object.staff_role.id
		lecture_batch_dict['batch_id'] = lecture_batch_object.batch.id
		lecture_batch_dict['batch_name'] = lecture_batch_object.batch.name
		lecture_batch_dict['branch_name'] = lecture_batch_object.batch.branch.name
		lecture_batch_dict['standard_id'] = lecture_batch_object.batch.standard.id
		lecture_batch_dict['standard_name'] = lecture_batch_object.batch.standard.name
		lecture_batch_dict['is_done'] = lecture_batch_object.is_done
		return lecture_batch_dict

	elif is_none_id and is_none_date and not is_none_lecture_id and is_none_staff_role_id and not is_none_batch_id and is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(batch = Batch.objects.get(id = batch_id),lecture = Lecture.objects.get(id = lecture_id))
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['duration'] = i.duration
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['staff_role_id'] = i.staff_role.id
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list

	elif is_none_id and not is_none_date and is_none_lecture_id and is_none_staff_role_id and is_none_batch_id and is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(date = date)
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['duration'] = i.duration
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['staff_role_id'] = i.staff_role.id
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list

	elif is_none_id and is_none_date and not is_none_lecture_id and is_none_staff_role_id and is_none_batch_id and is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(lecture = Lecture.objects.get(id = lecture_id))
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['duration'] = i.duration
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['staff_role_id'] = i.staff_role.id
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list

	elif is_none_id and is_none_date and is_none_lecture_id and not is_none_staff_role_id and is_none_batch_id and is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(staff_role = StaffRole.objects.get(id = staff_role_id))
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['duration'] = i.duration
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['staff_role'] = i.staff_role
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_dict['is_done'] = i.is_done
			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list

	elif is_none_id and is_none_date and not is_none_lecture_id and is_none_staff_role_id and not is_none_batch_id and not is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(staff_role__staff__id = staff_id, lecture__id=lecture_id, batch__id=batch_id)
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['duration'] = i.duration
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['staff_role'] = i.staff_role
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['branch_name'] = i.batch.branch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_dict['is_done'] = i.is_done
			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list

	elif is_none_id and is_none_date and is_none_lecture_id and is_none_staff_role_id and not is_none_batch_id and is_none_staff_id:
		lecture_batch_list = []
		lecture_batch_object = LectureBatch.objects.filter(batch = Batch.objects.get(id = batch_id))
		for i in lecture_batch_object:
			lecture_batch_dict={}
			lecture_batch_dict['id'] = i.id
			lecture_batch_dict['name'] = i.name
			lecture_batch_dict['description'] = i.description
			lecture_batch_dict['date'] = i.date
			lecture_batch_dict['lecture_id'] = i.lecture.id
			lecture_batch_dict['lecture_name'] = i.lecture.name
			lecture_batch_dict['subject_name'] = i.lecture.subject_year.subject.name
			lecture_batch_dict['staff_role_id'] = i.staff_role.id
			lecture_batch_dict['staff_role_name'] = i.staff_role.staff.first_name + " " + i.staff_role.staff.last_name
			lecture_batch_dict['batch_id'] = i.batch.id
			lecture_batch_dict['batch_name'] = i.batch.name
			lecture_batch_dict['standard_id'] = i.batch.standard.id
			lecture_batch_dict['standard_name'] = i.batch.standard.name
			lecture_batch_dict['is_done'] = i.is_done
			lecture_batch_dict['branch_name'] = i.batch.branch.name

			lecture_batch_list.append(lecture_batch_dict)
		return lecture_batch_list







def set_lecture_batch(id = None, name = None, description = None, date = None, duration = None, lecture_id = None, staff_role_id = None,batch_id = None, is_done=None):
	print is_done
	is_none_id = id == None
	is_none_name = name == None
	is_none_description = description == None
	is_none_date = date == None
	is_none_duration = duration == None
	is_none_lecture_id = lecture_id == None
	is_none_staff_role_id = staff_role_id == None
	is_none_batch_id = batch_id == None
	is_none_is_done = is_done == None

	if is_none_id and not is_none_lecture_id and not is_none_staff_role_id and not is_none_batch_id:
		lecture_object = LectureBatch(name = name,description = description,date = date, duration = duration, lecture = Lecture.objects.get(id = lecture_id),
						staff_role = StaffRole.objects.get(id = staff_role_id),batch = Batch.objects.get(id = batch_id))
		lecture_object.save()
		return lecture_object.id

	elif not is_none_id:
		lecture_object = LectureBatch.objects.get(id = id)
		if not is_none_name:
			lecture_object.name = name
		if not is_none_description:
			lecture_object.description = description
		if not is_none_date:
			lecture_object.date = date
		if not is_none_duration:
			lecture_object.duration = duration
		if not is_none_lecture_id:
			lecture_object.lecture = Lecture.objects.get(id = lecture_id)
		if not is_none_staff_role_id:
			lecture_object.staff_role = StaffRole.objects.get(id = staff_role_id)
		if not is_none_batch_id:
			lecture_object.batch = Batch.objects.get(id = batch_id)
		if not is_none_is_done:
			lecture_object.is_done = is_done
		lecture_object.save()
		return lecture_object.id
