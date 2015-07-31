from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.accountant_views.dashboard'),
    url(r'^view-profile/$', 'portal.views.accountant_views.view_profile'),
]
