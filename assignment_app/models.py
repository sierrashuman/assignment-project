from django.db import models
from django_mysql.models import ListTextField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    courses = modelbbs.ListTextField(
        base_field=IntegerField(),
        size=50
    )
class Course(models.Model):
    name = models.CharField(max_length=50)
    course_id = models.IntegerField()
    professor = models.CharField(max_length=50)
    course_descrip = models.TextField()
    lecture_times = models.TextField()
    prereqs = models.ListTextField(
        base_field-IntegerField),
        size-5,
        max_length=(5*10)
    )
    enrolled = models.ManyToManyField(User)
