from portal.models import Notice, NoticeViewer, Staff

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