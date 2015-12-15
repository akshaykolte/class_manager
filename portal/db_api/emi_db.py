from portal.models import *


def set_emi(id = None, student_id = None, amount_due = None, time_deadline = None, description = None):

	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_amount_due = amount_due == None
	is_none_time_deadline = time_deadline == None
	is_none_description = description == None

	if not is_none_id :
		#Edit amount, deadline, description. Student cannot be edited
		emi_object = EMI.objects.get(id = id)
		emi_object.amount_due = amount_due
		emi_object.time_deadline = time_deadline
		emi_object.description = description
		emi_object.save()

		return emi_object.id

	if is_none_id and not is_none_student_id and not is_none_amount_due and not is_none_time_deadline and not is_none_description :
		
		student_object = Student.objects.get(id = student_id)
		emi_object = EMI(student = student_object, amount_due = amount_due, time_deadline = time_deadline, description = description)
		emi_object.save()

		return emi_object.id

	else :
		raise Exception('Wrong set of arguments')
			