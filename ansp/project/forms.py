import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Form
import datetime 
from django import forms
from django.contrib.admin import widgets 
from django.forms.models import inlineformset_factory
from project.models import (
    Project,
    File,
)

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'created', 'deadline']
        labels = {
            'decription': _('Decription (optional)'),
        }
        error_messages = {
            'name': {
                'max_length': _("This name is too long (100 characters max)."),
            },
        }
        

class FileForm(forms.ModelForm):
    
    class Meta:
        model = File
        exclude = ()
        

FileFormSet = inlineformset_factory(Project, File, form=FileForm, extra=1)  # extra=2
