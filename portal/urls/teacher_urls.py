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
    # url(r'^attendance/mark-attendance/$', 'portal.views.teacher_views.mark_attendance'),
    # url(r'^attendance/view-attendance/$', 'portal.views.teacher_views.view_attendance'),
    
    # # Lecture
    url(r'^lectures/add-lectures/$', 'portal.views.teacher_views.add_lectures'),
    # url(r'^lectures/view-lecture/$', 'portal.views.teacher_views.view_lecture'),
]
