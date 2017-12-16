from django.shortcuts import render, redirect, HttpResponse
from account.forms import RegistrationForm
from django.contrib.auth.models import User

# after registration user must be log in
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/projects')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'account/register_form.html', args)
    

def profile(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    args = {'user': request.user}
    return render(request, 'account/profile.html', args)