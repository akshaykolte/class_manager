from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

def dashboard(request):
	return render(request,'admin/dashboard.html')