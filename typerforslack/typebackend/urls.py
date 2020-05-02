from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('api-token-auth/',obtain_auth_token,name='Login_token'),
    path('register',views.Register.as_view(),name='register'),
    path('logout',views.Logout.as_view(),name='logout')
    # path('postspeed',views.postspeed,name='postspeed')
]