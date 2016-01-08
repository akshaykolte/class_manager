# set_staff(staff_id,details)
# set_staff_role(staff_role_id,role_id,staff_id,branch_id)
# get_staff(staff_id)
# get_staff_role(staff_role_id,role_id,staff_id,branch_id) possible combinations: 0000 0001 0010 0100 1000
from portal.models import Staff,StaffRole,Branch,Role

def set_staff(id = None, username = None, password = None, first_name = None, last_name = None, address = None, email = None, phone_number = None, gender = None):
	is_none_id = id == None
	is_none_username = username == None
	is_none_password = password == None
	is_none_first_name = first_name == None
	is_none_last_name = last_name == None
	is_none_address = address == None
	is_none_email = email == None
	is_none_phone_number = phone_number == None
	is_none_gender = gender == None

	if is_none_id:
		staff_object = Staff(username = username,password = password,
						first_name = first_name,last_name =last_name, address = address, email = email,phone_number=phone_number, gender=gender)
		staff_object.save()
		return staff_object.id

	else:
		staff_object = Staff.objects.get(id=id)
		if not is_none_username:
			staff_object.username = username
		if not is_none_password:
			staff_object.password = password
		if not is_none_first_name:
			staff_object.first_name = first_name
		if not is_none_last_name:
			staff_object.last_name = last_name
		if not is_none_address:
			staff_object.address = address
		if not is_none_email:
			staff_object.email = email
		if not is_none_phone_number:
			staff_object.phone_number = phone_number
		if not is_none_gender:
			staff_object.gender = gender
		staff_object.save()
		return staff_object.id

def set_staff_role(id = None,role_id = None,staff_id = None,branch_id = None):
	is_none_id = id == None
	is_none_role_id = role_id == None
	is_none_staff_id = staff_id == None
	is_none_branch_id = branch_id == None
	try:

		if is_none_id:
			staff_role_object = StaffRole(role = Role.objects.get(id = role_id),staff = Staff.objects.get(id = staff_id),branch = Branch(id=branch_id))
			staff_role_object.save()
			return staff_role_object.id

		else:
			staff_role_object = StaffRole.objects.get(id = id)
			if not is_none_role_id:
				staff_role_object.role = Role.objects.get(id = role_id)
			if not is_none_staff_id:
				staff_role_object.staff = Staff.objects.get(id = staff_id)
			if not is_none_branch_id:
				staff_role_object.branch = Branch.objects.get(id = branch_id)
			staff_role_object.save()
			return staff_role_object.id

	except Exception, e: # TODO catch IntegrityError
		print str(e)
		# try except is intentionally done here.
		return False

def get_staff(id = None, role_name = None, branch_id=None):
	'''
			Possible combination of parameters: 000, 1XX, 010, 001, 011
	'''
	is_none_id = id == None
	is_none_role_name = role_name == None
	is_none_branch_id = branch_id == None
	if not is_none_id:
		'''
			Parameter combination: 1XX
		'''
		staff_object = Staff.objects.get(id=id)
		staff = {}
		staff['id'] = staff_object.id
		staff['username'] = staff_object.username
		staff['password'] = staff_object.password
		staff['first_name'] = staff_object.first_name
		staff['last_name'] = staff_object.last_name
		staff['address'] = staff_object.address
		staff['email'] = staff_object.email
		staff['phone_number'] = staff_object.phone_number
		staff['gender'] = staff_object.gender
		return staff

	staff_object_list = []
	if is_none_role_name and is_none_branch_id:
		'''
			Parameter combination: 000
		'''
		staff_object_list = Staff.objects.all()
	elif not is_none_role_name and is_none_branch_id:
		'''
			Parameter combination: 010
		'''
		staff_object_list = Staff.objects.filter(staffrole__role__name=role_name).distinct()
	elif is_none_role_name and not is_none_branch_id:
		'''
			Parameter combination: 001
		'''
		staff_object_list = Staff.objects.filter(staffrole__branch__id=branch_id).distinct()
	elif not is_none_role_name and not is_none_branch_id:
		'''
			Parameter combination: 001
		'''
		staff_object_list = Staff.objects.filter(staffrole__role__name=role_name, staffrole__branch__id=branch_id).distinct()


	staff_list=[]
	for staff_object in staff_object_list:
		staff = {}
		staff['id'] = staff_object.id
		staff['username'] = staff_object.username
		staff['password'] = staff_object.password
		staff['first_name'] = staff_object.first_name
		staff['last_name'] = staff_object.last_name
		staff['address'] = staff_object.address
		staff['email'] = staff_object.email
		staff['phone_number'] = staff_object.phone_number
		staff['gender'] = staff_object.gender
		staff_list.append(staff)
	return staff_list



def get_staff_role(id = None,role_id = None,staff_id = None,branch_id = None,role_name = None):
	is_none_id = id == None
	is_none_role_id = role_id == None
	is_none_staff_id = staff_id == None
	is_none_branch_id = branch_id == None
	is_none_role_name = role_name == None

	#00000
	if is_none_id and is_none_role_id and is_none_staff_id and is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.all()
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role['branch_id'] = staff_role_object.branch.id
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role_list.append(staff_role)
		return staff_role_list

	#10000
	elif not is_none_id and is_none_role_id and is_none_staff_id and is_none_branch_id and is_none_role_name:
		staff_role_object = StaffRole.objects.get(id=id)
		staff_role = {}
		staff_role['id'] = staff_role_object.id
		staff_role['role'] = staff_role_object.role.name
		staff_role['staff_first_name'] = staff_role_object.staff.first_name
		staff_role['staff_last_name'] = staff_role_object.staff.last_name
		staff_role['branch'] = staff_role_object.branch.name
		staff_role['branch_id'] = staff_role_object.branch.id
		staff_role['branch_name'] = staff_role_object.branch.name
		return staff_role

	#01000
	elif is_none_id and not is_none_role_id and is_none_staff_id and is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.filter(role = Role.objects.get(id = role_id))
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role['branch_id'] = staff_role_object.branch.id
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role_list.append(staff_role)
		return staff_role_list

	#00100
	elif is_none_id and is_none_role_id and not is_none_staff_id and is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.filter(staff = Staff.objects.get(id=staff_id))
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role['branch_id'] = staff_role_object.branch.id
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role['staff_id'] = staff_role_object.staff.id
			staff_role_list.append(staff_role)
		return staff_role_list

	#01100
	elif is_none_id and not is_none_role_id and not is_none_staff_id and is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.filter(staff = Staff.objects.get(id=staff_id), role__id = role_id)
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role['branch_id'] = staff_role_object.branch.id
			staff_role_list.append(staff_role)
		return staff_role_list

	#00010
	elif is_none_id and is_none_role_id and is_none_staff_id and not is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.filter(branch = Branch.objects.get(id = branch_id))
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role_list.append(staff_role)
		return staff_role_list
	#01110
	elif is_none_id and not is_none_role_id and not is_none_staff_id and not is_none_branch_id and is_none_role_name:
		staff_role_object_list = StaffRole.objects.filter(staff = Staff.objects.get(id=staff_id), role__id = role_id, branch__id = branch_id)
		staff_role_list = []
		for staff_role_object in staff_role_object_list:
			staff_role = {}
			staff_role['id'] = staff_role_object.id
			staff_role['role'] = staff_role_object.role.name
			staff_role['staff_first_name'] = staff_role_object.staff.first_name
			staff_role['staff_last_name'] = staff_role_object.staff.last_name
			staff_role['branch'] = staff_role_object.branch.name
			staff_role['branch_name'] = staff_role_object.branch.name
			staff_role['branch_id'] = staff_role_object.branch.id
			staff_role_list.append(staff_role)
		return staff_role_list
	#00111
	elif is_none_id and is_none_role_id and not is_none_staff_id and not is_none_branch_id and not is_none_role_name:
		print "---!"
		print staff_id, role_name, branch_id
		staff_role_object = StaffRole.objects.get(staff__id=staff_id, role__name = role_name, branch__id = branch_id)
		print "--- ",staff_role_object
		staff_role = {}
		staff_role['id'] = staff_role_object.id
		staff_role['role'] = staff_role_object.role.name
		staff_role['staff_first_name'] = staff_role_object.staff.first_name
		staff_role['staff_last_name'] = staff_role_object.staff.last_name
		staff_role['branch'] = staff_role_object.branch.name
		staff_role['branch_name'] = staff_role_object.branch.name
		staff_role['branch_id'] = staff_role_object.branch.id
		return staff_role

def search_staffs(first_name='', last_name='', username='', email='', phone_number=''):
	# TODO Think of optimisation (probably using indexes)
	staffs = Staff.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name, username__icontains=username, email__icontains=email, phone_number__icontains=phone_number)
	staff_list = []
	for i in staffs:
		staff_dict = {}
		staff_dict['id'] = i.id
		staff_dict['username'] = i.username
		staff_dict['first_name'] = i.first_name
		staff_dict['last_name'] = i.last_name
		staff_dict['email'] = i.email
		staff_dict['phone_number'] = i.phone_number
		staff_list.append(staff_dict)

	return staff_list


def delete_staff_role(staff=None, role=None, branch=None):
	StaffRole.objects.filter(staff__id=staff, role__id=role, branch__id=branch).delete()
