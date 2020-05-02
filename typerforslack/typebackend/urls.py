from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns=[
    path('',views.index,name='index'),
   path('api-token-auth/',obtain_auth_token,name='token')
    # path('register',views.register,name='register')
    # path('postspeed',views.postspeed,name='postspeed')
]