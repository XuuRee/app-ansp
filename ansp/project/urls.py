from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    url(r'create/$', views.create_project, name="project-create"),
    url(r'^(?P<pk>[0-9]+)/delete-note/$', views.delete_note, name="delete-note"),
    url(r'^(?P<pk>[0-9]+)/files/$', views.file_handler, name="file-handler"),
    url(r'^(?P<pk>[0-9]+)/delete-file/$', views.delete_file, name="delete-file"),
    url(r'^(?P<pk>[0-9]+)/project-finish/$', views.project_finish, name="project-finish"),
    url(r'^(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name="project-update"),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name="project-delete"),
]