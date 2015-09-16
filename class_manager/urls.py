from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # Examples:
    # url(r'^$', 'class_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^pentadmin/', include(admin.site.urls)),
    url(r'^change/', 'portal.views.change.change_use_as'),
    url(r'^$', 'portal.views.auth_views.home'),
    url(r'^login/$', 'portal.views.auth_views.login'),
    url(r'^logout/$', 'portal.views.auth_views.logout'),
    url(r'^student-search/$', 'portal.views.student_search_views.home'),
    url(r'^staff-search/$', 'portal.views.staff_search_views.home'),
    url(r'^student/', include('portal.urls.student_urls')),
    url(r'^parent/', include('portal.urls.parent_urls')),
    url(r'^teacher/', include('portal.urls.teacher_urls')),
    url(r'^accountant/', include('portal.urls.accountant_urls')),
    url(r'^manager/', include('portal.urls.manager_urls')),
    url(r'^admin/', include('portal.urls.admin_urls')),
	#patterns('',(r'^', include('portal.urls')),) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

]

