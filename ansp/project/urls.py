from django.conf.urls import url
from .import views

app_name = 'project'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name="detail"),
    # projects
    url(r'create/$', views.create_project, name="project-create"),
    url(r'^(?P<pk>[0-9]+)/update/$', views.update_project, name="project-update"),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete_project, name="project-delete"),
    url(r'^(?P<pk>[0-9]+)/finish/$', views.change_project_finalization, name="change-project-finalization"),
    # notes
    url(r'^(?P<pk>[0-9]+)/delete-note/$', views.delete_note, name="delete-note"),
    # files
    url(r'^(?P<pk>[0-9]+)/files/$', views.file_handler, name="file-handler"),
    url(r'^(?P<pk>[0-9]+)/delete-file/$', views.delete_file, name="delete-file"),
    # comments
    url(r'^(?P<pk>[0-9]+)/delete-comment/$', views.delete_comment, name="delete-comment"),
    # tasks
    url(r'^(?P<pk>[0-9]+)/tasks/$', views.task_handler, name="task-handler"),
    url(r'^(?P<pk>[0-9]+)/tasks/update/$', views.update_task, name="update-task"),
    url(r'^(?P<pk>[0-9]+)/tasks/delete-task/$', views.delete_task, name="delete-task"),
    url(r'^(?P<pk>[0-9]+)/tasks/importance/$', views.change_importance, name="change-importance"),
    url(r'^(?P<pk>[0-9]+)/tasks/finish/$', views.change_finalization, name="change-finalization"),
    # collaboration
    url(r'^(?P<pk>[0-9]+)/members/$', views.manage_members, name="manage-members"),
    url(r'^(?P<pk>[0-9]+)/members/leave/$', views.leave_project, name="leave-project"),
    url(r'^(?P<pk>[0-9]+)/members/add-searched-member/$', views.add_searched_member, name="add-searched-member"),
]