#from django.shortcuts import render, get_object_or_404
#from django.utils import timezone
from .models import Project
from django.views import generic


# Create your views here.
# Generic views IndexView(), DetailView()

class IndexView(generic.ListView):
    template_name = 'project/index.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        return Project.objects.all()


class DetailView(generic.DetailView):
    model = Project
    context_object_name = 'specific_project'
    template_name = 'project/detail.html'
    