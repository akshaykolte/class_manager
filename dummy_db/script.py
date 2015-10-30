from portal.models import *
from portal.db_api.academic_year_db import get_current_academic_year
from itertools import combinations
from time import sleep
import sys, math, random, datetime


def add_progress(i,length):
	num = int(float((i+1)*100)/length)
	if(num > 100):
		num = 100
	sys.stdout.write('\r')
	sys.stdout.write("\t\t\t\t\t%d%%" % num)
	sys.stdout.flush()


def insert_academic_years():
	print "Adding Academic Years...",

	f = open("dummy_db/academic_years.txt", "r+")
	ay_list = f.readlines()
	length = len(ay_list)
	for i,ay in enumerate(ay_list):
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,length)
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
		add_progress(i,n)
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
	base_fee_object = FeeType.objects.get(name="base fee")
	for i,stud in enumerate(students):
		add_progress(i,stud_len)
		if counter >= it_len:
			batch_it+=1
			counter = 0

		if batch_it > batch_len:
			break

		if not StudentBatch.objects.filter(student=stud, batch=batches[batch_it]).exists():
			stud_bat_obj = StudentBatch(student=stud, batch=batches[batch_it])
			stud_bat_obj.save()
			subject_year_list = SubjectYear.objects.filter(subject=(Subject.objects.filter(standard=stud_bat_obj.batch.standard)), academic_year=cur_ay_obj)
			rn = random.randint(1, len(subject_year_list))
			# For 1 subject fee is 5000 for 2 it is 8000 and for 3 it is 12000 (Randomly considered, nothing specific)
			if rn == 1:
				amount = 5000
			elif rn == 2:
				amount = 8000
			elif rn == 3:
				amount = 12000
			if not FeeTransaction.objects.filter(student_batch = stud_bat_obj,amount = amount,fee_type = base_fee_object, date = datetime.datetime.now()).exists():
				transaction_object = FeeTransaction(student_batch = stud_bat_obj,amount = amount,fee_type = base_fee_object, date = datetime.datetime.now())
				transaction_object.save()
			for i in range(rn):
				stud_bat_obj.subject_years.add(subject_year_list[i].id)

		counter+=1

	print ""

def insert_staff(n=20):

	print "Adding Staff...",
	n += 1
	f = open("dummy_db/staffs.txt", "r+")
	staff_list = f.readlines()
	length = n-1

	for i,staff in enumerate(staff_list):
		add_progress(i,length)
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
	staff_obj = Staff.objects.all()
	role_obj = Role.objects.all()
	branch_obj = Branch.objects.all()

	bsize = len(branch_obj)
	rsize = len(role_obj)

	for i in xrange(len(staff_obj)):
		add_progress(i,len(staff_obj))
		branch = branch_obj[i%bsize]
		role = role_obj[i%rsize]
		staff = staff_obj[i]

		if role.name != 'teacher':
			if not StaffRole.objects.filter(staff=Staff.objects.get(id=staff.id), role=Role.objects.get(id=role.id), branch=Branch.objects.get(id=branch.id)).exists():

				staff_role_obj = StaffRole(staff=Staff.objects.get(id=staff.id), role=Role.objects.get(id=role.id), branch=Branch.objects.get(id=branch.id))

				staff_role_obj.save()

		else:
			for br in branch_obj:
				if not StaffRole.objects.filter(staff=staff, role=role, branch=br).exists():
					staff_role_obj = StaffRole(staff=staff, role=role, branch=br)
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
		add_progress(i,length)
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

def insert_lecture_batches():
	print "Adding Lecture Batches...",

	cur_ay = get_current_academic_year()['id']
	cur_ay_obj = AcademicYear.objects.get(id=cur_ay)
	standard_list = Standard.objects.all()
	lecture_list = Lecture.objects.all()
	batch_list = Batch.objects.all()
	staff_role_list = StaffRole.objects.filter(role__name='teacher')
	staff_it = 0
	staff_role_length = len(staff_role_list)
	j = 0
	total_iterations = len(standard_list)*len(lecture_list)*len(batch_list)
	for i,std in enumerate(standard_list):
		lecture_list = Lecture.objects.filter(subject_year__subject__standard__id=std.id)
		batch_list = Batch.objects.filter(standard__id=std.id)
		for batch in batch_list:
			for lecture in lecture_list:
				add_progress(j, total_iterations - lecture.count)
				j += lecture.count
				for i in xrange(lecture.count):
					while batch.branch != staff_role_list[staff_it%staff_role_length].branch:
						staff_it+=1
						staff_it%=staff_role_length

					if not LectureBatch.objects.filter(name=lecture.name+" "+str(i+1), lecture=lecture, batch=batch).exists():
						lecture_batch_obj = LectureBatch(name=lecture.name+" "+str(i+1), description="Temporary Description", date=datetime.datetime.strptime("2015-08-31", "%Y-%m-%d").date(), duration="2 Hours", lecture=lecture, staff_role=staff_role_list[staff_it%staff_role_length], batch=batch)
						lecture_batch_obj.save()
					staff_it+=1
					staff_it%=staff_role_length
	print ""

def insert_notices():
	print "Adding Notices...",


	staff_list = Staff.objects.all()
	staff_length = len(staff_list)
	f = open("dummy_db/notice.txt", "r+")
	notices = f.readlines()
	for i,n in enumerate(notices):
		add_progress(i,len(notices))
		line = n.split('$')
		title = line[0]
		description = line[1]
		staff_index = random.randint(0,staff_length-1)
		if not Notice.objects.filter(title=title,description=description).exists():
			notice_object = Notice(title = title,description = description,uploader = staff_list[staff_index])
			notice_object.save()
			for_students = random.randint(0,1)
			if for_students:
				if not NoticeViewer.objects.filter(notice=notice_object, for_students=True):
					notice_viewer_obj = NoticeViewer(notice=notice_object, for_students=True)
					notice_viewer_obj.save()
			else:
				if not NoticeViewer.objects.filter(notice=notice_object, for_staff=True):
					notice_viewer_obj = NoticeViewer(notice=notice_object, for_staff=True)
					notice_viewer_obj.save()
	print ""


def insert_base_fees():

	print "Adding Base Fees...",
	if BaseFee.objects.filter().exists():
		add_progress(99,100)
		print ""
		return
	ays = AcademicYear.objects.all()
	standards = Standard.objects.all()
	length = len(ays)

	for i,ay in enumerate(ays):
		add_progress(i,length)
		for std in standards:
			sub_years = SubjectYear.objects.filter(subject__standard__id=std.id, academic_year__id=ay.id)
			k=3
			for i in xrange(k,0,-1):
				for p in combinations(sub_years, i):
					if i == 1:
						amount = 5000
					elif i == 2:
						amount = 8000
					elif i == 3:
						amount = 12000
					base_fee_object = BaseFee(amount=amount)
					base_fee_object.save()
					for perm in p :
						base_fee_object.subject_years.add(perm)

	print ""


def insert_tests():
	print "Adding Tests...",
	subject_year_list = SubjectYear.objects.all()
	a ="unit_test"
	length = len(subject_year_list)
	for i,n in enumerate(subject_year_list):
		add_progress(i, length)
		x = a + str(i)
		if not Test.objects.filter(subject_year = n,name = x).exists():
			test_object = Test(subject_year = n,name = x,total_marks = 100)
			test_object.save()
	print ""


def insert_transactions():
	print"Adding Transactions...",
	student_batches = StudentBatch.objects.all()
	payment_type = FeeType.objects.get(name="payment")
	base_fee_type = FeeType.objects.get(name="base fee")
	length = len(student_batches)
	for i,n in enumerate(student_batches):
		add_progress(i,length)
		amount = random.randint(1,10)
		amount *= 1000
		present_payment_done = 0
		fee_objects = FeeTransaction.objects.filter(student_batch=n, fee_type=payment_type)
		for fee_obj in fee_objects:
			present_payment_done += fee_obj.amount
		base_fee_obj = FeeTransaction.objects.get(student_batch=n, fee_type=base_fee_type)
		if present_payment_done + amount > base_fee_obj.amount:
			amount = base_fee_obj.amount - present_payment_done
		if amount != 0:
			transaction_object = FeeTransaction(student_batch = n,amount = amount,fee_type = payment_type, date = datetime.datetime.now())
			transaction_object.save()

	print ""

def insert_attendance():
	pass


starttime = datetime.datetime.now()
insert_academic_years()
insert_branches()
insert_roles()
insert_fee_types()
insert_standards()
insert_batches()
insert_subjects()
insert_subject_years()

insert_students()
insert_parents()
assign_student_parent()
insert_student_batches()

insert_staff()
insert_staff_role()
insert_lectures()
insert_lecture_batches()
insert_notices()
insert_attendance()
insert_tests()
insert_base_fees()
insert_transactions()

endtime = datetime.datetime.now()
print "Time taken: ",str((endtime-starttime).seconds)+"."+str((endtime-starttime).microseconds)[0:3],"seconds\n"
