from project.forms import ProjectForm, FileForm, NoteForm, FilterFileForm, CommentForm, ManageUserForm, ChooseUserForm, TaskForm
from .models import Project, File, Note, Comment, Task
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
from django.contrib import messages


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
        notes = Note.objects.filter(
                    id_project=pk,
                    author=request.user
                )
        all_comments = Comment.objects.filter(id_project=pk).order_by('-date')
        tasks = Task.objects.filter(
                    id_project=pk,
                    finish=False).order_by('-important')
        page = request.GET.get('page', 1)
        paginator = Paginator(all_comments, 18)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
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
            return redirect('/projects')
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
    return redirect(request.META.get('HTTP_REFERER'))   # better solution


########################################################
# NOTES FUNCTIONS
########################################################


@login_required
def add_note(request, pk):
    """ Add a note to the project. """
    form = NoteForm(request.POST)
    if form.is_valid():
        note = form.save(commit=False)
        note.id_project = Project.objects.get(id_project=pk)
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
        messages.success(
            request,
            'The file was added.',
            extra_tags='alert'
        )
        return redirect('/projects/{}/files'.format(pk))
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
    types, match = list(map(lambda s: s.strip(), types.split(','))), []
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
        if not files:
            messages.info(
                request,
                'Not found any files.',
                extra_tags='alert'
            )
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
    messages.success(
        request,
        'The file was deleted.',
        extra_tags='alert'
    )
    return redirect(request.META.get('HTTP_REFERER')) # better solution


########################################################
# MEMBERS FUNCTIONS
########################################################


@login_required
def leave_project(request, pk):
    """ Take authenticate user and remove him from
    project. Project is deleted if there is no
    user left. """
    project = Project.objects.get(id_project=pk)
    project.collaborators.remove(request.user)
    if project.collaborators.count() == 0:
        project.delete()
    return redirect('/projects')


def remove_member(request, project):
    """ Remove a member from project according to
    given operation. """
    userstring = request.POST.get('user')
    try:
        user = User.objects.get(username=userstring)
    except User.DoesNotExist:
        messages.error(
            request,
            'ERROR: User is not in database.',
            extra_tags='alert'
        )
    else:
        project.collaborators.remove(user)
        messages.success(
            request,
            'User was removed from the project.',
            extra_tags='alert'
        )
    return redirect('/projects/{}/members'.format(project.id_project))  # http_referer


def add_member(request, project):
    """ Add a member from project according to
    given operation. """
    form = ManageUserForm(request.POST)
    if form.is_valid():
        userstring = form.cleaned_data['user']
        try:
            user = User.objects.get(username=userstring)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=userstring)
            except User.DoesNotExist:
                messages.error(
                    request,
                    'ERROR: User is not in database.',
                    extra_tags='alert'
                )
                return redirect('/projects/{}/members'.format(project.id_project))
        project.collaborators.add(user)
        messages.success(
            request,
            'User was added to the project.',
            extra_tags='alert'
        )
        return redirect('/projects/{}/members'.format(project.id_project))


@login_required
def add_searched_member(request, pk):
    id_user = request.POST.get('id_user', False)
    if not id_user:
        messages.ERROR(
            request,
            'ERROR: User is not in database.',
            extra_tags='alert'
        )
    else:
        user = User.objects.get(id=id_user)
        project = Project.objects.get(id_project=pk)
        project.collaborators.add(user)
        messages.success(
            request,
            'User was added to the project.',
            extra_tags='alert'
        )
    return redirect('/projects/{}/members'.format(pk))


def search_members(request, project):
    """ Search specific user in database of users. """
    result_list = []
    project_collaborators = project.collaborators.all()
    form = ManageUserForm(request.POST)
    if form.is_valid():
        userstring = form.cleaned_data['user']
        for user in User.objects.all():
            if user != request.user and user not in project_collaborators:
                if userstring in user.username:
                    result_list.append(user)
                elif userstring in user.email:
                    result_list.append(user)
    if not result_list:
        messages.warning(request, 'Not found any users.', extra_tags='alert')
    return result_list


@login_required
def manage_members(request, pk):
    project = Project.objects.get(id_project=pk)
    searched_members = []
    if request.method == 'POST':
        if 'SelectMemberButton' in request.POST:
            return add_member(request, project)
        if 'RemoveUserButton' in request.POST:
            return remove_member(request, project)
        if 'SearchUserButton' in request.POST:
            searched_members = search_members(request, project)
    choices = (
        (user.username, user.username)
        for user in project.collaborators.all()
        if user != request.user
    )
    context = {
        'project_pk': pk,
        'collaborators': project.collaborators.all(),
        'searched_members': searched_members,
        'add_form': ManageUserForm(),
        'remove_form': ChooseUserForm(choices),
    }
    return render(request, 'project/member_form.html', context)


########################################################
# TASKS FUNCTIONS
########################################################


def delete_task(request, pk):
    """ Remove a specific task. """
    Task.objects.get(pk=pk).delete()
    messages.success(
        request,
        'The task was deleted.',
        extra_tags='alert'
    )
    return redirect(request.META.get('HTTP_REFERER'))   # better solution


def change_finalization(request, pk):
    """ Finish a specific task. """
    task = Task.objects.get(id_task=pk)
    if task.finish:
        task.finish = False
        messages.success(
            request,
            'The task is in process again.',
            extra_tags='alert'
        )
    else:
        task.finish = True
        messages.success(
            request,
            'The task was completed.',
            extra_tags='alert'
        )
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


def change_importance(request, pk):
    """ Change importance of the task. """
    task = Task.objects.get(id_task=pk)
    if task.important:
        task.important = False
        messages.info(
            request,
            'The task is not important now.',
            extra_tags='alert'
        )
    else:
        task.important = True
        messages.info(
            request,
            'The task is important now.',
            extra_tags='alert'
        )
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def update_task(request, pk):
    """ Update a specific task. """
    instance = Task.objects.get(id_task=pk)
    project = instance.id_project
    task_form = TaskForm(project.id_project, request.POST or None, instance=instance)
    if task_form.is_valid():
        task_form.save()
        messages.success(
            request,
            'The task was updated.',
            extra_tags='alert'
        )
        return redirect('/projects/{}/tasks'.format(project.id_project))
    finished_tasks = Task.objects.filter(
        id_project=project.id_project,
        finish=True
    )
    unfinished_tasks = Task.objects.filter(
        id_project=project.id_project,
        finish=False
    )
    context = {
        'task_form': task_form,
        'finished_tasks': finished_tasks,
        'unfinished_tasks': unfinished_tasks,
        'project_pk': project.id_project,
        'update': True,
    }
    return render(request, 'project/task_form.html', context)


@login_required
def task_handler(request, pk):
    """ Task handler for creating, deleting and
    updating the task . """
    task_form = TaskForm(pk)
    if request.method == 'POST':
        task_form = TaskForm(pk, request.POST or None)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.id_project = Project.objects.get(id_project=pk)
            task_form.save()
            messages.success(
                request,
                'The task was added to the unfinished section.',
                extra_tags='alert'
            )
            return redirect('/projects/{}/tasks'.format(pk))
    finished_tasks = Task.objects.filter(id_project=pk, finish=True).order_by('-important')
    unfinished_tasks = Task.objects.filter(id_project=pk, finish=False).order_by('-important')
    context = {
        'task_form': task_form,
        'finished_tasks': finished_tasks,
        'unfinished_tasks': unfinished_tasks,
        'project_pk': pk,
        'update': False,
    }
    return render(request, 'project/task_form.html', context)
