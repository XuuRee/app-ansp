from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from project.forms import ProjectForm, FileForm, NoteForm, SearchFileForm, CommentForm
from .models import Project, File, Note, Comment
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
        if 'NoteFormButton' in request.POST:
            return add_note(request, pk)
        if 'CommentFormButton' in request.POST:
            return add_comment(request, pk)
    else:
        specific_project = Project.objects.get(id_project=pk)
        files = File.objects.filter(id_project=pk)
        notes = Note.objects.filter(id_project=pk)
        comments = Comment.objects.filter(id_project=pk)
        form = NoteForm()
        comment_form = CommentForm()
        context = {
            "specific_project": specific_project,
            "files": files,
            "notes": notes,
            "form": form,
            "comments": comments,
            "comment_form": comment_form,
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
def add_comment(request, pk):
    """ Add a comment to the project. """
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.id_project = Project.objects.get(id_project=pk)
        comment.author = request.user
        form.save()
        return redirect('/projects/{}/'.format(pk))


@login_required
def delete_note(request, pk):
    Note.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # better solution


def add_file(request, pk):
    """ Add a file to the project. """
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.save(commit=False)
        file.id_project = Project.objects.get(id_project=pk)
        form.save()
        return redirect('/projects/{}/files'.format(pk))


def get_files(files, types):
    types, match = list(map(lambda s:s.strip(), types.split(','))), []
    for orig_file in files:
        file_type = orig_file.filepath.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type in types:
            match.append(orig_file)
    return match


def filter_files(request, pk):
    form = SearchFileForm(request.POST)     #not search, but filter form
    if form.is_valid():
        file_types = form.cleaned_data['file_types']
        files = File.objects.filter(id_project=pk)  # twice
        files = get_files(files, file_types)
        form, filter_form = FileForm(), SearchFileForm()        
        context = {
            'form': form,
            'filter_form': filter_form,
            'files': files,
            'primary_key': pk,
        }
        return render(request, 'project/file_form.html', context)


@login_required
def file_handler(request, pk):
    if request.method == 'POST':
        if 'FileFormButton' in request.POST:
            return add_file(request, pk)    # empty file!
        if 'SearchFileFormButton' in request.POST:
            return filter_files(request, pk)    
    else:
        form, filter_form = FileForm(), SearchFileForm()
        files = File.objects.filter(id_project=pk)
        context = {
            'form': form,
            'filter_form': filter_form,
            'files': files,
            'primary_key': pk,
        }
        return render(request, 'project/file_form.html', context)
    

@login_required
def delete_file(request, pk):
    File.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def project_finish(request, pk):
    project = Project.objects.get(pk=pk)
    project.finish = True
    project.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def project_continue(request, pk):
    project = Project.objects.get(pk=pk)
    project.finish = False
    project.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'description', 'created', 'deadline']


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('project:index')
