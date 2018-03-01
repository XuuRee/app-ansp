import datetime
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Form
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from project.models import (
    Project,
    File,
    Note,
    Comment,
    Task,
)
from django.contrib.admin import widgets


class DateInput(forms.DateInput):
    input_type = 'date'
    

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'created', 'deadline']
        labels = {
            'decription': _('Description (optional)'),
            'deadline': _('Deadline (optional)'),
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows': 6}),
          'deadline': DateInput()
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
            'filename': _('Name of the file'),
            'filepath': _('Select a file'),
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
        widget = {
            'note_text': forms.Textarea(attrs={'rows': 5, 'cols': 10}), # why not?
        }
        error_messages = {
            'note_text': {
                'max_length': _("This text is too long (400 characters max)."),
            },
        }


class SearchFileForm(forms.Form):
    
    file_types = forms.CharField(max_length=200, label="",
                                 widget=forms.TextInput(attrs={'placeholder': 'jpg, png, pdf etc.'}))


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        exclude = ['id_project']
        fields = ['comment_text']
        widgets = {
          'comment_text': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }
        labels = {       
            'comment_text': _("Write a comment"),
        }


class ManageUserForm(forms.Form):
    
    user = forms.CharField(max_length=200, label="",
                            widget=forms.TextInput(attrs={'placeholder': 'username'}))
    
    
class ChooseUserForm(forms.Form):
    
    user = forms.ChoiceField(choices = [], label="Choose user from project")
    
    def __init__(self, choices, *args, **kwargs):
        super(ChooseUserForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = choices


class TaskForm(forms.ModelForm):
    
    def __init__(self, pk, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["collaborators"].widget = CheckboxSelectMultiple()
        project = Project.objects.get(id_project=pk)
        self.fields['collaborators'].queryset = project.collaborators.all()

    class Meta:
        model = Task
        exclude = ['id_project']
        fields = ['important', 'description', 'collaborators']
        widgets = {
          'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'description': _('Description'),
            'important': _('Is this important task?'),
            'collaborators': _('Sketch members for the task'),
        }

