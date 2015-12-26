from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.manager_views.dashboard'),
    url(r'^profile/view-profile/$', 'portal.views.manager_views.view_profile'),
    url(r'^profile/edit-profile/$', 'portal.views.manager_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.manager_views.edit_profile_submit'),
    url(r'^profile/change-password/$', 'portal.views.manager_views.change_password'),
    url(r'^profile/change-password/submit$', 'portal.views.manager_views.change_password_submit'),
    url(r'^lectures/add-lectures/$', 'portal.views.manager_views.add_lectures'),
	url(r'^lectures/view-lectures/$', 'portal.views.manager_views.view_lectures'),
	url(r'^teacher/add-teacher/$', 'portal.views.manager_views.add_teacher'),
	url(r'^teacher/view-teacher/$', 'portal.views.manager_views.view_teacher'),
	url(r'^tests/add-tests/$', 'portal.views.manager_views.add_tests'),
	url(r'^tests/view-tests/$', 'portal.views.manager_views.view_tests'),
	url(r'^tests/sms-tests/$', 'portal.views.manager_views.sms_tests'),
    url(r'^tests/sms-tests/submit$', 'portal.views.manager_views.sms_tests_submit'),
	url(r'^attendance-reports/lecturewise-attendance/$', 'portal.views.manager_views.lecturewise_attendance'),
	url(r'^attendance-reports/studentwise-attendance/$', 'portal.views.manager_views.studentwise_attendance'),
	url(r'^attendance-reports/batchwise-attendance/$', 'portal.views.manager_views.batchwise_attendance'),
	url(r'^daywise-attendance-reports/studentwise-attendance/$', 'portal.views.manager_views.daywise_studentwise_attendance'),
	url(r'^daywise-attendance-reports/batchwise-attendance/$', 'portal.views.manager_views.daywise_batchwise_attendance'),
	url(r'^batches/add-batch/$', 'portal.views.manager_views.add_batch'),
	url(r'^batches/view-batch/$', 'portal.views.manager_views.view_batch'),

	#SMS
    url(r'^sms-status/$', 'portal.views.manager_views.sms_status'),
    url(r'^notices/send-sms-notice/$', 'portal.views.manager_views.send_sms_notice'),
    url(r'^notices/send-sms-notice/submit$', 'portal.views.manager_views.send_sms_notice_submit'),

	url(r'^notices/add-student-notice/$', 'portal.views.manager_views.add_student_notice'),
	url(r'^notices/add-staff-notice/$', 'portal.views.manager_views.add_staff_notice'),
	url(r'^notices/view-my-notices/$', 'portal.views.manager_views.view_my_notices'),
	url(r'^notices/edit-my-notice/$', 'portal.views.manager_views.edit_my_notice'),

	url(r'^download/$', 'portal.views.manager_views.respond_as_attachment'),
]
