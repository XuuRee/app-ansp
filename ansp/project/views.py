#from django.shortcuts import render, get_object_or_404
#from django.utils import timezone
from django.views import generic
from .models import Project, File

# Create your views here.

class IndexView(generic.ListView):
    
    template_name = 'project/index.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        return Project.objects.all()


class DetailView(generic.DetailView):
    
    model = Project
    template_name = 'project/detail.html'
