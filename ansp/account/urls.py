from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'account'

urlpatterns = [
    # /account/ ... login, register etc. 
    url(r'^$', views.home),
    # /account/login
    url(r'^login/$', login, {'template_name': 'account/login.html'}),
    # /account/logout
    url(r'^logout/$', logout, {'template_name': 'account/logout.html'}),
    # /account/register
    url(r'^register/$', views.register, name="register"),
]