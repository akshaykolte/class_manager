from portal.models import Attendance, StudentBatch, LectureBatch
from django.db.models import Count

def attendance_report(lecture_id = None, branch_id = None):
	# Valid cases: 11
	bit_list = []
	for i in [lecture_id, branch_id]:
		if i == None: bit_list.append('0')
		else: bit_list.append('1')
	if ''.join(bit_list) == '11':
		attendance_list = Attendance.objects.filter(lecture_batch__lecture__id = lecture_id, student_batch__batch__branch__id=branch_id).values('student_batch__student__first_name', 'student_batch__student__last_name', 'student_batch__id', 'lecture_batch__batch__name', 'lecture_batch__id').annotate(Count('lecture_batch__batch'))
		
		student_list = StudentBatch.objects.filter(batch__branch__id = branch_id)
		
		lecture_batch_list = LectureBatch.objects.filter(lecture__id = lecture_id).values('batch__name', 'id').annotate(Count('batch'))

		attendance_dict = {}
		lecture_dict = {}
		
		index = 0
		for lecture in lecture_batch_list:
			lecture_dict[lecture['id']] = [index, lecture['batch__count'], lecture['batch__name']]
			index += 1
		
		for student in student_list:
			attendance_dict[student.id] = []

		for attendance in attendance_list:
			attendance_dict[attendance['student_batch__id']].append(attendance)

		'''
		print ''


		print 'student_list', student_list
		print ''

		print 'lecture_dict', lecture_dict
		print ''

		print 'attendance_dict', attendance_dict
		print ''
		'''


		report_table = []

		for student in student_list:
			report_table.append([ '' for i in range(len(lecture_dict))])
			for lec in xrange(len(lecture_batch_list)):
				report_table[-1][lec] = '-/'+str(lecture_batch_list[lec]['batch__count'])
			for attendance in attendance_dict[student.id]:
				report_table[-1][ lecture_dict[attendance['lecture_batch__id']][0] ] = str(attendance['lecture_batch__batch__count'])+'/'+str(lecture_dict[attendance['lecture_batch__id']][1])
			report_table[-1] = [student.student.first_name+' '+student.student.last_name] + report_table[-1]


		report_list = [[],[]]
		report_list[0] = lecture_batch_list
		report_list[1] = report_table

		return report_list