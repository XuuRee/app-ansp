from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from .models import Project

# Create your views here.


class IndexView(generic.ListView):
    template_name = 'project/index.html'
    context_object_name = 'all_projects'

    def get_queryset(self):
        return Project.objects.all()


class DetailView(generic.DetailView):
    model = Project
    context_object_name = 'specific_project'
    template_name = 'project/detail.html'


class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'description', 'created', 'finished', 'deadline']
    