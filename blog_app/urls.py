from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', homePage, name='homePage'),
    url(r'^user/(?P<username>\w+)/$', userProfile, name = 'userProfile'),
    url(r'^blog/(?P<username>\w+)/$', blogPage, name = 'blogPage'),
    url(r'^register/$', userRegister.as_view(), name = 'registerForm'),
    url(r'^article/(?P<id>\d+)/$', articlePage, name = 'articlePage'),
    url(r'^article/new/$', newArticle, name = 'newArticle'),
    url(r'^article/(?P<id>\d+)/edit/$', editArticle, name = 'editArticle'),
    url(r'^article/(?P<id>\d+)/delete/$', deleteArticle, name = 'deleteArticle'),
    url(r'^article/(?P<id>\d+)/comment/new/$', newComment, name = 'newComment'),
    url(r'^article/(?P<idArt>\d+)/comment/(?P<idKom>\d+)/edit/$', editComment, name = 'editComment'),
    url(r'^article/(?P<idArt>\d+)/comment/(?P<idKom>\d+)/delete/$', deleteComment, name ='deleteComment'),
]
