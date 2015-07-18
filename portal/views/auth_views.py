from django.shortcuts import render,redirect
from portal.db_api.auth_db import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
	context = {}
	auth_dict = get_user(request)
	if auth_dict['logged_in']:
		context = {'logged_in':True,'message':'You are logged in'}
	return render(request,'home.html',context)
