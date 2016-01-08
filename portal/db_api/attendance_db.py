from portal.models import Attendance,StudentBatch,LectureBatch
def set_attendance(id = None ,count = None, student_batch_id = None, lecture_batch_id = None):
	is_none_id = id == None
	is_none_count = count == None
	is_none_student_batch_id = student_batch_id == None
	is_none_lecture_batch_id = lecture_batch_id == None

	#new attendance
	if is_none_id and not is_none_count and not is_none_student_batch_id and not is_none_lecture_batch_id:
		student_batch_object = StudentBatch.objects.get(id = student_batch_id)
		lecture_batch_object = LectureBatch.objects.get(id = lecture_batch_id)
		if Attendance.objects.filter(student_batch=student_batch_object, lecture_batch = lecture_batch_object).exists():
			# attendance already marked for student_batch and lecture_batch
			return Attendance.objects.get(student_batch=student_batch_object, lecture_batch = lecture_batch_object).id
		else:
			attendance_object = Attendance(count = count, student_batch = student_batch_object, lecture_batch = lecture_batch_object)
			attendance_object.save()
			return attendance_object.id

	elif not is_none_id:
		attendance_object = Attendance.objects.get(id = id)
		if not is_none_count:
			attendance_object.count = count
		if not is_none_student_batch_id:
			attendance_object.student_batch = StudentBatch.objects.get(id=student_batch_id)
		if not is_none_lecture_batch_id:
			attendance_object.lecture_batch = LectureBatch.objects.get(id=lecture_batch_id)
		attendance_object.save()

		return attendance_object.id
	else :
		raise Exception('Wrong set of arguments')

def get_attendance(id= None,student_batch_id=None,lecture_batch_id= None, staff_id = None):
	is_none_id = id == None
	is_none_student_batch_id = student_batch_id == None
	is_none_lecture_batch_id = lecture_batch_id == None
	is_none_staff_id = staff_id == None

	if not is_none_id:
		attendance_object = Attendance.objects.get(id=id)
		attendance = {}
		attendance['id'] = attendance_object.id
		attendance['count'] = attendance_object.count
		attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
		attendance['student_batch_id'] = attendance_object.student_batch.id
		attendance['student_batch'] = attendance_object.student_batch.batch.name
		attendance['lecture_batch'] = attendance_object.lecture_batch.name
		attendance['date'] = attendance_object.lecture_batch.date
		attendance['duration'] = attendance_object.lecture_batch.duration


		return attendance

	elif is_none_id and not is_none_student_batch_id and is_none_lecture_batch_id:
		attendance_object_list = Attendance.objects.filter(student_batch = StudentBatch.objects.get(id=student_batch_id))
		attendance_list=[]
		for attendance_object in attendance_object_list:
			attendance = {}
			attendance['id'] = attendance_object.id
			attendance['count'] = attendance_object.count
			attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
			attendance['student_batch_id'] = attendance_object.student_batch.id
			attendance['student_batch'] = attendance_object.student_batch.batch.name
			attendance['lecture_batch'] = attendance_object.lecture_batch.name
			attendance['date'] = attendance_object.lecture_batch.date
			attendance['duration'] = attendance_object.lecture_batch.duration
			attendance_list.append(attendance)
		return attendance_list

	elif is_none_id and is_none_student_batch_id and not is_none_lecture_batch_id:
		attendance_object_list = Attendance.objects.filter(lecture_batch = LectureBatch.objects.get(id=lecture_batch_id))
		attendance_list=[]
		for attendance_object in attendance_object_list:
			attendance = {}
			attendance['id'] = attendance_object.id
			attendance['count'] = attendance_object.count
			attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
			attendance['student_batch_id'] = attendance_object.student_batch.id
			attendance['student_batch'] = attendance_object.student_batch.batch.name
			attendance['lecture_batch'] = attendance_object.lecture_batch.name
			attendance['date'] = attendance_object.lecture_batch.date
			attendance['duration'] = attendance_object.lecture_batch.duration
			attendance_list.append(attendance)
		return attendance_list

	elif is_none_id and is_none_student_batch_id and is_none_lecture_batch_id and not is_none_staff_id:
		attendance_object_list = Attendance.objects.filter(lecture_batch__staff_role__staff__id = staff_id)
		attendance_list=[]
		for attendance_object in attendance_object_list:
			attendance = {}
			attendance['id'] = attendance_object.id
			attendance['count'] = attendance_object.count
			attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
			attendance['student_batch_id'] = attendance_object.student_batch.id
			attendance['student_batch'] = attendance_object.student_batch.batch.name
			attendance['lecture_batch'] = attendance_object.lecture_batch.name
			attendance['lecture_batch_id'] = attendance_object.lecture_batch.id
			attendance['date'] = attendance_object.lecture_batch.date
			attendance['duration'] = attendance_object.lecture_batch.duration
			attendance_list.append(attendance)
		return attendance_list

def delete_attendance(student_batch_id = None, lecture_batch_id = None):
	Attendance.objects.filter(student_batch__id=student_batch_id, lecture_batch__id=lecture_batch_id).delete()
