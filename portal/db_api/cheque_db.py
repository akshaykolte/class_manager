from portal.models import *


def set_cheque(id = None, student_id = None, amount = None, cheque_date = None, cleared = None, clearance_date = None, description = None, cheque_number = None, bank_name = None, bank_branch_name = None):

	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_amount = amount == None
	is_none_cheque_date = cheque_date == None
	is_none_cleared = cleared == None
	is_none_clearance_date = clearance_date == None
	is_none_description = description == None
	is_none_cheque_number = cheque_number == None
	is_none_bank_name = bank_name == None
	is_none_bank_branch_name = bank_branch_name == None	

	if not is_none_id :
		#Edit amount, chequedate, description,cleared, clearancedate. Student cannot be edited
		cheque_object = Cheque.objects.get(id = id)
		
		cheque_object.amount = amount
		cheque_object.cheque_date = cheque_date
		cheque_object.cleared = cleared
		cheque_object.clearance_date = clearance_date
		cheque_object.description = description
		cheque_object.cheque_number =cheque_number
		cheque_object.bank_name = bank_name
		cheque_object.bank_branch_name = bank_branch_name

		cheque_object.save()

		return cheque_object.id

	if is_none_id and not is_none_student_id and not is_none_amount and not is_none_cheque_date and not is_none_cleared :
		
		student_object = Student.objects.get(id = student_id)
		cheque_object = Cheque(student = student_object, amount = amount, cheque_date = cheque_date, cleared = cleared, clearance_date = clearance_date, description = description, cheque_number = cheque_number, bank_name = bank_name, bank_branch_name = bank_branch_name)
		cheque_object.save()

		return cheque_object.id

	else :
		raise Exception('Wrong set of arguments')
			