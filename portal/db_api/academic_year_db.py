# add/modify academic year
# get academic year
# set current academic year
# get current academic year
from portal.models import AcademicYear

def set_academic_year(id = None , year_start = None , year_end = None):
	is_none_id = id == None
	is_none_year_start = year_start == None
	is_none_year_end = year_end == None

	if is_none_id:
		academic_year_object = AcademicYear(year_start=year_start , year_end=year_end , is_current = False)
		academic_year_object.save()
		return academic_year_object.id

	else:
		academic_year_object = AcademicYear.objects.get(id=id)
		if not is_none_year_start:
			academic_year_object.year_start = year_start
		if not is_none_year_end:
			academic_year_object.year_end = year_end
		academic_year_object.save()
		return academic_year_object.id	

def get_academic_year(id=None):
	is_none_id = id == None

	if is_none_id:
		academic_year_list = []
		academic_year_object_list = AcademicYear.objects.all()
		for academic_year_object in academic_year_object_list:
			academic_year_id = academic_year_object.id
			academic_year_name = str(academic_year_object.year_start) + '-' + str(academic_year_object.year_end)
			academic_year_object_year_start = academic_year_object.year_start
			academic_year_object_year_end = academic_year_object.year_end
			academic_year_list.append({'id': academic_year_id , 'name' : academic_year_name , 'year_start' : academic_year_object_year_start , 'year_end' :  academic_year_object_year_end})
		return academic_year_list
	else:
		academic_year_object = AcademicYear.objects.get(id=id)
		academic_year_id = academic_year_object.id
		academic_year_name = str(academic_year_object.year_start) + '-' + str(academic_year_object.year_end)
		academic_year_object_year_start = academic_year_object.year_start
		academic_year_object_year_end = academic_year_object.year_end
		return {'id': academic_year_id , 'name' : academic_year_name , 'year_start' : academic_year_object_year_start , 'year_end' :  academic_year_object_year_end}



def set_current_academic_year(id):

	if not AcademicYear.objects.filter(id=id).exists():
		raise Exception('No Such Academic Year Found')
	else:
		AcademicYear.objects.all().update(is_current=False)
		academic_year_object = AcademicYear.objects.get(id=id)
		academic_year_object.is_current = True
		academic_year_object.save()
		return academic_year_object.id

def get_current_academic_year():
	if not AcademicYear.objects.filter(is_current=True).exists():
		raise Exception("No Current Academic Year Set")
	else:
		current_academic_year = AcademicYear.objects.get(is_current=True)	
		current_academic_year_id = current_academic_year.id
		current_academic_year_name = str(current_academic_year.year_start) + '-' + str(current_academic_year.year_end)
		current_academic_year_start = current_academic_year.year_start
		current_academic_year_end = current_academic_year.year_end
		return {'id' : current_academic_year_id ,'name': current_academic_year_name, 'year_start' : current_academic_year_start , 'year_end' : current_academic_year_end}

