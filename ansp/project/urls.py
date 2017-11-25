from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    # /projects/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /projects/<id_project>
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
    # /projects/create
    url(r'projects/create/$', views.ProjectCreate.as_view(), name="project-create"),
]