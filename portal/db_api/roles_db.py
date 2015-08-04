from portal.models import Role

def get_role_by_name(role_name):
	role = Role.objects.get(name=role_name)
	role_obj = {}
	role_obj['id'] = role.id
	role_obj['name'] = role.name

	return role_obj