from portal.models import *

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

		