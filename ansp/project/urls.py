from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [
    url(r'^$', views.index, name='index'),                              # /projects/
    url(r'^(?P<id_project>[0-9]+)/$', views.detail, name="detail"),     # /projects/<id_project>
]