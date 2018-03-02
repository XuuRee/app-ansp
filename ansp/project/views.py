from project.forms import ProjectForm, FileForm, NoteForm, FilterFileForm, CommentForm, ManageUserForm, ChooseUserForm, TaskForm
from .models import Project, File, Note, Comment, Task
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


@login_required
def index(request):
    """ Main view, index page. """
    unfinished_projects = Project.objects.filter(collaborators__in=[request.user], finish=False).order_by('-created')
    finished_projects = Project.objects.filter(collaborators__in=[request.user], finish=True).order_by('-created')
    tasks = Task.objects.filter(
        collaborators__in=[request.user],
        finish=False,
        important=True
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(unfinished_projects, 9)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    context = {
        'projects': projects,
        'finished_projects': finished_projects,
        'tasks': tasks,
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
        project = Project.objects.get(id_project=pk)
        notes = Note.objects.filter(id_project=pk, author=request.user)
        comments = Comment.objects.filter(id_project=pk)
        tasks = Task.objects.filter(id_project=pk, finish=False)
        context = {
            'specific_project': project,
            'form': NoteForm(),
            'comment_form': CommentForm(),
            'notes': notes,
            'comments': comments,
            'tasks': tasks,
        }
        return render(request, "project/detail.html", context)


########################################################
# PROJECTS FUNCTIONS
########################################################


@login_required
def create_project(request):
    """ Create new project. """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            form.save()
            project.collaborators.add(request.user)
            return redirect('/projects')    # on specific project
    else:
        form = ProjectForm()
        context = {
            'form': form,
            'update': False,
        }
        return render(request, 'project/project_form.html', context) # project_form


@login_required
def update_project(request, pk):
    """ Update a specific project. """
    instance = Project.objects.get(id_project=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/projects')
    else:
        context = {
            'form': form,
            'update': True,
        }
        return render(request, 'project/project_form.html', context)


def delete_project(request, pk):
    """ Delete a specific project. """
    Project.objects.get(pk=pk).delete()
    return redirect('/projects')           # index(request)


def change_project_finalization(request, pk):
    """ Finish or restore a project. """
    project = Project.objects.get(pk=pk)
    if project.finish:
        project.finish = False
    else:
        project.finish = True
    project.save()
    return redirect('/projects')


########################################################
# COMMENTS FUNCTIONS
########################################################


@login_required
def add_comment(request, pk):
    """ Add a comment to the project. """
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.id_project = Project.objects.get(id_project=pk)
        comment.author = request.user
        comment.date = date.today()
        form.save()
        return redirect('/projects/{}/'.format(pk))


@login_required
def delete_comment(request, pk):
    """ Delete comment from the project. """
    Comment.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # better solution


########################################################
# NOTE FUNCTIONS
########################################################


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
    return redirect(request.META.get('HTTP_REFERER'))   # better solution


########################################################
# FILES FUNCTIONS
#   - where heroku save files.
########################################################


def add_file(request, pk):
    """ Add a file to the project. """
    file_form = FileForm(request.POST, request.FILES)
    if file_form.is_valid():
        upload_file = file_form.save(commit=False)
        upload_file.id_project = Project.objects.get(id_project=pk)
        file_form.save()
        return redirect('/projects/{}/files'.format(pk))
    else:
        filter_form = FilterFileForm()
        files = File.objects.filter(id_project=pk)
        context = {
            'file_form': file_form,
            'filter_form': filter_form,
            'files': files,
            'project_pk': pk,
        }
        return render(request, 'project/file_form.html', context)


def get_files(files, types):
    """ Return files with given types. """
    types, match = list(map(lambda s:s.strip(), types.split(','))), []
    for orig_file in files:
        file_type = orig_file.filepath.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type in types:
            match.append(orig_file)
    return match


def filter_files(request, files, pk):
    """ Filter all files with the given suffixes. """
    filter_form = FilterFileForm(request.POST)
    if filter_form.is_valid():
        file_types = filter_form.cleaned_data['file_types']
        files = get_files(files, file_types)      
        context = {
            'file_form': FileForm(),
            'filter_form': FilterFileForm(),
            'files': files,
            'project_pk': pk,
        }
        return render(request, 'project/file_form.html', context)


@login_required
def file_handler(request, pk):
    files = File.objects.filter(id_project=pk)
    if request.method == 'POST':
        if 'FileFormButton' in request.POST:
            return add_file(request, pk)    
        if 'FilterFileFormButton' in request.POST:  
            return filter_files(request, files, pk)    
    else:
        context = {
            'file_form': FileForm(),
            'filter_form': FilterFileForm(),
            'files': files,
            'project_pk': pk,
        }
        return render(request, 'project/file_form.html', context)
    

@login_required
def delete_file(request, pk):
    File.objects.get(pk=pk).delete()
    return redirect(request.META.get('HTTP_REFERER')) # better solution


########################################################
# MEMBERS FUNCTIONS
########################################################


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


def delete_task(request, pk):
    """ Remove a specific task. """
    Task.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   # better solution


def change_finalization(request, pk):
    """ Finish a specific task. """
    task = Task.objects.get(id_task=pk)
    if task.finish:
        task.finish = False
    else:
        task.finish = True
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_importance(request, pk):
    """ Change importance of the task. """
    task = Task.objects.get(id_task=pk)
    if task.important:
        task.important = False
    else:
        task.important = True
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # really?


def distribute_tasks(tasks):
    """ Divide all the tasks to to finish / unfinish. """
    finish, unfinish = [], []
    for task in tasks:
        if task.finish:
            finish.append(task)
        else:
            unfinish.append(task)
    return (finish, unfinish)


def update_task(request, pk):
    """ Update a specific task. """
    instance = Task.objects.get(id_task=pk)
    project = instance.id_project
    task_form = TaskForm(project.id_project, request.POST or None, instance=instance)
    if task_form.is_valid():
        task_form.save()
        return redirect('/projects/{}/tasks'.format(project.id_project)) 
    tasks = distribute_tasks(Task.objects.filter(id_project=project.id_project))
    context = {
        'task_form': task_form,
        'finished_tasks': tasks[0],
        'unfinished_tasks': tasks[1],
        'primary_key': project.id_project,
        'update': True,
    }
    return render(request, 'project/task_form.html', context)

@login_required
def task_handler(request, pk):
    """ Task handler for creating, deleting and
    updating the task . """
    if request.method == 'POST':
        form = TaskForm(pk, request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.id_project = Project.objects.get(id_project=pk)
            form.save()
            return redirect('/projects/{}/tasks'.format(pk))
    else:
        task_form = TaskForm(pk)
        finished_tasks = Task.objects.filter(finish=True)
        unfinished_tasks = Task.objects.filter(finish=False)
        tasks = distribute_tasks(Task.objects.filter(id_project=pk))
        context = {
            'task_form': task_form,
            'finished_tasks': finished_tasks,
            'unfinished_tasks': unfinished_tasks,
            'primary_key': pk,
            'update': False,
        }
        return render(request, 'project/task_form.html', context)

