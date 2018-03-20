import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import date


class Project(models.Model):
    id_project = models.AutoField(primary_key=True)
    collaborators = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(default=datetime.date.today)
    deadline = models.DateField(null=True, blank=False)
    finish = models.BooleanField(default=False)
    
    @property
    def is_past_due(self):
        if self.deadline is None:
            return False
        return date.today() > self.deadline
    
    @property
    def is_finish(self):
        return self.finish
    
    
class File(models.Model):
    id_file = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    filepath = models.FileField(null=False, blank=False)
    

class Note(models.Model):
    id_note = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    note_text = models.CharField(max_length=400)


class Comment(models.Model):
    id_comment = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    date = models.DateField(null=False, blank=True)


# headline, date.
class Task(models.Model):
    id_task = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User)
    description = models.TextField()
    important = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    
