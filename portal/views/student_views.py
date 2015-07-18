from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

def dashboard(request):
	return render(request,'student/dashboard.html')

def attendance(request):
	return render(request,'student/attendance.html')