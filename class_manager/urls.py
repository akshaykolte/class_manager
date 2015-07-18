from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'portal.views.auth_views.home'),
    url(r'^login/$', 'portal.views.auth_views.login'),
    url(r'^logout/$', 'portal.views.auth_views.logout'),
    url(r'^student/', include('portal.urls.student_urls')),
    url(r'^teacher/', include('portal.urls.teacher_urls')),
    url(r'^accountant/', include('portal.urls.accountant_urls')),
    url(r'^manager/', include('portal.urls.manager_urls')),
    url(r'^admin/', include('portal.urls.admin_urls')),
]
