from django.views.generic.edit import DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from project.forms import ProjectForm, FileForm, NoteForm, SearchFileForm, CommentForm, ManageUserForm, ChooseUserForm, TaskForm
from .models import Project, File, Note, Comment, Task
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
    """ Check if deadline is past due. """
    if project_date is None:
        return False
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
        notes = notes.filter(author=request.user)
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
        note.id_project = Project.objects.get(id_project=pk) # has to be?
        note.author = request.user
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


def remove_member(request, project, pk):
    """ Remove a member from project according to
    given operation. """
    userstring = request.POST.get('user')
    try:
        user = User.objects.get(username=userstring)   # not only username?
    except User.DoesNotExist:
        return False
    project.collaborators.remove(user)
    return True


def add_member(request, project, pk):
    """ Add a member from project according to
    given operation. """
    form = ManageUserForm(request.POST)
    if form.is_valid():
        userstring = form.cleaned_data['user']
        try:
            user = User.objects.get(username=userstring)   # not only username?
        except User.DoesNotExist:
            return False
        project.collaborators.add(user)
        return True
    return False


@login_required
def add_searched_member(request, pk):
    id_user = request.POST["id_user"]
    project = Project.objects.get(id_project=pk)
    user = User.objects.get(id=id_user)
    project.collaborators.add(user)
    context = {
        'primary_key': pk,
        'searched_members': [],
        'add_success': True,
        'remove_success': None,
    }
    return http_members(request, context)


# not search authenticate user, and user that are already
# in project
def search_members(request, project, pk):
    """ Search specific user in database of users. """
    result_list = []
    form = ManageUserForm(request.POST)
    if form.is_valid():
        userstring = form.cleaned_data['user']
        all_users = User.objects.all()
        for user in all_users:
            if userstring in user.username:
                result_list.append(user)
    return result_list


def http_members(request, context):
    pk = context.get("primary_key")
    project = Project.objects.get(id_project=pk)
    add_form = ManageUserForm()
    choices = ((x.username, x.username) for x in project.collaborators.all())
    remove_form = ChooseUserForm(choices)  
    context['add_form'] = add_form
    context['remove_form'] = remove_form
    return render(request, 'project/member_form.html', context)


@login_required
def manage_members(request, pk):
    # what happen if remove myself?
    project = Project.objects.get(id_project=pk)
    searched_members = []
    add_success, remove_success = None, None
    if request.method == 'POST':
        if 'SelectMemberButton' in request.POST:
            add_success = add_member(request, project, pk)   
        if 'RemoveUserButton' in request.POST:
            remove_success = remove_member(request, project, pk)
        if 'SearchUserButton' in request.POST:
            searched_members = search_members(request, project, pk)
    context = {
        'primary_key': pk,
        'searched_members': searched_members,
        'add_success': add_success,
        'remove_success': remove_success,
    }
    return http_members(request, context)


########################################################
# TASK FUNCTIONS
########################################################

@login_required
def create_task(request, pk):
    """ Create a new task. """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            print("VALID")
            task = form.save(commit=False)
            task.id_project = Project.objects.get(id_project=pk)
            userlist = request.POST.getlist('collaborators')
            print(userlist)
            for username in userlist.values:
                user = User.objects.get(username=username)
                task.collaborators.add(user)
            form.save()
            return redirect('/projects/{}/create-task'.format(pk))
        else:
            print("NOT VALID")
    else:
        project = Project.objects.get(id_project=pk)
        queryset = project.collaborators.all()
        task_form = TaskForm(queryset)
        tasks = Task.objects.filter(id_project=pk)
        context = {
            'task_form': task_form,
            'tasks': tasks,
        }
        return render(request, 'project/task_form.html', context)


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
