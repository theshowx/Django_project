from django.conf.urls import url
from django.urls import include, path
from .views import *

urlpatterns = [
    url(r'^$', homePage, name='homePage'),
    url(r'^user/(?P<username>\w+)/$', userProfile, name = 'userProfile'),
    url(r'^blog/(?P<username>\w+)/$', blogPage, name = 'blogPage'),
    url(r'^article/(?P<id>\d+)/$', articlePage, name = 'articlePage'),
    url(r'^register/$', userRegister.as_view(), name = 'registerForm'),
]