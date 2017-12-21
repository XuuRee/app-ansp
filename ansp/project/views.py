from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from project.forms import ProjectForm, FileForm, NoteForm
from .models import Project, File, Note
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required
def index(request):
    """ Index page. """
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


@login_required
def create_project(request):
    """ Create new project. """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            form.save()
            return redirect('/projects')
    else:
        form = ProjectForm()
        context = {
            'form': form,
        }
        return render(request, 'project/project_form.html', context)


@login_required
def add_note(request, pk):
    """ Add a note to the project. """
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.id_project = Project.objects.get(id_project=pk)
            form.save()
            return redirect('/projects/{}/'.format(pk))
    else:
        form = NoteForm()
        return render(request, 'project/note_form.html', {'form': form})


@login_required
def add_file(request, pk):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.id_project = Project.objects.get(id_project=pk)
            form.save()
            return redirect('/projects/{}/'.format(pk))
    else:
        form = FileForm()
        return render(request, 'project/file_form.html', {'form': form})


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'description', 'created', 'finished', 'deadline']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project:index')
