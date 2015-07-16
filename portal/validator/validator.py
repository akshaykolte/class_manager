from portal.models import *

def validate_lecture_batch(lecture_batch_object):

	if lecture_batch_object.batch.academic_year.id == lecture_batch_object.lecture.subject_year.academic_year.id:
		return True
	else:
		return False		
