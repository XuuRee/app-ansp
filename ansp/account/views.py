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


@login_required
def view_profile(request):
    user = request.user
    notes = Note.objects.get(author=user)
    # statistics etc.
    context = {
        'user': user,
        'notes': notes,
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
            return redirect('/accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})

