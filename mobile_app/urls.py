from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^login/$', 'mobile_app.views.auth'),
    url(r'^branches/$', 'mobile_app.views.branches'),
]
