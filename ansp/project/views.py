from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from project.forms import ProjectForm, FileForm, NoteForm, SearchFileForm, CommentForm, ManageUserForm
from .models import Project, File, Note, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import date


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required
def index(request):
    """ Index page. """
    author_name = request.user.username
    all_projects, projects = Project.objects.all(), []
    # better solution
    for project in all_projects:
        if request.user in project.collaborators.all():
            projects.append(project)
    # ---
    context = {
        'author_name': author_name,
        'all_projects': projects,
    }
    return render(request, "project/index.html/", context)


def is_past_due(project_date):
    return date.today() > project_date


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
        note_form, comment_form = NoteForm(), CommentForm()
        date_deadline = is_past_due(specific_project.deadline)
        context = {
            'specific_project': specific_project,
            'files': files,
            'notes': notes,
            'form': note_form,
            'comments': comments,
            'comment_form': comment_form,
            'date_deadline': date_deadline,
        }
        return render(request, "project/detail.html", context)


@login_required
def create_project(request):
    """ Create new project. """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            form.save()
            project.collaborators.add(request.user)
            return redirect('/projects')
    else:
        form = ProjectForm()
        return render(request, 'project/project_form.html', {'form': form})


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
def delete_comment(request, pk):
    """ Delete comment from the project. """
    Comment.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # better solution


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


# what happen if remove yourself?
def add_remove_member(request, pk, operation):
    """ Add or remove member from project according to
    given operation. """
    success = True
    form = ManageUserForm(request.POST)
    if form.is_valid():
        userstring = request.POST.get('users')
        try:
            project = Project.objects.get(id_project=pk)
            user = User.objects.get(username=userstring)   # not only username?
        except User.DoesNotExist or Project.DoesNotExit:
            success = False
        if success and operation == 'add':
            project.collaborators.add(user)
        if success and operation == 'remove':
            project.collaborators.remove(user)
    form = ManageUserForm()
    context = {
        'primary_key': pk,
        'form': form,
        'success': success,
        'operation': operation,
    }
    return render(request, 'project/member_form.html', context)


@login_required
def manage_members(request, pk):
    if request.method == 'POST':
        if 'SelectMemberButton' in request.POST:
            return add_remove_member(request, pk, 'add')   
        if 'RemoveUserButton' in request.POST:
            return add_remove_member(request, pk, 'remove')
        if 'SearchUserButton' in request.POST:
            return filter_files(request, pk)
    else:
        form = ManageUserForm()
        context = {
            'primary_key': pk,
            'form': form,
            'success': None,
        }
        return render(request, 'project/member_form.html', context)


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
