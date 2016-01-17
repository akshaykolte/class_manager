from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^web_debug/$', 'mobile_app.views.web_debug'),
    url(r'^auth/$', 'mobile_app.views.auth'),
    url(r'^login/$', 'mobile_app.views.auth'),
    url(r'^get_all/$', 'mobile_app.views.get_all'),
    url(r'^save_lecture_batch/$', 'mobile_app.views.save_lecture_batch'),
    url(r'^save_attendance/$', 'mobile_app.views.save_attendance'),
    url(r'^remove_attendance/$', 'mobile_app.views.remove_attendance')
]
