from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dashboard/$', 'portal.views.student_views.dashboard'),
    url(r'^attendance/$', 'portal.views.student_views.attendance'),
]
