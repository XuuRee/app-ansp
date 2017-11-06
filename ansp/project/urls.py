from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),                              # /projects/
    url(r'^(?P<id_project>[0-9]+)/$', views.detail, name="detail"),     # /projects/<id_project>
]