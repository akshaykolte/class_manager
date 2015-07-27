from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.teacher_views.dashboard'),
    url(r'^attendance/mark-attendance/$', 'portal.views.teacher_views.mark_attendance'),
    url(r'^attendance/view-attendance/$', 'portal.views.teacher_views.view_attendance'),
]
