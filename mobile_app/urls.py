from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^login/$', 'mobile_app.views.auth'),
    url(r'^branches/$', 'mobile_app.views.branches'),
    url(r'^academic_year/$', 'mobile_app.views.academic_year'),
    url(r'^standard/$', 'mobile_app.views.standard'),
    url(r'^batch/$', 'mobile_app.views.batch'),
    url(r'^subject_year/$', 'mobile_app.views.subject_year'),
    url(r'^staff_role/$', 'mobile_app.views.staff_role'),
    url(r'^lecture/$', 'mobile_app.views.lecture'),
    url(r'^student_batch/$', 'mobile_app.views.student_batch'),
    url(r'^lecture_batch/$', 'mobile_app.views.lecture_batch'),
    url(r'^attendance/$', 'mobile_app.views.attendance'),
    url(r'^get_all/$', 'mobile_app.views.get_all'),
    url(r'^save_lecture_batch/$', 'mobile_app.views.save_lecture_batch'),
    url(r'^save_attendance/$', 'mobile_app.views.save_attendance'),
    url(r'^remove_attendance/$', 'mobile_app.views.remove_attendance')
]
