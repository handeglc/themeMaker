from django.db import models
from django.contrib import admin

class File(models.Model):
    name_field = models.CharField(max_length=100)
    file_field = models.FileField(upload_to='uploads/')

admin.site.register(File)

