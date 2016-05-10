from portal.models import *

def get_user(request):
	msg = 'Incorrect login details'
	if 'login' in request.POST:
		request.session['user'] = {'logged_in':False, 'msg': msg}
		username = request.POST['username']
		password = request.POST['password']

		if Staff.objects.filter(username=username,password=password).exists() and Staff.objects.get(username=username,password=password).current_employee == True:
			staff_obj = Staff.objects.get(username=username,password=password)

			request.session['user']['logged_in'] = True
			request.session['user']['login_type'] = 'staff'
			request.session['user']['user_name'] = username
			request.session['user']['first_name'] = staff_obj.first_name
			request.session['user']['last_name'] = staff_obj.last_name

			request.session['user']['permission_admin'] = False
			request.session['user']['permission_manager'] = False
			request.session['user']['permission_teacher'] = False
			request.session['user']['permission_accountant'] = False
			request.session['user']['permission_parent'] = False
			request.session['user']['permission_student'] = False

			staff_roles = StaffRole.objects.filter(staff__id = staff_obj.id)

			for staff_role_obj in staff_roles:
				if(staff_role_obj.role.name == 'manager'):
					request.session['user']['permission_manager'] = True


				if(staff_role_obj.role.name == 'teacher'):
					request.session['user']['permission_teacher'] = True

				if(staff_role_obj.role.name == 'accountant'):
					request.session['user']['permission_accountant'] = True

				if(staff_role_obj.role.name == 'admin'):
					request.session['user']['permission_admin'] = True
					request.session['user']['permission_manager'] = True
					request.session['user']['permission_teacher'] = True
					request.session['user']['permission_accountant'] = True


			request.session['user']['id'] = staff_obj.id

			request.session.modified = True

		elif Student.objects.filter(username=username,password=password).exists():
			student_obj = Student.objects.get(username=username,password=password)
			if StudentBatch.objects.filter(student = student_obj,academic_year = AcademicYear.objects.get(is_current = True)).exists() or StudentBatch.objects.filter(student = student_obj,batch__academic_year = AcademicYear.objects.get(is_current = True)).exists():
				request.session['user']['user_name'] = username
				request.session['user']['logged_in'] = True
				request.session['user']['login_type']='student'
				request.session['user']['first_name'] = student_obj.first_name
				request.session['user']['last_name'] = student_obj.last_name

				request.session['user']['permission_admin'] = False
				request.session['user']['permission_manager'] = False
				request.session['user']['permission_teacher'] = False
				request.session['user']['permission_accountant'] = False
				request.session['user']['permission_parent'] = False

				request.session['user']['permission_student'] = True
				request.session['user']['id'] = student_obj.id
				request.session['user']['first_name'] = student_obj.first_name
				request.session['user']['last_name'] = student_obj.last_name
				request.session.modified = True
			else:
				msg = 'Sorry, you are not admitted to current academic year'
				request.session['user']['msg'] = msg


		elif Parent.objects.filter(username=username,password=password).exists():
			parent_obj = Parent.objects.get(username=username,password=password)

			if not StudentParent.objects.filter(parent = parent_obj).exists():
				msg = 'No ward assigned to you, please contact the organisation'
				request.session['user']['msg'] = msg
			elif StudentBatch.objects.filter(student = StudentParent.objects.get(parent = parent_obj).student ,academic_year = AcademicYear.objects.get(is_current = True)).exists() or StudentBatch.objects.filter(student = StudentParent.objects.get(parent = parent_obj).student, batch__academic_year = AcademicYear.objects.get(is_current = True)).exists():
				request.session['user']['user_name'] = username
				request.session['user']['logged_in'] = True
				request.session['user']['login_type']='parent'
				request.session['user']['first_name'] = parent_obj.first_name
				request.session['user']['last_name'] = parent_obj.last_name

				request.session['user']['permission_admin'] = False
				request.session['user']['permission_manager'] = False
				request.session['user']['permission_teacher'] = False
				request.session['user']['permission_accountant'] = False
				request.session['user']['permission_student'] = False

				request.session['user']['permission_parent'] = True
				request.session['user']['id'] = parent_obj.id
				request.session.modified = True
			else:
				msg = 'Sorry, your ward is not admitted to current academic year'
				request.session['user']['msg'] = msg

	if not 'user' in request.session:
		request.session['user'] = {'logged_in':False, 'msg': msg}
		request.session.modified = True
	return request.session['user']



def set_logout(request):
	request.session['user']={'logged_in':False}


def change_password_db(request):

	if 'oldpassword' in request.POST :

		if request.POST['newpassword'] == request.POST['repassword']:
			if request.session['user']['login_type']=='staff':
				staff_obj=Staff.objects.get(id=request.session['user']['id'])
				if staff_obj.password == request.POST['oldpassword']:
					staff_obj.password=request.POST['newpassword']
					staff_obj.save()
					return True

				else:
					#print "passwd dont match"
					return False


			elif request.session['user']['login_type']=='parent':
				parent_obj=Parent.objects.get(id=request.session['user']['id'])
				if parent_obj.password == request.POST['oldpassword']:
					parent_obj.password=request.POST['newpassword']
					parent_obj.save()
					return True

				else:
					#print "passwd dont match"
					return False

			elif request.session['user']['login_type']=='student':
				student_obj=Student.objects.get(id=request.session['user']['id'])
				if student_obj.password == request.POST['oldpassword']:
					student_obj.password=request.POST['newpassword']
					student_obj.save()
					return True
				else:
					#print "passwd dont match"
					return False
		else:
				#print "passwd dont match"
				return False

	else:
				#print "passwd dont match"
				return False

	return request.session['user']
