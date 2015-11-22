"""mysite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# from backs.views import MyBase
# from backs.views import index
from backs.views import *

urlpatterns = [
	# url(r'^$', 'backs.views.index', name='home'),
	url(r'^add/$', 'backs.views.add', name='add'),
	url(r'^add/(\d+)/(\d+)/$', 'backs.views.add2', name='add2'),
	# url(r'^$', 'backs.views.home', name='home'),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/$', 'backs.views.index', name='index'),
    url(r'^admin/index/$', 'backs.views.index', name='index'),
    # url(r'^admin[/]$', index.as_view()),
    url(r'^admin/home/$', 'backs.views.home', name='home'),
    url(r'^admin/login/$', login.as_view(), name='login'),
    url(r'^admin/logout/$', 'backs.views.logout', name='logout'),

    url(r'^admin/user/$', 'backs.views.user', name='user'),
    url(r'^admin/user/list$', 'backs.views.user_list', name='user_list'),
    url(r'^admin/user/add$', user_add.as_view(), name='user_add'),
    url(r'^admin/user/edit$', user_edit.as_view(), name='user_edit'),
    url(r'^admin/user/del$', 'backs.views.user_del', name='user_del'),

]
