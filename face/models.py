from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255)
    picture = models.FileField(upload_to='known/')
