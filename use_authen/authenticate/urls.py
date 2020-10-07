from django.contrib import admin
from django.conf.urls import patterns, url
from authenticate import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$', views.register, name='register'),
        url(r'^login/(?P<user_profile_id>[\w\-]+)/$', views.after_pwd, name='after_pwd'),
        url(r'^tologin/(?P<user_profile_id>[\w\-]+)/$', views.otp_verification, name='otp_verification'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/$', views.restricted, name='restricted'),
        url(r'^logout/$', views.user_logout, name='logout'),
)