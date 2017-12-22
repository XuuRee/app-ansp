import datetime
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Form
from django import forms 
from django.forms.models import inlineformset_factory
from project.models import (
    Project,
    File,
    Note,
)

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'created', 'deadline']
        labels = {
            'decription': _('Description (optional)'),
        }
        error_messages = {
            'name': {
                'max_length': _("This name is too long (100 characters max)."),
            },
        }
        

class FileForm(forms.ModelForm):
    
    class Meta:
        model = File
        exclude = ['id_project']
        fields = [
            'filename',
            'filepath'
        ]
        labels = {                   
            'filename': _('Filename'),
            'filepath': _('Path'),
        }
        error_messages = {
            'filename': {
                'max_length': _("This text is too long (100 characters max)."),
            },
        }
        

class NoteForm(forms.ModelForm):
    
    class Meta:
        model = Note
        exclude = ['id_project']
        fields = ['note_text']
        labels = {       # work?
            'note_text': _("Write a note"), # text field
        }
        error_messages = {
            'note_text': {
                'max_length': _("This text is too long (400 characters max)."),
            },
        }
