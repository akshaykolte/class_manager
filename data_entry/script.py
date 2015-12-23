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
	for i in range(1, 96):
		studparent_obj = StudentParent(student = Student.objects.get(id = i), parent = Parent.objects.get(id = i))
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
	for i in range(64, 96):
		student = Student.objects.get(id = i)
		batch = Batch.objects.get(id = 3)
		subject_years = SubjectYear.objects.all()
		subject_year_list = []
		for subject_year in subject_years:
			subject_year_list.append(subject_year.id)
		student_batch_id = set_student_batch(id=None,student_id = student.id, batch_id = batch.id, subject_year_id_list= subject_year_list, academic_year_id = None, standard_id = None)
		


#insert_parent()
#writebackup()
#insert_studentparent()
#edit_student()
#add_student_batch()