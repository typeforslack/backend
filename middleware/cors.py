from rest_framework.response import Response
from django.http import HttpResponse

def SimplecorsMiddleware(get_response):
    def middleware(request):
        if request.method.lower() == "options":
        	response = HttpResponse()
        else:
            response = get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, HEAD'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    return middleware