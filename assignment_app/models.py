from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
#from django_mysql.models import ListTextField

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    course_id = models.IntegerField()
    professor = models.CharField(max_length=50)
    course_description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return self.name

    
# class User(models.Model):
#     name = models.CharField(max_length=50)
#     courses = models.ListCharField(
#         base_field=CharField(),
#         size=10,
#         max_length=(10*50)
#     )

#     def __str__(self):
#         return self.name

#class Course(models.Model):
    
 #   enrolled = models.ManyToManyField(User, through = 'Enrollment')

 #   def __str__(self):
  #      return self.course

# class Enrollment(models.Model):
#     course = models.ForeignKey(Courses)
#     student = models.ForeignKey(User)

    

