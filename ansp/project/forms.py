from django import forms
from .models import Project, File


class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'created', 'deadline']


class FileForm(forms.ModelForm):
    
    class Meta:
        model = File
        fields = ['filename', 'filepath']
    