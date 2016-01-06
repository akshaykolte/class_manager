from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from portal.db_api.branch_db import *
from portal.db_api.academic_year_db import *
from portal.db_api.standard_db import *
from portal.db_api.batch_db import *
from portal.db_api.subject_db import *
from portal.db_api.staff_db import *
from portal.db_api.lecture_db import *
from portal.db_api.student_db import *
from portal.db_api.lecture_db import *
from portal.db_api.attendance_db import *

@csrf_exempt
def auth(request):
    pass

@csrf_exempt
def branches(request):
    branches_list = get_branch()
    return JsonResponse({'branches':branches_list})

@csrf_exempt
def academic_year(request):
    academic_year_object = get_current_academic_year()
    return JsonResponse({'academic_year': academic_year})

@csrf_exempt
def standard(request):
    standards = get_standard()
    return JsonResponse({'standards': standards})

@csrf_exempt
def batch(request):
    batches = get_batch(academic_year_id=get_current_academic_year()['id'])
    return JsonResponse({'batches': batches})

@csrf_exempt
def subject_year(request):
    subject_years = get_subjects(academic_year_id=get_current_academic_year()['id'])
    return JsonResponse({'batches': batches})

@csrf_exempt
def staff_role(request):
    staff_role_list = get_staff_role(staff_id=request.GET['staff_id'])
    return JsonResponse({'staff_role': staff_role_list})

@csrf_exempt
def lecture(request):
    lectures = get_lecture_batch(staff_id = request.GET['staff_id'])
    return JsonResponse({'lectures': lectures})

@csrf_exempt
def student_batch(request):
    student_batch_list = get_student_batch(academic_year_id = get_current_academic_year()['id'])
    return JsonResponse({'student_batch': student_batch_list})

@csrf_exempt
def lecture_batch(request):
    lecture_batch_list = get_lecture_batch(staff_id = request.GET['staff_id'])
    return JsonResponse({'lecture_batch': lecture_batch_list})

@csrf_exempt
def attendance(request):
    attendance_list = get_student_batch(staff_id = request.GET['staff_id'])
    return JsonResponse({'attendance': attendance_list})
