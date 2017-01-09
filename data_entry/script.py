
from portal.models import *
from portal.db_api.student_db import *
from portal.db_api.academic_year_db import get_current_academic_year
from itertools import combinations
from time import sleep
import sys, math, random, datetime
import string


def insert_studentparent():
	students = Student.objects.all()
	parents = Parent.objects.all()
	for i in range(318, 357):
		studparent_obj = StudentParent(student = Student.objects.get(id = i), parent = Parent.objects.get(id = i-1))
		studparent_obj.save()

def backup():
	students = Student.objects.all()
	f = open('backup','w')

	for student in students:
		first_name = student.first_name
		f.write(first_name+'\n')
		last_name = student.last_name
		f.write(last_name+'\n')
		phone_number = student.phone_number
		f.write(phone_number+'\n')
	f.close()


def writebackup():
	cnt = 0
	with open("backup", "r") as ins:
	    for line in ins:

	    	if cnt == 0:
	        	first_name = line
	        	cnt = cnt+1
	        	#print "dsfdsf"
	        elif cnt == 1:
	        	last_name = line+' Senior'
	        	student_last_name = line
	        	cnt=cnt+1
	        else:	
				phone_number = line
				cnt = 0
				stud_object = Student.objects.get(first_name = first_name, phone_number = phone_number)
				stud_object.last_name = student_last_name
				stud_object.save()
						



def edit_student():
	students = Student.objects.all()
	for student in students:
		last_name = student.last_name
		for letter in last_name:
			student.last_name = letter
			student.save()
			break

def add_student_batch():
	for i in range(318, 357):
		student = Student.objects.get(id = i)
		batch = Batch.objects.get(id = 14)
		subject_years = SubjectYear.objects.filter(subject__standard__id = 1 )
	        print subject_years
		subject_year_list = []
		for subject_year in subject_years:
			subject_year_list.append(subject_year.id)
		student_batch_id = set_student_batch(id=None,student_id = student.id, batch_id = batch.id, subject_year_id_list= subject_year_list, academic_year_id = None, standard_id = None)
		


def writebackup1():
    cnt = 0
    with open("data_entry/data.txt", "r") as ins:
        i = 210
	for line in ins:
            #print line	
	    #line = line.split()
            print line
	    #print line[1]
	    stud =Parent.objects.get(id = i)
	    i = i + 1
	    stud.phone_number = line
	    stud.save()


def insertstudent():
        cnt = 0
        with open("data_entry/data.txt", "r") as ins:
        	with open("data_entry/data2.txt", "r") as ins2:

	    		for line,line1 in zip(ins,ins2):
				name = line.split()
				s = Student(first_name = name[0], last_name = name[1])
				s.save()
				p = Parent(first_name = name[0], last_name = name[1]+" Senior", phone_number = line1 )
				p.save()
				print name[0] + "---- " + name[1]+"----" + line1
		


#insertstudent()
#insert_parent()
#writebackup1()
insert_studentparent()
#edit_student()
add_student_batch()
