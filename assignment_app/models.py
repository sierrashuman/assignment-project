from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=50)
    course_mnemonic = models.CharField(max_length=10) # For example, 'CS 3240'
    professor = models.CharField(max_length=50)
    course_description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    monday = models.BooleanField()  # To keep track of what days it meets if we make a schedule
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()

    def __str__(self):
        return self.name

    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    

