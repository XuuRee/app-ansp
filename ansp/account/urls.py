from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'account'

urlpatterns = [
    # /account/ ... login, register etc. 
    url(r'^$', views.home),
    # /account/login
    url(r'^login/$', login, {'template_name': 'account/login.html'})
]