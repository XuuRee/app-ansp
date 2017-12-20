from django.conf.urls import url
from . import views

app_name = 'project'

urlpatterns = [
    # /projects/
    url(r'^$', views.index, name='index'),    #views.IndexView.as_view()
    # /projects/<id_project>
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
    # /projects/create
    url(r'create/$', views.ProjectCreate.as_view(), name="project-create"),
    # /projects/<id_project>/update
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name="project-update"),
    # /projects/<id_project>/delete !
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name="project-delete"),
]