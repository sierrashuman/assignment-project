from django.contrib.auth import get_user_model
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse

class Course(models.Model):
    name = models.CharField(max_length=50)
    course_id = models.IntegerField()
    professor = models.CharField(max_length=50)
    course_description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return self.name

class PDF(models.Model):
    title = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    pdf_file = models.FileField(upload_to='pdfs/', validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
# class User(models.Model):
#     name = models.CharField(max_length=50)
#     courses = models.ListCharField(
#         base_field=CharField(),
#         size=10,
#         max_length=(10*50)
#     )

#     def __str__(self):
#         return self.name

# class Enrollment(models.Model):
#     course = models.ForeignKey(Courses)
#     student = models.ForeignKey(User)

# cal/models.py
    

