from django.shortcuts import render, redirect
from account.forms import RegistrationForm

# Create your views here.


def home(request):
    return render(request, 'account/login.html')


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