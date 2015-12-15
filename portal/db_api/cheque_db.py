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
			

def get_cheque(id = None, student_id = None, start_date = None, end_date = None, cleared = None, cheque_number = None):

	is_none_id = id == None
	is_none_student_id = student_id == None
	is_none_start_date = start_date == None
	is_none_end_date = end_date == None
	is_none_cleared = cleared == None
	is_none_cheque_number = cheque_number == None

	#get particular cheque
	if not is_none_id:
		i = Cheque.objects.get(id = id)
		cheque_dict = {}
		cheque_dict['id'] = i.id
		cheque_dict['student_id'] = i.student.id
		cheque_dict['amount'] = i.amount
		cheque_dict['cheque_date'] = i.cheque_date
		cheque_dict['cleared'] = i.cleared
		cheque_dict['clearance_date'] = i.clearance_date
		cheque_dict['description'] = i.description
		cheque_dict['cheque_number'] = i.cheque_number
		cheque_dict['bank_name'] = i.bank_name
		cheque_dict['bank_branch_name'] = i.bank_branch_name

		return cheque_dict
	
	#get cheques of particular student		
	if not is_none_student_id:
		cheques = Cheque.objects.filter(student = Student.objects.get(id = student_id))
		cheque_list = []

		for i in cheques:
			cheque_dict = {}
			cheque_dict['id'] = i.id
			cheque_dict['student_id'] = i.student.id
			cheque_dict['amount'] = i.amount
			cheque_dict['cheque_date'] = i.cheque_date
			cheque_dict['cleared'] = i.cleared
			cheque_dict['clearance_date'] = i.clearance_date
			cheque_dict['description'] = i.description
			cheque_dict['cheque_number'] = i.cheque_number
			cheque_dict['bank_name'] = i.bank_name
			cheque_dict['bank_branch_name'] = i.bank_branch_name

			cheque_list.append(cheque_dict)

		return cheque_list	

	#get cleared checques (all/in a date range according to clearance date) 	
	if not is_none_cleared and cleared:
		#all cleared cheques
		if is_none_start_date and is_none_end_date:
			cheques = Cheque.objects.filter(cleared = True)
			cheque_list = []

			for i in cheques:
				cheque_dict = {}
				cheque_dict['id'] = i.id
				cheque_dict['student_id'] = i.student.id
				cheque_dict['amount'] = i.amount
				cheque_dict['cheque_date'] = i.cheque_date
				cheque_dict['cleared'] = i.cleared
				cheque_dict['clearance_date'] = i.clearance_date
				cheque_dict['description'] = i.description
				cheque_dict['cheque_number'] = i.cheque_number
				cheque_dict['bank_name'] = i.bank_name
				cheque_dict['bank_branch_name'] = i.bank_branch_name

				cheque_list.append(cheque_dict)

			return cheque_list

		#in a date range
		if not is_none_start_date and is_none_end_date:
			cheques = Cheque.objects.filter(cleared = True, clearance_date__gte = start_date)
			cheque_list = []

			for i in cheques:
				cheque_dict = {}
				cheque_dict['id'] = i.id
				cheque_dict['student_id'] = i.student.id
				cheque_dict['amount'] = i.amount
				cheque_dict['cheque_date'] = i.cheque_date
				cheque_dict['cleared'] = i.cleared
				cheque_dict['clearance_date'] = i.clearance_date
				cheque_dict['description'] = i.description
				cheque_dict['cheque_number'] = i.cheque_number
				cheque_dict['bank_name'] = i.bank_name
				cheque_dict['bank_branch_name'] = i.bank_branch_name

				cheque_list.append(cheque_dict)

			return cheque_list

		if is_none_start_date and not is_none_end_date:
			cheques = Cheque.objects.filter(cleared = True, clearance_date__lte = end_date)
			cheque_list = []

			for i in cheques:
				cheque_dict = {}
				cheque_dict['id'] = i.id
				cheque_dict['student_id'] = i.student.id
				cheque_dict['amount'] = i.amount
				cheque_dict['cheque_date'] = i.cheque_date
				cheque_dict['cleared'] = i.cleared
				cheque_dict['clearance_date'] = i.clearance_date
				cheque_dict['description'] = i.description
				cheque_dict['cheque_number'] = i.cheque_number
				cheque_dict['bank_name'] = i.bank_name
				cheque_dict['bank_branch_name'] = i.bank_branch_name

				cheque_list.append(cheque_dict)

			return cheque_list

		if not is_none_start_date and not is_none_end_date:
			cheques = Cheque.objects.filter(cleared = True, clearance_date__lte = end_date, clearance_date__gte = start_date)
			cheque_list = []

			for i in cheques:
				cheque_dict = {}
				cheque_dict['id'] = i.id
				cheque_dict['student_id'] = i.student.id
				cheque_dict['amount'] = i.amount
				cheque_dict['cheque_date'] = i.cheque_date
				cheque_dict['cleared'] = i.cleared
				cheque_dict['clearance_date'] = i.clearance_date
				cheque_dict['description'] = i.description
				cheque_dict['cheque_number'] = i.cheque_number
				cheque_dict['bank_name'] = i.bank_name
				cheque_dict['bank_branch_name'] = i.bank_branch_name

				cheque_list.append(cheque_dict)

			return cheque_list		












	#get all cheques
	else: 
		cheques = Cheque.objects.all()
		cheque_list = []

		for i in cheques:
			cheque_dict = {}
			cheque_dict['id'] = i.id
			cheque_dict['student_id'] = i.student.id
			cheque_dict['amount'] = i.amount
			cheque_dict['cheque_date'] = i.cheque_date
			cheque_dict['cleared'] = i.cleared
			cheque_dict['clearance_date'] = i.clearance_date
			cheque_dict['description'] = i.description
			cheque_dict['cheque_number'] = i.cheque_number
			cheque_dict['bank_name'] = i.bank_name
			cheque_dict['bank_branch_name'] = i.bank_branch_name

			cheque_list.append(cheque_dict)

		return cheque_list