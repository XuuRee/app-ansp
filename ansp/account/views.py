from django.urls import reverse
from django.shortcuts import render, redirect
from account.forms import (
    RegistrationForm,
    EditProfileForm
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from project.models import Project, File, Note, Comment, Task


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()                                         # return object 'user' -> user.username
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/projects/')
        else:
            return render(request, 'account/register_form.html', {'form': form})
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'account/register_form.html', context)


def compute_percent(item, one_percent):
    try:
        result = item / one_percent
    except ZeroDivisionError:
        return 0
    return round(result, 2)


def make_dict_statistics(items):
    one_percent = sum(items) / 100
    statistics = {
        'Projects': compute_percent(items[0], one_percent),
        'Tasks': compute_percent(items[1], one_percent),
        'Comments': compute_percent(items[2], one_percent),
        'Notes': compute_percent(items[3], one_percent),
    }
    return statistics


@login_required
def view_profile(request):
    notes = Note.objects.filter(author=request.user) # print author note
    comments = Comment.objects.filter(author=request.user)
    projects = Project.objects.filter(collaborators__in=[request.user])
    tasks = Task.objects.filter(collaborators__in=[request.user])
    items = [
        len(projects),
        len(tasks),
        len(comments),
        len(notes)
    ]
    statistics = make_dict_statistics(items)
    ratio = list(statistics.values())
    context = {
        'statistics': statistics,
        'items': items,
        'ratio': ratio,
    }
    return render(request, 'account/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'account/edit_profile.html', {'form': form})
    

@login_required    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return render(request, 'account/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})

