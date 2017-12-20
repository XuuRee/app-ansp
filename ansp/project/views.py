from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from .models import Project
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    author_name = request.user.username
    all_projects = Project.objects.filter(author=request.user)
    context = {
        'author_name': author_name,
        'all_projects': all_projects
    }
    return render(request, "project/index.html/", context)


class DetailView(generic.DetailView):
    model = Project
    context_object_name = 'specific_project'
    template_name = 'project/detail.html'


class ProjectCreate(CreateView):
    model = Project
    fields = ['author', 'name', 'description', 'created', 'finished', 'deadline']


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['author', 'name', 'description', 'created', 'finished', 'deadline']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project:index')
