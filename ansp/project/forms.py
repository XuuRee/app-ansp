from django import forms
from django.forms.models import inlineformset_factory
from project.models import (
    Project,
    File,
)

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        exclude = ()


class FileForm(forms.ModelForm):
    
    class Meta:
        model = File
        exclude = ()
        

FileFormSet = inlineformset_factory(Project, File, form=FileForm, extra=1)  # extra=2
