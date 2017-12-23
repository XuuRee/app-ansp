from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from project.forms import ProjectForm, FileForm, NoteForm
from .models import Project, File, Note
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


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


@login_required
def detail(request, pk):
    if request.method == 'POST':    # better solution
        return add_note(request, pk)
    else:
        specific_project = Project.objects.get(id_project=pk)
        files = File.objects.filter(id_project=pk)
        notes = Note.objects.filter(id_project=pk)
        form = NoteForm()
        context = {
            "specific_project": specific_project,
            "files": files,
            "notes": notes,
            "form": form,
        }
        return render(request, "project/detail.html", context)


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
        return render(request, 'project/project_form.html', {'form': form})


@login_required
def add_note(request, pk):
    """ Add a note to the project. """
    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.id_project = Project.objects.get(id_project=pk)
        form.save()
        return redirect('/projects/{}/'.format(pk))


@login_required
def delete_note(request, pk):
    Note.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # better solution
    

@login_required
def add_file(request, pk):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.id_project = Project.objects.get(id_project=pk)
            form.save()
            return redirect('/projects/{}/add-file'.format(pk))
    else:
        form = FileForm()
        files = File.objects.filter(id_project=pk)
        context = {
            'form': form,
            'files': files,
        }
        return render(request, 'project/file_form.html', context)
    

@login_required
def delete_file(request, pk):
    File.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'description', 'created', 'finished', 'deadline']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project:index')
