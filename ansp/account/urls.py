from . import views
from django.conf.urls import url
from django.contrib.auth.views import login, logout

app_name = 'account'

urlpatterns = [
    # /account/login
    url(r'^login/$', login, {'template_name': 'account/login.html'}),
    # /account/logout
    url(r'^logout/$', logout, {'template_name': 'account/logout.html'}),
    # /account/register
    url(r'^register/$', views.register, name="register"),
    # /account/profile
    url(r'^profile/$', views.view_profile, name="view_profile"),
    # /account/profile/edit
    url(r'^profile/edit/$', views.edit_profile, name="edit_profile"),
]