from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

# Create your views here.

class index(APIView):
    renderer_classes = [JSONRenderer]
    def get(self,request):
        success={
            'status':'Server is running!'
        }
        return Response(success)

class UserNameAvailability(APIView):
    def get(self,request):
        username=request.GET.get('username',None)
        
        data={
            'is_taken':User.objects.filter(username=username).exists(),
        }
        if data['is_taken']:
            data['error']='Username already exists'

        return Response(data)
