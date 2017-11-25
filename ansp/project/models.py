from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.

class Project(models.Model):
    id_project = models.AutoField(primary_key=True)     # delete item
    author = models.ForeignKey('auth.User')             # delete item
    name = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateField()
    deadline = models.DateField()
    finished = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('project:detail', kwargs={'pk': self.id_project})

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    
class File(models.Model):
    id_file = models.AutoField(primary_key=True)        # delete item
    id_project = models.ForeignKey('Project', on_delete=models.CASCADE)
    filename = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.filename
    