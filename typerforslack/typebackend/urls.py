from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import typingviews

urlpatterns=[
    path('',views.index.as_view(),name='index'),
    path('api-token-auth/',obtain_auth_token,name='Login_token'),
    path('register',views.Register.as_view(),name='register'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('userlog',typingviews.PostSpeed.as_view(),name='userlog')
]