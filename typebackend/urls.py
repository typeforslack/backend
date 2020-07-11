from django.urls import include,path,re_path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import typingviews

urlpatterns=[
    path('',views.index.as_view(),name='index'),
    path('api-token-auth/',obtain_auth_token,name='login_token'),
    path('register',views.Register.as_view(),name='register'),
    path('validate-username',views.UserNameAvailability.as_view(),name='validate_username'),
    path('logout',views.Logout.as_view(),name='logout'),
    path('userlog',typingviews.PostSpeed.as_view(),name='userlog'),
    path('para',typingviews.Paradetails.as_view(),name='para'),
    path('paraForRaceTrack',typingviews.RaceTrack.as_view(),name='racetrack'),
    re_path(r'^getuserlog/(?:last=(?P<days>\d+)/)?$',typingviews.DashboardData.as_view(),name='graph'),
    path('signup/', include('allauth.urls')),
]