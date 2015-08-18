from portal.models import *


def insert_roles():

	print "Adding Roles..."
	
	f = open("dummy_db/roles.txt", "r+")
	for role in f.readlines():
		if not Role.objects.filter(name=role).exists():
			role_obj = Role(name=role);
			role_obj.save()

	print "Added Roles Successfully"
	
def insert_academic_years():
	print "Adding Academic Years..."
	
	f = open("dummy_db/academic_years.txt", "r+")
	for ay in f.readlines():
		line = ay.split()
		year_start = int(line[0])
		year_end = int(line[1])
		if line[2] == "true":
			is_current = 1
		else:
			is_current = 0

		if not AcademicYear.objects.filter(year_start=year_start, year_end=year_end).exists():
			ay_obj = AcademicYear(year_start=year_start, year_end=year_end, is_current=is_current)
			ay_obj.save()

	print "Added Academic Years Successfully"


def insert_fee_types():
	print "Adding Fee Types..."
	
	f = open("dummy_db/fee_types.txt", "r+")
	for fee in f.readlines():
		if not FeeType.objects.filter(name=fee).exists():
			fee_obj = FeeType(name=fee)
			fee_obj.save()

	print "Added Fee Types Successfully"



insert_academic_years()
insert_roles()
insert_fee_types()
