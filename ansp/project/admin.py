from django.contrib import admin
from project.models import Project, File, Note, Comment, Task


admin.site.register(Project)
admin.site.register(File)
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Task)