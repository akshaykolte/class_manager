from portal.models import *

	
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
	f.close()
	print "Added Academic Years Successfully"
	print ""


def insert_branches():

	print "Adding Branches..."
	
	f = open("dummy_db/branches.txt", "r+")
	for branch in f.readlines():
		line = branch.split('$')
		name = line[0]
		address = line[1]
		address = address.rstrip('\n')
		if not Branch.objects.filter(name=name, address=address).exists():
			br_obj = Branch(name=name, address=address);
			br_obj.save()
	f.close()
	print "Added Branches Successfully"
	print ""



def insert_roles():

	print "Adding Roles..."
	
	f = open("dummy_db/roles.txt", "r+")
	for role in f.readlines():
		role = role.rstrip('\n')
		if not Role.objects.filter(name=role).exists():
			role_obj = Role(name=role);
			role_obj.save()
	f.close()
	print "Added Roles Successfully"
	print ""


def insert_fee_types():
	print "Adding Fee Types..."
	
	f = open("dummy_db/fee_types.txt", "r+")
	for fee in f.readlines():
		fee = fee.rstrip('\n')
		if not FeeType.objects.filter(name=fee).exists():
			fee_obj = FeeType(name=fee)
			fee_obj.save()
	f.close()
	print "Added Fee Types Successfully"
	print ""


def insert_standards():
	print "Adding Standards..."
	
	f = open("dummy_db/standards.txt", "r+")
	for st in f.readlines():
		st = st.rstrip('\n')
		if not Standard.objects.filter(name=st).exists():
			st_obj = Standard(name=st)
			st_obj.save()
	f.close()
	print "Added Standards Successfully"
	print ""


def insert_subjects():
	print "Adding Subjects..."

	f = open("dummy_db/subjects.txt", "r+")
	
	for subs in f.readlines():
		line = subs.split()
		name = line[0]
		standard = line[1]
		standard = standard.rstrip('\n')
		if not Subject.objects.filter(name=name, standard=Standard.objects.get(name=standard)).exists():
			sub_obj = Subject(name=name, standard=Standard.objects.get(name=standard))
			sub_obj.save()
	f.close()
	print "Added Subjects Successfully"
	print ""


def insert_students():
	print "Adding Students..."

	f = open("dummy_db/students.txt", "r+")
	
	for stu in f.readlines():
		line = stu.split('$')
		username = line[0]
		password = line[1]
		first_name = line[2]
		last_name = line[3]
		address = line[4]
		email = line[5]
		phone_number = line[6]
		gender = line[7].rstrip('\n')
		if not Student.objects.filter(username=username).exists():
			stu_obj = Student(username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			stu_obj.save()
	f.close()
	print "Added Students Successfully"
	print ""


def insert_parents():
	print "Adding Parents..."

	f = open("dummy_db/parents.txt", "r+")
	
	for par in f.readlines():
		line = par.split('$')
		username = line[0]
		password = line[1]
		first_name = line[2]
		last_name = line[3]
		address = line[4]
		email = line[5]
		phone_number = line[6]
		gender = line[7].rstrip('\n')
		if not Parent.objects.filter(username=username).exists():
			par_obj = Parent(username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			par_obj.save()
	f.close()
	print "Added Parents Successfully"
	print ""


def assign_student_parent():

	print "Assigning Students to Parents"
	f = open("dummy_db/students.txt", "r+")
	stu_list = f.readlines()
	f.close()
	f = open("dummy_db/parents.txt", "r+")
	par_list = f.readlines()
	f.close()

	for i in xrange(min(len(stu_list), len(par_list))):
		line1 = stu_list[i].split('$')
		line2 = par_list[i].split('$')
		s_username = line1[0]
		s_password = line1[1]
		s_first_name = line1[2]
		s_last_name = line1[3]
		s_address = line1[4]
		s_email = line1[5]
		s_phone_number = line1[6]
		s_gender = line1[7].rstrip('\n')
		
		p_username = line2[0]
		p_password = line2[1]
		p_first_name = line2[2]
		p_last_name = line2[3]
		p_address = line2[4]
		p_email = line2[5]
		p_phone_number = line2[6]
		p_gender = line2[7].rstrip('\n')

		if not StudentParent.objects.filter(student=Student.objects.get(username=s_username), parent=Parent.objects.get(username=p_username)).exists():
			stu_par_obj = StudentParent(student=Student.objects.get(username=s_username), parent=Parent.objects.get(username=p_username))
			stu_par_obj.save()

	print "Assigned Students to Parents Successfully"




insert_academic_years()
insert_branches()
insert_roles()
insert_fee_types()
insert_standards()
insert_subjects()

insert_students()
insert_parents()
assign_student_parent()
# insert_staff()
