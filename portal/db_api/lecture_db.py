#get_lecture(individual,all)
#set_lecture((add or modify if already exists)
#get_lecture_batch(of batch,of date, of staffrole,of duration)
#set_lecture_batch(add or modify if already exists)
from portal.models import Lecture,LectureBatch,SubjectYear,StaffRole,Batch

def get_lecture(id = None):
	is_none_id = id == None

	if not is_none_id:
		lecture = Lecture.objects.get(id = id)
		lecture_obj = {}
		lecture_obj['name'] = lecture.name
		lecture_obj['description'] = lecture.description
		lecture_obj['count'] = lecture.count
		lecture_obj['subjects'] = lecture.subject_year
		return lecture_obj
	else:
		lecture_list = []
		lecture = Lecture.objects.all()
		for i in lecture:
			lecture_dict = {}
			lecture_dict['name'] = i.name
			lecture_dict['description'] = i.description
			lecture_dict['count'] = i.count
			lecture_dict['subjects'] = i.subject_year	
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
			lecture_object.subject_year = SubjectYear.objects.filter(id = subject_year_id)
		lecture_object.save()
		return lecture_object.id

			

def set_lecture_batch(id = None, name = None, description = None, date = None, duration = None, lecture_id = None, staff_role_id = None,batch_id = None):
	is_none_id = id == None
	is_none_name = name == None
	is_none_description = description == None
	is_none_date = date == None
	is_none_duration = duration == None
	is_none_lecture_id = lecture_id == None
	is_none_staff_role_id = staffrole_id == None
	is_none_batch_id = batch_id == None

	if is_none_id:
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
		lecture_object.save()
		return lecture_object.id	


