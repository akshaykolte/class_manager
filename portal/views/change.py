from django.shortcuts import render, redirect
from django.http import Http404
from portal.db_api.auth_db import *
from portal.db_api.staff_db import *


def change_use_as(request):
	auth_dict = get_user(request)
	print auth_dict
	if auth_dict['logged_in'] != True:
		raise Exception("Not logged in");

	if auth_dict['login_type'] != 'staff':
		raise Exception("Not a staff")

	if request.GET['use_as'] == 'teacher' and auth_dict['permission_teacher'] == True: 
		return redirect("/teacher/dashboard/")
	elif request.GET['use_as'] == 'accountant' and auth_dict['permission_accountant'] == True: 
		return redirect("/accountant/dashboard/")
	elif request.GET['use_as'] == 'admin' and auth_dict['permission_admin'] == True: 
		return redirect("/admin/dashboard/")
	elif request.GET['use_as'] == 'manager' and auth_dict['permission_manager'] == True: 
		return redirect("/manager/dashboard/")
	else:
		raise Http404