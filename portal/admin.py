from django.contrib import admin
from portal.models import *

admin.site.register(AcademicYear)
admin.site.register(Branch)
admin.site.register(Batch)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentParent)
admin.site.register(Staff)
admin.site.register(Role)
admin.site.register(StaffRole)
admin.site.register(Standard)
admin.site.register(Subject)
admin.site.register(SubjectYear)
admin.site.register(SMS)
class StudentBatchCustom(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		subject_year_id_list = map(int,request.POST.getlist('subject_years'))
		# No validations through save
		# Validations will only be done while .add() generates pre_save signal
		obj.save()

admin.site.register(StudentBatch, StudentBatchCustom)
admin.site.register(Lecture)
admin.site.register(LectureBatch)
admin.site.register(Attendance)
admin.site.register(BaseFee)
admin.site.register(FeeType)
admin.site.register(FeeTransaction)

admin.site.register(Test)
admin.site.register(TestBatch)
admin.site.register(TestStaffRole)

admin.site.register(Notice)
admin.site.register(NoticeViewer)

admin.site.register(TestStudentBatch)
admin.site.register(AttendanceDaywise)
