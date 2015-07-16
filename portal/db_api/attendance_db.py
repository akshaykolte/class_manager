def set_attendance(id = None ,count = count, student_batch_id = None, lecture_batch_id = None):
	is_none_id = id == None
	is_none_count = count == None
	is_none_student_batch_id = student_batch_id == None
	is_none_lecture_batch_id = lecture_batch_id == None
	
	#new attendance
	if is_none_id and not is_none_count and not is_none_student_batch_id and not is_none_lecture_batch_id:
		student_batch_object = StudentBatch.objects.get(id = student_batch_id)
		lecture_batch_object = LectureBatch.objects.get(id = lecture_batch_id)
		attendance_object = Attendance(count = count, student_batch = student_batch_object, lecture_batch = lecture_batch_object)
		attendance_object.save()
		
		return attendance_object.id

	if not is_none_id and not is_none_count and is_none_student_batch_id and is_none_lecture_batch_id: 
		attendance_object = Attendance.objects.get(id = id)
		attendance_object.count = count
		attendance_object.save()
		
		return attendance_object.id
	else :
		raise Exception('Wrong set of arguments')
