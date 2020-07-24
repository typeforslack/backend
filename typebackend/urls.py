from django.urls import path,re_path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import typingviews

urlpatterns=[
    path('',views.index.as_view(),name='index'),
    path('validate-username',views.UserNameAvailability.as_view(),name='validate_username'),
    path('userlog',typingviews.PostSpeed.as_view(),name='userlog'),
    path('para',typingviews.Paradetails.as_view(),name='para'),
    path('internal/racetrack/para',typingviews.RaceTrack.as_view(),name='racetrack'),
    path('dashboard',typingviews.Dashboard.as_view(),name='streak'),
    re_path(r'^getuserlog/(?:last=(?P<days>\d+)/)?$',typingviews.GraphData.as_view(),name='graph')
]