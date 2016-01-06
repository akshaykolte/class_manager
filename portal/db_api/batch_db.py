# set_batch(batch_id,branch_id,academic_year_id,standard_id,name,desc)

# get_batch(batch_id,branch_id,academic_year_id,standard_id)

	# if academic_year_id is None then academic_year_id = get_current_academic_year()['id']
	# possible combinations: 0011, 0111, 0110, 1000
from portal.models import Batch,Branch,AcademicYear,Standard
from portal.db_api.academic_year_db import *

def set_batch(id=None,branch_id=None,academic_year_id=None,standard_id=None,name=None,description=None):
	is_none_id = id == None
	is_none_branch_id = branch_id == None
	is_none_academic_year_id = academic_year_id == None
	is_none_standard_id = standard_id == None
	is_none_name = name == None
	is_none_description = description == None

	if is_none_id:
		if is_none_academic_year_id:
			academic_year_id = get_current_academic_year()['id']
		batch_object = Batch(branch = Branch.objects.get(id = branch_id),academic_year = AcademicYear.objects.get(id = academic_year_id),
							standard = Standard.objects.get(id = standard_id),name = name,description = description)
		batch_object.save()
		return batch_object.id
	else:
		batch_object = Batch.objects.get(id = id)
		if not is_none_branch_id:
			batch_object.branch = Branch.objects.get(id = branch_id)
		if not is_none_academic_year_id:
			batch_object.academic_year = AcademicYear.objects.get(id = academic_year_id)
		if not is_none_standard_id:
			batch_object.standard = Standard.objects.get(id = standard_id)
		if not is_none_name:
			batch_object.name = name
		if not is_none_description:
			batch_object.description = description
		batch_object.save()
		return batch_object.id

def get_batch(id=None,branch_id =None,academic_year_id =None,standard_id =None):
	is_none_id = id == None
	is_none_branch_id = branch_id == None
	is_none_academic_year_id = academic_year_id == None
	is_none_standard_id = standard_id == None

	#0000
	if is_none_id and is_none_branch_id and is_none_academic_year_id and is_none_standard_id:
		batch_object_list = Batch.objects.all()
		batch_list = []

		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list

	#0010
	if is_none_id and is_none_branch_id and not is_none_academic_year_id and is_none_standard_id:
		batch_object_list = Batch.objects.filter(academic_year__id = academic_year_id)
		batch_list = []

		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year_id'] = batch_object.academic_year.id
			batch['branch_id'] = batch_object.branch.id
			batch['standard_id'] = batch_object.standard.id
			batch_list.append(batch)
		return batch_list


	#1000
	if not is_none_id:
		batch_object = Batch.objects.get(id = id)
		batch = {}
		batch['id'] = batch_object.id
		batch['name'] = batch_object.name
		batch['description'] = batch_object.description
		batch['academic_year'] = batch_object.academic_year
		batch['branch'] = batch_object.branch.name
		batch['branch_id'] = batch_object.branch.id
		batch['standard'] = batch_object.standard.name
		return batch

	#0110
	if is_none_id and not is_none_branch_id and not is_none_academic_year_id and is_none_standard_id:
		batch_object_list = Batch.objects.filter(branch = Branch.objects.get(id = branch_id),
						academic_year = AcademicYear.objects.get(id = academic_year_id))
		batch_list = []
		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list

	#0100
	if is_none_id and not is_none_branch_id and is_none_academic_year_id and is_none_standard_id:
		batch_object_list = Batch.objects.filter(branch = Branch.objects.get(id = branch_id),
						academic_year__id = get_current_academic_year()['id'])
		batch_list = []
		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list

	#0111
	if is_none_id and not is_none_branch_id and not is_none_academic_year_id and not is_none_standard_id:
		batch_object_list = Batch.objects.filter(branch = Branch.objects.get(id = branch_id),
						academic_year = AcademicYear.objects.get(id = academic_year_id),standard = Standard.objects.get(id = standard_id))
		batch_list = []
		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list

	#0101
	if is_none_id and not is_none_branch_id and is_none_academic_year_id and not is_none_standard_id:
		batch_object_list = Batch.objects.filter(branch = Branch.objects.get(id = branch_id),
						academic_year__id = get_current_academic_year()['id'],standard = Standard.objects.get(id = standard_id))
		batch_list = []
		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list

	#0011
	if is_none_id and is_none_branch_id and not is_none_academic_year_id and not is_none_standard_id:
		batch_object_list = Batch.objects.filter(academic_year = AcademicYear.objects.get(id = academic_year_id),standard = Standard.objects.get(id = standard_id))
		batch_list = []
		for batch_object in batch_object_list:
			batch = {}
			batch['id'] = batch_object.id
			batch['name'] = batch_object.name
			batch['description'] = batch_object.description
			batch['academic_year'] = batch_object.academic_year
			batch['branch'] = batch_object.branch.name
			batch['standard'] = batch_object.standard.name
			batch_list.append(batch)
		return batch_list
