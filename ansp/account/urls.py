from . import views
from django.conf.urls import url
from django.contrib.auth.views import login, logout

app_name = 'account'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'account/login.html'}),           # /accounts/login
    url(r'^logout/$', logout, {'template_name': 'account/logout.html'}),        # /accounts/logout
    url(r'^register/$', views.register, name="register"),                       # /accounts/register
    url(r'^profile/$', views.view_profile, name="view_profile"),                # /accounts/profile
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),           # /accounts/profile/edit
    url(r'^change-password/$', views.change_password, name="change_password"),  # /accounts/change-password
]