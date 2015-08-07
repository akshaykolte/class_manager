from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^profile/view-profile/$', 'portal.views.student_views.view_profile'),
	url(r'^profile/edit-profile/$', 'portal.views.student_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.student_views.edit_profile_submit'),
	url(r'^profile/change-password/$', 'portal.views.student_views.change_password'),
	url(r'^profile/change-password/submit$', 'portal.views.student_views.change_password_submit'),
	
   	# Dashboard
    url(r'^dashboard/$', 'portal.views.student_views.dashboard'),
    url(r'^attendance/view-attendance/$', 'portal.views.student_views.view_attendance'),
]
