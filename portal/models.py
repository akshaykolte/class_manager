from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from datetime import datetime, timedelta

class AcademicYear(models.Model):
	year_start = models.IntegerField()
	year_end = models.IntegerField()
	is_current = models.BooleanField()

	def __str__(self):
		return str(self.year_start) + '-' + str(self.year_end) + ':' + str(self.is_current)

	class Meta:
		unique_together = (('year_start', 'year_end',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_academic_year
		if validate:
			if not validate_academic_year(self):
				raise Exception('Validation Failed')

		super(AcademicYear, self).save()


class Branch(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_branch
		if validate:
			if not validate_branch(self):
				raise Exception('Validation Failed')

		super(Branch, self).save()

class Standard(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_standard
		if validate:
			if not validate_standard(self):
				raise Exception('Validation Failed')

		super(Standard, self).save()

class Batch(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	academic_year = models.ForeignKey(AcademicYear)
	branch = models.ForeignKey(Branch)
	standard = models.ForeignKey(Standard)

	def __str__(self):
		return self.name + ' - ' + str(self.standard) + ' ' + str(self.branch)
	
	class Meta:
		unique_together = (('name', 'academic_year', 'branch', 'standard',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_batch
		if validate:
			if not validate_batch(self):
				raise Exception('Validation Failed')

		super(Batch, self).save()

class Student(models.Model):

	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		unique_together = (('username',), ('email',), ('phone_number',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_student
		if validate:
			if not validate_student(self):
				raise Exception('Validation Failed')

		super(Student, self).save()

class Parent(models.Model):

	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		unique_together = (('username',), ('email',), ('phone_number',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_parent
		if validate:
			if not validate_parent(self):
				raise Exception('Validation Failed')

		super(Parent, self).save()

class StudentParent(models.Model):
	student = models.ForeignKey(Student)
	parent = models.ForeignKey(Parent)

	def __str__(self):
		return str(self.student) + ' : ' + str(self.parent)

	class Meta:
		unique_together = (('student', 'parent',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_student_parent
		if validate:
			if not validate_student_parent(self):
				raise Exception('Validation Failed')

		super(StudentParent, self).save()

class Staff(models.Model):

	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	address = models.CharField(max_length=200)
	email = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=13)
	gender = models.CharField(max_length=1)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		unique_together = (('username',), ('email',), ('phone_number',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_staff
		if validate:
			if not validate_staff(self):
				raise Exception('Validation Failed')

		super(Staff, self).save()

class Role(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_role
		if validate:
			if not validate_role(self):
				raise Exception('Validation Failed')

		super(Role, self).save()

class StaffRole(models.Model):
	role = models.ForeignKey(Role)
	staff = models.ForeignKey(Staff)
	branch = models.ForeignKey(Branch)

	def __str__(self):
		return str(self.role) + ' ' + str(self.staff)

	class Meta:
		unique_together = (('role', 'staff', 'branch',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_staff_role
		if validate:
			if not validate_staff_role(self):
				raise Exception('Validation Failed')

		super(StaffRole, self).save()

class Subject(models.Model):
	name = models.CharField(max_length=50)
	standard = models.ForeignKey(Standard)

	def __str__(self):
		return self.name + '-' + str(self.standard)

	class Meta:
		unique_together = (('name', 'standard',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_subject
		if validate:
			if not validate_subject(self):
				raise Exception('Validation Failed')

		super(Subject, self).save()

class SubjectYear(models.Model):
	subject = models.ForeignKey(Subject)
	academic_year = models.ForeignKey(AcademicYear)

	def __str__(self):
		return str(self.subject) + ' ' + str(self.academic_year)

	class Meta:
		unique_together = (('subject', 'academic_year',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_subject_year
		if validate:
			if not validate_subject_year(self):
				raise Exception('Validation Failed')

		super(SubjectYear, self).save()

class StudentBatch(models.Model):
	student = models.ForeignKey(Student)
	batch = models.ForeignKey(Batch, blank=True, null=True)
	subject_years = models.ManyToManyField(SubjectYear)
	academic_year = models.ForeignKey(AcademicYear, blank=True, null=True)
	standard = models.ForeignKey(Standard, blank=True, null=True)

	def __str__(self):
		return str(self.student) + ' ' + str(self.batch)

	class Meta:
		unique_together = (('student', 'batch',),)

	# Receiver is defined below this function
	# While adding through admin panel, default validation will be done using the pre_add receiver
	# While adding through python, validation should be done through save(validate=True, subject_year_id_list=list) first, so that no error is encountered while doing .add(subject_year_object)
	def save(self, validate=False, subject_year_id_list = [] ):
		from portal.validator.validator import validate_student_batch
		# print SubjectYear.objects.filter()
		if validate:
			if not validate_student_batch(self, subject_year_id_list):
				raise Exception('Validation Failed')
		super(StudentBatch, self).save()

@receiver(m2m_changed, sender = StudentBatch.subject_years.through)
def student_batch_subject_years_pre_add(sender, instance, action, reverse, model, pk_set, **kwargs):
	from portal.validator.validator import validate_student_batch
	if action == 'pre_add':
		if not validate_student_batch(instance, list(pk_set)):
			raise Exception('Validation Failed')

class Lecture(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	count = models.IntegerField()
	subject_year = models.ForeignKey(SubjectYear)

	def __str__(self):
		return self.name + '-' + str(self.count) + ' lectures'

	class Meta:
		unique_together = (('name', 'subject_year',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_lecture
		if validate:
			if not validate_lecture(self):
				raise Exception('Validation Failed')

		super(Lecture, self).save()

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

	class Meta:
		unique_together = (('lecture', 'batch', 'name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_lecture_batch
		if validate:
			if not validate_lecture_batch(self):
				raise Exception('Validation Failed')

		super(LectureBatch, self).save()

class Attendance(models.Model):
	count = models.IntegerField()
	lecture_batch = models.ForeignKey(LectureBatch)
	student_batch = models.ForeignKey(StudentBatch)

	def __str__(self):
		return str(self.student_batch) + ' ' + str(self.lecture_batch)

	class Meta:
		unique_together = (('lecture_batch', 'student_batch',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_attendance
		if validate:
			if not validate_attendance(self):
				raise Exception('Validation Failed')

		super(Attendance, self).save()

class BaseFee(models.Model):
	amount = models.IntegerField()
	subject_years = models.ManyToManyField(SubjectYear)
	
	def __str__(self):
		return str(self.subject_years.all()) + '- Rs. ' + str(self.amount)

	def save(self, validate=False, subject_year_id_list = [] ):
		from portal.validator.validator import validate_base_fee
		if validate:
			for i in subject_years.all():
				subject_year_id_list.append(i.id)
			if not validate_base_fee(self, subject_year_id_list):
				raise Exception('Validation Failed')

		super(BaseFee, self).save()

@receiver(m2m_changed, sender = BaseFee.subject_years.through)
def base_fee_subject_years_pre_add(sender, instance, action, reverse, model, pk_set, **kwargs):
	from portal.validator.validator import validate_base_fee
	if action == 'pre_add':
		subject_year_id_list = list(pk_set)
		for i in instance.subject_years.all():
			subject_year_id_list.append(i.id)
		if not validate_base_fee(instance, subject_year_id_list):
			raise Exception('Validation Failed')

class FeeType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_fee_type
		if validate:
			if not validate_fee_type(self):
				raise Exception('Validation Failed')

		super(FeeType, self).save()

class FeeTransaction(models.Model):
	amount = models.IntegerField()
	date = models.DateField()
	time = models.TimeField()
	timestamp = models.DateTimeField(auto_now_add=True)
	receipt_number = models.CharField(max_length=50)
	student_batch = models.ForeignKey(StudentBatch)
	fee_type = models.ForeignKey(FeeType)

	def __str__(self):
		return str(self.student_batch) + ':' + str(self.fee_type) + '- Rs. ' + str(self.amount)

	class Meta:
		unique_together = (('receipt_number',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_fee_transaction
		if validate:
			if not validate_fee_transaction(self):
				raise Exception('Validation Failed')

		super(FeeTransaction, self).save()

class Test(models.Model):
	subject_year = models.ForeignKey(SubjectYear)
	name = models.CharField(max_length=50)
	
	class Meta:
		unique_together = (('name','subject_year',),)

	def __str__(self):
		return str(self.name)+' - '+str(self.subject_year)

	# save() overriding not required

class TestBatch(models.Model):
	test = models.ForeignKey(Test)
	batch = models.ForeignKey(Batch)

	class Meta:
		unique_together = (('test','batch',),)
	
	def __str__(self):
		return str(self.test)+' - '+str(self.batch)

	# save() overriding not required

class TestStaffRole(models.Model):
	test = models.ForeignKey(Test)
	staff_role = models.ForeignKey(StaffRole)

	class Meta:
		unique_together = (('test','staff_role'),)

	def __str__(self):
		return str(self.test)+' - '+str(self.staff_role)

	# save() overriding not required

class Notice(models.Model):
	title = models.CharField(max_length=200, null=False)
	description = models.CharField(max_length=1000, blank=True, null=False)
	uploader = models.ForeignKey(Staff, null=False)
	expiry_date = models.DateField(blank=True, default=datetime.now()+timedelta(days=30)) # TODO: timedelta
	important = models.BooleanField(blank=True, default=False)

	def __str__(self):
		return str(self.title) + ' - ' + str(self.uploader)

class NoticeViewer(models.Model):
	notice = models.ForeignKey(Notice, null=False)
	for_students = models.BooleanField(default=False)
	for_staff = models.BooleanField(default=False)
	branch = models.ForeignKey(Branch, blank=True, null=True)
	batch = models.ForeignKey(Batch, blank=True, null=True)
	student = models.ForeignKey(Student, blank=True, null=True)
	staff = models.ForeignKey(Staff, blank=True, null=True)

	def __str__(self):
		return str(self.notice)