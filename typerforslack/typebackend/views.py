from django.shortcuts import render
import json
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

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
        username=data['username'] if hasattr(data,'username') else False
        password=data['password'] if hasattr(data,'password') else False
        verifying_user=authenticate(username=username,password=password)
        if verifying_user:
            return JsonResponse({'success':'true'})
        else:
            return JsonResponse({'success':'false','error':'Invalid User'})
    else:
        return JsonResponse({"success":"false","error":"Expecting a POST Request"})


        