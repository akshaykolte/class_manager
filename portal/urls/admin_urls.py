from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.admin_views.dashboard'),
    url(r'^fees/view-fees/$', 'portal.views.admin_views.view_fees'),
    url(r'^staff/add-staff/$', 'portal.views.admin_views.add_staff'),
    url(r'^staff/view-staff/$', 'portal.views.admin_views.view_staff'),
    url(r'^staff/assign-roles/$', 'portal.views.admin_views.assign_roles'),
    url(r'^set-current-academic-year/$', 'portal.views.admin_views.set_current_academic_year_view'),
    url(r'^track-progress/detailed-progress/$', 'portal.views.admin_views.detailed_progress'),
    url(r'^track-progress/graphical-overview/$', 'portal.views.admin_views.graphical_overview'),

    url(r'^notices/add-student-notice/$', 'portal.views.admin_views.add_student_notice'),
	url(r'^notices/add-staff-notice/$', 'portal.views.admin_views.add_staff_notice'),	
]
