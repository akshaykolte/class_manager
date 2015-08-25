from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.admin_views.dashboard'),
    url(r'^batchwise-fees/$', 'portal.views.admin_views.batchwise_fees'),
    url(r'^staff/add-staff/$', 'portal.views.admin_views.add_staff'),
    url(r'^staff/view-staff/$', 'portal.views.admin_views.view_staff'),
    url(r'^set-current-academic-year/$', 'portal.views.admin_views.set_current_academic_year_view'),
]
