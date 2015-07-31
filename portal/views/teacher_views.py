from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt

def dashboard(request):
	return render(request,'teacher/dashboard.html')

def view_attendance(request):
	return render(request,'teacher/attendance.html')

def mark_attendance(request):
	return render(request,'teacher/attendance.html')
