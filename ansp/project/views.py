from django.shortcuts import render
from django.utils import timezone
from .models import Project, File

# Create your views here.

def index(request):
    projects, files = Project.objects.all(), File.objects.all()
    return render(request, 'project/index.html', {'projects' : projects, 'files' : files})