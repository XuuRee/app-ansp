from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from .models import Project, File

# Create your views here.


def index(request):
    all_projects = Project.objects.all()
    return render(request, "project/index.html/", { "all_projects": all_projects })
    
   
def detail(request, id_project):
    try:
        specific_project = Project.objects.get(pk=id_project)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    files = File.objects.filter(id_project=id_project)
    context = {
        "specific_project": specific_project,
        "files": files,
    }
    return render(request, "project/detail.html", context)
    
    