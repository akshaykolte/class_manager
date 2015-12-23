from portal.models import AttendanceDaywise,StudentBatch,Batch
def set_attendance_daywise(id = None ,attended = None, student_batch_id = None, date = None):
	is_none_id = id == None
	is_none_attended = attended == None
	is_none_student_batch_id = student_batch_id == None
	is_none_date = date == None

	#new attendance
	if is_none_id and not is_none_attended and not is_none_student_batch_id and not is_none_date:
		
		student_batch_object = StudentBatch.objects.get(id = student_batch_id)
		
		if AttendanceDaywise.objects.filter(student_batch=student_batch_object, date = date).exists():
			# attendance already marked for student_batch and date/Edit
			attendance_object = AttendanceDaywise.objects.get(student_batch=student_batch_object, date = date)
			if not is_none_attended:
				attendance_object.attended = attended
			
			if not is_none_date:
				attendance_object.date = date
			attendance_object.save()

			return attendance_object.id
		else:
			attendance_object = AttendanceDaywise(attended = attended, student_batch = student_batch_object, date = date)
			attendance_object.save()
			return attendance_object.id

	elif not is_none_id:
		attendance_object = AttendanceDaywise.objects.get(id = id)
		if not is_none_attended:
			attendance_object.attended = attended
		
		if not is_none_date:
			attendance_object.date = date
		attendance_object.save()

		return attendance_object.id
	else :
		raise Exception('Wrong set of arguments')

def get_attendance_daywise(id= None, student_batch_id = None, date = None, batch_id = None):
	is_none_id = id == None
	is_none_student_batch_id = student_batch_id == None
	is_none_date = date == None
	is_none_batch_id = batch_id == None

	if not is_none_id:
		attendance_object = AttendanceDaywise.objects.get(id=id)
		attendance = {}
		attendance['id'] = attendance_object.id
		attendance['attended'] = attendance_object.attended
		attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
		attendance['student_batch_id'] = attendance_object.student_batch.id
		attendance['student_batch'] = attendance_object.student_batch.batch
		attendance['date'] = attendance_object.date


		return attendance

	elif is_none_id and not is_none_student_batch_id and is_none_date and is_none_batch_id:
		attendance_object_list = AttendanceDaywise.objects.filter(student_batch = StudentBatch.objects.get(id=student_batch_id))
		attendance_list=[]
		for attendance_object in attendance_object_list:
			attendance = {}
			attendance['id'] = attendance_object.id
			attendance['attended'] = attendance_object.attended
			attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
			attendance['student_batch_id'] = attendance_object.student_batch.id
			attendance['student_batch'] = attendance_object.student_batch.batch
			attendance['date'] = attendance_object.date
			attendance_list.append(attendance)
		return attendance_list

	#daywise attendance for batch
	elif is_none_id and is_none_student_batch_id and not is_none_date and not is_none_batch_id:
		attendance_object_list = AttendanceDaywise.objects.filter(student_batch__batch = Batch.objects.get(id = batch_id), date = date)
		attendance_list=[]
		for attendance_object in attendance_object_list:
			attendance = {}
			attendance['id'] = attendance_object.id
			attendance['attended'] = attendance_object.attended
			attendance['student'] = str(attendance_object.student_batch.student.first_name) + " " +str(attendance_object.student_batch.student.last_name)
			attendance['student_batch_id'] = attendance_object.student_batch.id
			attendance['student_batch'] = attendance_object.student_batch.batch
			attendance['student_id'] = attendance_object.student_batch.student.id
			attendance['date'] = attendance_object.date
			attendance_list.append(attendance)
		return attendance_list

def delete_attendance_daywise(student_batch_id = None, date = None):
	AttendanceDaywise.objects.filter(student_batch__id=student_batch_id,date = date).delete()
