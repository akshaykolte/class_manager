from portal.models import Attendance, StudentBatch, LectureBatch
from django.db.models import Count

def attendance_report(lecture_id = None, branch_id = None):
	# Valid cases: 11
	bit_list = []
	for i in [lecture_id, branch_id]:
		if i == None: bit_list.append('0')
		else: bit_list.append('1')
	if ''.join(bit_list) == '11':
		attendance_list = Attendance.objects.filter(lecture_batch__lecture__id = lecture_id, student_batch__batch__branch__id=branch_id).values('student_batch__student__first_name', 'student_batch__student__last_name', 'student_batch__id', 'lecture_batch__batch__name').annotate(Count('lecture_batch__batch'))
		print 'attendance_list', attendance_list
		
		student_list = StudentBatch.objects.filter(batch__branch__id = branch_id)
		
		lecture_batch_list = LectureBatch.objects.filter(lecture__id = lecture_id).values('name').annotate(Count('batch'))
		
		print 'lecture_batch_list', lecture_batch_list

		report_list = [[],[]]
		report_list[0] = lecture_batch_list
		
		student_dict = {}
		for student in student_list:
			student_dict[student.id] = student

		print student_dict, 'lol'
