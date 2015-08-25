from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^profile/view-profile/$', 'portal.views.parent_views.view_profile'),
	url(r'^profile/edit-profile/$', 'portal.views.parent_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.parent_views.edit_profile_submit'),
	url(r'^profile/change-password/$', 'portal.views.parent_views.change_password'),
	url(r'^profile/change-password/submit$', 'portal.views.parent_views.change_password_submit'),
	
   	# Dashboard
    url(r'^dashboard/$', 'portal.views.parent_views.dashboard'),
    url(r'^attendance/view-attendance/$', 'portal.views.parent_views.view_attendance'),
]
