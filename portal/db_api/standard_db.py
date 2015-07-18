# set_standard(standard_id,name)
# set_standard(standard_id) if no parameters passed then return all standards

from portal.models import Standard
def set_standard(id = None,name = None):
	is_none_id = id == None
	is_none_name = name == None

	if is_none_id:
		standard_object = Standard(name = name)
		standard_object.save()
		return standard_object.id
	else:
		standard_object = Standard.objects.get(id = id)
		if not is_none_name:
			standard_object.name = name
		standard_object.save()
		return standard_object.id
