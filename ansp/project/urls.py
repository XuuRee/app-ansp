from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    # /projects/
    url(r'^$', views.index, name='index'),    #views.IndexView.as_view()
    # /projects/<id_project>
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    # /projects/create
    url(r'create/$', views.create_project, name="project-create"),
    
    # /projects/<id_project>/add-note
    #url(r'^(?P<pk>[0-9]+)/$', views.add_note, name="add-note"),    #url(r'^(?P<pk>[0-9]+)/add-note/$', views.add_note, name="add-note"),
    
    # /projects/<id_project>/delete !
    url(r'^(?P<pk>[0-9]+)/delete-note$', views.delete_note, name="delete-note"),
    
    # /projects/<id_project>/add-file
    url(r'^(?P<pk>[0-9]+)/add-file/$', views.add_file, name="add-file"),
    # /projects/<id_project>/update
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name="project-update"),
    # /projects/<id_project>/delete !
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name="project-delete"),
]