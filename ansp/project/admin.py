from django.contrib import admin
from project.models import Project, File, Note, Comment


admin.site.register(Project)
admin.site.register(File)
admin.site.register(Note)
admin.site.register(Comment)