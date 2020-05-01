from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

# Create your views here.


def index(request):
    success={
        'status':'Server is running'
    }
    return JsonResponse(success)

@csrf_exempt
def login(request):
    if request.method=='POST':
        data=json.loads(request.body)
        username=data['username'] if 'username' in data else False
        password=data['password'] if 'password' in data else False
        verifying_user=authenticate(username=username,password=password)
        if verifying_user:
            return JsonResponse({'success':'true'})
        else:
            return JsonResponse({'success':'false','error':'Invalid User'})
    else:
        return JsonResponse({"success":"false","error":"Expecting a POST Request"})

@csrf_exempt
def register(request):
    if request.method=='POST':
        data=json.loads(request.body)
        username=data['username'] if 'username' in data else False
        password=data['password'] if 'password' in data else False
        email_id= data['email_id'] if 'email_id' in data else False
        try:
            newuser=User.objects.create_user(username,password,email_id)
        # if newuser:
            return JsonResponse({'success':'true'})
        except Exception as e:
            return JsonResponse({'sucess':'false','error':e.args})
    else:
        return JsonResponse({"success":'false','error':'Expecting a POST Request'})


