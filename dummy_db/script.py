from portal.models import *
from portal.db_api.academic_year_db import get_current_academic_year
from itertools import combinations
from time import sleep
import sys, math
	
def insert_academic_years():
	print "Adding Academic Years...",
	
	f = open("dummy_db/academic_years.txt", "r+")
	ay_list = f.readlines()
	length = len(ay_list)
	for i,ay in enumerate(ay_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
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
	print ""


def insert_branches():

	print "Adding Branches...",
	
	f = open("dummy_db/branches.txt", "r+")
	br_list = f.readlines()
	length = len(br_list)
	
	for i,branch in enumerate(br_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		line = branch.split('$')
		name = line[0]
		address = line[1]
		address = address.rstrip('\n')
		if not Branch.objects.filter(name=name, address=address).exists():
			br_obj = Branch(name=name, address=address);
			br_obj.save()
	f.close()
	print ""
	


def insert_roles():

	print "Adding Roles...",
	
	f = open("dummy_db/roles.txt", "r+")
	rl_list = f.readlines()
	length = len(rl_list)
	
	for i,role in enumerate(rl_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		role = role.rstrip('\n')
		if not Role.objects.filter(name=role).exists():
			role_obj = Role(name=role);
			role_obj.save()
	f.close()
	print ""
	

def insert_fee_types():
	print "Adding Fee Types...",
	
	f = open("dummy_db/fee_types.txt", "r+")
	fee_list = f.readlines()
	length = len(fee_list)
	
	for i,fee in enumerate(fee_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		fee = fee.rstrip('\n')
		if not FeeType.objects.filter(name=fee).exists():
			fee_obj = FeeType(name=fee)
			fee_obj.save()
	f.close()
	print ""
	

def insert_standards():
	print "Adding Standards...",
	
	f = open("dummy_db/standards.txt", "r+")
	st_list = f.readlines()
	length = len(st_list)
	
	for i,st in enumerate(st_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		st = st.rstrip('\n')
		if not Standard.objects.filter(name=st).exists():
			st_obj = Standard(name=st)
			st_obj.save()
	f.close()
	print ""
	
def insert_batches():
	print "Adding Batches...",
	cur_ay = get_current_academic_year()['id']
	cur_ay_obj = AcademicYear.objects.get(id=cur_ay)
	branches = Branch.objects.all()
	standards = Standard.objects.all()
	batches = ['Morning Batch', 'Evening Batch']
	length = len(standards)
	for i,std in enumerate(standards):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		for br in branches:
			for bat in batches:
				if not Batch.objects.filter(name=bat, academic_year=cur_ay_obj, branch=br, standard=std).exists():
					bat_obj = Batch(name=bat, description="Temporary Description", academic_year=cur_ay_obj, branch=br, standard=std)
					bat_obj.save()
	
	print ""
	

def insert_subjects():
	print "Adding Subjects...",

	f = open("dummy_db/subjects.txt", "r+")
	sub_list = f.readlines()
	length = len(sub_list)
	for i,subs in enumerate(sub_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		line = subs.split()
		name = line[0]
		standard = line[1]
		standard = standard.rstrip('\n')
		if not Subject.objects.filter(name=name, standard=Standard.objects.get(name=standard)).exists():
			sub_obj = Subject(name=name, standard=Standard.objects.get(name=standard))
			sub_obj.save()
	f.close()
	print ""
	

def insert_subject_years():
	print "Adding Subject Years...",

	subjects = Subject.objects.all()
	years = AcademicYear.objects.all()
	length = len(years)
	
	for i,year in enumerate(years):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		for sub in subjects:

			if not SubjectYear.objects.filter(subject=Subject.objects.get(id=sub.id), academic_year=AcademicYear.objects.get(id=year.id)).exists():
				sub_year_obj = SubjectYear(subject=Subject.objects.get(id=sub.id), academic_year=AcademicYear.objects.get(id=year.id))
				sub_year_obj.save()

	print ""
	

def insert_students(n=105):
	print "Adding Students...",
	n+=1
	f = open("dummy_db/students.txt", "r+")
	stu_list = f.readlines()
	length = n-1
	for i,stu in enumerate(stu_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		n-=1;
		if n <= 0:
			break
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
	print ""
	

def insert_parents(n=105):
	print "Adding Parents...",
	n+=1
	f = open("dummy_db/parents.txt", "r+")
	par_list = f.readlines()
	length = n-1
	
	for i,par in enumerate(par_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		n-=1;
		if n <= 0:
			break
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
	print ""
	

def assign_student_parent(n=105):

	print "Assigning Students to Parents",
	# n+=1
	f = open("dummy_db/students.txt", "r+")
	stu_list = f.readlines()
	f.close()
	f = open("dummy_db/parents.txt", "r+")
	par_list = f.readlines()
	f.close()

	for i in xrange(n):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/n))
		sys.stdout.flush()
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

	print ""
	
def insert_student_batches():
	print "Adding Student Batches...",
	
	batches = Batch.objects.all()
	batch_len = len(batches)
	students = Student.objects.all()
	stud_len = len(students)
	it_len = stud_len/batch_len
	it_len += 1
	cur_ay_obj = AcademicYear.objects.get(id=get_current_academic_year()['id'])
	batch_it = 0
	counter = 0

	for i,stud in enumerate(students):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/stud_len))
		sys.stdout.flush()
		if counter >= it_len:
			batch_it+=1
			counter = 0

		if batch_it > batch_len:
			break

		if not StudentBatch.objects.filter(student=stud, batch=batches[batch_it], academic_year=cur_ay_obj).exists():
			stud_bat_obj = StudentBatch(student=stud, batch=batches[batch_it], academic_year=cur_ay_obj, standard=batches[batch_it].standard)
			stud_bat_obj.save()
		
		counter+=1
		    
	print ""
	
def insert_staff(n=100):

	print "Adding Staff...",
	n+=1
	f = open("dummy_db/staffs.txt", "r+")
	staff_list = f.readlines()
	length = n-1
	
	for i,staff in enumerate(staff_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		
		n-=1;
		if n <= 0:
			break

		line = staff.split('$')
		username = line[0]
		password = line[1]
		first_name = line[2]
		last_name = line[3]
		address = line[4]
		email = line[5]
		phone_number = line[6]
		gender = line[7].rstrip('\n')
		if not Staff.objects.filter(username=username).exists():
			staff_obj = Staff(username=username, password=password, first_name=first_name, last_name=last_name, address=address, email=email, phone_number=phone_number, gender=gender)
			staff_obj.save()
	f.close()
	print ""
	
def insert_staff_role():

	print "Assigning Roles to each Staff...",
	staff_obj = Staff.objects.all();
	role_obj = Role.objects.all();
	branch_obj = Branch.objects.all();
	
	bsize = len(branch_obj)
	rsize = len(role_obj)
	
	for i in xrange(len(staff_obj)):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/len(staff_obj)))
		sys.stdout.flush()
		branch = branch_obj[i%bsize]
		role = role_obj[i%rsize]
		staff = staff_obj[i]

		if not StaffRole.objects.filter(staff=Staff.objects.get(id=staff.id), role=Role.objects.get(id=role.id), branch=Branch.objects.get(id=branch.id)).exists():

			staff_role_obj = StaffRole(staff=Staff.objects.get(id=staff.id), role=Role.objects.get(id=role.id), branch=Branch.objects.get(id=branch.id))

			staff_role_obj.save()

	print ""
	

def insert_lectures():
	print "Adding Lectures...",
	
	f = open("dummy_db/lectures.txt", "r+")
	cur_ay = get_current_academic_year()['id']
	cur_ay_obj = AcademicYear.objects.get(id=cur_ay)
	lec_list = f.readlines()
	length = len(lec_list)
	
	for i,lec in enumerate(lec_list):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		line = lec.split('$')
		name = line[0]
		subject = line[1]
		standard = line[2]
		count = line[3].rstrip('\n')
		
		if not Lecture.objects.filter(name=name, subject_year=SubjectYear.objects.get(subject=Subject.objects.get(name=subject, standard=Standard.objects.get(name=standard)), academic_year=cur_ay_obj)).exists():
			
			lec_obj = Lecture(name=name, description="Temporary description", count=count, subject_year=SubjectYear.objects.get(subject=Subject.objects.get(name=subject, standard=Standard.objects.get(name=standard)), academic_year=cur_ay_obj))
			lec_obj.save()
	f.close()
	print ""
	
def insert_base_fees():

	print "Adding Base Fees...",

	ays = AcademicYear.objects.all()
	standards = Standard.objects.all()
	length = len(ays)

	for i,ay in enumerate(ays):
		sys.stdout.write('\r')
		sys.stdout.write("\t\t\t\t\t%d%%" % int(float((i+1)*100)/length))
		sys.stdout.flush()
		for std in standards:
			sub_years = SubjectYear.objects.filter(subject__standard__id=std.id, academic_year__id=ay.id)
			k=2
			for i in xrange(1,k+1):
				for p in combinations(sub_years, i):
					if i == 1:
						amount = 5000
					elif i == 2:
						amount = 8000
					base_fee_object = BaseFee(amount=amount)
					base_fee_object.save()
					for perm in p :
						base_fee_object.subject_years.add(perm)

	print ""
	

insert_academic_years()
insert_branches()
insert_roles()
insert_fee_types()
insert_standards()
insert_batches()
insert_subjects()
insert_subject_years()

# print "How many Students and Parents you want to enter do you want to enter?(MAX = 105)"
# n = int(raw_input())

# while n > 105 and n < 0:
# 	print "Maximum exceeded, enter again."
# 	print "How many Students and Parents you want to enter do you want to enter?(MAX = 105)"
# 	n = int(raw_input())

insert_students()
insert_parents()
assign_student_parent()
insert_student_batches()

# print "How many staffs do you want to enter?(MAX = 100)"
# n = int(raw_input())

# while n > 100 and n < 0:
# 	print "Maximum exceeded, enter again."
# 	print "How many Students and Parents you want to enter do you want to enter?(MAX = 105)"
# 	n = int(raw_input())

insert_staff()
insert_staff_role()
insert_lectures()

insert_base_fees()

