from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.admin_views.dashboard'),
    url(r'^profile/view-profile/$', 'portal.views.admin_views.view_profile'),
    url(r'^profile/edit-profile/$', 'portal.views.admin_views.edit_profile'),
    url(r'^profile/edit-profile/submit$', 'portal.views.admin_views.edit_profile_submit'),
    url(r'^profile/change-password/$', 'portal.views.admin_views.change_password'),
    url(r'^profile/change-password/submit$', 'portal.views.admin_views.change_password_submit'),
    
    url(r'^fees/view-fees/$', 'portal.views.admin_views.view_fees'),
    url(r'^staff/add-staff/$', 'portal.views.admin_views.add_staff'),
    url(r'^staff/view-staff/$', 'portal.views.admin_views.view_staff'),
    url(r'^staff/assign-roles/$', 'portal.views.admin_views.assign_roles'),
    url(r'^set-current-academic-year/$', 'portal.views.admin_views.set_current_academic_year_view'),
    url(r'^track-progress/detailed-progress/$', 'portal.views.admin_views.detailed_progress'),
    url(r'^track-progress/graphical-overview/$', 'portal.views.admin_views.graphical_overview'),

    #SMS
    url(r'^sms-status/$', 'portal.views.admin_views.sms_status'),
    url(r'^notices/send-sms-notice/$', 'portal.views.admin_views.send_sms_notice'),
    url(r'^notices/send-sms-notice/submit$', 'portal.views.admin_views.send_sms_notice_submit'),
    

    url(r'^notices/add-student-notice/$', 'portal.views.admin_views.add_student_notice'),
	url(r'^notices/add-staff-notice/$', 'portal.views.admin_views.add_staff_notice'),	
	url(r'^notices/view-my-notices/$', 'portal.views.admin_views.view_my_notices'),
	url(r'^notices/edit-my-notice/$', 'portal.views.admin_views.edit_my_notice'),

    url(r'^download/$', 'portal.views.admin_views.respond_as_attachment'),

]
