from django.urls import path,re_path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns=[
    path('api-token-auth/',obtain_auth_token,name='login_token'),
    path('google/login',views.LoginOrSignUpForGoogleUsers.as_view(),name='google_login'),
    path('register',views.Register.as_view(),name='register'),
    path('logout',views.Logout.as_view(),name='logout'),
]