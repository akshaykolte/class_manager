from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/dashboard/$', 'portal.views.accountant_views.dashboard'),
    url(r'^profile/view-profile/$', 'portal.views.accountant_views.view_profile'),
    url(r'^profile/change-password/$', 'portal.views.accountant_views.change_password'),
	url(r'^profile/change-password/submit$', 'portal.views.accountant_views.change_password_submit'),
	url(r'^profile/edit-profile/$', 'portal.views.accountant_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.accountant_views.edit_profile_submit'),
]
