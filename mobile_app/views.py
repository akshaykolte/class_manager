from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from portal.db_api.branch_db import *

@csrf_exempt
def auth(request):
    pass

@csrf_exempt
def branches(request):
    branches = get_branch()
    return JsonResponse({'branches':branches})
