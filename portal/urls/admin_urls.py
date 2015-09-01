from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.admin_views.dashboard'),
    url(r'^fees/view-fees/$', 'portal.views.admin_views.view_fees'),
    url(r'^staff/add-staff/$', 'portal.views.admin_views.add_staff'),
    url(r'^staff/view-staff/$', 'portal.views.admin_views.view_staff'),
    url(r'^staff/assign-roles/$', 'portal.views.admin_views.assign_roles'),
    url(r'^set-current-academic-year/$', 'portal.views.admin_views.set_current_academic_year_view'),
    url(r'^track-progress/$', 'portal.views.admin_views.track_progress'),
]
