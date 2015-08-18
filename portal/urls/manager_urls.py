from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.manager_views.dashboard'),
    url(r'^lectures/add-lectures/$', 'portal.views.manager_views.add_lectures'),
	url(r'^lectures/view-lectures/$', 'portal.views.manager_views.view_lectures'),
	url(r'^teacher/add-teacher/$', 'portal.views.manager_views.add_teacher'),
	url(r'^teacher/view-teacher/$', 'portal.views.manager_views.view_teacher'),
	url(r'^tests/add-tests/$', 'portal.views.manager_views.add_tests'),
	url(r'^tests/view-tests/$', 'portal.views.manager_views.view_tests'),
	url(r'^attendance-reports/lecturewise-attendance/$', 'portal.views.manager_views.lecturewise_attendance'),
]
