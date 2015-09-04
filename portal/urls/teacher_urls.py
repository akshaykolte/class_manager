from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

	# Profile
	url(r'^profile/view-profile/$', 'portal.views.teacher_views.view_profile'),
	url(r'^profile/edit-profile/$', 'portal.views.teacher_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.teacher_views.edit_profile_submit'),
	url(r'^profile/change-password/$', 'portal.views.teacher_views.change_password'),
	url(r'^profile/change-password/submit$', 'portal.views.teacher_views.change_password_submit'),
	url(r'^profile/logout/$', 'portal.views.teacher_views.logout'),

	# Dashboard
    url(r'^dashboard/$', 'portal.views.teacher_views.dashboard'),

    # Attendance
    url(r'^attendance/add-attendance/$', 'portal.views.teacher_views.add_attendance'),
    url(r'^attendance/view-attendance/$', 'portal.views.teacher_views.view_attendance'),

    # # Lecture
    url(r'^lectures/add-lectures/$', 'portal.views.teacher_views.add_lectures'),
    url(r'^lectures/view-lecture/$', 'portal.views.teacher_views.view_lecture'),

    url(r'^notices/add-student-notice/$', 'portal.views.teacher_views.add_student_notice'),
	#url(r'^notices/add-staff-notice/$', 'portal.views.teacher_views.add_staff_notice'),
	url(r'^notices/view-my-notices/$', 'portal.views.teacher_views.view_my_notices'),
	url(r'^notices/edit-my-notice/$', 'portal.views.teacher_views.edit_my_notice'),
	
    url(r'^test/add-test-marks/$', 'portal.views.teacher_views.add_test_marks'),
    url(r'^test/view-test-marks/$', 'portal.views.teacher_views.view_test_marks'),
]
