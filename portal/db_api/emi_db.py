from portal.models import *
import datetime
from django.db.models import Sum, Max


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

def get_student_emi(student_id):
	#TODO
	pass

def get_pending_emi():
	emis = EMI.objects.filter(time_deadline__lte = datetime.datetime.now()).values('student__id', 'student__first_name', 'student__last_name').annotate(Sum('amount_due'), Max('time_deadline'))
	payments = FeeTransaction.objects.filter(fee_type__name = 'payment').values('student__id', 'student__first_name', 'student__last_name').annotate(Sum('amount'))

	payments_dict = {}

	for payment in payments:
		payments_dict[(payment['student__id'], payment['student__first_name'], payment['student__last_name'])] = payment['amount__sum']

	pending_students_list = []

	for emi in emis:
		student_tuple = (emi['student__id'], emi['student__first_name'], emi['student__last_name'])
		if emi['amount_due__sum'] > payments_dict[student_tuple]:
			pending_students_list.append(list(student_tuple) + [emi['time_deadline__max']])

	#print pending_students_list
	return pending_students_list

def get_next_week_emi():

	pending_emi_list = get_pending_emi()
	student_id_set = set()

	for emi in pending_emi_list:
		student_id_set.add(emi[0])

	emis = EMI.objects.filter(time_deadline__lte = datetime.datetime.now() + datetime.timedelta(days=7)).values('student__id', 'student__first_name', 'student__last_name').annotate(Sum('amount_due'), Max('time_deadline'))
	payments = FeeTransaction.objects.filter(fee_type__name = 'payment').values('student__id', 'student__first_name', 'student__last_name').annotate(Sum('amount'))

	payments_dict = {}

	for payment in payments:
		payments_dict[(payment['student__id'], payment['student__first_name'], payment['student__last_name'])] = payment['amount__sum']

	pending_students_list = []

	for emi in emis:
		student_tuple = (emi['student__id'], emi['student__first_name'], emi['student__last_name'])
		if emi['amount_due__sum'] > payments_dict[student_tuple]:
			if student_tuple[0] not in student_id_set:
				pending_students_list.append(list(student_tuple) + [emi['time_deadline__max']])

	print pending_students_list
