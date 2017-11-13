from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Project, File

# Create your views here.


def index(request):
    all_projects = Project.objects.all()
    return render(request, "project/index.html/", { "all_projects": all_projects })
    
   
def detail(request, id_project):
    specific_project = get_object_or_404(Project, pk=id_project)
    files = File.objects.filter(id_project=id_project)
    context = {
        "specific_project": specific_project,
        "files": files,
    }
    return render(request, "project/detail.html", context)
    
    