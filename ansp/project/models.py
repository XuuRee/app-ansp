#from django import forms
from django.db import models
#from django.forms import extras
import datetime
from django.utils.translation import gettext_lazy as _
#from django.utils.timezone import now
from django.core.urlresolvers import reverse


class Project(models.Model):
    id_project = models.AutoField(primary_key=True)     # delete item
    author = models.ForeignKey('auth.User')             # delete item
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(_("Date"), default=datetime.date.today)
    deadline = models.DateField()
    finished = models.DateField()

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'pk': self.id_project})

    def __str__(self):
        return self.name
    
    
class File(models.Model):
    id_file = models.AutoField(primary_key=True)        # delete item
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    filename = models.CharField(max_length=100)
    filepath = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.filename
    

class Note(models.Model):
    id_note = models.AutoField(primary_key=True)
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    note_text = models.CharField(max_length=400)
