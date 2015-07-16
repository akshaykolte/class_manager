from django.db import models

class AcademicYear(models.Model):
	year_start = models.IntegerField()
	year_end = models.IntegerField()
	is_current = models.BooleanField()

	def __str__(self):
		return str(self.year_start) + '-' + str(self.year_end) + ':' + str(self.is_current)

class Branch(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Standard(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Batch(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	academic_year = models.ForeignKey(AcademicYear)
	branch = models.ForeignKey(Branch)
	standard = models.ForeignKey(Standard)

	def __str__(self):
		return self.name

class Student(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Parent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class StudentParent(models.Model):
	student = models.ForeignKey(Student)
	parent = models.ForeignKey(Parent)

	def __str__(self):
		return str(student) + ' ' + str(parent) 

class Staff(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class Role(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class StaffRole(models.Model):
	role = models.ForeignKey(Role)
	staff = models.ForeignKey(Staff)
	branch = models.ForeignKey(Branch)

	def __str__(self):
		return str(self.role) + ' ' + str(self.staff)



class Subject(models.Model):
	name = models.CharField(max_length=50)
	standard = models.ForeignKey(Standard)

	def __str__(self):
		return self.name + '-' + str(self.standard)

class SubjectYear(models.Model):
	subject = models.ForeignKey(Subject)
	academic_year = models.ForeignKey(AcademicYear)

	def __str__(self):
		return str(self.subject) + ' ' + str(self.academic_year)

class StudentBatch(models.Model):
	student = models.ForeignKey(Student)
	batch = models.ForeignKey(Batch)
	subject_years = models.ManyToManyField(SubjectYear)

	def __str__(self):
		return str(self.student) + ' ' + str(self.batch)

class Lecture(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	count = models.IntegerField()
	subject_year = models.ForeignKey(SubjectYear)

	def __str__(self):
		return self.name + '-' + str(self.count) + ' lectures'

class LectureBatch(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	date = models.DateField()
	duration = models.CharField(max_length=50)
	lecture = models.ForeignKey(Lecture)
	staff_role = models.ForeignKey(StaffRole)
	batch = models.ForeignKey(Batch)

	def __str__(self):
		return self.name + ' ' + str(self.date)

class Attendance(models.Model):
	count = models.IntegerField()
	lecture_batch = models.ForeignKey(LectureBatch)
	student_batch = models.ForeignKey(StudentBatch)

	def __str__(self):
		return str(student_batch) + ' ' + str(lecture_batch)

class BaseFee(models.Model):
	amount = models.IntegerField()
	subject_years = models.ManyToManyField(SubjectYear)
	
	def __str__(self):
		return str(self.subject_years.all()) + '- Rs. ' + str(self.amount)

class FeeType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class FeeTransaction(models.Model):
	amount = models.IntegerField()
	date = models.DateField()
	time = models.TimeField()
	timestamp = models.DateTimeField(auto_now_add=True)
	receipt_number = models.CharField(max_length=50)
	student_batch = models.ForeignKey(StudentBatch)
	fee_type = models.ForeignKey(FeeType)

	def __str__(self):
		return str(student_batch) + ':' + str(fee_type) + '- Rs. ' + str(amount)







