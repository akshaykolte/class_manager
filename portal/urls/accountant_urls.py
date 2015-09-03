from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^dashboard/$', 'portal.views.accountant_views.dashboard'),

    url(r'^profile/view-profile/$', 'portal.views.accountant_views.view_profile'),
    url(r'^profile/change-password/$', 'portal.views.accountant_views.change_password'),
	url(r'^profile/change-password/submit$', 'portal.views.accountant_views.change_password_submit'),
	url(r'^profile/edit-profile/$', 'portal.views.accountant_views.edit_profile'),
	url(r'^profile/edit-profile/submit$', 'portal.views.accountant_views.edit_profile_submit'),
	
	url(r'^fees/view-fees/$', 'portal.views.accountant_views.view_fees'),
	url(r'^fees/make-transaction/$', 'portal.views.accountant_views.make_transaction'),

	url(r'^fees/add-base-fees/$', 'portal.views.accountant_views.add_base_fees'),	
	url(r'^fees/view-base-fees/$', 'portal.views.accountant_views.view_base_fees'),	
	url(r'^fees/edit-base-fees/$', 'portal.views.accountant_views.edit_base_fees'),		
	#url(r'^fees/edit-base-fees/submit$', 'portal.views.accountant_views.edit_base_fees_submit'),	

	url(r'^student/create-student/$', 'portal.views.accountant_views.create_student'),	
	url(r'^student/admit-student/$', 'portal.views.accountant_views.admit_student'),	

	url(r'^notices/add-student-notice/$', 'portal.views.accountant_views.add_student_notice'),
	url(r'^notices/add-staff-notice/$', 'portal.views.accountant_views.add_staff_notice'),

]
