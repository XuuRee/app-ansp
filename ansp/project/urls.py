from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    # /projects/
    url(r'^$', views.index, name='index'),
    # /projects/<id_project>
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    # /projects/create
    url(r'create/$', views.create_project, name="project-create"),
    # /projects/<id_project>/delete !
    url(r'^(?P<pk>[0-9]+)/delete-note/$', views.delete_note, name="delete-note"),
    # /projects/<id_project>/add-file
    url(r'^(?P<pk>[0-9]+)/files/$', views.file_handler, name="file-handler"),
    # /projects/<id_project>/add-file
    url(r'^(?P<pk>[0-9]+)/files/images$', views.file_handler_images, name="file-handler-images"),
    # /projects/<id_project>/delete 
    url(r'^(?P<pk>[0-9]+)/delete-file/$', views.delete_file, name="delete-file"),
    
    url(r'^(?P<pk>[0-9]+)/project-finish/$', views.project_finish, name="project-finish"),
    
    # /projects/<id_project>/update
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name="project-update"),
    # /projects/<id_project>/delete !
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name="project-delete"),
]