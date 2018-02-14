import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    id_project = models.AutoField(primary_key=True)
    collaborators = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(_("Created"), default=datetime.date.today)
    deadline = models.DateField(null=True, blank=True)
    finish = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'pk': self.id_project})

    def __str__(self):
        return self.name
    
    
class File(models.Model):
    id_file = models.AutoField(primary_key=True)        # delete item
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    filepath = models.FileField(null=True, blank=False)

    def __str__(self):
        return self.filename
    

class Note(models.Model):
    id_note = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', null=True) # delete null
    note_text = models.CharField(max_length=400)


class Comment(models.Model):
    id_comment = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', null=True) # delete null
    comment_text = models.TextField(blank=False)
    
    
class Task(models.Model):
    id_task = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User)
    description = models.TextField(blank=False)
    important = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)

