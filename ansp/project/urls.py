from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),                              # /projects/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),     # /projects/<id_project>
]