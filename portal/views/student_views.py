from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from portal.db_api.student_db import *
from portal.db_api.auth_db import *

def dashboard(request):
	auth_dict = get_user(request)

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404

	return render(request,'student/dashboard.html')

def view_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404

	details = get_students(id = auth_dict['id'])
	context['auth_dict'] = auth_dict
	context['details'] = details
	return render(request,'student/profile/view-profile.html', context)



def edit_profile(request):
	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404

	details = get_students(id=auth_dict['id'])
	
	context['auth_dict'] =auth_dict
	context['details'] = details

	return render(request, 'student/profile/edit-profile.html', context)

@csrf_exempt
def edit_profile_submit(request):

	auth_dict = get_user(request)
	context = {}

	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404

	set_student(id = auth_dict['id'], first_name = request.POST['first_name'], last_name = request.POST['last_name'], address = request.POST['address'], email = request.POST['email'], phone_number = request.POST['phone_number'], gender = request.POST['gender'])

	return redirect('/student/profile/view-profile')


def change_password(request):

	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404
	if 'message' in request.GET:
		context['message'] = request.GET['message']
	
	elif 'message_error' in request.GET:
		context['message_error'] = request.GET['message_error']

	return render(request,'student/profile/change-password.html', context)

@csrf_exempt
def change_password_submit(request):

	auth_dict = get_user(request)
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404
	if change_password_db(request):
		return redirect('/student/profile/change-password/?message=Password Successfully Changed')
	else:
		return redirect('/student/profile/change-password/?message_error=Password Change Failed')

def logout(request):
	auth_dict = get_user(request)
	context = {}
	if auth_dict['logged_in'] == False:
		raise Http404

	if auth_dict['permission_student'] != True:
		raise Http404

	set_logout(request)
	return redirect('/')
