# set_branch(branch_id,name)
# get_branch(branch_id)	if no parameters passed then return all branches

from portal.models import Branch

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


