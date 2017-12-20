from . import views
from django.conf.urls import url
from django.contrib.auth.views import (
    login,
    logout,
    password_reset,         # not done
    password_reset_done,
    password_reset_confirm,
    password_reset_complete
)

app_name = 'account'

urlpatterns = [
    # /accounts/login
    url(r'^login/$', login, {'template_name': 'account/login.html'}, name="login"),
    # /accounts/logout
    url(r'^logout/$', logout, {'template_name': 'account/logout.html'}, name="logout"),
    # /accounts/register
    url(r'^register/$', views.register, name="register"),
    # /accounts/profile
    url(r'^profile/$', views.view_profile, name="view_profile"),
    # /accounts/profile/edit
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
    # /accounts/change-password
    url(r'^change-password/$', views.change_password, name="change_password")
]