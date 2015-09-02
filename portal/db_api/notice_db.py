from portal.models import *
from portal.db_api.academic_year_db import get_current_academic_year

# uploader_id is necessary, even for edit, i.e., if id is not none.

def set_notice(id=None, title=None, description=None, uploader_id=None, expiry_date=None, important=None):
	is_id_none = id==None
	is_title_none = title==None
	is_description_none = description==None
	is_uploader_id_none = uploader_id==None
	is_expiry_date_none = expiry_date==None
	is_important_none = important==None

	if is_id_none:
		# Create new notice and save
		uploader = Staff.objects.get(id=uploader_id)
		notice_object = Notice(title=title, description=description, uploader=uploader, expiry_date=expiry_date, important=important)
		notice_object.save()
	elif not is_id_none:
		# Edit notice
		notice_object = Notice.objects.get(id=id)
		if uploader_id != notice_object.uploader.id: # Uploader cannot be modified
			return None
		else:
			if not is_title_none:
				notice_object.title = title
			if not is_description_none:
				notice_object.description = description
			if not is_expiry_date_none:
				notice_object.expiry_date = expiry_date
			if not is_important_none:
				notice_object.important = important
	notice_object.save()

	return notice_object.id



def upload_notice(id=None, notice_id = None, for_students = None, for_staff = None, branch_id = None, batch_id = None, student_id = None, staff_id = None):
	is_id_none = id == None
	is_for_students_none = for_students == None
	is_for_staff_none = for_staff == None
	is_branch_id_none = branch_id == None
	is_batch_id_none = batch_id == None
	is_student_id_none = student_id == None
	is_staff_id_none = staff_id == None
	if is_id_none:
		
		# Create new noticeviwer and save
		print for_students
		print for_staff

		if for_students and not for_staff:
			#student notice
			
			print "dffdsfds"
			notice_object = Notice.objects.get(id = notice_id)
			if not is_branch_id_none:
				notice_viewer = NoticeViewer(notice = notice_object, for_students = True, for_staff = False, branch = Branch.objects.get(id = branch_id), batch = None, student = None, staff = None )
				notice_viewer.save()
			elif not is_batch_id_none:
				notice_viewer = NoticeViewer(notice = notice_object, for_students = True, for_staff = False, batch = Batch.objects.get(id = batch_id), branch = None, student = None, staff = None )
				notice_viewer.save()
			elif not is_student_id_none:
				notice_viewer = NoticeViewer(notice = notice_object, for_students = True, for_staff = False, student = Student.objects.get(id = student_id), branch = None, batch = None, staff = None )
				notice_viewer.save()		
			else:
				notice_viewer = NoticeViewer(notice = notice_object, for_students = True, for_staff = False, student = None, branch = None, batch = None, staff = None )
				notice_viewer.save()		
			return notice_viewer.id
	elif not is_id_none:
		# TODO
		pass

		

def get_personal_notices(student_batch_id=None, staff_id=None, for_students=None, for_staff=None, notice_id=None):
		is_notice_id_none = notice_id==None
		is_student_batch_id_none = student_batch_id==None
		is_staff_id_none = staff_id==None
		is_for_students_none = for_students==None
		is_for_staff_none = for_staff==None
		
		if not is_notice_id_none:
			personal_notice = Notice.objects.get(id=notice_id)
			notice_object = {}
			notice_object['id'] = personal_notice.id
			notice_object['title'] = personal_notice.title
			notice_object['description'] = personal_notice.description
			notice_object['uploader'] = personal_notice.uploader
			notice_object['expiry_date'] = personal_notice.expiry_date
			notice_object['important'] = personal_notice.important
			return notice_object

		elif not is_student_batch_id_none:
			# get all objects related to that student, i.e., his own, his batch's, his branch's
			all_notices = []

			personal_notices = []
			student_batch_object = StudentBatch.objects.get(id=student_batch_id)
			personal_notice_set = NoticeViewer.objects.filter(student_batch=student_batch_object)
			for personal_notice in personal_notice_set:
				notice_object = {}
				notice_object['id'] = personal_notice.notice.id
				notice_object['student_batch'] = personal_notice.student_batch
				notice_object['batch'] = personal_notice.batch
				notice_object['branch'] = personal_notice.branch
				notice_object['for_staff'] = personal_notice.for_staff
				notice_object['for_students'] = personal_notice.for_students
				notice_object['staff'] = personal_notice.staff
				notice_object['title'] = personal_notice.notice.title
				notice_object['description'] = personal_notice.notice.description
				notice_object['uploader'] = personal_notice.notice.uploader
				notice_object['expiry_date'] = personal_notice.notice.expiry_date
				notice_object['important'] = personal_notice.notice.important

				personal_notices.append(notice_object)

			related_batch_notices = []
			student_batch = StudentBatch.objects.get(id=student_batch_id)
			is_batch_none = student_batch.batch == None
			is_academic_year_none = student_batch.academic_year == None
			is_standard_none = student_batch.standard == None

			if not is_batch_none:
				related_batch_notice_set = NoticeViewer.objects.filter(batch=student_batch.batch)

				for related_batch_notice in related_batch_notice_set:
					notice_object = {}
					notice_object['id'] = related_batch_notice.notice.id
					notice_object['student'] = related_batch_notice.student
					notice_object['batch'] = related_batch_notice.batch
					notice_object['branch'] = related_batch_notice.branch
					notice_object['for_staff'] = related_batch_notice.for_staff
					notice_object['for_students'] = related_batch_notice.for_students
					notice_object['staff'] = related_batch_notice.staff
					notice_object['title'] = related_batch_notice.notice.title
					notice_object['description'] = related_batch_notice.notice.description
					notice_object['uploader'] = related_batch_notice.notice.uploader
					notice_object['expiry_date'] = related_batch_notice.notice.expiry_date
					notice_object['important'] = related_batch_notice.notice.important

					related_batch_notices.append(notice_object)

			elif (not is_standard_none) and (not is_academic_year_none):
				# add standard related field to model NoticeViewer
				pass


			related_branch_notices = []
			related_branch_notice_set = NoticeViewer.objects.filter(branch=student_batch.batch.branch)

			for related_branch_notice in related_branch_notice_set:
				notice_object = {}
				notice_object['id'] = related_branch_notice.notice.id
				notice_object['student_batch'] = related_branch_notice.student_batch
				notice_object['for_staff'] = related_branch_notice.for_staff
				notice_object['for_students'] = related_branch_notice.for_students
				notice_object['staff'] = related_branch_notice.staff
				notice_object['title'] = related_branch_notice.notice.title
				notice_object['description'] = related_branch_notice.notice.description
				notice_object['uploader'] = related_branch_notice.notice.uploader
				notice_object['expiry_date'] = related_branch_notice.notice.expiry_date
				notice_object['important'] = related_branch_notice.notice.important

				related_branch_notices.append(notice_object)

			all_notices = personal_notices + related_batch_notices + related_branch_notices
			return all_notices

def get_batch_notices():
	pass

def get_branch_notices():
	pass

