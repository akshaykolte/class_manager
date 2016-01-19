from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
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
from portal.db_api.auth_db import *
from django.contrib.sessions.models import Session
import traceback

def is_teacher(session_key):
    if not Session.objects.filter(session_key=session_key).exists():
        return False
    session = Session.objects.get(session_key=session_key)
    if 'user' in session.get_decoded() and 'permission_teacher' in session.get_decoded()['user'] and session.get_decoded()['user']['permission_teacher'] == True:
        return True
    else:
        return False

def web_debug(request):
    string = '''
        <form action="/mobile/auth/" method="POST">
            <input type="text" name="username" placeholder="Username"><br/><br/>
            <input type="hidden" name="login" value="true">
            <input type="password" name="password" placeholder="Password"><br/><br/>
            <input type="submit">
        </form>
    '''
    return HttpResponse(string)

@csrf_exempt
def auth(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    auth_dict = get_user(request)
    return_dict = {}
    if auth_dict['logged_in'] == True and auth_dict['permission_teacher'] == True:
        return_dict['status'] = 'Success'
        request.session.set_expiry(10**7)
        return_dict['session_key'] = request.session.session_key
        print request.session['user']
    else:
        return_dict['status'] = "Authentication Failed"
    print return_dict
    return JsonResponse(return_dict)

@csrf_exempt
def get_all(request):
    if not is_teacher(request.GET['sessionid']):
        return JsonResponse( {'status': "Authentication Failed"} )
    session = Session.objects.get(session_key=request.GET['sessionid'])
    staff_id = session.get_decoded()['user']['id']
    branches_list = get_branch()
    academic_year_object = get_current_academic_year()
    standards = get_standard()
    batches = get_batch(academic_year_id=get_current_academic_year()['id'])
    subject_years = get_subjects(academic_year_id=get_current_academic_year()['id'])
    staff_role_list = get_staff_role(staff_id=staff_id, role_name = 'teacher')
    lectures = get_lecture()
    student_batch_list = get_student_batch()
    lecture_batch_list = get_lecture_batch(staff_id = staff_id)
    attendance_list = get_attendance(staff_id = staff_id)
    all_dict = {
        'status': 'Success',
        'branches':branches_list,
        'academic_year': academic_year_object,
        'standards': standards,
        'batches': batches,
        'subject_year': subject_years,
        'staff_role': staff_role_list,
        'lectures': lectures,
        'student_batch': student_batch_list,
        'lecture_batch': lecture_batch_list,
        'attendance': attendance_list
    }
    print 'status in get_all: ', all_dict['status']
    return JsonResponse(all_dict)

@csrf_exempt
def save_lecture_batch(request):
    if not is_teacher(request.GET['sessionid']):
        return JsonResponse( {'status': "Authentication Failed"} )
    is_done_lecture_batch = False
    if request.GET['is_done'] == 'true':
        is_done_lecture_batch = True
    lecture_batch_id = set_lecture_batch(name = request.GET['name'], description = request.GET['description'], date = request.GET['date'], duration = "2 Hours", lecture_id = request.GET['lecture_id'], staff_role_id = request.GET['staff_id'], batch_id = request.GET['batch_id'], is_done = is_done_lecture_batch)
    return JsonResponse({'status': 'Success', 'server_id': lecture_batch_id})

@csrf_exempt
def save_attendance(request):
    if not is_teacher(request.GET['sessionid']):
        return JsonResponse( {'status': "Authentication Failed"} )
    attendance_id = set_attendance(count = 1, student_batch_id = request.GET['student_batch_id'], lecture_batch_id = request.GET['lecture_batch_id'])
    return JsonResponse({'status': 'Success', 'server_id': attendance_id})

@csrf_exempt
def remove_attendance(request):
    if not is_teacher(request.GET['sessionid']):
        return JsonResponse( {'status': "Authentication Failed"} )
    delete_attendance(student_batch_id = request.GET['student_batch_id'], lecture_batch_id = request.GET['lecture_batch_id'])
    return JsonResponse({'status': 'Success'})
