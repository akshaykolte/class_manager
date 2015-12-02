from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.db import IntegrityError
from portal.validator.validator import PentaError, validate_phone_number

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
			validation = validate_academic_year(self)
			if not validation:
				validation.raise_error()
		try:
			super(AcademicYear, self).save()
		except IntegrityError, e:
			PentaError(1017).raise_error()

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
			if self.name == '' or self.address == '':
				PentaError(997).raise_error()
			validation = validate_branch(self)
			if not validation:
				validation.raise_error()
		try:
			super(Branch, self).save()
		except IntegrityError, e:
			PentaError(1018).raise_error()

class Standard(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_standard
		if validate:
			if self.name == '':
				PentaError(997).raise_error()
			validation = validate_standard(self)
			if not validation:
				validation.raise_error()
		try:
			super(Standard, self).save()
		except IntegrityError, e:
			PentaError(1019).raise_error()

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
			if self.name == '' or self.description == '':
				PentaError(997).raise_error()
			validation = validate_batch(self)
			if not validation:
				validation.raise_error()
		try:
			super(Batch, self).save()
		except IntegrityError, e:
			PentaError(1020).raise_error()

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
			if self.username == '' or self.password == '' or self.first_name == '' or self.last_name == '' or self.address == '' or self.email == '' or self.gender == '':
				PentaError(997).raise_error()
			if self.gender != 'M' and self.gender != 'F':
				PentaError(995).raise_error()
			if not validate_phone_number(self.phone_number):
				PentaError(996).raise_error()
			validation = validate_student(self)
			if not validation:
				validation.raise_error()

		try:
			super(Student, self).save()
		except IntegrityError, e:
			PentaError(1021).raise_error()

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
			if self.username == '' or self.password == '' or self.first_name == '' or self.last_name == '' or self.address == '' or self.email == '' or self.gender == '':
				print 'username', self.username
				print 'password', self.password
				print 'first name', self.first_name
				print 'last name', self.last_name
				print 'address', self.address
				print 'email', self.email
				print 'gender', self.gender
				PentaError(997).raise_error()
			if self.gender != 'M' and self.gender != 'F':
				PentaError(995).raise_error()
			if not validate_phone_number(self.phone_number):
				PentaError(996).raise_error()
			validation = validate_parent(self)
			if not validation:
				validation.raise_error()
		try:
			super(Parent, self).save()
		except IntegrityError, e:
			PentaError(1022).raise_error()

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
			validation = validate_student_parent(self)
			if not validation:
				validation.raise_error()
		try:
			super(StudentParent, self).save()
		except IntegrityError, e:
			PentaError(1023).raise_error()

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
			if self.username == '' or self.password == '' or self.first_name == '' or self.last_name == '' or self.address == '' or self.email == '' or self.gender == '':
				PentaError(997).raise_error()
			if self.gender != 'M' and self.gender != 'F':
				PentaError(995).raise_error()
			if not validate_phone_number(self.phone_number):
				PentaError(996).raise_error()
			validation = validate_staff(self)
			if not validation:
				validation.raise_error()
		try:
			super(Staff, self).save()
		except IntegrityError,e:
			PentaError(1024).raise_error()

class Role(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_role
		if validate:
			if self.name == '':
				PentaError(997).raise_error()
			validation = validate_role(self)
			if not validation:
				validation.raise_error()
		try:
			super(Role, self).save()
		except IntegrityError, e:
			PentaError(1025).raise_error()

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
			validation = validate_staff_role(self)
			if not validation:
				validation.raise_error()
		try:
			super(StaffRole, self).save()
		except IntegrityError, e:
			PentaError(1026).raise_error()

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
			validation = validate_subject(self)
			if not validation:
				validation.raise_error()
		try:
			super(Subject, self).save()
		except IntegrityError, e:
			PentaError(1027).raise_error()

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
			validation = validate_subject_year(self)
			if not validation:
				validation.raise_error()
		try:
			super(SubjectYear, self).save()
		except IntegrityError, e:
			PentaError(1028).raise_error()

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
			validation = validate_student_batch(self, subject_year_id_list)
			if not validation:
				validation.raise_error()
		try:
			super(StudentBatch, self).save()
		except IntegrityError, e:
			PentaError(1029).raise_error()

@receiver(m2m_changed, sender = StudentBatch.subject_years.through)
def student_batch_subject_years_pre_add(sender, instance, action, reverse, model, pk_set, **kwargs):
	from portal.validator.validator import validate_student_batch
	if action == 'pre_add':
		validation = validate_student_batch(instance, list(pk_set))
		if not validation:
			validation.raise_error()

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
			if self.name == '' or self.description == '':
				PentaError(997).raise_error()
			validation = validate_lecture(self)
			if not validation:
				validation.raise_error()
		try:
			super(Lecture, self).save()
		except IntegrityError, e:
			PentaError(1030).raise_error()

class LectureBatch(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	date = models.DateField()
	duration = models.CharField(max_length=50)
	lecture = models.ForeignKey(Lecture)
	staff_role = models.ForeignKey(StaffRole)
	batch = models.ForeignKey(Batch)
	is_done = models.BooleanField(default=False)

	def __str__(self):
		return self.name + ' ' + str(self.date)

	class Meta:
		unique_together = (('lecture', 'batch', 'name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_lecture_batch
		if validate:
			if self.name == '' or self.description == '' or self.duration == '':
				PentaError(997).raise_error()
			validation = validate_lecture_batch(self)
			if not validation:
				validation.raise_error()
		try:
			super(LectureBatch, self).save()
		except IntegrityError, e:
			PentaError(1031).raise_error()

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
			validation = validate_attendance(self)
			if not validation:
				validation.raise_error()
		try:
			super(Attendance, self).save()
		except IntegrityError, e:
			PentaError(1032).raise_error()

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

			validation = validate_base_fee(self, subject_year_id_list)
			if not validation:
				validation.raise_error()
		try:
			super(BaseFee, self).save()
		except IntegrityError, e:
			PentaError(1033).raise_error()

@receiver(m2m_changed, sender = BaseFee.subject_years.through)
def base_fee_subject_years_pre_add(sender, instance, action, reverse, model, pk_set, **kwargs):
	from portal.validator.validator import validate_base_fee
	if action == 'pre_add':
		subject_year_id_list = list(pk_set)
		for i in instance.subject_years.all():
			subject_year_id_list.append(i.id)

		validation = validate_base_fee(instance, subject_year_id_list)
		if not validation:
			validation.raise_error()

class FeeType(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

	class Meta:
		unique_together = (('name',),)

	def save(self, validate=True):
		from portal.validator.validator import validate_fee_type
		if validate:
			if self.name == '':
				PentaError(997).raise_error()
			validation = validate_fee_type(self)
			if not validation:
				validation.raise_error()
		try:
			super(FeeType, self).save()
		except IntegrityError, e:
			PentaError(1034).raise_error()

class FeeTransaction(models.Model):
	amount = models.IntegerField()
	date = models.DateField()
	timestamp = models.DateTimeField(auto_now_add=True)
	student_batch = models.ForeignKey(StudentBatch)
	fee_type = models.ForeignKey(FeeType)
	# TODO: uncomment the following line after finalising the Cheque model
	# cheque = models.ForeignKey(Cheque, blank=True, null=True)

	def __str__(self):
		return str(self.student_batch) + ':' + str(self.fee_type) + '- Rs. ' + str(self.amount)

	pass
	class Meta:
		unique_together = ()

	def save(self, validate=True):
		from portal.validator.validator import validate_fee_transaction
		if validate:
			validation = validate_fee_transaction(self)
			if not validation:
				validation.raise_error()
		try:
			super(FeeTransaction, self).save()
		except IntegrityError, e:
			PentaError(1035).raise_error()

class Test(models.Model):
	subject_year = models.ForeignKey(SubjectYear)
	name = models.CharField(max_length=50)
	total_marks = models.IntegerField()

	class Meta:
		unique_together = (('name','subject_year',),)

	def __str__(self):
		return str(self.name)+' - '+str(self.subject_year)


	def save(self, validate=True):
		if validate:
			if self.name == '':
				PentaError(997).raise_error()
		try:
			super(Test, self).save()
		except IntegrityError, e:
			PentaError(1041).raise_error()

class TestBatch(models.Model):
	test = models.ForeignKey(Test)
	batch = models.ForeignKey(Batch)
	test_date = models.DateField(default=datetime.now())

	class Meta:
		unique_together = (('test','batch',),)

	def __str__(self):
		return str(self.test)+' - '+str(self.batch)

	def save(self, validate=True):
		from portal.validator.validator import validate_test_batch
		if validate:
			validation = validate_test_batch(self)
			if not validation:
				validation.raise_error()
		try:
			super(TestBatch, self).save()
		except IntegrityError, e:
			PentaError(1042).raise_error()

class TestStaffRole(models.Model):
	test = models.ForeignKey(Test)
	staff_role = models.ForeignKey(StaffRole)

	class Meta:
		unique_together = (('test','staff_role'),)

	def __str__(self):
		return str(self.test)+' - '+str(self.staff_role)

	def save(self, validate=True):
		try:
			super(TestStaffRole, self).save()
		except IntegrityError, e:
			PentaError(1043).raise_error()

class TestStudentBatch(models.Model):
	test = models.ForeignKey(Test)
	student_batch = models.ForeignKey(StudentBatch)
	obtained_marks = models.IntegerField()

	class Meta:
		unique_together = (('test', 'student_batch',),)

	def __str__(self):
		return str(self.test) + ' - ' + str(self.student_batch)

	def save(self, validate=True):
		from portal.validator.validator import validate_test_student_batch
		if validate:
			validation = validate_test_student_batch(self)
			if not validation:
				validation.raise_error()

		try:
			super(TestStudentBatch, self).save()
		except IntegrityError, e:
			PentaError(1044).raise_error()

class Notice(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=1000, blank=True, null=False)
	uploader = models.ForeignKey(Staff)
	expiry_date = models.DateField(default=datetime.now()+timedelta(days=30))
	important = models.BooleanField(default=False)
	document = models.FileField(upload_to='documents/%Y/%m/%d')

	def __str__(self):
		return str(self.title) + ' - ' + str(self.uploader)

	def save(self, validate=True):
		if validate:
			if self.title == '' or self.description == '':
				PentaError(997).raise_error()
		try:
			super(Notice, self).save()
		except IntegrityError, e:
			PentaError(1050).raise_error()

class NoticeViewer(models.Model):
	notice = models.ForeignKey(Notice)
	for_students = models.BooleanField(default=False)
	for_staff = models.BooleanField(default=False)
	branch = models.ForeignKey(Branch, blank=True, null=True)
	batch = models.ForeignKey(Batch, blank=True, null=True)
	student = models.ForeignKey(Student, blank=True, null=True)
	staff = models.ForeignKey(Staff, blank=True, null=True)

	def save(self, validate=True):
		from portal.validator.validator import validate_notice_viewer
		if validate:
			validation = validate_notice_viewer(self)
			if not validation:
				validation.raise_error()
		try:
			super(NoticeViewer, self).save()
		except IntegrityError, e:
			PentaError(1040).raise_error()

	def __str__(self):
		return str(self.notice)

class AttendanceDaywise(models.Model):
	date = models.DateField()
	student_batch = models.ForeignKey(StudentBatch)
	attended = models.BooleanField()

	class Meta:
		unique_together = (('date', 'student_batch', ), )

	def __str__(self):
		return str(date) + ' - ' + str(student_batch)

'''
class EMI(models.Model):
	# TODO: think about whether to use StudentBatch or Student
	student_batch = models.ForeignKey(StudentBatch) or student = models.ForeignKey(Student)
	amount_due = models.IntegerField()
	time_deadline = models.DateField()
	description = models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		unique_together = (('student_batch/student', 'time_deadline'))

class Cheque(models.Model):
	# TODO: think about whether to use StudentBatch or Student
	student_batch = models.ForeignKey(StudentBatch) or student = models.ForeignKey(Student)
	amount = models.IntegerField()
	cheque_date = models.DateField()
	cleared = models.BooleanField(default=False)
	clearance_date = models.DateField(blank=True, null=True)
	description = models.CharField(max_length=100, blank=True, null=True)
	cheque_number = models.CharField(max_length=30, blank=True, null=True)
	bank_name = models.CharField(max_length=50, blank=True, null=True)

'''
