import datetime
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, Form
from django import forms 
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from project.models import (
    Project,
    File,
    Note,
    Comment,
)

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'created', 'deadline']
        labels = {
            'decription': _('Description (optional)'),
            'deadline': _('Deadline (optional)'),
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
    
    users = forms.CharField(max_length=200, label="",
                            widget=forms.TextInput(attrs={'placeholder': 'username'}))
    
    
class RemoveUserForm(forms.Form):
    
    users = forms.ChoiceField(choices = [], label="Remove user from project")    #model choice field
    
    def __init__(self, id_project, *args, **kwargs):
        super(RemoveUserForm, self).__init__(*args, **kwargs)
        project = Project.objects.get(id_project=id_project)
        self.fields['users'].choices = ((x.username, x.username) for x in project.collaborators.all())

