from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.manager_views.dashboard'),
    url(r'^lectures/add-lectures/$', 'portal.views.manager_views.add_lectures'),
]
