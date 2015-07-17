from portal.models import *

def get_user(request):
	if 'username' in request.POST:
		request.session['user'] = {'logged_in':False}
		username = request.POST['username']
		password = request.POST['password']

		if Staff.objects.filter(username=username,password=password).exists():
			staff_obj = Staff.objects.get(username=username,password=password)
			
			request.session['user']['logged_in'] = True
			request.session['user']['login_type'] = 'staff'

			request.session['user']['permission_admin'] = False
			request.session['user']['permission_manager'] = False
			request.session['user']['permission_teacher'] = False
			request.session['user']['permission_accountant'] = False
			request.session['user']['permission_parent'] = False
			request.session['user']['permission_student'] = False

			staff_roles = Staff.objects.filter(staff = staff_obj)

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
			request.session['user']['logged_in'] = True
			request.session['user']['login_type']='student'

			request.session['user']['permission_admin'] = False
			request.session['user']['permission_manager'] = False
			request.session['user']['permission_teacher'] = False
			request.session['user']['permission_accountant'] = False
			request.session['user']['permission_parent'] = False

			request.session['user']['permission_student'] = True
			request.session['user']['id'] = student_obj.id
			request.session.modified = True


		elif Parent.objects.filter(username=username,password=password).exists():
			parent_obj = Parent.objects.get(username=username,password=password)
			request.session['user']['logged_in'] = True
			request.session['user']['login_type']='parent'

			
			request.session['user']['permission_admin'] = False
			request.session['user']['permission_manager'] = False
			request.session['user']['permission_teacher'] = False
			request.session['user']['permission_accountant'] = False
			request.session['user']['permission_student'] = False

			request.session['user']['permission_parent'] = True
			request.session['user']['id'] = parent_obj.id
			request.session.modified = True

	if not 'user' in request.session:
		request.session['user'] = {'logged_in':False}
		request.session.modified = True
	return request.session['user']



def set_logout(request):
	request.session['user']={'logged_in':False}


def change_password_db(request):

	if 'oldpassword' in request.POST :
		
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


	return request.session['user']

		
