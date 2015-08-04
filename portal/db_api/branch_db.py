# set_branch(branch_id,name)
# get_branch(branch_id)	if no parameters passed then return all branches

from portal.models import Branch
from portal.models import StaffRole
from portal.models import Role

def set_branch(id = None,name = None):
	is_none_id = id == None
	is_none_name = name == None

	if is_none_id:
		branch_object = Branch(name=name)
		branch_object.save()
		return branch_object.id
	else:
		branch_object = Branch.objects.get(id=id)
		if not is_none_name:
			branch_object.name = name
		branch_object.save()
		return branch_object.id

def get_branch(id=None):
	is_none_id = id == None
	if not is_none_id:
		branch_object = Branch.objects.get(id=id)
		branch={}
		branch['name'] = branch_object.name
		return branch
	else:
		branch_object_list = Branch.objects.all()
		branch_list=[]
		for branch_object in branch_object_list:
			branch={}
			branch['name'] = branch_object.name
			branch_list.append(branch)
		return branch_list

def get_branch_of_manager(manager_id):
	staff_roles = StaffRole.objects.filter(role__name='manager', staff__id=manager_id)
	branch_list = []
	for staff_role in staff_roles:
		branch_obj = {}
		branch_obj['id'] = staff_role.branch.id
		branch_obj['name'] = staff_role.branch.name
		branch_list.append(branch_obj)
	return branch_list
