from portal.models import Attendance, StudentBatch, LectureBatch, Lecture, SubjectYear
from django.db.models import Count, IntegerField, Case, When

def attendance_report(lecture_id = None, branch_id = None, student_id = None, subjects = None):
	# Valid cases: 1100, 0011
	bit_list = []
	for i in [lecture_id, branch_id, student_id, subjects]:
		if i == None: bit_list.append('0')
		else: bit_list.append('1')
	if ''.join(bit_list) == '1100':
		attendance_list = Attendance.objects.filter(lecture_batch__lecture__id = lecture_id, student_batch__batch__branch__id=branch_id).values('student_batch__student__first_name', 'student_batch__student__last_name', 'student_batch__id', 'lecture_batch__batch__name', 'lecture_batch__batch__id').annotate(Count('lecture_batch__batch'))
		
		print ''
		print 'attendance_list', attendance_list
		student_list = StudentBatch.objects.filter(batch__branch__id = branch_id)
		
		lecture_batch_list = LectureBatch.objects.filter(lecture__id = lecture_id).values('batch__name', 'batch_id').annotate(Count('batch'))

		attendance_dict = {}
		lecture_dict = {}
		
		index = 0
		for lecture in lecture_batch_list:
			lecture_dict[lecture['batch_id']] = [index, lecture['batch__count'], lecture['batch__name']]
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
				report_table[-1][ lecture_dict[attendance['lecture_batch__batch__id']][0] ] = str(attendance['lecture_batch__batch__count'])+'/'+str(lecture_dict[attendance['lecture_batch__batch__id']][1])
			report_table[-1] = [student.student.first_name+' '+student.student.last_name] + report_table[-1]


		report_list = [[],[]]
		report_list[0] = lecture_batch_list
		report_list[1] = report_table

		return report_list

	if ''.join(bit_list) == '0011':
		if len(subjects) == 1:
			subject_id = subjects[0]

			lectures = Lecture.objects.filter(lecturebatch__batch = StudentBatch.objects.get(id=student_id).batch).annotate(Count('lecturebatch'))
			lectures_dict = {}
			for lecture in lectures:
				lectures_dict[lecture.id] = lecture
			
			
			attendance_list = Attendance.objects.filter(student_batch__id=student_id, lecture_batch__lecture__subject_year__id = subject_id).values('lecture_batch__lecture__name', 'lecture_batch__lecture__id').annotate(Count('lecture_batch'))
		
			report_table = []
			attendance_dict = {}
			sum = [0,0]
			for attendance in attendance_list:
				report_table.append([])
				report_table[-1].append(lectures_dict[attendance['lecture_batch__lecture__id']].name)
				report_table[-1].append(attendance['lecture_batch__count'])
				report_table[-1].append(lectures_dict[attendance['lecture_batch__lecture__id']].lecturebatch__count)
				sum[0] += attendance['lecture_batch__count']
				sum[1] += lectures_dict[attendance['lecture_batch__lecture__id']].lecturebatch__count
			
			report_table.append(['Total', sum[0], sum[1]])
			
			'''
			print ''
			print 'lectures', lectures
			print ''
			print 'attendance_list', attendance_list
			print ''
			print 'report_table', report_table
			'''
			
			return report_table
		elif len(subjects) > 1:
			subject_list = LectureBatch.objects.filter(lecture__subject_year__in=subjects, batch=StudentBatch.objects.get(id=student_id).batch).values('lecture__subject_year__id', 'lecture__subject_year__subject__name').annotate(Count('name'))
			subject_dict = {}
			subject_object_list = SubjectYear.objects.filter(id__in=subjects)
			for subject in subject_object_list:
				subject_dict[subject.id] = [0,subject.subject.name]
			for subject in subject_list:
				subject_dict[subject['lecture__subject_year__id']] = [ subject['name__count'], subject['lecture__subject_year__subject__name'] ]
			
			attendance_list = Attendance.objects.filter(student_batch__id = student_id, lecture_batch__lecture__subject_year__in=subjects).values('lecture_batch__lecture__subject_year__id').annotate(Count('count'))
			
			attendance_dict = {}
			
			for attendance in attendance_list:
				attendance_dict[attendance['lecture_batch__lecture__subject_year__id']] = attendance

			'''
			print ''
			print attendance_list

			print ''
			print 'subject_dict', subject_dict
			'''

			report_table = []
			for subject in subject_dict:
				report_table.append([])
				report_table[-1].append(subject_dict[subject][1])
				if subject in attendance_dict:
					report_table[-1].append(attendance_dict[subject]['count__count'])
				else:
					report_table[-1].append(0)
				report_table[-1].append(subject_dict[subject][0])

			return report_table