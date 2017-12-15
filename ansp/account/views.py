from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def home(request):
    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/projects')
    else:
        form = UserCreationForm()
        args = {'form': form}
        return render(request, 'account/register_form.html', args)