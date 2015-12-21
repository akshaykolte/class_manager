from portal.models import *
from portal.db_api.academic_year_db import get_current_academic_year
from itertools import combinations
from time import sleep
import sys, math, random, datetime
import string


def insert_parent():
	students = Student.objects.all()

	for student in students:
		first_name = student.first_name
		last_name = student.last_name+' Senior'
		phone_number = student.phone_number
		if not Parent.objects.filter(first_name = first_name, last_name = last_name, phone_number = phone_number).exists():

			parent_object = Parent(first_name = first_name, last_name = last_name, phone_number = phone_number)
			parent_object.save()


insert_parent()
